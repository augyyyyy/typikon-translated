import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

n997 = Path('scratch/cohort76_extracted/notes_p997.txt').read_text(encoding='utf-8')
n998 = Path('scratch/cohort76_extracted/notes_p998.txt').read_text(encoding='utf-8')

full_notes = n997 + "\n" + n998

import re
notes = {}
current_num = None
current_text = []

for line in full_notes.splitlines():
    m = re.match(r'^(\d+)\.\s*(.*)', line)
    if m:
        if current_num is not None:
            notes[current_num] = "\n".join(current_text).strip()
        current_num = int(m.group(1))
        current_text = [m.group(2)]
    else:
        if current_num is not None:
            current_text.append(line)

if current_num is not None:
    notes[current_num] = "\n".join(current_text).strip()

print(f"Total parsed notes: {len(notes)}")
for n in range(564, 583):
    print(f"--- Note {n} ---")
    print(notes.get(n, "MISSING"))
