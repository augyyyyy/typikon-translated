import os
import sys
import re
from pathlib import Path

raw_path = Path("scratch/cohort99_source_raw.txt")
raw_text = raw_path.read_text(encoding='utf-8')

# Let's find note starts: lines starting with or containing note numbers 268 to 457
notes_found = []
for m in re.finditer(r'(?:^|\n)(\d{3})\.[\s\xa0]', raw_text):
    num = int(m.group(1))
    notes_found.append(num)

print(f"Total 3-digit notes found: {len(notes_found)}")
expected = list(range(268, 458))
print(f"Missing from 268..457: {[n for n in expected if n not in notes_found]}")
print(f"Extra notes: {[n for n in notes_found if n not in expected]}")
