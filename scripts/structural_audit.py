#!/usr/bin/env python3
"""
Universal Structural & Rubrical Sequence Auditor
================================================
Audits English translation drafts to ensure unbroken statutory numbering,
rubrical sequence integrity, and correct genre-scoped markdown heading levels.

Usage:
    python scripts/structural_audit.py --target draft.md
    python scripts/structural_audit.py --monument 1891_lviv_synod --cohort 3
"""

import sys
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Set

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

from orchestrator_state import resolve_monument_type, load_monument_scaffold

BANNED_FABRICATED_HEADING_PATTERNS = [
    (re.compile(r"^#{1,6}\s+(?:At\s+(?:Sunday\s+)?(?:Midnight\s+Office|Matins|Vespers|the\s+Praises)|Sunday\s+Divine\s+Liturgy|On\s+(?:Saturday|Sunday)\s+Evening|On\s+Sunday\s+at\s+the\s+Liturgy|Canon\s+(?:to|of)\s+|Ode\s+\d+|Sessional\s+Hymn|Hypakoe|Hymns\s+of\s+Ascent|Gradual\s+Hymns|Prokeimenon|The\s+Beatitudes|Penitential\s+Stichera|Other\s+Stichera|Antiphon\s+\d+)", re.IGNORECASE), "FABRICATED_LITURGICAL_HEADING"),
]


def extract_accounted_leaves(text: str) -> Set[int]:
    """Extracts all physical leaf numbers witnessed in text content."""
    accounted: Set[int] = set()
    for m in re.finditer(r'===\s*LEAF\s+p?(\d+)\s*===', text, re.IGNORECASE):
        accounted.add(int(m.group(1)))
    return accounted


def parse_leaf_blocks(text: str) -> Dict[int, str]:
    """Parses text into {leaf_num: leaf_body} using canonical === LEAF pN === delimiters."""
    blocks: Dict[int, str] = {}
    matches = list(re.finditer(r'===\s*LEAF\s+p?(\d+)\s*===', text, re.IGNORECASE))
    for idx, m in enumerate(matches):
        leaf_num = int(m.group(1))
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        blocks[leaf_num] = text[start:end].strip()
    return blocks


def get_allowed_h1_landmarks(monument_id: Optional[str], mon_entry: Dict[str, Any]) -> List[str]:
    """
    Returns genre-scoped H1 landmark regexes for the monument, combining explicit
    publication_spec.parts landmarks with the monument_type scaffold's allowed_h1_patterns.
    """
    pub_spec = mon_entry.get("publication_spec", {})
    parts = pub_spec.get("parts", [])
    allowed: List[str] = [p.get("start_landmark") for p in parts if p.get("start_landmark")]

    scaf = load_monument_scaffold(monument_id or "", mon_entry)
    mon_type = scaf.get("monument_type", resolve_monument_type(monument_id or "", mon_entry))
    for pat in scaf.get("allowed_h1_patterns", []):
        if pat and pat not in allowed:
            allowed.append(pat)
    for sp in scaf.get("parts", []):
        lm = sp.get("start_landmark")
        if lm and lm not in allowed:
            allowed.append(lm)

    # Generic structural H1 patterns allowed across all monuments (with optional leading 'THE ')
    generic_h1 = [
        r"^#\s+(?:THE\s+)?PREFACE(?::\s+TO\s+THE\s+READER)?",
        r"^#\s+(?:THE\s+)?(?:PART\s+[IVXLCDM\d]+|CHAPTER\s+\d+|SECTION\s+[IVXLCDM\d]+|APPENDIX|TABLE\s+OF\s+CONTENTS|ORDER\s+OF|SELECTED\s+PSALMS|BOOK\s+OF|PASCHALION|MENOLOGION|KANONIKON|COLOPHON)",
    ]
    for g in generic_h1:
        if g not in allowed:
            allowed.append(g)

    if mon_type in ("octoechos", "irmologion"):
        for oct_pat in (
            r"^#\s+(?:THE\s+)?TONE\s+\d+",
            r"^#\s+(?:THE\s+)?EXAPOSTILARIA",
            r"^#\s+(?:THE\s+)?WEEKDAY\s+(?:OCTOECHOS|OFFICES)",
            r"^#\s+(?:THE\s+)?(?:ASCETIC\s+HOMILIES|GENERAL\s+PARASTAS|PARASTAS)",
        ):
            if oct_pat not in allowed:
                allowed.append(oct_pat)

    return allowed


def audit_structure(
    filepath: Path,
    prev_filepath: Optional[Path] = None,
    cohort_num: Optional[int] = None,
    monument_id: Optional[str] = None
) -> Dict[str, Any]:
    if not filepath.exists():
        raise FileNotFoundError(f"Target file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()

    is_bilingual = False
    resolved_monument = monument_id
    if not resolved_monument:
        candidate = filepath.name.split("_cohort")[0]
        if candidate:
            resolved_monument = candidate

    mon_entry = {}
    if REGISTRY_FILE.exists() and resolved_monument:
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as rf:
                reg_data = json.load(rf)
            mon_entry = reg_data.get("monuments", {}).get(resolved_monument, {})
            lang = mon_entry.get("source_language", "")
            if "bilingual" in lang.lower():
                is_bilingual = True
        except (KeyError, json.JSONDecodeError, OSError):
            pass
    if "1888_violakis" in filepath.name:
        is_bilingual = True

    headings: List[Dict[str, Any]] = []
    numbered_items: List[int] = []
    odd_numbered_items: List[int] = []
    even_numbered_items: List[int] = []
    current_leaf: Optional[int] = None
    paragraph_count = 0
    anomalies: List[str] = []

    for line_num, line in enumerate(lines, 1):
        s = line.strip()
        if not s:
            continue
        paragraph_count += 1

        m_leaf = re.match(r"===\s*LEAF\s+p?(\d+)", s, re.IGNORECASE)
        if m_leaf:
            current_leaf = int(m_leaf.group(1))

        if s.startswith("#"):
            level = len(s) - len(s.lstrip("#"))
            title = s.lstrip("#").strip()
            headings.append({"line": line_num, "level": level, "title": title, "leaf": current_leaf})

        m_statute = re.match(r"^(?:\*{1,2})?(\d+)\.(?:\*{1,2})?\s+", s)
        if m_statute:
            num = int(m_statute.group(1))
            numbered_items.append(num)
            if current_leaf is not None:
                if current_leaf % 2 == 1:
                    odd_numbered_items.append(num)
                else:
                    even_numbered_items.append(num)

    breaks = []
    if is_bilingual:
        for i in range(len(odd_numbered_items) - 1):
            curr_n = odd_numbered_items[i]
            next_n = odd_numbered_items[i + 1]
            if next_n > curr_n + 1 and next_n < curr_n + 5:
                breaks.append(f"Odd/Source leaf jump from {curr_n} to {next_n}")
        for i in range(len(even_numbered_items) - 1):
            curr_n = even_numbered_items[i]
            next_n = even_numbered_items[i + 1]
            if next_n > curr_n + 1 and next_n < curr_n + 5:
                breaks.append(f"Even/Translation leaf jump from {curr_n} to {next_n}")
    else:
        for i in range(len(numbered_items) - 1):
            curr_n = numbered_items[i]
            next_n = numbered_items[i + 1]
            if next_n > curr_n + 1 and next_n < curr_n + 5:
                breaks.append(f"Jump from {curr_n} to {next_n}")

    curr_leaves = extract_accounted_leaves(content)
    leaf_stats: Dict[str, Any] = {
        "leaves_count": len(curr_leaves),
        "min_leaf": min(curr_leaves) if curr_leaves else None,
        "max_leaf": max(curr_leaves) if curr_leaves else None,
    }

    target_blocks = parse_leaf_blocks(content)
    if curr_leaves:
        c_min, c_max = min(curr_leaves), max(curr_leaves)
        intra_gaps = sorted(list(set(range(c_min, c_max + 1)) - curr_leaves))
        if intra_gaps:
            anomalies.append(f"Intra-cohort leaf gaps detected: {intra_gaps}")

        for p_num, body_txt in sorted(target_blocks.items()):
            if len(body_txt) < 5:
                anomalies.append(f"Empty or trivial leaf block for === LEAF p{p_num} === ({len(body_txt)} chars)")

        if cohort_num == 1 and c_min != 1:
            anomalies.append(f"Cohort 1 initial anchor violation: expected leaf p1, but found starting leaf p{c_min}.")

        if prev_filepath and prev_filepath.exists():
            with open(prev_filepath, "r", encoding="utf-8") as pf:
                prev_text = pf.read()
            prev_leaves = extract_accounted_leaves(prev_text)
            if prev_leaves:
                prev_max = max(prev_leaves)
                expected_next = prev_max + 1
                if c_min > expected_next:
                    missing_span = list(range(expected_next, c_min))
                    anomalies.append(
                        f"Inter-cohort leaf chasm: Previous cohort ended at p{prev_max}, "
                        f"current cohort starts at p{c_min}. Missing folios: {missing_span}"
                    )
                elif c_max < prev_max:
                    anomalies.append(
                        f"Out-of-order cohort sequence: Current max leaf p{c_max} "
                        f"precedes previous max leaf p{prev_max}."
                    )

    is_hymnographic = False
    genre = mon_entry.get("genre_register", "").lower()
    mon_type = resolve_monument_type(resolved_monument or "", mon_entry)
    if genre == "hymnographic" or mon_type in ("octoechos", "lenten_triodion", "pentecostarion", "anthologion", "akathistnik", "irmologion"):
        is_hymnographic = True

    allowed_landmarks = get_allowed_h1_landmarks(resolved_monument, mon_entry)

    for h in headings:
        line_no = h["line"]
        lvl = h["level"]
        htitle = h["title"]
        hleaf = h.get("leaf")

        for pat, pat_name in BANNED_FABRICATED_HEADING_PATTERNS:
            if pat.search(f"{'#' * lvl} {htitle}"):
                anomalies.append(
                    f"PRE_TRAINING_DATA_INCURSION (L{line_no}, leaf p{hleaf}): "
                    f"Heading '{htitle}' is a fabricated modern office / liturgical heading. "
                    f"Historical codices format rubrics as inline italics ('*...*')."
                )

        if is_hymnographic and lvl >= 2:
            is_authorized_h2 = False
            if lvl == 2:
                guardrails_str = " ".join(mon_entry.get("flash_execution_guardrails", []))
                if "H1 & H2" in guardrails_str:
                    is_authorized_h2 = True
            if not is_authorized_h2:
                anomalies.append(
                    f"EPIGRAPHIC_HEADING_VIOLATION (L{line_no}, leaf p{hleaf}): "
                    f"Level-{lvl} heading '{htitle}' is prohibited in hymnographic codices. "
                    f"Use inline italic rubrics ('*...*')."
                )

        if lvl == 1:
            is_valid_h1 = any(re.search(lm, f"# {htitle}", re.IGNORECASE) for lm in allowed_landmarks if lm)
            if not is_valid_h1:
                anomalies.append(
                    f"UNSANCTIONED_H1_HEADING (L{line_no}, leaf p{hleaf}): "
                    f"'# {htitle}' does not match any authorized publication landmark for monument_type='{mon_type}'."
                )

    passed = len(anomalies) == 0 and len(breaks) == 0 and paragraph_count > 0

    return {
        "file": str(filepath.name),
        "passed": passed,
        "paragraphs": paragraph_count,
        "headings_count": len(headings),
        "headings": headings[:15],
        "numbered_items_count": len(numbered_items),
        "number_breaks": breaks,
        "leaf_stats": leaf_stats,
        "anomalies": anomalies
    }


def main():
    parser = argparse.ArgumentParser(description="Universal Structural & Rubrical Sequence Auditor")
    parser.add_argument("--target", help="Path to text or markdown file")
    parser.add_argument("--prev-target", help="Path to previous cohort text or markdown file")
    parser.add_argument("--monument", help="Monument ID")
    parser.add_argument("--cohort", type=int, help="Cohort number")
    parser.add_argument("--json", action="store_true", help="Output JSON results")

    args = parser.parse_args()

    target_path = None
    prev_path = None

    if args.prev_target:
        prev_path = Path(args.prev_target)

    if args.target:
        target_path = Path(args.target)
    elif args.monument and args.cohort:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            registry = json.load(f)
        mon_info = registry.get("monuments", {}).get(args.monument, {})
        ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{args.monument}")

        final_cand = ws / "Final MD" / f"{args.monument}_cohort{args.cohort}.md"
        draft_cand = ws / "Draft" / f"{args.monument}_cohort{args.cohort}_raw_draft.md"
        target_path = final_cand if final_cand.exists() else draft_cand

        if not prev_path and args.cohort > 1:
            prev_cohort = args.cohort - 1
            prev_final = ws / "Final MD" / f"{args.monument}_cohort{prev_cohort}.md"
            prev_draft = ws / "Draft" / f"{args.monument}_cohort{prev_cohort}_raw_draft.md"
            if prev_final.exists():
                prev_path = prev_final
            elif prev_draft.exists():
                prev_path = prev_draft

    if not target_path:
        print("ERROR: Specify --target or (--monument and --cohort)", file=sys.stderr)
        sys.exit(1)

    res = audit_structure(target_path, prev_filepath=prev_path, cohort_num=args.cohort, monument_id=args.monument)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"Structural Audit for: {res['file']}")
        print(f"Paragraphs: {res['paragraphs']} | Headings: {res['headings_count']} | Numbered Items: {res['numbered_items_count']}")
        leaf_s = res.get('leaf_stats', {})
        if leaf_s.get('leaves_count'):
            print(f"Accounted Leaves: {leaf_s['leaves_count']} folios (span: p{leaf_s['min_leaf']}..p{leaf_s['max_leaf']})")
        print(f"Status: {'PASSED' if res['passed'] else 'FAILED'}")
        if res["number_breaks"]:
            print(f"  Numbering Breaks: {res['number_breaks']}")
        if res["anomalies"]:
            print(f"  Anomalies: {res['anomalies']}")

    sys.exit(0 if res["passed"] else 1)


if __name__ == "__main__":
    main()
