# -*- coding: utf-8 -*-
"""
scripts/lint_epistemic_bibliography.py

Epistemic Bibliography Linter for Critical Apparatus & Footnotes.
Borrowed and adapted from Chant Indexer (engine/epistemic_linter.py).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_SHARED_BIB = PROJECT_ROOT.parent / "Shared_Lexicon" / "authoritative_bibliography.json"

DEFAULT_BIBLIOGRAPHY = {
    "DOLNYTSKY_1899": {
        "title": "Typik Cerkovnyj",
        "author": "Isidore Dolnytsky",
        "year": 1899,
        "city": "Lviv"
    },
    "MIKITA_1901": {
    "title": "Typikon cerkve rusko-katoliceskija",
        "author": "Alexander Mikita",
        "year": 1901,
        "city": "Uzhhorod"
    },
    "LVIV_SYNOD_1891": {
        "title": "Acta et Decreta Synodi Provincialis Ruthenorum Galiciae",
        "author": "Ruthenian Metropolitan Church",
        "year": 1891,
        "city": "Lviv"
    },
    "KACHMAR_2020": {
        "title": "Tradition of the Kyivan Typikon",
        "author": "Vasyl Kachmar",
        "year": 2020,
        "city": "Lviv"
    },
    "DMITRIEVSKY_1901": {
        "title": "Opisanie Liturgicheskikh Rukopisei",
        "author": "Aleksei Dmitrievsky",
        "year": 1901,
        "city": "Kyiv"
    }
}


class EpistemicBibliographyLinter:
    DOGMATIC_UNANCHORED_PATTERNS = [
        r"\b(has to be|must be|always consists of|can only be)\b",
        r"\b(obviously represents|clearly proves|undoubtedly)\b"
    ]

    CITATION_PATTERN = r"\[([A-Z0-9_]{4,})\]"

    def __init__(self, bib_path: Optional[Path] = None):
        target_bib_path = bib_path or (DEFAULT_SHARED_BIB if DEFAULT_SHARED_BIB.exists() else None)
        self.bib_path = target_bib_path
        if self.bib_path and self.bib_path.exists():
            with open(self.bib_path, "r", encoding="utf-8") as f:
                self.bibliography = json.load(f)
        else:
            self.bibliography = DEFAULT_BIBLIOGRAPHY

    def audit_footnotes(self, footnotes_text: str) -> List[Dict[str, Any]]:
        violations = []
        for line_no, line in enumerate(footnotes_text.splitlines(), 1):
            line_str = line.strip()
            if not line_str.startswith("[^"):
                continue

            # Check unanchored dogmatism
            for pat in self.DOGMATIC_UNANCHORED_PATTERNS:
                if re.search(pat, line_str, re.IGNORECASE):
                    citations = re.findall(self.CITATION_PATTERN, line_str)
                    valid_cites = [c for c in citations if c in self.bibliography]
                    if not valid_cites:
                        violations.append({
                            "line": line_no,
                            "type": "UNANCHORED_ASSERTION",
                            "text": line_str,
                            "message": f"Dogmatic assertion in footnote without registered citation key: '{line_str}'"
                        })

        return violations


def main():
    parser = argparse.ArgumentParser(description="Audit footnotes for epistemic scholarly provenance")
    parser.add_argument("--file", required=True, help="Footnotes markdown file")
    parser.add_argument("--bib", help="Optional path to custom bibliography JSON")
    args = parser.parse_args()

    bib_path = Path(args.bib) if args.bib else None
    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()

    linter = EpistemicBibliographyLinter(bib_path=bib_path)
    violations = linter.audit_footnotes(content)
    if violations:
        print(f"[FAIL] Found {len(violations)} epistemic bibliography violations:")
        for v in violations:
            print(f"  Line {v['line']}: {v['message']}")
        sys.exit(1)
    else:
        print("[PASS] All footnotes comply with epistemic bibliography requirements.")
        sys.exit(0)


if __name__ == "__main__":
    main()
