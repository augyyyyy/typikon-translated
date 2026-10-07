from pathlib import Path
import re

source_path = Path("Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Source Text/1888_violakis_typikon_cohort8_source.txt")
draft_path = Path("Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Draft/1888_violakis_typikon_cohort8_raw_draft.md")
fn_path = Path("Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Draft/1888_violakis_typikon_cohort8_footnotes.txt")

print(f"Source exists: {source_path.exists()}, size={source_path.stat().st_size}, lines={len(source_path.read_text(encoding='utf-8').splitlines())}")
print(f"Draft exists: {draft_path.exists()}, size={draft_path.stat().st_size}, lines={len(draft_path.read_text(encoding='utf-8').splitlines())}")
print(f"Footnotes exists: {fn_path.exists()}, size={fn_path.stat().st_size}, lines={len(fn_path.read_text(encoding='utf-8').splitlines())}")

draft_text = draft_path.read_text(encoding='utf-8')
source_text = source_path.read_text(encoding='utf-8')

draft_leaves = re.findall(r'=== LEAF p(\d+) ===', draft_text)
source_leaves = re.findall(r'=== LEAF p(\d+) ===', source_text)

print("Draft leaves:", draft_leaves)
print("Source leaves:", source_leaves)

draft_fns = sorted(list(set(re.findall(r'\[\^(\d+)\]', draft_text))), key=int)
fn_text = fn_path.read_text(encoding='utf-8')
fn_defs = sorted(list(set(re.findall(r'\[\^(\d+)\]:', fn_text))), key=int)

print("Draft footnote markers:", draft_fns)
print("Footnote file definitions:", fn_defs)
assert draft_fns == fn_defs, f"Mismatch: {draft_fns} != {fn_defs}"
print("Footnote bijectivity confirmed: 100% match!")

banned = ['verily', 'betwixt', 'twas', 'methinks', 'hearken', 'wherefore', 'peradventure', 'effulgent', 'resplendent', 'lo and behold', 'tapestry', 'beacon', 'for ever and ever']
found_banned = []
for b in banned:
    if re.search(r'\b' + re.escape(b) + r'\b', draft_text, re.IGNORECASE):
        found_banned.append(b)
    if re.search(r'\b' + re.escape(b) + r'\b', fn_text, re.IGNORECASE):
        found_banned.append(f"{b} (in fn)")

print("Banned words check:", found_banned if found_banned else "PASSED (0 violations)")
