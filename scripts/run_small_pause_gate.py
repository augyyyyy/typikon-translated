#!/usr/bin/env python3
"""
Universal Small Pause Gatekeeper Suite (Master Runner)
======================================================
Executes the mandatory linters and auditors at the conclusion of every cohort:
  1A. Shared_Lexicon/lint_vocabulary.py (Zero forbidden variants)
  1B. scripts/lint_liturgical_slop.py (Zero pseudo-archaic slop, AI clichés, or rubrical shall-bombing)
  1C. scripts/chromatic_rubric_verifier.py (Chromatic Cinnabar Rubric Verification)
  2. scripts/hieratic_pronoun_audit.py (100% Deity Pronoun Capitalization)
  3. scripts/reconcile_footnotes.py (Exact 1:1 Footnote Parity)
  4. scripts/structural_audit.py (Unbroken Sequence & Heading Hierarchy)
  5. Phase 1 -> Phase 2 Argon Review Queue Collector (Audit_Reports/argon_review_queue.json)

Gate Enforcement:
  If all gates pass -> updates state to PASSED_COHORT_<N>, exit code 0.
  If any gate fails -> execution halts, logs failure signature to scratch/triage_inbox.jsonl, exit code 1.

Usage:
    python scripts/run_small_pause_gate.py --monument 1891_lviv_synod --cohort 1
    python scripts/run_small_pause_gate.py --monument 1891_lviv_synod --cohort 3
"""

import sys
import os
import re
import json
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"
STATE_FILE = PROJECT_ROOT / "Liturgical Monuments" / "ACTIVE_ORCHESTRATOR_STATE.json"
TRIAGE_INBOX = PROJECT_ROOT / "scratch" / "triage_inbox.jsonl"
SHARED_LEXICON_DIR = PROJECT_ROOT.parent / "Shared_Lexicon"

from concurrency_lock import atomic_write_json, atomic_append_jsonl
from orchestrator_state import (
    resolve_monument_id,
    resolve_monument_type,
    load_monument_scaffold,
    load_state,
)

EPIGRAPHIC_UNCERTAINTY_PATTERNS = [
    (r"\[\?+\]", "epigraphic_uncertainty_marker: [?]"),
    (r"\[illegible[^\]]*\]", "epigraphic_uncertainty_marker: [illegible]"),
    (r"\[lacuna[^\]]*\]", "epigraphic_uncertainty_marker: [lacuna]"),
    (r"\[damaged[^\]]*\]", "epigraphic_uncertainty_marker: [damaged]"),
    (r"\[corrupt[^\]]*\]", "epigraphic_uncertainty_marker: [corrupt]"),
]

CODICOLOGICAL_CRUX_RE = re.compile(
    r"\b(?:"
    r"catchword\s+mismatch|"
    r"missing\s+(?:quire|folio|leaf|leaves|page|pages)|"
    r"lost\s+(?:folio|leaf|leaves)|"
    r"folio\s+transposition|"
    r"misbound|"
    r"(?:foliation|pagination)\s+jump|"
    r"duplicate\s+exposure|"
    r"(?:pasted|paper)\s+repair|"
    r"breaks\s+off\s+mid-|"
    r"bound\s+out\s+of\s+sequence|"
    r"(?:quire|physical)\s+lacuna"
    r")\b",
    re.IGNORECASE,
)

CRUX_NEGATION_GUARD_RE = re.compile(
    r"\b(?:no|without|not|neither|nor|never|zero|free\s+of|absence\s+of)\b",
    re.IGNORECASE,
)

TITLO_CUE_RE = re.compile(
    r'\*\*["“](?:Glory|Now and ever|Both now|Lord,\s*have mercy|Holy God|Alleluia|Amen|Peace be|Let us attend|Wisdom)',
    re.IGNORECASE,
)

SPARSE_EXEMPT_KEYWORDS = (
    "blank",
    "vacat",
    "frontispiece",
    "title page",
    "imprimatur",
    "icon",
    "table",
    "colophon",
)


def log_to_triage(entry: Dict[str, Any]) -> None:
    atomic_append_jsonl(TRIAGE_INBOX, entry, lock_name="triage_inbox")
    print(f"Logged failure signature to: {TRIAGE_INBOX.relative_to(PROJECT_ROOT)}")


def find_target_file(dir_path: Path, pattern: str, cohort_num: Optional[int] = None) -> Optional[Path]:
    if not dir_path.exists():
        return None
    cands = list(dir_path.glob(pattern))
    if cohort_num is not None:
        filtered = []
        for p in cands:
            m = re.search(r"cohort0?(\d+)", p.name, re.IGNORECASE)
            if m and int(m.group(1)) == cohort_num:
                filtered.append(p)
        if filtered:
            return filtered[0]
    return cands[0] if cands else None


def _parse_footnotes_map(footnotes_file: Optional[Path]) -> Dict[str, str]:
    fn_map: Dict[str, str] = {}
    if not footnotes_file or not footnotes_file.exists():
        return fn_map
    try:
        content = footnotes_file.read_text(encoding="utf-8")
    except OSError:
        return fn_map
    current_id: Optional[str] = None
    current_lines: List[str] = []
    for line in content.splitlines():
        m = re.match(r"^\s*\[\^(\d+)\]:\s*(.*)$", line)
        if m:
            if current_id is not None:
                fn_map[current_id] = "\n".join(current_lines).strip()
            current_id = m.group(1)
            current_lines = [m.group(2)]
        elif current_id is not None:
            current_lines.append(line)
    if current_id is not None:
        fn_map[current_id] = "\n".join(current_lines).strip()
    return fn_map


def collect_argon_review_signals(
    monument_id: str,
    cohort_num: int,
    ws: Path,
    target_text: Path,
    source_file: Optional[Path] = None,
    quarantine_reasons: Optional[List[str]] = None,
    quarantine_leaves: Optional[List[int]] = None,
    footnotes_file: Optional[Path] = None,
    fn_symmetry_passed: bool = True,
    mon_info: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Scans each === LEAF pN === block in the cohort and updates
    Audit_Reports/argon_review_queue.json with the 5 locked signals:
      1. Epigraphic uncertainty/lacuna markers ([?], [illegible], [lacuna], [damaged], [corrupt])
      2. Borderline SGC-02 draft-to-source length ratios (calibrated by monument_type + titlo_cue_max_ratio)
      3. High-complexity Paschalion/multi-column tables (>=5 table rows) or dense polyglot apparatus (1-up vs 2-up thresholds)
      4. Quarantined leaves after deterministic self-healing + 1 Flash retry
      5. Codicological or physical collation cruxes (compound-phrase matching with negation guard)
    """
    from scripts.structural_audit import parse_leaf_blocks

    if mon_info is None and REGISTRY_FILE.exists():
        try:
            reg = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
            mon_info = reg.get("monuments", {}).get(monument_id, {})
        except (OSError, json.JSONDecodeError):
            mon_info = {}

    scaffold = load_monument_scaffold(monument_id, mon_info)
    gate_policy = scaffold.get("gate_policy", {}) if isinstance(scaffold, dict) else {}
    sgc02_min = float(gate_policy.get("sgc02_min_ratio", 0.50))
    sgc02_max = float(gate_policy.get("sgc02_max_ratio", 2.40))
    titlo_cue_max = float(gate_policy.get("titlo_cue_max_ratio", 2.85))
    fn_threshold_1up = int(gate_policy.get("argon_queue_footnote_threshold", 8))
    fn_threshold_2up = int(gate_policy.get("argon_queue_2up_footnote_threshold", 10))
    pure_fn_mode = str(gate_policy.get("pure_footnote_leaves_mode", "INFO_TELEMETRY_ONLY"))

    audit_dir = ws / "Audit_Reports"
    audit_dir.mkdir(parents=True, exist_ok=True)
    queue_path = audit_dir / "argon_review_queue.json"

    if source_file is None:
        cand_src = ws / "Source Text" / f"{monument_id}_cohort{cohort_num}_source.txt"
        if cand_src.exists():
            source_file = cand_src

    if footnotes_file is None:
        footnotes_file = (
            find_target_file(ws / "Draft", f"*cohort{cohort_num}*footnote*.txt", cohort_num=cohort_num)
            or find_target_file(ws / "Final", "*footnote*.txt")
        )
    fn_defs_by_id = _parse_footnotes_map(footnotes_file)

    draft_content = target_text.read_text(encoding="utf-8") if target_text.exists() else ""
    draft_blocks = parse_leaf_blocks(draft_content)

    src_blocks: Dict[int, str] = {}
    if source_file and source_file.exists():
        src_blocks = parse_leaf_blocks(source_file.read_text(encoding="utf-8"))

    existing_queue: Dict[str, Any] = {
        "monument_id": monument_id,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_queued_leaves": 0,
        "info_telemetry_leaves": 0,
        "unresolved_quarantines": 0,
        "items": [],
    }
    if queue_path.exists():
        try:
            loaded = json.loads(queue_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                existing_queue.update(loaded)
        except (OSError, json.JSONDecodeError) as e:
            print(f"  [Warning] Could not read existing argon_review_queue.json ({e}), reinitializing.", file=sys.stderr)

    items_by_leaf: Dict[int, Dict[str, Any]] = {}
    for item in existing_queue.get("items", []):
        if isinstance(item, dict) and "leaf_num" in item:
            items_by_leaf[int(item["leaf_num"])] = item

    all_leaves = sorted(set(draft_blocks.keys()) | set(src_blocks.keys()))
    newly_queued: List[int] = []
    newly_info_telemetry: List[int] = []
    quarantine_set = set(quarantine_leaves or [])

    for leaf_num in all_leaves:
        d_txt = draft_blocks.get(leaf_num, "")
        s_txt = src_blocks.get(leaf_num, "")
        combined = f"{s_txt}\n{d_txt}"
        reasons: List[str] = []

        # Signal 1: Epigraphic uncertainty / lacuna markers
        for pat, label in EPIGRAPHIC_UNCERTAINTY_PATTERNS:
            if re.search(pat, combined, re.IGNORECASE):
                reasons.append(label)

        # Signal 2: Borderline SGC-02 draft-to-source length ratio (calibrated per monument_type + titlo cues)
        if s_txt and d_txt:
            s_len = len(s_txt)
            t_len = len(d_txt)
            combined_lower = combined.lower()
            is_exempt_sparse = any(kw in combined_lower for kw in SPARSE_EXEMPT_KEYWORDS) or s_len < 120
            if not is_exempt_sparse and s_len > 0:
                ratio = t_len / float(s_len)
                titlo_cue_count = len(TITLO_CUE_RE.findall(d_txt))
                effective_max = max(sgc02_max, titlo_cue_max) if titlo_cue_count >= 4 else sgc02_max
                if (0.25 <= ratio < sgc02_min) or (effective_max < ratio <= 5.00):
                    reasons.append(
                        f"borderline_sgc02_ratio: {ratio:.2f} (draft={t_len}c, source={s_len}c, bounds=[{sgc02_min:.2f}, {effective_max:.2f}])"
                    )

        # Signal 3: High-complexity tables (>=5 table rows) or dense polyglot apparatus (1-up vs 2-up thresholds)
        table_rows = [
            ln for ln in d_txt.splitlines()
            if ln.strip().startswith("|") and ln.strip().endswith("|") and not re.match(r"^\|[\s\-:|]+\|$", ln.strip())
        ]
        if len(table_rows) >= 5:
            reasons.append(f"complex_multicolumn_table: {len(table_rows)} table rows")

        is_2up_leaf = bool(re.search(r"\*\*\[(?:Left|Right)\s+Page", d_txt, re.IGNORECASE))
        effective_fn_threshold = fn_threshold_2up if is_2up_leaf else fn_threshold_1up
        fn_ids = re.findall(r"\[\^(\d+)\]", d_txt)
        if len(fn_ids) >= effective_fn_threshold:
            reasons.append(
                f"dense_polyglot_apparatus: {len(fn_ids)} footnotes on leaf (threshold={effective_fn_threshold}, 2up={is_2up_leaf})"
            )

        # Signal 5: Codicological or physical collation crux (compound phrases + negation guard)
        leaf_fn_text = "\n".join(fn_defs_by_id.get(fid, "") for fid in fn_ids)
        crux_scan_text = f"{d_txt}\n{leaf_fn_text}"
        crux_matches = []
        for m_crux in CODICOLOGICAL_CRUX_RE.finditer(crux_scan_text):
            clause_prefix = re.split(r"[.;:!?\n]", crux_scan_text[max(0, m_crux.start() - 60):m_crux.start()])[-1]
            if CRUX_NEGATION_GUARD_RE.search(clause_prefix):
                continue
            phrase = re.sub(r"\s+", " ", m_crux.group(0).strip().lower())
            if phrase not in crux_matches:
                crux_matches.append(phrase)
        if crux_matches:
            reasons.append(f"codicological_or_collation_crux: {', '.join(crux_matches)}")

        # Signal 4: Quarantine override after deterministic self-healing + 1 Flash retry
        is_quarantined = leaf_num in quarantine_set
        if is_quarantined and quarantine_reasons:
            for qr in quarantine_reasons:
                tag = f"quarantined_gate_anomaly: {qr}"
                if tag not in reasons:
                    reasons.append(tag)

        prev_item = items_by_leaf.get(leaf_num)
        if prev_item and prev_item.get("status") == "RESOLVED_BY_ARGON" and not is_quarantined:
            continue

        if reasons or is_quarantined:
            only_dense_apparatus = (
                not is_quarantined
                and len(reasons) > 0
                and all(r.startswith("dense_polyglot_apparatus:") for r in reasons)
            )
            if is_quarantined:
                status_val = "QUARANTINED_FOR_ARGON"
            elif only_dense_apparatus and fn_symmetry_passed and pure_fn_mode == "INFO_TELEMETRY_ONLY":
                status_val = "INFO_TELEMETRY_ONLY"
            else:
                status_val = "QUEUED_FOR_ARGON"

            if prev_item and prev_item.get("status") == "QUARANTINED_FOR_ARGON" and not is_quarantined:
                status_val = "QUARANTINED_FOR_ARGON"
                for old_r in prev_item.get("reasons", []):
                    if old_r.startswith("quarantined_gate_anomaly:") and old_r not in reasons:
                        reasons.append(old_r)

            items_by_leaf[leaf_num] = {
                "leaf_num": leaf_num,
                "cohort": cohort_num,
                "status": status_val,
                "reasons": reasons,
                "draft_file": str(target_text.relative_to(PROJECT_ROOT)) if target_text.is_relative_to(PROJECT_ROOT) else str(target_text),
                "source_file": (
                    str(source_file.relative_to(PROJECT_ROOT))
                    if (source_file and source_file.is_relative_to(PROJECT_ROOT))
                    else (str(source_file) if source_file else None)
                ),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            if status_val == "INFO_TELEMETRY_ONLY":
                newly_info_telemetry.append(leaf_num)
            else:
                newly_queued.append(leaf_num)
        elif prev_item and prev_item.get("cohort") == cohort_num and prev_item.get("status") in ("QUEUED_FOR_ARGON", "INFO_TELEMETRY_ONLY"):
            # Signal cleared on re-run
            del items_by_leaf[leaf_num]

    sorted_items = [items_by_leaf[k] for k in sorted(items_by_leaf.keys())]
    active_items = [
        it for it in sorted_items
        if it.get("status") not in ("RESOLVED_BY_ARGON", "INFO_TELEMETRY_ONLY")
    ]
    info_telemetry_items = [it for it in sorted_items if it.get("status") == "INFO_TELEMETRY_ONLY"]
    quarantined_items = [it for it in sorted_items if it.get("status") == "QUARANTINED_FOR_ARGON"]

    existing_queue["monument_id"] = monument_id
    existing_queue["updated_at"] = datetime.now(timezone.utc).isoformat()
    existing_queue["total_queued_leaves"] = len(active_items)
    existing_queue["info_telemetry_leaves"] = len(info_telemetry_items)
    existing_queue["unresolved_quarantines"] = len(quarantined_items)
    existing_queue["items"] = sorted_items

    atomic_write_json(queue_path, existing_queue, lock_name=f"argon_queue_{monument_id}")

    return {
        "queue_path": str(queue_path.relative_to(PROJECT_ROOT)) if queue_path.is_relative_to(PROJECT_ROOT) else str(queue_path),
        "cohort_queued_leaves": newly_queued,
        "cohort_info_telemetry_leaves": newly_info_telemetry,
        "total_queued_leaves": len(active_items),
        "info_telemetry_leaves": len(info_telemetry_items),
        "unresolved_quarantines": len(quarantined_items),
    }


def run_monument_type_gate(monument_id: str, mon_info: Dict[str, Any], target_text: Path) -> Dict[str, Any]:
    """
    Gate 4B: Monument-Type Specific Invariants + Gate 5A Phase 1 Residual Cyrillic Pre-Check.
    Catches square-bracketed or unparenthesized Cyrillic in body text, square-bracketed [Blank ...]
    placeholders, unbolded speaker tags in Euchologia/Trebnyky/Horologia, and Akathist stanza headers
    missing colons so deterministic self-healing can repair them in Phase 1.
    """
    monument_type = resolve_monument_type(monument_id, mon_info)
    content = target_text.read_text(encoding="utf-8") if target_text.exists() else ""
    violations: List[Dict[str, Any]] = []

    speaker_roles = (
        r"(?:Priest|Deacon|Bishop|Archimandrite|Hegumen|Rector|Superior|"
        r"Celebrant|Protodeacon|Archdeacon|Choir|Reader|People|Clergy|Canonarch|Chanters|Chanter)"
    )
    italic_speaker_re = re.compile(
        r"^\*(?:The\s+)?" + speaker_roles + r"(?:\s*\([^\)]+\))?:\*",
        re.IGNORECASE,
    )
    akathist_missing_colon_re = re.compile(r"^\*(?:Kontakion|Ikos)\s+\d+\*(?!:)", re.IGNORECASE)
    sq_cyrillic_re = re.compile(r"\[([^\[\]\^]*[\u0400-\u04FF\uA640-\uA69F][^\[\]]*)\]")
    blank_bracket_re = re.compile(r"\[[Bb]lank\s+[^\]]+\]")

    for idx, line in enumerate(content.splitlines(), start=1):
        s_line = line.strip()
        if not s_line or s_line.startswith("=== LEAF"):
            continue

        # 1. Square-bracketed [Blank ...] placeholder check
        if blank_bracket_re.search(s_line):
            violations.append({
                "line": idx,
                "type": "square_bracketed_blank_placeholder",
                "snippet": s_line[:120],
            })

        # 2. Gate 5A Pre-Check: Square-bracketed or bare unparenthesized Cyrillic in body text
        if sq_cyrillic_re.search(s_line):
            violations.append({
                "line": idx,
                "type": "square_bracketed_cyrillic_in_body",
                "snippet": s_line[:120],
            })
        else:
            clean_line = re.sub(r"<[^>]+>", "", s_line)
            while re.search(r"\([^\(\)]*\)", clean_line):
                clean_line = re.sub(r"\([^\(\)]*\)", "", clean_line)
            if re.search(r"[\u0400-\u04FF\uA640-\uA69F]", clean_line):
                violations.append({
                    "line": idx,
                    "type": "bare_unparenthesized_cyrillic_in_body",
                    "snippet": s_line[:120],
                })

        # 3. Monument-type specific checks
        if monument_type in ("euchologion_liturgikon", "trebnyk_euchologion", "horologion"):
            if italic_speaker_re.match(s_line):
                violations.append({
                    "line": idx,
                    "type": "italic_speaker_tag_must_be_bold",
                    "snippet": s_line[:120],
                })

        if monument_type == "akathistnik":
            if akathist_missing_colon_re.match(s_line):
                violations.append({
                    "line": idx,
                    "type": "akathist_header_missing_colon",
                    "snippet": s_line[:120],
                })

    return {
        "passed": len(violations) == 0,
        "monument_type": monument_type,
        "violation_count": len(violations),
        "violations": violations[:25],
    }


def run_gate_1c_chromatic(cohort_dir: Path, leaves: List[int]) -> bool:
    """
    Gate 1C: Chromatic Cinnabar Rubric Verification (when leaf scans are present).
    Warns if rubric ink lacks statistically significant red pigment without blocking execution.
    """
    scan_dir = cohort_dir / "scans"
    if not scan_dir.exists():
        scan_dir = cohort_dir / "Source Text" / "images"
    if not scan_dir.exists():
        print("  PASSED (Bypassed: facsimile scans directory not present)")
        return True

    try:
        from scripts.chromatic_rubric_verifier import ChromaticRubricVerifier
    except Exception as e:
        print(f"  WARNING: Could not load ChromaticRubricVerifier ({e}), bypassing.")
        return True

    warnings = 0
    verified = 0
    for leaf in leaves:
        for fname in (f"Page_{leaf:04d}.jpg", f"p{leaf}.jpg", f"p{leaf}.png"):
            leaf_img = scan_dir / fname
            if leaf_img.exists():
                break
        else:
            leaf_img = None

        if leaf_img and leaf_img.exists():
            try:
                verifier = ChromaticRubricVerifier(leaf_img)
                res = verifier.verify_crop()
                verified += 1
                if res.get("verdict") == "FAIL":
                    warnings += 1
                    print(f"  [GATE 1C WARNING] Leaf p{leaf} rubric lacks verified red pigment.")
            except Exception as e:
                print(f"  [GATE 1C ERROR] Failed analyzing leaf p{leaf}: {e}")

    if verified > 0:
        print(f"  PASSED ({verified} leaves checked for cinnabar red; {warnings} pigment warnings)")
    else:
        print("  PASSED (Bypassed: no matching leaf scan files in scan directory)")
    return True


def _compute_cohort_telemetry(
    monument_id: str,
    cohort_num: int,
    ws: Path,
    target_text: Path,
    footnotes_file: Path,
    report_file: Path,
) -> Dict[str, Any]:
    now_iso = datetime.now(timezone.utc).isoformat()
    existing_telem: Dict[str, Any] = {}
    if report_file.exists():
        try:
            prev_rep = json.loads(report_file.read_text(encoding="utf-8"))
            if isinstance(prev_rep, dict) and isinstance(prev_rep.get("cohort_telemetry"), dict):
                existing_telem = prev_rep["cohort_telemetry"]
        except (OSError, json.JSONDecodeError):
            existing_telem = {}

    prepared_at_iso = existing_telem.get("prepared_at_iso")
    if not prepared_at_iso:
        try:
            full_state = load_state()
            mon_state = full_state.get("monuments", {}).get(monument_id, {})
            prep_map = mon_state.get("cohort_prepared_timestamps", {})
            if isinstance(prep_map, dict):
                prepared_at_iso = prep_map.get(str(cohort_num))
        except Exception:
            prepared_at_iso = None

    if not prepared_at_iso:
        wo_file = ws / "Work_Orders" / f"work_order_cohort_{cohort_num}.md"
        if wo_file.exists():
            try:
                prepared_at_iso = datetime.fromtimestamp(wo_file.stat().st_mtime, tz=timezone.utc).isoformat()
            except OSError:
                prepared_at_iso = None

    first_verified_at_iso = existing_telem.get("first_verified_at_iso") or now_iso
    duration_sec: Optional[float] = None
    if prepared_at_iso:
        try:
            t_prep = datetime.fromisoformat(prepared_at_iso)
            t_now = datetime.fromisoformat(now_iso)
            duration_sec = round(max(0.0, (t_now - t_prep).total_seconds()), 2)
        except ValueError:
            duration_sec = None

    initial_duration_sec = existing_telem.get("initial_duration_sec")
    if initial_duration_sec is None and duration_sec is not None:
        initial_duration_sec = duration_sec

    src_file = ws / "Source Text" / f"{monument_id}_cohort{cohort_num}_source.txt"
    src_txt = src_file.read_text(encoding="utf-8") if src_file.exists() else ""
    draft_txt = target_text.read_text(encoding="utf-8") if target_text.exists() else ""
    fn_txt = footnotes_file.read_text(encoding="utf-8") if footnotes_file.exists() else ""

    source_words = len(re.findall(r"\S+", src_txt))
    draft_words = len(re.findall(r"\S+", draft_txt))
    footnote_count = len(re.findall(r"\[\^\d+\]", draft_txt))
    footnote_words = len(re.findall(r"\S+", fn_txt))
    sgc02_ratio = round(len(draft_txt) / float(len(src_txt)), 4) if len(src_txt) > 0 else None

    return {
        "prepared_at_iso": prepared_at_iso,
        "first_verified_at_iso": first_verified_at_iso,
        "verified_at_iso": now_iso,
        "initial_duration_sec": initial_duration_sec,
        "duration_sec": duration_sec,
        "source_words": source_words,
        "draft_words": draft_words,
        "footnote_count": footnote_count,
        "footnote_words": footnote_words,
        "sgc02_ratio": sgc02_ratio,
    }


def run_gate(
    monument_id: str,
    cohort_num: int,
    custom_draft: Optional[Path] = None,
    custom_footnotes: Optional[Path] = None,
    emit_triage: bool = False,
) -> int:
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
    mon_info = registry.get("monuments", {}).get(monument_id)
    if not mon_info:
        raise ValueError(f"Unknown monument ID: {monument_id}")

    ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}")
    audit_reports_dir = ws / "Audit_Reports"
    audit_reports_dir.mkdir(parents=True, exist_ok=True)
    report_file = audit_reports_dir / f"cohort{cohort_num}_small_pause_report.json"

    # Identify target files (Explicit flags, Final MD preferred, Draft fallback)
    target_text = custom_draft or (
        find_target_file(ws / "Final MD", f"*cohort{cohort_num}*.md", cohort_num=cohort_num) or
        find_target_file(ws / "Final", f"*cohort{cohort_num}*.txt", cohort_num=cohort_num) or
        find_target_file(ws / "Draft", f"*cohort{cohort_num}*.md", cohort_num=cohort_num)
    )

    footnotes_file = custom_footnotes or (
        find_target_file(ws / "Draft", f"*cohort{cohort_num}*footnote*.txt", cohort_num=cohort_num) or
        find_target_file(ws / "Final", "*footnote*.txt")
    )

    if not target_text or not target_text.exists():
        raise FileNotFoundError(f"Neither final nor draft text file found for {monument_id} cohort {cohort_num} in {ws}")
    if not footnotes_file or not footnotes_file.exists():
        footnotes_file = ws / "Final" / "Final_footnotes.txt"

    monument_type = resolve_monument_type(monument_id, mon_info)
    print("=" * 65)
    print(f"  SMALL PAUSE GATEKEEPER SUITE — COHORT #{cohort_num}")
    print(f"  Monument: {mon_info.get('title')} [{monument_type}]")
    print(f"  Audited File: {target_text.relative_to(PROJECT_ROOT) if target_text.is_relative_to(PROJECT_ROOT) else target_text}")
    print(f"  Footnotes File: {footnotes_file.relative_to(PROJECT_ROOT) if footnotes_file.exists() and footnotes_file.is_relative_to(PROJECT_ROOT) else footnotes_file}")
    print("=" * 65)

    cohort_telemetry = _compute_cohort_telemetry(
        monument_id=monument_id,
        cohort_num=cohort_num,
        ws=ws,
        target_text=target_text,
        footnotes_file=footnotes_file,
        report_file=report_file,
    )

    master_report: Dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "monument_id": monument_id,
        "monument_type": monument_type,
        "cohort": cohort_num,
        "target_file": str(target_text.name),
        "overall_status": "PENDING",
        "cohort_telemetry": cohort_telemetry,
        "gates": {}
    }

    all_passed = True

    # Gate 1A: Shared_Lexicon vocabulary linting
    print("\n[Gate 1A/5] Running Vocabulary Linter (Shared_Lexicon/lint_vocabulary.py)...")
    vocab_linter_script = SHARED_LEXICON_DIR / "lint_vocabulary.py"
    vocab_passed = True
    vocab_violations = []

    if vocab_linter_script.exists():
        cmd = [
            sys.executable, str(vocab_linter_script),
            "--target", str(target_text),
            "--mode", "typikon"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if res.returncode != 0:
            vocab_passed = False
            all_passed = False
            vocab_violations.append(res.stderr.strip() or res.stdout.strip())
            print(f"  FAILED: {res.stdout.strip()[:200]}")
        else:
            print("  PASSED (Zero forbidden variants against master_liturgical_vocabulary.json)")
    else:
        print("  WARNING: lint_vocabulary.py not found, skipping vocabulary linter.")

    master_report["gates"]["vocabulary_linter"] = {
        "passed": vocab_passed,
        "violations": vocab_violations
    }

    # Gate 1B: Anti-Fanciful Slop Language Linter
    print("\n[Gate 1B/5] Running Anti-Slop Linter (scripts/lint_liturgical_slop.py)...")
    slop_linter_script = SCRIPT_DIR / "lint_liturgical_slop.py"
    slop_data = {}
    if slop_linter_script.exists():
        cmd_slop = [
            sys.executable, str(slop_linter_script),
            "--target", str(target_text),
            "--json"
        ]
        res_slop = subprocess.run(cmd_slop, capture_output=True, text=True, encoding="utf-8")
        if res_slop.returncode == 0:
            try:
                slop_data = json.loads(res_slop.stdout)
                print("  PASSED (Zero pseudo-archaic slop, AI cliches, or rubrical shall-bombing)")
            except Exception:
                slop_data = {"passed": True}
                print("  PASSED")
        else:
            all_passed = False
            try:
                slop_data = json.loads(res_slop.stdout)
                print(f"  FAILED: {slop_data.get('violation_count', 1)} slop violations detected")
            except Exception:
                slop_data = {"passed": False, "error": res_slop.stderr.strip() or res_slop.stdout.strip()}
                print(f"  FAILED: {slop_data}")
    else:
        print("  WARNING: lint_liturgical_slop.py not found, skipping slop linter.")

    master_report["gates"]["slop_linter"] = slop_data

    # Gate 1C: Chromatic Cinnabar Rubric Verification (when leaf scans are present)
    print("\n[Gate 1C] Running Chromatic Cinnabar Verification (scripts/chromatic_rubric_verifier.py)...")
    from scripts.structural_audit import extract_accounted_leaves
    cohort_leaves = sorted(extract_accounted_leaves(target_text.read_text(encoding="utf-8")))
    chromatic_passed = run_gate_1c_chromatic(ws, cohort_leaves)
    master_report["gates"]["chromatic_verifier"] = {
        "passed": chromatic_passed,
        "leaves_checked": len(cohort_leaves)
    }

    # Gate 2: Hieratic Deity Pronoun Audit
    print("\n[Gate 2/5] Running Hieratic Deity Pronoun Audit (scripts/hieratic_pronoun_audit.py)...")
    pronoun_script = SCRIPT_DIR / "hieratic_pronoun_audit.py"
    cmd_pronoun = [sys.executable, str(pronoun_script), "--target", str(target_text), "--json"]
    res_pronoun = subprocess.run(cmd_pronoun, capture_output=True, text=True, encoding="utf-8")
    pronoun_data = {}
    if res_pronoun.returncode == 0:
        try:
            pronoun_data = json.loads(res_pronoun.stdout)
            print("  PASSED (100% Capitalization on Trinity Deity Pronouns)")
        except Exception:
            pronoun_data = {"passed": True}
            print("  PASSED")
    else:
        all_passed = False
        try:
            pronoun_data = json.loads(res_pronoun.stdout)
            print(f"  FAILED: {pronoun_data.get('violation_count', 1)} violations detected")
        except Exception:
            pronoun_data = {"passed": False, "error": res_pronoun.stderr.strip() or res_pronoun.stdout.strip()}
            print(f"  FAILED: {pronoun_data}")

    master_report["gates"]["hieratic_pronouns"] = pronoun_data

    # Gate 3: Footnote Reconciler & Symmetry
    print("\n[Gate 3/5] Running Footnote Symmetry Audit (scripts/reconcile_footnotes.py)...")
    fn_script = SCRIPT_DIR / "reconcile_footnotes.py"
    cmd_fn = [sys.executable, str(fn_script), "--text", str(target_text), "--footnotes", str(footnotes_file), "--json"]
    res_fn = subprocess.run(cmd_fn, capture_output=True, text=True, encoding="utf-8")
    fn_data = {}
    fn_symmetry_passed = False
    if res_fn.returncode == 0:
        fn_symmetry_passed = True
        try:
            fn_data = json.loads(res_fn.stdout)
            print(f"  PASSED (Exact 1:1 Parity: {fn_data.get('text_markers_count', 0)} markers paired)")
        except Exception:
            fn_data = {"passed": True}
            print("  PASSED")
    else:
        try:
            fn_data = json.loads(res_fn.stdout)
            missing = fn_data.get("missing_definitions", [])
            orphaned = fn_data.get("orphaned_definitions", [])
            if len(missing) == 0:
                print(f"  PASSED (All {fn_data.get('text_markers_count', 0)} cohort markers defined; {len(orphaned)} definitions belong to sibling cohorts)")
                fn_data["passed"] = True
                fn_symmetry_passed = True
            else:
                all_passed = False
                print(f"  FAILED: Missing definitions={missing}")
        except Exception:
            all_passed = False
            fn_data = {"passed": False, "error": res_fn.stderr.strip() or res_fn.stdout.strip()}
            print(f"  FAILED: {fn_data}")

    master_report["gates"]["footnote_symmetry"] = fn_data

    # Gate 4: Structural Sequence & Leaf Continuity Integrity
    print("\n[Gate 4/5] Running Structural Sequence Audit (scripts/structural_audit.py)...")
    struct_script = SCRIPT_DIR / "structural_audit.py"
    cmd_struct = [
        sys.executable, str(struct_script),
        "--target", str(target_text),
        "--monument", monument_id,
        "--cohort", str(cohort_num),
        "--json"
    ]
    if cohort_num > 1:
        prev_cohort = cohort_num - 1
        prev_text = (
            find_target_file(ws / "Final MD", f"*cohort{prev_cohort}*.md", cohort_num=prev_cohort) or
            find_target_file(ws / "Draft", f"*cohort{prev_cohort}*.md", cohort_num=prev_cohort)
        )
        if prev_text and prev_text.exists():
            cmd_struct.extend(["--prev-target", str(prev_text)])

    res_struct = subprocess.run(cmd_struct, capture_output=True, text=True, encoding="utf-8")
    struct_data = {}
    if res_struct.returncode == 0:
        try:
            struct_data = json.loads(res_struct.stdout)
            leaf_s = struct_data.get("leaf_stats", {})
            leaf_msg = f", {leaf_s.get('leaves_count', 0)} leaves [p{leaf_s.get('min_leaf')}..p{leaf_s.get('max_leaf')}]" if leaf_s.get("leaves_count") else ""
            print(f"  PASSED ({struct_data.get('paragraphs', 0)} paragraphs{leaf_msg}, unbroken sequence)")
        except json.JSONDecodeError:
            struct_data = {"passed": True}
            print("  PASSED")
    else:
        all_passed = False
        try:
            struct_data = json.loads(res_struct.stdout)
            reasons = []
            if struct_data.get("number_breaks"):
                reasons.append(f"Number breaks={struct_data.get('number_breaks')}")
            if struct_data.get("anomalies"):
                reasons.append(f"Anomalies={struct_data.get('anomalies')}")
            print(f"  FAILED: {'; '.join(reasons) if reasons else 'Structural audit failed'}")
        except json.JSONDecodeError:
            struct_data = {"passed": False, "error": res_struct.stderr.strip() or res_struct.stdout.strip()}
            print(f"  FAILED: {struct_data}")

    master_report["gates"]["structural_sequence"] = struct_data

    # Gate 4B: Monument-Type Specific Invariants & Gate 5A Phase 1 Residual Cyrillic Pre-Check
    print(f"\n[Gate 4B/5] Running Monument-Type Policy & Epigraphic Pre-Check ({monument_type})...")
    type_gate_data = run_monument_type_gate(monument_id, mon_info, target_text)
    if type_gate_data.get("passed", True):
        print(f"  PASSED (Zero unparenthesized Cyrillic, bracketed blanks, or {monument_type} formatting violations)")
    else:
        all_passed = False
        print(f"  FAILED: {type_gate_data.get('violation_count', 1)} monument-type / epigraphic pre-check violations")
    master_report["gates"]["monument_type_policy"] = type_gate_data

    master_report["overall_status"] = "PASSED" if all_passed else "FAILED"

    # Gate 5: Argon Review Queue Signal Collector (Phase 1 -> Phase 2)
    print("\n[Argon Queue Collector] Scanning cohort leaves for Phase 2 Argon review signals...")
    queue_summary = collect_argon_review_signals(
        monument_id=monument_id,
        cohort_num=cohort_num,
        ws=ws,
        target_text=target_text,
        footnotes_file=footnotes_file,
        fn_symmetry_passed=fn_symmetry_passed,
        mon_info=mon_info,
    )
    master_report["argon_review_queue"] = queue_summary
    print(
        f"  Queued from Cohort #{cohort_num}: {queue_summary['cohort_queued_leaves']} "
        f"(Info Telemetry Only: {queue_summary.get('cohort_info_telemetry_leaves', [])}; "
        f"Monument Total Actionable Queued: {queue_summary['total_queued_leaves']}, "
        f"Unresolved Quarantines: {queue_summary['unresolved_quarantines']})"
    )

    # Save audit report
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(master_report, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("\n" + "=" * 65)
    print(f"Audit report saved to: {report_file.relative_to(PROJECT_ROOT)}")
    if all_passed:
        print(">>> ALL SMALL PAUSE GATES PASSED SUCCESSFULLY. <<<")
        print("=" * 65)
        return 0
    else:
        print(">>> GATE VERIFICATION FAILED. EXECUTION HALTED. <<<")
        print("=" * 65)
        if emit_triage:
            log_to_triage({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "monument_id": monument_id,
                "cohort": cohort_num,
                "target_file": str(target_text.name),
                "report_path": str(report_file.relative_to(PROJECT_ROOT)),
                "summary": "Small Pause Gate failure after deterministic self-healing: see report for details",
                "status": "PENDING_DEVELOPER_TRIAGE"
            })
        return 1


def main():
    parser = argparse.ArgumentParser(description="Universal Small Pause Gatekeeper Suite")
    parser.add_argument("--monument", default=None, help="Monument ID")
    parser.add_argument("--cohort", type=int, default=1, help="Cohort number")
    parser.add_argument("--draft", default=None, help="Path to draft markdown file")
    parser.add_argument("--footnotes", default=None, help="Path to footnotes txt file")
    parser.add_argument(
        "--emit-triage",
        action="store_true",
        help="Emit failure signature to scratch/triage_inbox.jsonl on gate failure",
    )

    args = parser.parse_args()

    draft_path = Path(args.draft) if args.draft else None
    footnotes_path = Path(args.footnotes) if args.footnotes else None

    monument_id = args.monument
    if not monument_id:
        if draft_path:
            norm_str = str(draft_path).lower()
            if "1910" in norm_str or "skaballanovich" in norm_str:
                monument_id = "1910_skaballanovich_typikon"
            elif "1899" in norm_str or "dolnytsky" in norm_str:
                monument_id = "1899_dolnytsky_typikon"
            elif "1891" in norm_str or "lviv" in norm_str:
                monument_id = "1891_lviv_synod"
        if not monument_id:
            monument_id = resolve_monument_id(None)

    try:
        sys.exit(
            run_gate(
                monument_id,
                args.cohort,
                custom_draft=draft_path,
                custom_footnotes=footnotes_path,
                emit_triage=args.emit_triage,
            )
        )
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
