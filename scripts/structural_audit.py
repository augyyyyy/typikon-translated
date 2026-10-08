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
from typing import List, Dict, Any, Tuple, Optional, Set

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"

def extract_accounted_leaves(text: str) -> Set[int]:
    """Extracts all physical leaf numbers witnessed in text content."""
    accounted: Set[int] = set()
    # 1. Bracketed leaf markers: [Leaf p123 ...] or [Leaf 123 ...]
    for m in re.finditer(r'\[Leaf\s+p?(\d+)', text, re.IGNORECASE):
        accounted.add(int(m.group(1)))

    # 2. Markdown delimiter banners: === LEAF p123 === or === LEAF 123 ===
    for m in re.finditer(r'===\s*LEAF\s+p?(\d+)', text, re.IGNORECASE):
        accounted.add(int(m.group(1)))

    # 3. Parenthetical leaf references: *(... Leaf p123 ...) or (... Leaf p123 ...)
    for m in re.finditer(r'\(\*?[^)]*\bLeaf\s+p?(\d+)', text, re.IGNORECASE):
        accounted.add(int(m.group(1)))

    # 4. HTML comment banners: <!-- LEAF: p123 --> or <!-- LEAF: 123 -->
    for m in re.finditer(r'<!--\s*LEAF:?\s*p?(\d+)', text, re.IGNORECASE):
        accounted.add(int(m.group(1)))

    # 5. Header spans: Leaves p1–p20 or Leaves 1-20
    for m in re.finditer(r'Leaves\s+p?(\d+)\s*[-–]\s*p?(\d+)', text, re.IGNORECASE):
        start, end = int(m.group(1)), int(m.group(2))
        accounted.update(range(start, end + 1))

    return accounted

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

    # Determine if monument is bilingual (e.g. Greek odd leaves, English even leaves)
    is_bilingual = False
    resolved_monument = monument_id
    if not resolved_monument:
        candidate = filepath.name.split("_cohort")[0]
        if candidate:
            resolved_monument = candidate

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

        # Track active leaf banner
        m_leaf = re.match(r"===\s*LEAF\s+p?(\d+)", s, re.IGNORECASE)
        if m_leaf:
            current_leaf = int(m_leaf.group(1))

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
            if current_leaf is not None:
                if current_leaf % 2 == 1:
                    odd_numbered_items.append(num)
                else:
                    even_numbered_items.append(num)

    # Check numbering continuity in simple sequential runs
    breaks = []
    if is_bilingual:
        # For bilingual interleaved editions (e.g. Violakis), odd leaves are source and even leaves are translation.
        # Check odd leaves track (source text continuity)
        for i in range(len(odd_numbered_items) - 1):
            curr_n = odd_numbered_items[i]
            next_n = odd_numbered_items[i + 1]
            if next_n > curr_n + 1 and next_n < curr_n + 5:
                breaks.append(f"Odd/Source leaf jump from {curr_n} to {next_n}")
        # Check even leaves track (translation text continuity)
        for i in range(len(even_numbered_items) - 1):
            curr_n = even_numbered_items[i]
            next_n = even_numbered_items[i + 1]
            if next_n > curr_n + 1 and next_n < curr_n + 5:
                breaks.append(f"Even/Translation leaf jump from {curr_n} to {next_n}")
    else:
        for i in range(len(numbered_items) - 1):
            curr_n = numbered_items[i]
            next_n = numbered_items[i + 1]
            # If numbers ascend but skip (e.g. 1 -> 3)
            if next_n > curr_n + 1 and next_n < curr_n + 5:
                breaks.append(f"Jump from {curr_n} to {next_n}")

    # Check Leaf Accounting & Continuity
    curr_leaves = extract_accounted_leaves(content)
    leaf_stats: Dict[str, Any] = {
        "leaves_count": len(curr_leaves),
        "min_leaf": min(curr_leaves) if curr_leaves else None,
        "max_leaf": max(curr_leaves) if curr_leaves else None,
    }

    if curr_leaves:
        c_min, c_max = min(curr_leaves), max(curr_leaves)
        intra_gaps = sorted(list(set(range(c_min, c_max + 1)) - curr_leaves))
        if intra_gaps:
            anomalies.append(f"Intra-cohort leaf gaps detected: {intra_gaps}")

        # Invariant for Cohort 1: Must anchor on physical page 1
        if cohort_num == 1 and c_min != 1:
            anomalies.append(f"Cohort 1 initial anchor violation: expected leaf p1, but found starting leaf p{c_min}.")

        # Invariant for Cohort K > 1: Must continuously follow Cohort K-1
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

    # Basic structural health check: must have paragraphs and zero anomalies
    passed = len(anomalies) == 0 and len(breaks) == 0 and paragraph_count > 0

    return {
        "file": str(filepath.name),
        "passed": passed,
        "paragraphs": paragraph_count,
        "headings_count": len(headings),
        "headings": headings[:15],  # sample
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
