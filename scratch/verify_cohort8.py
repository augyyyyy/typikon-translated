# -*- coding: utf-8 -*-
"""
Verification Script for Monument 6 - Cohort 8
"""

import sys
import re
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MONUMENT_DIR = PROJECT_ROOT / "Liturgical Monuments" / "Monument 6 - 1910 Skaballanovich Typikon"
SRC_FILE = MONUMENT_DIR / "Source Text" / "1910_skaballanovich_typikon_cohort8_source.txt"
DRAFT_FILE = MONUMENT_DIR / "Draft" / "1910_skaballanovich_typikon_cohort8_raw_draft.md"
NOTES_FILE = MONUMENT_DIR / "Draft" / "1910_skaballanovich_typikon_cohort8_footnotes.txt"

def verify():
    errors = []
    
    # 1. Check existence
    for f in [SRC_FILE, DRAFT_FILE, NOTES_FILE]:
        if not f.exists():
            errors.append(f"Missing file: {f}")
        elif f.stat().st_size == 0:
            errors.append(f"Empty file: {f}")
    if errors:
        print("FAIL: Missing or empty files:", errors)
        return False

    src_text = SRC_FILE.read_text(encoding="utf-8")
    draft_text = DRAFT_FILE.read_text(encoding="utf-8")
    notes_text = NOTES_FILE.read_text(encoding="utf-8")

    # 2. Check Leaf Banners
    expected_leaves = [f"=== LEAF p{i} ===" for i in range(71, 81)]
    for leaf in expected_leaves:
        if leaf not in src_text:
            errors.append(f"Source text missing leaf: {leaf}")
        if leaf not in draft_text:
            errors.append(f"Draft text missing leaf: {leaf}")

    # 3. Check Original Page Numbers
    for p in range(76, 86):
        src_marker = f"{{с. {p}}}"
        draft_marker = f"*(Orig. p. {p})*"
        if src_marker not in src_text:
            errors.append(f"Source text missing page marker: {src_marker}")
        if draft_marker not in draft_text:
            errors.append(f"Draft text missing page marker: {draft_marker}")

    # 4. Check Footnote Bijection
    draft_markers = re.findall(r'\[\^(\d+)\]', draft_text)
    notes_defs = re.findall(r'\[\^(\d+)\]:', notes_text)

    draft_set = set(draft_markers)
    notes_set = set(notes_defs)

    print(f"Draft footnote count: {len(draft_markers)} (unique {len(draft_set)})")
    print(f"Notes footnote count: {len(notes_defs)} (unique {len(notes_set)})")

    if draft_markers != sorted(draft_markers, key=int):
        errors.append("Draft footnote markers are not monotonically increasing")
    
    if int(draft_markers[0]) != 361:
        errors.append(f"Starting footnote is {draft_markers[0]}, expected 361")
    if int(draft_markers[-1]) != 414:
        errors.append(f"Ending footnote is {draft_markers[-1]}, expected 414")

    if draft_set != notes_set:
        diff_dn = draft_set - notes_set
        diff_nd = notes_set - draft_set
        if diff_dn:
            errors.append(f"Footnotes in draft but missing in notes file: {diff_dn}")
        if diff_nd:
            errors.append(f"Footnotes in notes file but missing in draft: {diff_nd}")

    expected_indices = [str(i) for i in range(361, 415)]
    if sorted(draft_set, key=int) != expected_indices:
        errors.append("Footnote indices are not contiguous 361..414")

    # 5. Anti-slop check
    banned_words = [
        r'\bwherefore\b',
        r'for ever and ever',
        r'\bverily\b',
        r'\bbetwixt\b',
        r'\bmethinks\b',
        r'\btwas\b',
        r'\btapestry\b',
        r'beacon of',
        r'testament to'
    ]
    for b in banned_words:
        m = re.findall(b, draft_text, re.IGNORECASE)
        if m:
            errors.append(f"Draft contains banned slop pattern '{b}': {m}")

    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("ALL VERIFICATION CHECKS PASSED PERFECTLY!")
        return True

if __name__ == "__main__":
    success = verify()
    if not success:
        sys.exit(1)
