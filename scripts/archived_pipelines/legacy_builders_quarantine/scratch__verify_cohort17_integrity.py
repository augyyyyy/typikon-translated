import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

draft_path = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort17_raw_draft.md")
fn_path = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort17_footnotes.txt")

draft_text = draft_path.read_text(encoding="utf-8")
fn_text = fn_path.read_text(encoding="utf-8")

# 1. Footnotes in draft
draft_fn = [int(x) for x in re.findall(r'\[\^(\d+)\]', draft_text)]
print(f"Draft footnotes: count={len(draft_fn)}, min={min(draft_fn)}, max={max(draft_fn)}")

# 2. Footnotes in file
file_fn = [int(x) for x in re.findall(r'^\[\^(\d+)\]:', fn_text, re.MULTILINE)]
print(f"Footnotes file: count={len(file_fn)}, min={min(file_fn)}, max={max(file_fn)}")

# Check bijection
assert draft_fn == file_fn, f"Mismatch between draft and file! Diff draft-file: {set(draft_fn) - set(file_fn)}, Diff file-draft: {set(file_fn) - set(draft_fn)}"
assert draft_fn == list(range(773, 868)), f"Expected 773..867, got min={min(draft_fn)}, max={max(draft_fn)}"
print("Footnote bijection is 100% PERFECT: 95 footnotes from [^773] to [^867]!")

# 3. Leaf banners
leaves = re.findall(r'=== LEAF p(\d+) ===', draft_text)
print(f"Leaf banners: {leaves}")
assert [int(x) for x in leaves] == list(range(161, 171)), f"Leaf banners mismatch: {leaves}"
print("Leaf banners are 100% contiguous: p161 through p170!")

# 4. Slop linter check
banned = ["wherefore", "verily", "betwixt", "methinks", "twas", "for ever and ever"]
found_slop = []
for b in banned:
    m = re.findall(rf'\b{b}\b', draft_text, re.IGNORECASE)
    if m:
        found_slop.append((b, len(m)))
    m2 = re.findall(rf'\b{b}\b', fn_text, re.IGNORECASE)
    if m2:
        found_slop.append((f"fn:{b}", len(m2)))

if found_slop:
    print(f"FOUND SLOP VIOLATIONS: {found_slop}")
else:
    print("Zero liturgical slop violations found!")
