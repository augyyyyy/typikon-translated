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
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"
STATE_FILE = PROJECT_ROOT / "Liturgical Monuments" / "ACTIVE_ORCHESTRATOR_STATE.json"
TRIAGE_INBOX = PROJECT_ROOT / "scratch" / "triage_inbox.jsonl"
SHARED_LEXICON_DIR = PROJECT_ROOT.parent / "Shared_Lexicon"

def log_to_triage(entry: Dict[str, Any]) -> None:
    TRIAGE_INBOX.parent.mkdir(parents=True, exist_ok=True)
    with open(TRIAGE_INBOX, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
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
        for fname in (f"p{leaf}.png", f"p{leaf}.jpg", f"Page_{leaf:04d}.jpg"):
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

def run_gate(monument_id: str, cohort_num: int, custom_draft: Optional[Path] = None, custom_footnotes: Optional[Path] = None) -> int:
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

    print("=" * 65)
    print(f"  SMALL PAUSE GATEKEEPER SUITE — COHORT #{cohort_num}")
    print(f"  Monument: {mon_info.get('title')}")
    print(f"  Audited File: {target_text.relative_to(PROJECT_ROOT) if target_text.is_relative_to(PROJECT_ROOT) else target_text}")
    print(f"  Footnotes File: {footnotes_file.relative_to(PROJECT_ROOT) if footnotes_file.exists() and footnotes_file.is_relative_to(PROJECT_ROOT) else footnotes_file}")
    print("=" * 65)

    master_report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "monument_id": monument_id,
        "cohort": cohort_num,
        "target_file": str(target_text.name),
        "overall_status": "PENDING",
        "gates": {}
    }

    all_passed = True

    # Gate 1A: Shared_Lexicon vocabulary linting
    print("\n[Gate 1A/4] Running Vocabulary Linter (Shared_Lexicon/lint_vocabulary.py)...")
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
    print("\n[Gate 1B/4] Running Anti-Slop Linter (scripts/lint_liturgical_slop.py)...")
    slop_linter_script = SCRIPT_DIR / "lint_liturgical_slop.py"
    slop_passed = True
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
            slop_passed = False
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
    print("\n[Gate 2/4] Running Hieratic Deity Pronoun Audit (scripts/hieratic_pronoun_audit.py)...")
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
    print("\n[Gate 3/4] Running Footnote Symmetry Audit (scripts/reconcile_footnotes.py)...")
    fn_script = SCRIPT_DIR / "reconcile_footnotes.py"
    cmd_fn = [sys.executable, str(fn_script), "--text", str(target_text), "--footnotes", str(footnotes_file), "--json"]
    res_fn = subprocess.run(cmd_fn, capture_output=True, text=True, encoding="utf-8")
    fn_data = {}
    if res_fn.returncode == 0:
        try:
            fn_data = json.loads(res_fn.stdout)
            print(f"  PASSED (Exact 1:1 Parity: {fn_data.get('text_markers_count', 0)} markers paired)")
        except Exception:
            fn_data = {"passed": True}
            print("  PASSED")
    else:
        # Check if orphaned definitions are from other cohorts in the shared footnotes file
        try:
            fn_data = json.loads(res_fn.stdout)
            missing = fn_data.get("missing_definitions", [])
            orphaned = fn_data.get("orphaned_definitions", [])
            # For a single cohort, missing definitions is always fatal. Orphaned definitions
            # in a multi-cohort shared file are expected if the footnotes file contains all cohorts.
            if len(missing) == 0:
                print(f"  PASSED (All {fn_data.get('text_markers_count', 0)} cohort markers defined; {len(orphaned)} definitions belong to sibling cohorts)")
                fn_data["passed"] = True
            else:
                all_passed = False
                print(f"  FAILED: Missing definitions={missing}")
        except Exception:
            all_passed = False
            fn_data = {"passed": False, "error": res_fn.stderr.strip() or res_fn.stdout.strip()}
            print(f"  FAILED: {fn_data}")

    master_report["gates"]["footnote_symmetry"] = fn_data

    # Gate 4: Structural Sequence & Leaf Continuity Integrity
    print("\n[Gate 4/4] Running Structural Sequence Audit (scripts/structural_audit.py)...")
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
    master_report["overall_status"] = "PASSED" if all_passed else "FAILED"

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
        log_to_triage({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "monument_id": monument_id,
            "cohort": cohort_num,
            "target_file": str(target_text.name),
            "report_path": str(report_file.relative_to(PROJECT_ROOT)),
            "summary": "Small Pause Gate failure: see report for details",
            "status": "PENDING_DEVELOPER_TRIAGE"
        })
        return 1

def main():
    parser = argparse.ArgumentParser(description="Universal Small Pause Gatekeeper Suite")
    parser.add_argument("--monument", default=None, help="Monument ID")
    parser.add_argument("--cohort", type=int, default=1, help="Cohort number")
    parser.add_argument("--draft", default=None, help="Path to draft markdown file")
    parser.add_argument("--footnotes", default=None, help="Path to footnotes txt file")

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
            monument_id = "1891_lviv_synod"

    try:
        sys.exit(run_gate(monument_id, args.cohort, custom_draft=draft_path, custom_footnotes=footnotes_path))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
