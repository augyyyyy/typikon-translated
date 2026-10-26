import re
from pathlib import Path

source_path = Path("Liturgical Monuments/Monument 1 - 1891 Lviv Synod/Source Text/1891_lviv_synod_cohort14_source.txt")
fn_draft_path = Path("Liturgical Monuments/Monument 1 - 1891 Lviv Synod/Draft/1891_lviv_synod_cohort14_footnotes.txt")
draft_path = Path("Liturgical Monuments/Monument 1 - 1891 Lviv Synod/Draft/1891_lviv_synod_cohort14_raw_draft.md")
md_path = Path("Liturgical Monuments/Monument 1 - 1891 Lviv Synod/Final MD/1891_synod_cohort14.md")
txt_path = Path("Liturgical Monuments/Monument 1 - 1891 Lviv Synod/Final/1891_synod_cohort14.txt")
fn_master_path = Path("Liturgical Monuments/Monument 1 - 1891 Lviv Synod/Final/Final_footnotes.txt")

source_text = source_path.read_text(encoding="utf-8")
fn_draft_text = fn_draft_path.read_text(encoding="utf-8")
draft_text = draft_path.read_text(encoding="utf-8")
md_text = md_path.read_text(encoding="utf-8")
txt_text = txt_path.read_text(encoding="utf-8")
fn_master_text = fn_master_path.read_text(encoding="utf-8")

# 1. Footnote Check: [^233] to [^275]
expected_fns = [f"[^{i}]" for i in range(233, 276)]
print(f"--- Footnote Verification ({len(expected_fns)} notes: [^233] to [^275]) ---")
missing_count = 0
for fn in expected_fns:
    in_draft = fn in draft_text
    in_md = fn in md_text
    in_txt = fn in txt_text
    in_draft_fn = (fn + ":") in fn_draft_text
    in_master_fn = (fn + ":") in fn_master_text
    if not (in_draft and in_md and in_txt and in_draft_fn and in_master_fn):
        print(f"MISSING {fn}: Draft={in_draft}, MD={in_md}, TXT={in_txt}, DraftFN={in_draft_fn}, MasterFN={in_master_fn}")
        missing_count += 1

if missing_count == 0:
    print(f"SUCCESS: All {len(expected_fns)} footnotes are bijectively present in Draft, MD, TXT, DraftFN, and Final_footnotes.txt!")
else:
    print(f"FAILURE: {missing_count} footnotes missing!")

# 2. Check for Banned Phrase: "for ever and ever"
print("\n--- Banned Phrase Check ('for ever and ever') ---")
banned_found = 0
for name, text in [("Source", source_text), ("Draft", draft_text), ("DraftFN", fn_draft_text), ("MD", md_text), ("TXT", txt_text), ("FinalFN", fn_master_text)]:
    matches = re.findall(r"for ever and ever", text, re.IGNORECASE)
    print(f"{name}: count = {len(matches)}")
    if matches:
        banned_found += len(matches)

if banned_found == 0:
    print("SUCCESS: 0 occurrences of 'for ever and ever' detected!")
else:
    print(f"FAILURE: {banned_found} occurrences detected!")

# 3. File Statistics
print("\n--- Cohort 14 File Statistics ---")
files = [
    ("Source Text", source_path, source_text),
    ("Draft Footnotes", fn_draft_path, fn_draft_text),
    ("Raw Draft MD", draft_path, draft_text),
    ("Final MD", md_path, md_text),
    ("Final TXT", txt_path, txt_text),
    ("Master Footnotes", fn_master_path, fn_master_text),
]

for label, p, content in files:
    lines = len(content.splitlines())
    chars = len(content)
    bytes_len = len(content.encode("utf-8"))
    print(f"- {label} ({p.name}): {lines} lines, {chars} chars, {bytes_len} bytes")
