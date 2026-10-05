#!/usr/bin/env python3
"""
Universal Footnote Reconciler & Symmetry Auditor
================================================
Verifies exact 1:1 bidirectional set parity between footnote markers in text
and footnote definitions in the critical apparatus:
    { [^1] ... [^N] in text } == { [^1]: ... [^N]: in apparatus }

Usage:
    python scripts/reconcile_footnotes.py --text draft.md --footnotes footnotes.txt
    python scripts/reconcile_footnotes.py --monument 1891_lviv_synod --cohort 3
"""

import sys
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Set, Optional

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"

def parse_definitions(content: str) -> Set[int]:
    """Finds all footnote definitions, which start with ^[^N]: on a line."""
    defs = set()
    for line in content.splitlines():
        m = re.match(r"^\s*\[\^(\d+)\]:\s*", line)
        if m:
            defs.add(int(m.group(1)))
    return defs

def parse_text_markers(content: str) -> Set[int]:
    """Finds all footnote markers in body text, excluding definition lines."""
    markers = set()
    for line in content.splitlines():
        # Skip definition lines
        if re.match(r"^\s*\[\^(\d+)\]:\s*", line):
            continue
        # Extract any [^N] markers on the line
        for match in re.finditer(r"\[\^(\d+)\]", line):
            markers.add(int(match.group(1)))
    return markers

def audit_footnotes(text_path: Path, footnotes_path: Path, cohort_filter: Optional[Set[int]] = None) -> Dict[str, Any]:
    if not text_path.exists():
        raise FileNotFoundError(f"Text file not found: {text_path}")
    if not footnotes_path.exists():
        raise FileNotFoundError(f"Footnotes file not found: {footnotes_path}")

    with open(text_path, "r", encoding="utf-8") as f:
        text_content = f.read()

    with open(footnotes_path, "r", encoding="utf-8") as f:
        fn_content = f.read()

    text_markers = parse_text_markers(text_content)
    def_markers = parse_definitions(fn_content)

    if cohort_filter:
        def_markers = def_markers.intersection(cohort_filter)

    missing_defs = sorted(list(text_markers - def_markers))
    # For orphaned, if evaluating a single cohort, only check definitions that were supposed to be in this cohort
    orphaned_defs = sorted(list(def_markers - text_markers)) if cohort_filter else sorted(list(def_markers - text_markers))

    passed = (len(missing_defs) == 0 and len(orphaned_defs) == 0)

    return {
        "text_file": str(text_path.name),
        "footnotes_file": str(footnotes_path.name),
        "passed": passed,
        "text_markers_count": len(text_markers),
        "definition_markers_count": len(def_markers),
        "text_markers": [f"[^{x}]" for x in sorted(list(text_markers))],
        "definition_markers": [f"[^{x}]" for x in sorted(list(def_markers))],
        "missing_definitions": [f"[^{x}]" for x in missing_defs],
        "orphaned_definitions": [f"[^{x}]" for x in orphaned_defs]
    }

def main():
    parser = argparse.ArgumentParser(description="Universal Footnote Reconciler & Symmetry Auditor")
    parser.add_argument("--text", help="Path to text or markdown file")
    parser.add_argument("--footnotes", help="Path to footnotes file")
    parser.add_argument("--monument", help="Monument ID")
    parser.add_argument("--min", type=int, help="Minimum footnote number to consider (cohort scoping)")
    parser.add_argument("--max", type=int, help="Maximum footnote number to consider (cohort scoping)")
    parser.add_argument("--json", action="store_true", help="Output JSON results")

    args = parser.parse_args()

    text_path = None
    fn_path = None

    if args.text and args.footnotes:
        text_path = Path(args.text)
        fn_path = Path(args.footnotes)
    elif args.monument and args.cohort:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            registry = json.load(f)
        mon_info = registry.get("monuments", {}).get(args.monument, {})
        ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{args.monument}")

        draft_text = ws / "Draft" / f"{args.monument}_cohort{args.cohort}_raw_draft.md"
        final_text = ws / "Final MD" / f"{args.monument}_cohort{args.cohort}.md"
        draft_fn = ws / "Draft" / f"{args.monument}_cohort{args.cohort}_footnotes.txt"
        final_fn = ws / "Final" / "Final_footnotes.txt"

        if final_text.exists():
            text_path = final_text
            fn_path = final_fn
        elif draft_text.exists():
            text_path = draft_text
            fn_path = draft_fn if draft_fn.exists() else final_fn
        else:
            print(f"ERROR: Could not locate text file for {args.monument} cohort {args.cohort}", file=sys.stderr)
            sys.exit(1)

    if not text_path or not fn_path:
        print("ERROR: Specify (--text and --footnotes) or (--monument and --cohort)", file=sys.stderr)
        sys.exit(1)

    cohort_filter = None
    if args.min is not None or args.max is not None:
        min_v = args.min if args.min is not None else 1
        max_v = args.max if args.max is not None else 99999
        cohort_filter = set(range(min_v, max_v + 1))

    res = audit_footnotes(text_path, fn_path, cohort_filter=cohort_filter)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"Footnote Parity Audit: {res['text_file']} <-> {res['footnotes_file']}")
        print(f"Text Markers: {res['text_markers_count']} | Definitions: {res['definition_markers_count']}")
        print(f"Status: {'PASSED (Exact 1:1 Parity)' if res['passed'] else 'FAILED'}")
        if res["missing_definitions"]:
            print(f"  Missing Definitions: {res['missing_definitions']}")
        if res["orphaned_definitions"]:
            print(f"  Orphaned Definitions: {res['orphaned_definitions']}")

    sys.exit(0 if res["passed"] else 1)

if __name__ == "__main__":
    main()
