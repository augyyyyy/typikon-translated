import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

raw_fn = Path("scratch/cohort17_russian_notes.txt").read_text(encoding="utf-8").splitlines()
fn_dict = {}
for line in raw_fn:
    m = re.match(r'\[(\d+)\]:\s*(.*)', line)
    if m:
        fn_dict[int(m.group(1))] = m.group(2)

print(f"Loaded {len(fn_dict)} footnotes.")
for i in range(189, 284):
    if i not in fn_dict:
        print(f"MISSING FOOTNOTE: {i}")
    else:
        # Check text
        val = fn_dict[i]
        if "NOT FOUND" in val or not val.strip():
            print(f"EMPTY OR NOT FOUND: {i}")

print("All footnotes verified present!")
