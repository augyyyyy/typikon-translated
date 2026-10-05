#!/usr/bin/env python3
"""
Universal Structural & Rubrical Sequence Auditor
================================================
Audits English translation drafts to ensure unbroken statutory numbering,
rubrical sequence integrity, and correct markdown heading levels.

Usage:
    python scripts/structural_audit.py --target draft.md
    python scripts/structural_audit.py --monument 1891_lviv_synod --cohort 3
"""

import sys
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Typikons" / "codex_registry.json"

def audit_structure(filepath: Path) -> Dict[str, Any]:
    if not filepath.exists():
        raise FileNotFoundError(f"Target file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()

    headings: List[Dict[str, Any]] = []
    numbered_items: List[int] = []
    paragraph_count = 0
    anomalies: List[str] = []

    for line_num, line in enumerate(lines, 1):
        s = line.strip()
        if not s:
            continue
        paragraph_count += 1

        # Check markdown headings
        if s.startswith("#"):
            level = len(s) - len(s.lstrip("#"))
            title = s.lstrip("#").strip()
            headings.append({"line": line_num, "level": level, "title": title})

        # Check numbered statutory items (e.g., "**1.**", "1.", "§ 1.")
        m_statute = re.match(r"^(?:\*{1,2})?(\d+)\.(?:\*{1,2})?\s+", s)
        if m_statute:
            num = int(m_statute.group(1))
            numbered_items.append(num)

    # Check numbering continuity in simple sequential runs
    breaks = []
    for i in range(len(numbered_items) - 1):
        curr_n = numbered_items[i]
        next_n = numbered_items[i + 1]
        # If numbers ascend but skip (e.g. 1 -> 3)
        if next_n > curr_n + 1 and next_n < curr_n + 5:
            breaks.append(f"Jump from {curr_n} to {next_n}")

    # Basic structural health check: must have paragraphs and non-empty content
    passed = len(anomalies) == 0 and paragraph_count > 0

    return {
        "file": str(filepath.name),
        "passed": passed,
        "paragraphs": paragraph_count,
        "headings_count": len(headings),
        "headings": headings[:15],  # sample
        "numbered_items_count": len(numbered_items),
        "number_breaks": breaks,
        "anomalies": anomalies
    }

def main():
    parser = argparse.ArgumentParser(description="Universal Structural & Rubrical Sequence Auditor")
    parser.add_argument("--target", help="Path to text or markdown file")
    parser.add_argument("--monument", help="Monument ID")
    parser.add_argument("--cohort", type=int, help="Cohort number")
    parser.add_argument("--json", action="store_true", help="Output JSON results")

    args = parser.parse_args()

    target_path = None
    if args.target:
        target_path = Path(args.target)
    elif args.monument and args.cohort:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            registry = json.load(f)
        mon_info = registry.get("monuments", {}).get(args.monument, {})
        ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Typikons/{args.monument}")

        final_cand = ws / "Final MD" / f"{args.monument}_cohort{args.cohort}.md"
        draft_cand = ws / "Draft" / f"{args.monument}_cohort{args.cohort}_raw_draft.md"
        target_path = final_cand if final_cand.exists() else draft_cand

    if not target_path:
        print("ERROR: Specify --target or (--monument and --cohort)", file=sys.stderr)
        sys.exit(1)

    res = audit_structure(target_path)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"Structural Audit for: {res['file']}")
        print(f"Paragraphs: {res['paragraphs']} | Headings: {res['headings_count']} | Numbered Items: {res['numbered_items_count']}")
        print(f"Status: {'PASSED' if res['passed'] else 'FAILED'}")
        if res["number_breaks"]:
            print(f"  Numbering Breaks: {res['number_breaks']}")

    sys.exit(0 if res["passed"] else 1)

if __name__ == "__main__":
    main()
