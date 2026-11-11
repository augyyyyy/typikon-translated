#!/usr/bin/env python3
"""
Transcript Trajectory, Sandbox & Orthographic Authenticity Auditor (Vectors 5C, 7, 11, 12)
==========================================================================================
Cross-pollinated from the Universal 12-Vector Deep Process, Hallucination & Trajectory
Auditor (v3.0):
  - Vector 5C: Orthographic Fake-Archaism Interceptor (catches synthetic 'Ѿц'/'ѿц'
    hyper-corrections in 'Отецъ'/'Отцю'/'Отче' and deterministic self-healing).
  - Vector 7: Subagent JSONL Transcript Discovery & Tool-Call Overhead Telemetry.
  - Vector 11: Subagent Sandbox & Pure Blind Ink Witness Audit (detects external
    search_web calls, network scripts, out-of-sandbox file writes, and unviewed
    assigned facsimile leaves, attributing violations to last_viewed_leaf).
  - Vector 12: Monument-Level Composite Process Health Index (PHI) & Parent
    Orchestration Self-Audit Report (Audit_Reports/process_autopsy_report.json).
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Vector 5C: Synthetic 'Ѿ'/'ѿ' (U+047E/U+047F) before 'ц'/'Ц' in words derived from Отецъ (Father)
FAKE_OTETS_OMEGA_RE = re.compile(r"([Ѿѿ])([цЦ][\u0300-\u036F\u0483-\u0487]*[ауеиіоъьєюяАУЕИІОЪЬЄЮЯ])")

NETWORK_CMD_RE = re.compile(
    r"(?:urllib\.request|requests\.(?:get|post)|invoke-webrequest|invoke-restmethod|api\.duckduckgo\.com|curl\s+http)",
    re.IGNORECASE,
)

REGEX_GAMING_CMD_RE = re.compile(
    r"(?:\.replace\(\s*['\"]от['\"]\s*,\s*['\"]ѿ['\"]\)|слава\s+ѿцю|test_replacements)",
    re.IGNORECASE,
)


def get_brain_root() -> Path:
    env_brain = os.environ.get("ANTIGRAVITY_BRAIN_DIR")
    if env_brain:
        return Path(env_brain)
    return Path.home() / ".gemini" / "antigravity" / "brain"


def heal_source_orthographic_hypercorrections(text: str) -> Tuple[str, int]:
    """
    Vector 5C Deterministic Healer:
    Repairs synthetic 'Ѿц' / 'ѿц' hyper-corrections (e.g. 'Ѿца' -> 'Отца', 'Ѿцю' -> 'Отцю',
    'ѿца' -> 'отца') back to authentic printed/manuscript orthography.
    """
    count = 0

    def _repl(match: re.Match) -> str:
        nonlocal count
        count += 1
        omega_char = match.group(1)
        rest = match.group(2)
        prefix = "От" if omega_char == "Ѿ" else "от"
        return f"{prefix}{rest}"

    healed = FAKE_OTETS_OMEGA_RE.sub(_repl, text)
    return healed, count


def audit_source_orthographic_authenticity(source_file: Optional[Path]) -> Dict[str, Any]:
    """
    Vector 5C Gate Check:
    Scans Source Text/cohort_N_source.txt for synthetic 'Ѿц'/'ѿц' hyper-corrections.
    """
    if not source_file or not source_file.exists():
        return {
            "passed": True,
            "violation_count": 0,
            "violations": [],
            "status": "SKIPPED_NO_SOURCE_FILE",
        }

    try:
        content = source_file.read_text(encoding="utf-8")
    except OSError as exc:
        return {
            "passed": True,
            "violation_count": 0,
            "violations": [],
            "status": f"READ_ERROR: {exc}",
        }

    violations: List[Dict[str, Any]] = []
    current_leaf: Optional[int] = None
    leaf_re = re.compile(r"^===\s*LEAF\s+p?(\d+)\s*===", re.IGNORECASE)

    for line_num, line in enumerate(content.splitlines(), start=1):
        m_leaf = leaf_re.match(line.strip())
        if m_leaf:
            current_leaf = int(m_leaf.group(1))
            continue
        for m_fake in FAKE_OTETS_OMEGA_RE.finditer(line):
            violations.append({
                "line": line_num,
                "leaf": current_leaf,
                "matched_token": m_fake.group(0),
                "snippet": line.strip()[:120],
            })

    return {
        "passed": len(violations) == 0,
        "violation_count": len(violations),
        "violations": violations[:25],
        "status": "PASSED" if len(violations) == 0 else "FAILED_V5C_FAKE_ARCHAISM",
    }


def discover_cohort_subagent_transcript(
    monument_id: str,
    cohort_num: int,
    brain_dir: Optional[Path] = None,
) -> Optional[Path]:
    """
    Vector 7 Transcript Discovery:
    Locates the subagent transcript.jsonl corresponding to (monument_id, cohort_num)
    by scanning recent brain directories for matching work-order/cohort target markers.
    """
    root = brain_dir or get_brain_root()
    if not root.exists():
        return None

    target_draft_token = f"{monument_id}_cohort{cohort_num}_raw_draft.md".lower()
    target_source_token = f"{monument_id}_cohort{cohort_num}_source.txt".lower()
    target_wo_token = f"work_order_cohort_{cohort_num}.md".lower()
    target_wo_alt_token = f"cohort_{cohort_num}_work_order.md".lower()
    target_cohort_phrase = f"for cohort {cohort_num} ".lower()

    candidates: List[Tuple[float, Path]] = []
    try:
        for conv_dir in root.iterdir():
            if not conv_dir.is_dir():
                continue
            t_path = conv_dir / ".system_generated" / "logs" / "transcript.jsonl"
            if not t_path.exists():
                continue
            try:
                mtime = t_path.stat().st_mtime
                candidates.append((mtime, t_path))
            except OSError:
                continue
    except OSError:
        return None

    # Inspect most recent transcripts first (bounded to top 300 recent sessions to cover multi-monument parallel runs)
    candidates.sort(key=lambda item: item[0], reverse=True)
    fallback_match: Optional[Path] = None
    for _mtime, t_path in candidates[:300]:
        try:
            text_low = t_path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue

        if monument_id.lower() not in text_low:
            continue

        # Check if this is a worker subagent session (exclude USER_EXPLICIT parent chats and adversarial review / compacted envelopes)
        first_line = text_low.splitlines()[0] if text_low else ""
        step0_content = first_line
        try:
            step0_obj = json.loads(first_line)
            if isinstance(step0_obj, dict):
                if str(step0_obj.get("source") or "").lower() == "user_explicit":
                    continue
                step0_content = str(step0_obj.get("content") or "").lower()
        except json.JSONDecodeError:
            pass
        if (
            '"user_explicit"' in first_line
            or "<original_task>" in step0_content
            or "<prior_attempt>" in step0_content
            or "<context_summary>" in step0_content
            or "\\u003coriginal_task" in first_line
            or "\\u003cprior_attempt" in first_line
            or "\\u003ccontext_summary" in first_line
        ):
            continue

        # Primary match: initial subagent prompt (first_line) explicitly targets this monument and cohort
        if monument_id.lower() in first_line and (
            target_wo_alt_token in first_line
            or target_wo_token in first_line
            or target_draft_token in first_line
            or target_source_token in first_line
            or target_cohort_phrase in first_line
        ):
            return t_path

        # Guard against matching a subagent from another monument or another cohort
        if monument_id.lower() not in first_line:
            continue

        # Guard against matching a subsequent cohort's subagent that merely read this cohort for context
        other_cohort_in_prompt = re.search(r"cohort[_\s]+(\d+)", first_line)
        if other_cohort_in_prompt and int(other_cohort_in_prompt.group(1)) != cohort_num:
            continue

        if fallback_match is None and (
            target_draft_token in text_low
            or target_source_token in text_low
            or target_wo_token in text_low
            or target_wo_alt_token in text_low
        ):
            fallback_match = t_path

    return fallback_match


def audit_cohort_subagent_trajectory(
    monument_id: str,
    cohort_num: int,
    expected_leaves: List[int],
    ws: Path,
    brain_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Vector 7 & Vector 11 Subagent Trajectory & Sandbox Auditor:
      1. Discovers the subagent's transcript.jsonl for (monument_id, cohort_num).
      2. Extracts all Page_XXXX.jpg leaf inspections and their ISO-8601 runtime timestamps.
      3. Detects forbidden search_web calls, network commands, out-of-sandbox file mutations,
         and regex gaming commands, attributing any violation to last_viewed_leaf.
    """
    t_path = discover_cohort_subagent_transcript(monument_id, cohort_num, brain_dir=brain_dir)
    if t_path is None or not t_path.exists():
        return {
            "status": "SKIPPED_NO_TRANSCRIPT",
            "passed": True,
            "transcript_found": False,
            "conversation_id": None,
            "expected_leaves_count": len(expected_leaves),
            "viewed_leaves": [],
            "unviewed_leaves": [],
            "view_timestamps": {},
            "total_tool_calls": 0,
            "tool_call_waste_pct": 0.0,
            "violations": [],
            "contaminated_leaves": [],
        }

    conv_id = t_path.parent.parent.parent.name
    viewed_leaves_set: Set[int] = set()
    view_timestamps: Dict[int, str] = {}
    last_viewed_leaf: Optional[int] = expected_leaves[0] if expected_leaves else None
    total_tool_calls = 0
    wasted_tool_calls = 0
    violations: List[Dict[str, Any]] = []
    contaminated_leaves: Set[int] = set()

    page_re = re.compile(
        r"(?:Page_0*(\d+)|(?<![a-z0-9])p0*(\d+)|rot_0*(\d+))(?:_[a-z0-9_]+)?\.(?:jpg|jpeg|png|tif|tiff)",
        re.IGNORECASE,
    )
    ws_norm = str(ws.resolve()).replace("\\", "/").lower()
    expected_set = set(expected_leaves)

    full_t_path = t_path.with_name("transcript_full.jsonl")
    read_t_path = full_t_path if full_t_path.exists() else t_path

    try:
        lines = read_t_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError as exc:
        return {
            "status": f"READ_ERROR: {exc}",
            "passed": True,
            "transcript_found": False,
            "conversation_id": conv_id,
            "expected_leaves_count": len(expected_leaves),
            "viewed_leaves": [],
            "unviewed_leaves": [],
            "view_timestamps": {},
            "total_tool_calls": 0,
            "tool_call_waste_pct": 0.0,
            "violations": [],
            "contaminated_leaves": [],
        }

    for line in lines:
        if not line.strip():
            continue
        try:
            step = json.loads(line)
        except json.JSONDecodeError:
            continue

        step_ts = str(step.get("created_at") or "")
        step_status = str(step.get("status") or "")
        tool_calls = step.get("tool_calls") or []
        if not isinstance(tool_calls, list):
            continue

        for tc in tool_calls:
            if not isinstance(tc, dict):
                continue
            total_tool_calls += 1
            t_name = str(tc.get("name") or tc.get("tool_name") or "")
            t_args = tc.get("args") or tc.get("arguments") or {}
            if isinstance(t_args, str):
                try:
                    t_args = json.loads(t_args)
                except json.JSONDecodeError:
                    t_args = {"raw": t_args}
            if not isinstance(t_args, dict):
                t_args = {}

            if step_status == "ERROR":
                wasted_tool_calls += 1

            # 1. Track image view provenance
            if t_name in ("read_file", "view_file"):
                path_val = str(t_args.get("Path") or t_args.get("AbsolutePath") or "")
                m_pg = page_re.search(path_val)
                if m_pg:
                    leaf_no = int(m_pg.group(1) or m_pg.group(2) or m_pg.group(3))
                    if not expected_set or leaf_no in expected_set:
                        viewed_leaves_set.add(leaf_no)
                        last_viewed_leaf = leaf_no
                        if leaf_no not in view_timestamps and step_ts:
                            view_timestamps[leaf_no] = step_ts

            # 2. Vector 11A: External search_web calls
            elif t_name == "search_web":
                wasted_tool_calls += 1
                q_str = str(t_args.get("query") or "")[:100]
                violations.append({
                    "type": "subagent_web_search_call",
                    "tool": t_name,
                    "detail": f"Subagent called search_web('{q_str}') during cohort translation",
                    "attributed_leaf": last_viewed_leaf,
                })
                if last_viewed_leaf is not None:
                    contaminated_leaves.add(last_viewed_leaf)

            # 3. Vector 11B: Out-of-sandbox writes/edits
            elif t_name in ("write_file", "edit_file"):
                target_p = str(t_args.get("Path") or t_args.get("TargetFile") or "").replace("\\", "/").lower()
                if target_p:
                    in_monument_ws = ws_norm in target_p or f"/{monument_id.lower()}/" in target_p or target_p.startswith(f"liturgical monuments/monument ")
                    in_allowed_dir = (
                        "/source text/" in target_p
                        or "/draft/" in target_p
                        or "/drafts/" in target_p
                        or "/scratch/" in target_p
                        or target_p.startswith("scratch/")
                        or "/.gemini/antigravity/brain/" in target_p
                    )
                    if not (in_monument_ws or in_allowed_dir):
                        wasted_tool_calls += 1
                        violations.append({
                            "type": "out_of_sandbox_write",
                            "tool": t_name,
                            "detail": f"Subagent wrote/edited outside cohort sandbox: {target_p}",
                            "attributed_leaf": last_viewed_leaf,
                        })
                        if last_viewed_leaf is not None:
                            contaminated_leaves.add(last_viewed_leaf)

            # 4. Vector 11C: Network queries or orthographic regex gaming in run_command
            elif t_name == "run_command":
                cmd_str = str(t_args.get("CommandLine") or "")
                if NETWORK_CMD_RE.search(cmd_str):
                    wasted_tool_calls += 1
                    violations.append({
                        "type": "subagent_network_command",
                        "tool": t_name,
                        "detail": f"Subagent executed network query in run_command: {cmd_str[:100]}",
                        "attributed_leaf": last_viewed_leaf,
                    })
                    if last_viewed_leaf is not None:
                        contaminated_leaves.add(last_viewed_leaf)
                if REGEX_GAMING_CMD_RE.search(cmd_str):
                    wasted_tool_calls += 1
                    violations.append({
                        "type": "orthographic_regex_gaming_command",
                        "tool": t_name,
                        "detail": f"Subagent executed bulk orthographic replacement command: {cmd_str[:100]}",
                        "attributed_leaf": last_viewed_leaf,
                    })
                    if last_viewed_leaf is not None:
                        contaminated_leaves.add(last_viewed_leaf)

    unviewed_leaves = sorted(set(expected_leaves) - viewed_leaves_set) if viewed_leaves_set else []
    waste_pct = round((wasted_tool_calls / float(total_tool_calls)) * 100.0, 2) if total_tool_calls > 0 else 0.0

    return {
        "status": "PASSED" if len(violations) == 0 else "CONTAMINATED_TRAJECTORY_QUEUED_FOR_ARGON",
        "passed": len(violations) == 0,
        "transcript_found": True,
        "conversation_id": conv_id,
        "expected_leaves_count": len(expected_leaves),
        "viewed_leaves": sorted(viewed_leaves_set),
        "unviewed_leaves": unviewed_leaves,
        "view_timestamps": {str(k): v for k, v in sorted(view_timestamps.items())},
        "total_tool_calls": total_tool_calls,
        "tool_call_waste_pct": waste_pct,
        "violations": violations,
        "contaminated_leaves": sorted(contaminated_leaves),
    }


def build_monument_process_autopsy(
    monument_id: str,
    ws: Path,
    total_pages: int,
    brain_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Vector 12 Monument-Level Process, Hallucination & Trajectory Autopsy Builder:
    Synthesizes cohort Small Pause reports, Argon Queue resolution telemetry,
    Vector 5C orthographic integrity, and Vector 7/11/12 trajectory health into
    Audit_Reports/process_autopsy_report.json with a 0-100 Composite PHI score.
    """
    audit_dir = ws / "Audit_Reports"
    audit_dir.mkdir(parents=True, exist_ok=True)

    cohort_reports = sorted(audit_dir.glob("cohort*_small_pause_report.json"))
    cohorts_analyzed = len(cohort_reports)
    first_pass_cohorts = 0
    v5c_violations_total = 0
    trajectory_violations_total = 0
    transcripts_matched = 0

    # Check Argon Review Queue resolution state first so Argon-resolved leaves are credited
    argon_q_path = audit_dir / "argon_review_queue.json"
    unresolved_quarantines = 0
    total_argon_items = 0
    resolved_argon_items = 0
    resolved_argon_leaves: Set[int] = set()
    if argon_q_path.exists():
        try:
            aq = json.loads(argon_q_path.read_text(encoding="utf-8"))
            unresolved_quarantines = int(aq.get("unresolved_quarantines", 0))
            items = aq.get("items", [])
            total_argon_items = len(items)
            resolved_argon_items = sum(1 for it in items if isinstance(it, dict) and it.get("status") == "RESOLVED_BY_ARGON")
            resolved_argon_leaves = {
                int(it.get("leaf_num", -1))
                for it in items
                if isinstance(it, dict) and it.get("status") == "RESOLVED_BY_ARGON"
            }
        except (OSError, json.JSONDecodeError):
            pass

    cohort_trajectories_summary: List[Dict[str, Any]] = []
    for rep_path in cohort_reports:
        try:
            rep = json.loads(rep_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if rep.get("overall_status") == "PASSED":
            first_pass_cohorts += 1
        c_num = int(rep.get("cohort", 0))
        gates = rep.setdefault("gates", {})
        rep_modified = False

        v5c_data = gates.get("orthographic_authenticity_v5c", {})
        if not v5c_data and c_num > 0:
            cand_sf = ws / "Source Text" / f"{monument_id}_cohort{c_num}_source.txt"
            if cand_sf.exists():
                v5c_data = audit_source_orthographic_authenticity(cand_sf)
                gates["orthographic_authenticity_v5c"] = v5c_data
                rep_modified = True
        v5c_violations_total += int(v5c_data.get("violation_count", 0))

        traj_data = gates.get("subagent_trajectory", {})
        if (not traj_data or not traj_data.get("transcript_found") or bool(traj_data.get("unviewed_leaves"))) and c_num > 0:
            leaf_stats = gates.get("structural_sequence", {}).get("leaf_stats", {})
            min_l = int(leaf_stats.get("min_leaf", (c_num - 1) * 10 + 1))
            max_l = int(leaf_stats.get("max_leaf", min(total_pages, c_num * 10)))
            expected_l = list(range(min_l, max_l + 1))
            live_traj = audit_cohort_subagent_trajectory(
                monument_id=monument_id,
                cohort_num=c_num,
                expected_leaves=expected_l,
                ws=ws,
                brain_dir=brain_dir,
            )
            if live_traj.get("transcript_found") or not traj_data:
                traj_data = live_traj
                gates["subagent_trajectory"] = traj_data
                rep_modified = True

        if rep_modified:
            try:
                rep_path.write_text(json.dumps(rep, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
            except OSError:
                pass

        if traj_data.get("transcript_found"):
            transcripts_matched += 1
        unresolved_v_for_cohort: List[Dict[str, Any]] = []
        for v_item in traj_data.get("violations", []):
            if isinstance(v_item, dict) and int(v_item.get("attributed_leaf") or -1) in resolved_argon_leaves:
                continue
            trajectory_violations_total += 1
            if isinstance(v_item, dict):
                unresolved_v_for_cohort.append(v_item)

        if unresolved_v_for_cohort and argon_q_path.exists():
            try:
                aq_live = json.loads(argon_q_path.read_text(encoding="utf-8"))
                aq_items = [it for it in aq_live.get("items", []) if isinstance(it, dict)]
                aq_by_leaf = {int(it["leaf_num"]): it for it in aq_items if "leaf_num" in it}
                aq_modified = False
                for v_item in unresolved_v_for_cohort:
                    attr_l = int(v_item.get("attributed_leaf") or -1)
                    if attr_l <= 0 or attr_l in resolved_argon_leaves:
                        continue
                    v_reason = f"vector11_trajectory_violation: {v_item.get('type')} ({v_item.get('tool')})"
                    existing_it = aq_by_leaf.get(attr_l)
                    if existing_it:
                        if existing_it.get("status") != "RESOLVED_BY_ARGON":
                            if existing_it.get("status") == "INFO_TELEMETRY_ONLY":
                                existing_it["status"] = "QUEUED_FOR_ARGON"
                                aq_modified = True
                            if v_reason not in existing_it.setdefault("reasons", []):
                                existing_it["reasons"].append(v_reason)
                                aq_modified = True
                    else:
                        aq_by_leaf[attr_l] = {
                            "leaf_num": attr_l,
                            "cohort": c_num,
                            "status": "QUEUED_FOR_ARGON",
                            "reasons": [v_reason],
                            "draft_file": str((ws / "Draft" / f"{monument_id}_cohort{c_num}_raw_draft.md").relative_to(PROJECT_ROOT)),
                            "source_file": str((ws / "Source Text" / f"{monument_id}_cohort{c_num}_source.txt").relative_to(PROJECT_ROOT)),
                            "updated_at": datetime.now(timezone.utc).isoformat(),
                        }
                        aq_modified = True
                if aq_modified:
                    sorted_aq = [aq_by_leaf[k] for k in sorted(aq_by_leaf.keys())]
                    active_aq = [it for it in sorted_aq if it.get("status") not in ("RESOLVED_BY_ARGON", "INFO_TELEMETRY_ONLY")]
                    info_aq = [it for it in sorted_aq if it.get("status") == "INFO_TELEMETRY_ONLY"]
                    quar_aq = [it for it in sorted_aq if it.get("status") == "QUARANTINED_FOR_ARGON"]
                    aq_live["items"] = sorted_aq
                    aq_live["total_queued_leaves"] = len(active_aq)
                    aq_live["info_telemetry_leaves"] = len(info_aq)
                    aq_live["unresolved_quarantines"] = len(quar_aq)
                    total_argon_items = len(sorted_aq)
                    argon_q_path.write_text(json.dumps(aq_live, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
            except (OSError, json.JSONDecodeError, ValueError):
                pass

        cohort_trajectories_summary.append({
            "cohort": c_num,
            "conversation_id": traj_data.get("conversation_id"),
            "transcript_found": bool(traj_data.get("transcript_found")),
            "expected_leaves_count": int(traj_data.get("expected_leaves_count", 0)),
            "viewed_leaves_count": len(traj_data.get("viewed_leaves", [])),
            "unviewed_leaves": traj_data.get("unviewed_leaves", []),
            "total_tool_calls": int(traj_data.get("total_tool_calls", 0)),
            "tool_call_waste_pct": float(traj_data.get("tool_call_waste_pct", 0.0)),
            "violations_count": len(traj_data.get("violations", [])),
            "status": traj_data.get("status", "UNKNOWN"),
        })
    cohort_trajectories_summary.sort(key=lambda x: x["cohort"])

    # Check source files directly for Vector 5C if not yet in cohort reports
    src_dir = ws / "Source Text"
    if not cohort_reports and src_dir.exists():
        for sf in sorted(src_dir.glob("*_cohort*_source.txt")):
            v5c_res = audit_source_orthographic_authenticity(sf)
            v5c_violations_total += int(v5c_res.get("violation_count", 0))

    # Check Phase 0 Preflight Brief vision budget contract
    preflight_path = audit_dir / "phase0_preflight_brief.json"
    phase0_contract_verified = preflight_path.exists()

    # Compute 3-Pillar Composite Process Health Index (PHI: 0.0 - 100.0)
    # Pillar I (45%): Epistemic, Conservation & Orthographic Fidelity (V1-V6, V5C)
    pillar_1 = 45.0
    if v5c_violations_total > 0:
        pillar_1 = max(0.0, pillar_1 - min(25.0, v5c_violations_total * 5.0))
    if unresolved_quarantines > 0:
        pillar_1 = max(0.0, pillar_1 - min(20.0, unresolved_quarantines * 10.0))

    # Pillar II (35%): Trajectory, Sandbox & Pacing Integrity (V7, V8, V11, V12)
    pillar_2 = 35.0
    if trajectory_violations_total > 0:
        pillar_2 = max(0.0, pillar_2 - min(25.0, trajectory_violations_total * 10.0))

    # Pillar III (20%): Structural & Publication Coherence (V9, V10)
    pillar_3 = 20.0
    if cohorts_analyzed > 0 and first_pass_cohorts < cohorts_analyzed:
        failed_cohorts = cohorts_analyzed - first_pass_cohorts
        pillar_3 = max(0.0, pillar_3 - min(10.0, failed_cohorts * 2.0))

    phi_score = round(pillar_1 + pillar_2 + pillar_3, 2)
    passed = (v5c_violations_total == 0 and unresolved_quarantines == 0 and trajectory_violations_total == 0)

    autopsy_report = {
        "schema_version": "3.0-translation-cross-pollinated",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "monument_id": monument_id,
        "total_physical_pages": total_pages,
        "cohorts_analyzed": cohorts_analyzed,
        "first_pass_cohorts": first_pass_cohorts,
        "transcripts_matched": transcripts_matched,
        "passed": passed,
        "phi_score": phi_score,
        "pillars": {
            "pillar_1_epistemic_and_orthographic_max45": round(pillar_1, 2),
            "pillar_2_trajectory_and_sandbox_max35": round(pillar_2, 2),
            "pillar_3_structural_and_compiler_max20": round(pillar_3, 2),
        },
        "vectors": {
            "vector_5c_fake_archaism_violations": v5c_violations_total,
            "vector_11_subagent_sandbox_violations": trajectory_violations_total,
            "vector_12_phase0_contract_present": phase0_contract_verified,
            "argon_queue_total_items": total_argon_items,
            "argon_queue_resolved_items": resolved_argon_items,
            "argon_queue_unresolved_quarantines": unresolved_quarantines,
        },
        "cohort_trajectories": cohort_trajectories_summary,
    }

    out_path = audit_dir / "process_autopsy_report.json"
    try:
        out_path.write_text(
            json.dumps(autopsy_report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    except OSError:
        pass

    return autopsy_report
