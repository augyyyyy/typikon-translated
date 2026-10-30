#!/usr/bin/env python3
"""
Anti-Fanciful Slop Language & Style Linter
==========================================
Enforces MTS-1 stylistic rigor across English liturgical translation drafts:
1. Rejects pseudo-archaic AI fantasy vocabulary (verily, betwixt, twas, peradventure, forsooth, haply, etc.).
2. Rejects AI conversational clichés and filler phrases (testament to, delve into, etc.).
3. Rejects gratuitous rubrical 'shall'-bombing in ceremonial actions (active present indicative required).
4. Rejects 3rd-person singular '-eth' verb drift across body and footnotes (unified 120+ verb detector).

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

NON_VERB_ETH_TOKENS = {
    "beth", "seth", "nazareth", "elizabeth", "gennesaret", "shibboleth",
    "kenneth", "teeth", "beneath", "underneath", "twentieth", "thirtieth",
    "fortieth", "fiftieth", "sixtieth", "seventieth", "eightieth",
    "ninetieth", "hundredth", "thousandth", "aseneth", "japheth",
    "mephibosheth", "ishbosheth", "gath", "sabbath", "hath", "doth",
}

BANNED_ETH_VERBS = (
    "abideth|agreeth|assuageth|battleth|becometh|begetteth|beginneth|beguileth|behooveth|"
    "believeth|blotteth|boweth|causeth|ceaseth|celebrateth|censeth|cleanseth|cleaveth|"
    "cometh|commiteth|committeth|compelleth|createth|crieth|cutteth|danceth|decreeth|"
    "defileth|denieth|describeth|desireth|dieth|dispelleth|doeth|donateth|draggeth|"
    "drieth|drinketh|driveth|droppeth|dryeth|dwelleth|eateth|edifieth|emptieth|endureth|"
    "entereth|enticeth|envieth|excelleth|expelleth|fadeth|fleeth|flieth|forbiddeth|"
    "forgetteth|forgiveth|freeth|freezeth|getteth|giveth|glorifieth|goeth|hateth|"
    "hearkeneth|hopeth|illumineth|inclineth|intercedeth|inundateth|issueth|judgeth|"
    "justifieth|kisseth|knitteth|letteth|lieth|liveth|looseth|loveth|magnifieth|maketh|"
    "marvelleth|moveth|multiplieth|partaketh|permitteth|pitieth|praiseth|prepareth|"
    "preserveth|proclaimeth|procureth|prophesieth|provoketh|purifieth|putteth|rageth|"
    "raiseth|readeth|rebuketh|receiveth|rejoiceth|removeth|repelleth|rideth|riseth|"
    "ruleth|runneth|saith|sanctifieth|satisfieth|saveth|sayeth|schemeth|seeth|setteth|"
    "shaketh|shareth|shippeth|shineth|shunneth|shutteth|signifieth|singeth|sinneth|"
    "sitteth|slippeth|sprinkleth|standeth|steppeth|stirreth|stoppeth|striketh|strippeth|"
    "submitteth|taketh|tasteth|testifieth|trampleth|trembleth|trieth|troubleth|turneth|"
    "undergoeth|vesteth|waketh|warreth|wasteth|winneth|worshippeth|writeth"
)

PROHIBITED_CATEGORIES: Dict[str, List[str]] = {
    "pseudo_archaic_slop": [
        r"\bverily\b",
        r"\btwas\b",
        r"\bbetwixt\b",
        r"\bmethinks\b",
        r"\bhearken\b",
        r"\bwherefore\b",
        r"\bperadventure\b",
        r"\bforsooth\b",
        r"\bhaply\b",
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
        rf"\b(?:{BANNED_ETH_VERBS})\b"
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

        # Strip quoted strings inside footnotes or scripture quotations when checking archaic verb drift or meta-commentary
        unquoted = re.sub(r'\"[^\"]*\"|“[^”]*”|\*\*"[^\*"]*"\*\*|\*[^*\r\n]+\*', '', s)

        for category, patterns in PROHIBITED_CATEGORIES.items():
            check_text = unquoted if (category == "archaic_rubrical_verb_drift" or is_footnote) else s
            for pat in patterns:
                if is_footnote and pat == r"\bwherefore\b":
                    continue
                m = re.search(pat, check_text, re.IGNORECASE)
                if m:
                    matched_tok = m.group(0)
                    if category == "archaic_rubrical_verb_drift" and matched_tok.lower() in NON_VERB_ETH_TOKENS:
                        continue
                    violations.append({
                        "line": line_num,
                        "category": category,
                        "pattern": pat,
                        "matched_text": matched_tok,
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
