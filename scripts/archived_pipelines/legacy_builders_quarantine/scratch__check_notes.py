import os
import sys
import re
from pathlib import Path

raw_path = Path("scratch/cohort99_source_raw.txt")
raw_text = raw_path.read_text(encoding='utf-8')

# Check note numbers present
notes = re.findall(r'(\d+)\.\s', raw_text)
print(f"Total notes found: {len(notes)}")
print(f"First note: {notes[0]}, Last note: {notes[-1]}")

# Check missing note numbers between 268 and 457
num_list = [int(n) for n in notes]
expected = list(range(268, 458))
missing = [n for n in expected if n not in num_list]
print(f"Missing note numbers: {missing}")

# Check duplicates
dups = [n for n in num_list if num_list.count(n) > 1]
print(f"Duplicate note numbers: {set(dups)}")
