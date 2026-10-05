import re
from pathlib import Path

md_path = Path("Typikons/1891 Lviv Synod/Final MD/1891_synod_cohort13.md")
txt_path = Path("Typikons/1891 Lviv Synod/Final/1891_synod_cohort13.txt")
fn_path = Path("Typikons/1891 Lviv Synod/Final/Final_footnotes.txt")

md_text = md_path.read_text(encoding="utf-8")
txt_text = txt_path.read_text(encoding="utf-8")
fn_text = fn_path.read_text(encoding="utf-8")

# 1. Check footnotes [^210] to [^232]
expected_fns = [f"[^{i}]" for i in range(210, 233)]

print("--- Footnote Check ---")
all_found = True
for fn in expected_fns:
    in_md = fn in md_text
    in_txt = fn in txt_text
    in_fn = (fn + ":") in fn_text
    if not (in_md and in_txt and in_fn):
        print(f"MISSING {fn}: MD={in_md}, TXT={in_txt}, FN_DEF={in_fn}")
        all_found = False
if all_found:
    print("All 23 footnotes accounted for in MD, TXT, and Final_footnotes.txt!")

# 2. Check banned phrase
print("\n--- Banned Phrase Check ---")
for name, text in [("MD", md_text), ("TXT", txt_text), ("FN", fn_text)]:
    matches = re.findall(r"for ever and ever", text, re.IGNORECASE)
    print(f"{name}: matches={len(matches)}")

# 3. Check anti-patterns & stats
print("\n--- File Stats ---")
print(f"MD: {len(md_text.splitlines())} lines, {len(md_text.encode('utf-8'))} bytes")
print(f"TXT: {len(txt_text.splitlines())} lines, {len(txt_text.encode('utf-8'))} bytes")
print(f"Final_footnotes: {len(fn_text.splitlines())} lines, {len(fn_text.encode('utf-8'))} bytes")
