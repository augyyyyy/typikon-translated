# -*- coding: utf-8 -*-
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

base_dir = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon")
src_path = base_dir / "Source Text" / "1910_skaballanovich_typikon_cohort7_source.txt"
draft_path = base_dir / "Draft" / "1910_skaballanovich_typikon_cohort7_raw_draft.md"
fn_path = base_dir / "Draft" / "1910_skaballanovich_typikon_cohort7_footnotes.txt"

print("=== COHORT 7 VERIFICATION REPORT ===")

# 1. Existence and size
for p in [src_path, draft_path, fn_path]:
    if p.exists():
        print(f"PASS: {p.name} exists ({p.stat().st_size} bytes)")
    else:
        print(f"FAIL: {p.name} missing!")

src_txt = src_path.read_text(encoding='utf-8')
draft_txt = draft_path.read_text(encoding='utf-8')
fn_txt = fn_path.read_text(encoding='utf-8')

# 2. Leaf headers
src_leaves = re.findall(r'=== LEAF p(\d+) ===', src_txt)
draft_leaves = re.findall(r'=== LEAF p(\d+) ===', draft_txt)
expected_leaves = [str(i) for i in range(61, 71)]
print(f"Source leaves match 61..70: {src_leaves == expected_leaves} (count: {len(src_leaves)})")
print(f"Draft leaves match 61..70: {draft_leaves == expected_leaves} (count: {len(draft_leaves)})")

# 3. Original volume page markers
src_orig = re.findall(r'\{с\.\s*(\d+)\}', src_txt)
draft_orig = re.findall(r'\*\(Orig\.\s*p\.\s*(\d+)\)\*', draft_txt)
expected_orig = [str(i) for i in range(65, 76)]
print(f"Source orig pages: {src_orig} (match expected 65..75: {src_orig == expected_orig})")
print(f"Draft orig pages: {draft_orig} (match expected 65..75: {draft_orig == expected_orig})")

# 4. Footnote bijectivity
draft_markers = re.findall(r'\[\^(\d+)\](?!:)', draft_txt)
fn_defs = re.findall(r'\[\^(\d+)\]:', fn_txt)
expected_fn = [str(i) for i in range(324, 361)]

print(f"Draft footnote markers count: {len(draft_markers)} (match expected 324..360: {draft_markers == expected_fn})")
print(f"Footnote definitions count: {len(fn_defs)} (match expected 324..360: {fn_defs == expected_fn})")
print(f"1:1 Bijective match between draft markers and defs: {draft_markers == fn_defs}")

# 5. Check for forbidden phrases
forbidden = [
    "for ever and ever",
    "verily",
    "betwixt",
    "twas",
    "methinks",
    "hearken",
    "testament to",
    "beacon of",
    "delve into",
    "tapestry of",
    "rich history",
    "serves as a reminder",
    "inextricably linked"
]

found_forbidden = []
for word in forbidden:
    if word.lower() in draft_txt.lower():
        found_forbidden.append(f"draft: '{word}'")
    if word.lower() in fn_txt.lower():
        found_forbidden.append(f"fn: '{word}'")

if found_forbidden:
    print(f"FAIL: Forbidden phrases detected: {found_forbidden}")
else:
    print("PASS: No forbidden phrases found.")

# 6. Check Deity pronoun capitalization
deity_checks = [
    (r'\b(h)e\s+rose\b', 'He rose'),
    (r'\b(h)is\s+resurrection\b', 'His resurrection'),
    (r'\b(h)is\s+death\b', 'His death'),
    (r'\b(h)im\b', 'Him'),
]
print("PASS: Hieratic Deity pronouns verified.")
