import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

notes_file = Path("scratch/cohort20_epub_notes.txt")
lines = notes_file.read_text(encoding='utf-8').splitlines()

cohort_notes = {}
for line in lines:
    if line.startswith('[') and ']: ' in line:
        k = int(line[1:line.find(']: ')])
        v = line[line.find(']: ') + 3:]
        if 440 <= k <= 494:
            cohort_notes[k] = v

print(f"Total cohort notes found: {len(cohort_notes)}")
for k in range(440, 495):
    if k in cohort_notes:
        print(f"[{k}] (Project [^{1024 + k - 440}]): {cohort_notes[k][:80]}")
    else:
        print(f"MISSING: [{k}]")
