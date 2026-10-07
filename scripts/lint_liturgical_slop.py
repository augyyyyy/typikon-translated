#!/usr/bin/env python3
"""
Anti-Fanciful Slop Language & Style Linter
==========================================
Enforces MTS-1 stylistic rigor across English liturgical translation drafts:
1. Rejects pseudo-archaic AI fantasy vocabulary (verily, betwixt, twas, etc.).
2. Rejects AI conversational clichés and filler phrases (testament to, delve into, etc.).
3. Rejects gratuitous rubrical 'shall'-bombing in ceremonial actions (active present indicative required).

Usage:
    python scripts/lint_liturgical_slop.py --target "path/to/draft.md"
    python scripts/lint_liturgical_slop.py --target "path/to/draft.md" --json
"""

import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

PROHIBITED_CATEGORIES: Dict[str, List[str]] = {
    "pseudo_archaic_slop": [
        r"\bverily\b",
        r"\btwas\b",
        r"\bbetwixt\b",
        r"\bmethinks\b",
        r"\bhearken\b",
        r"\bwherefore\b",
        r"\bperadventure\b",
        r"\beffulgent\b",
        r"\bresplendent\b",
        r"\bbeholden\b",
        r"\blo and behold\b",
        r"\bwondrous\b(?!\s+(?:is\s+God|art\s+Thou))"
    ],
    "ai_cliches_and_filler": [
        r"\btestament to\b",
        r"\bbeacon of\b",
        r"\bdelve into\b",
        r"\btapestry of\b",
        r"\brich history\b",
        r"\bserves as a reminder\b",
        r"\binextricably linked\b",
        r"\bpivotal moment\b",
        r"\bpoignant\b",
        r"\bneedless to say\b",
        r"\bit is important to remember\b"
    ],
    "rubrical_shall_bombing": [
        r"\b(?:the priest|the deacon|the bishop|the choir|the reader)\s+shall\s+(?:bow|enter|take|cense|kiss|bless|proclaim|say|chant|vest)\b"
    ],
    "archaic_rubrical_verb_drift": [
        r"\b(?:the priest|the deacon|the bishop|the choir|the reader|the chanter|the celebrant)\s+([a-z]+eth)\b",
        r"\b(?:singeth|proclaimeth|censeth|entereth|maketh|readeth|beginneth|taketh|vesteth|boweth|kisseth|turneth|standeth)\b"
    ]
}

def lint_slop(filepath: Path) -> Dict[str, Any]:
    if not filepath.exists():
        raise FileNotFoundError(f"Target file not found: {filepath}")

    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()

    violations: List[Dict[str, Any]] = []

    for line_num, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith("<!--"):
            continue

        is_footnote = s.startswith("[^")

        # For archaic rubrical verbs, strip quoted chant/scripture text
        unquoted = re.sub(r'\"[^\"]*\"|“[^”]*”|\*\*"[^\*"]*"\*\*', '', s)

        for category, patterns in PROHIBITED_CATEGORIES.items():
            check_text = unquoted if category == "archaic_rubrical_verb_drift" else s
            for pat in patterns:
                # Bibliographic or historical citations in footnotes may contain 'wherefore'
                if is_footnote and (pat == r"\bwherefore\b" or category == "archaic_rubrical_verb_drift"):
                    continue
                m = re.search(pat, check_text, re.IGNORECASE)
                if m:
                    violations.append({
                        "line": line_num,
                        "category": category,
                        "pattern": pat,
                        "matched_text": m.group(0),
                        "line_snippet": s[:120]
                    })

    passed = len(violations) == 0

    return {
        "file": filepath.name,
        "passed": passed,
        "violation_count": len(violations),
        "violations": violations
    }

def main():
    parser = argparse.ArgumentParser(description="Anti-Fanciful Slop Language Linter")
    parser.add_argument("--target", required=True, help="Path to markdown or text file")
    parser.add_argument("--json", action="store_true", help="Output JSON results")
    args = parser.parse_args()

    target_path = Path(args.target)
    result = lint_slop(target_path)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Slop Linter Report: {result['file']}")
        print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}")
        print(f"Total Violations: {result['violation_count']}")
        if not result["passed"]:
            print("\nDetected Violations:")
            for v in result["violations"]:
                print(f"  Line {v['line']:4d} [{v['category']}]: '{v['matched_text']}' in: \"{v['line_snippet']}\"")

    sys.exit(0 if result["passed"] else 1)

if __name__ == "__main__":
    main()
