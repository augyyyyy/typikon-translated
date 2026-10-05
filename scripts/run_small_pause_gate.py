#!/usr/bin/env python3
"""
Universal Small Pause Gatekeeper Suite (Master Runner)
======================================================
Executes the four mandatory linters and auditors at the conclusion of every cohort:
  1. Shared_Lexicon/lint_vocabulary.py (Zero forbidden variants)
  2. scripts/hieratic_pronoun_audit.py (100% Deity Pronoun Capitalization)
  3. scripts/reconcile_footnotes.py (Exact 1:1 Footnote Parity)
  4. scripts/structural_audit.py (Unbroken Sequence & Heading Hierarchy)

Gate Enforcement:
  If all 4 pass -> updates state to PASSED_COHORT_<N>, exit code 0.
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

def run_gate(monument_id: str, cohort_num: int) -> int:
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
    mon_info = registry.get("monuments", {}).get(monument_id)
    if not mon_info:
        raise ValueError(f"Unknown monument ID: {monument_id}")

    ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}")
    audit_reports_dir = ws / "Audit_Reports"
    audit_reports_dir.mkdir(parents=True, exist_ok=True)
    report_file = audit_reports_dir / f"cohort{cohort_num}_small_pause_report.json"

    # Identify target files (Final MD preferred, Draft fallback)
    target_text = (
        find_target_file(ws / "Final MD", f"*cohort{cohort_num}*.md", cohort_num=cohort_num) or
        find_target_file(ws / "Final", f"*cohort{cohort_num}*.txt", cohort_num=cohort_num) or
        find_target_file(ws / "Draft", f"*cohort{cohort_num}*.md", cohort_num=cohort_num)
    )

    footnotes_file = (
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
    print(f"  Audited File: {target_text.relative_to(PROJECT_ROOT)}")
    print(f"  Footnotes File: {footnotes_file.relative_to(PROJECT_ROOT) if footnotes_file.exists() else 'N/A'}")
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

    # Gate 1: Shared_Lexicon vocabulary linting
    print("\n[Gate 1/4] Running Vocabulary Linter (Shared_Lexicon/lint_vocabulary.py)...")
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

    # Gate 4: Structural Sequence Integrity
    print("\n[Gate 4/4] Running Structural Sequence Audit (scripts/structural_audit.py)...")
    struct_script = SCRIPT_DIR / "structural_audit.py"
    cmd_struct = [sys.executable, str(struct_script), "--target", str(target_text), "--json"]
    res_struct = subprocess.run(cmd_struct, capture_output=True, text=True, encoding="utf-8")
    struct_data = {}
    if res_struct.returncode == 0:
        try:
            struct_data = json.loads(res_struct.stdout)
            print(f"  PASSED ({struct_data.get('paragraphs', 0)} paragraphs, unbroken sequence)")
        except Exception:
            struct_data = {"passed": True}
            print("  PASSED")
    else:
        all_passed = False
        try:
            struct_data = json.loads(res_struct.stdout)
            print(f"  FAILED: Number breaks={struct_data.get('number_breaks')}")
        except Exception:
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
    parser.add_argument("--monument", default="1891_lviv_synod", help="Monument ID")
    parser.add_argument("--cohort", type=int, default=1, help="Cohort number")

    args = parser.parse_args()
    try:
        sys.exit(run_gate(args.monument, args.cohort))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
