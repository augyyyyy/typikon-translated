#!/usr/bin/env python3
"""
Patch Cohort Headings (Monument 1 - 1891 Lviv Synod)
====================================================
Tier 1 in-place cleanup of raw cohort files:
  1. Merge stacked Cyrillic headings into English parenthetical incipits (*...*).
  2. Purge mid-statute continuation headers (Continued / Conclusion) at cohort seams.
  3. Standardize apparatus headings to '## Footnotes'.
"""

import sys
import re
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
COHORTS_DIR = PROJECT_ROOT / "Liturgical Monuments" / "Monument 1 - 1891 Lviv Synod" / "Cohorts"

def patch_cohort_file(cf: Path) -> None:
    original = cf.read_text(encoding="utf-8")
    text = original

    # 1. Standardize apparatus headings to ## Footnotes
    text = re.sub(
        r"^##\s+(?:\d+[\.\)]\s*)?Scholarly Critical Apparatus & Footnotes\s*$",
        "## Footnotes",
        text,
        flags=re.MULTILINE | re.IGNORECASE
    )

    # 2. Specific stacked Cyrillic merges in Cohort 12 and 14
    if cf.name == "1891_lviv_synod_cohort12.md":
        # Titulus X. On Monks \n ### О Монахахъ
        text = re.sub(
            r"## Titulus X\. On Monks\s*\n+### О Монахахъ",
            "## Titulus X. On Monks (*О Монахахъ*)",
            text
        )
        # Titulus XI. On Fasts \n ### О постахъ
        text = re.sub(
            r"## Titulus XI\. On Fasts\s*\n+### О постахъ",
            "## Titulus XI. On Fasts (*О постахъ*)",
            text
        )
        # Purge top-of-cohort continuation headers at leaf p221
        text = re.sub(
            r"### Titulus VII \(Concluded\): On the Ecclesiastical Hierarchy\s*\n+",
            "",
            text
        )
        text = re.sub(
            r"### Chapter VII \(Concluded\): On Seminaries\s*\n+",
            "",
            text
        )

    if cf.name == "1891_lviv_synod_cohort14.md":
        # # Official Synodal Corrigenda & Typographical Errata \n ## Похибки друкарскî
        text = re.sub(
            r"# Official Synodal Corrigenda & Typographical Errata\s*\n+## Похибки друкарскî",
            "## Official Synodal Corrigenda & Typographical Errata (*Похибки друкарскî*)",
            text
        )

    # 3. Purge continuation headers at cohort seams
    if cf.name == "1891_lviv_synod_cohort4.md":
        # Seam at leaf p61
        text = re.sub(
            r"## 1\. Part VII: Acts of the Congregations and Sessions \(Continued\)\s*\n+",
            "",
            text
        )
        text = re.sub(
            r"### Nominal Subscription Roll Continued\s*\n+",
            "",
            text
        )

    elif cf.name == "1891_lviv_synod_cohort5.md":
        # Seam at leaf p81
        text = re.sub(
            r"## 1\. Decrees of the Ruthenian Provincial Synod: Titulus I\. On the Catholic Faith \(Continued\)\s*\n+",
            "",
            text
        )
        text = re.sub(
            r"### Chapter IV: On Communion in Sacred Things with Heretics and Schismatics \(Conclusion\)\s*\n+",
            "",
            text
        )

    elif cf.name == "1891_lviv_synod_cohort6.md":
        # Seam at leaf p101
        text = re.sub(
            r"## 1\. Decrees of the Ruthenian Provincial Synod: Titulus II\. On the Mysteries and Their Administration \(Continued\)\s*\n+",
            "",
            text
        )

    elif cf.name == "1891_lviv_synod_cohort7.md":
        # Seam at leaf p121
        text = re.sub(
            r"## 1\. Titulus IV\. On the Public Worship of God \(Continued\)\s*\n+",
            "",
            text
        )
        text = re.sub(
            r"### Chapter III: On the Canonical Hours \(The Church Rule\) and Other Public Divine Services \(Conclusion\)\s*\n+",
            "",
            text
        )

    elif cf.name == "1891_lviv_synod_cohort8.md":
        # Seam at leaf p141
        text = re.sub(
            r"## 1\. Titulus IV\. On the Public Worship of God \(Continued\)\s*\n+",
            "",
            text
        )
        text = re.sub(
            r"### Chapter VI: On the Celebration of Feast Days \(Conclusion\)\s*\n+",
            "",
            text
        )

    elif cf.name == "1891_lviv_synod_cohort9.md":
        # Seam at leaf p161
        text = re.sub(
            r"## 1\. Titulus V: On the Holy Liturgy \(Continued\)\s*\n+",
            "",
            text
        )
        text = re.sub(
            r"### Model Text, Order, and Manner of Celebrating the Divine Liturgy\s*\n+",
            "",
            text
        )

    elif cf.name == "1891_lviv_synod_cohort10.md":
        # Seam at leaf p181
        text = re.sub(
            r"## 1\. Titulus V: On the Holy Liturgy \(Conclusion\)\s*\n+",
            "",
            text
        )

    elif cf.name == "1891_lviv_synod_cohort11.md":
        # Seam at leaf p201
        text = re.sub(
            r"### Titulus VII \(Continued\): On the Ecclesiastical Hierarchy\s*\n+",
            "",
            text
        )

    elif cf.name == "1891_lviv_synod_cohort13.md":
        # Seam at leaf p245 (Titulus XI continued from Cohort 12)
        text = re.sub(
            r"## Titulus XI\. On Fasts\s*\n+\*\(Continued from p\. 240 / Leaf p245\)\*\s*\n+",
            "",
            text
        )

    elif cf.name == "1891_lviv_synod_cohort14.md":
        # Seam at leaf p262 (Titulus XV conclusion from Cohort 13)
        text = re.sub(
            r"## Titulus XV\. On Church Property \*\(Conclusion\)\*\s*\n+\*\(Continued from p\. 257 / Leaf p262\)\*\s*\n+",
            "",
            text
        )
        text = re.sub(
            r"\*\*6\.\*\*\s*\*\(Concluded\)\*\s*",
            "**6.** ",
            text
        )

    if text != original:
        cf.write_text(text, encoding="utf-8")
        print(f"  [PATCHED] {cf.name} (length diff: {len(text) - len(original):+} chars)")
    else:
        print(f"  [UNCHANGED] {cf.name}")

def main():
    print("=" * 70)
    print("PATCHING MONUMENT 1 COHORT HEADINGS (TIER 1 SOURCE CLEANUP)")
    print(f"Target Directory: {COHORTS_DIR.relative_to(PROJECT_ROOT)}")
    print("=" * 70)

    cohort_files = sorted(COHORTS_DIR.glob("*.md"))
    for cf in cohort_files:
        patch_cohort_file(cf)

    print("\nTier 1 patch complete.")

if __name__ == "__main__":
    main()
