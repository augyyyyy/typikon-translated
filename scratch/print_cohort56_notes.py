from pathlib import Path
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

for p in [964, 965, 966]:
    txt = Path(f'scratch/cohort56_extracted/notes_p{p}.txt').read_text(encoding='utf-8')
    print(f"==================== PAGE {p} ====================")
    print(txt)
