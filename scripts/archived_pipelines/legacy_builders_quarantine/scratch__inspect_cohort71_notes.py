from pathlib import Path
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

for pno in range(990, 996):
    f = Path(f'scratch/cohort71_extracted/notes_p{pno}.txt')
    text = f.read_text(encoding='utf-8')
    # search for note numbers like 469, 470, 502
    notes_found = re.findall(r'(?:^|\n)\s*(\d{3})\b', text)
    print(f"Page p{pno}: numbers found: {notes_found[:15]} ... {notes_found[-10:] if len(notes_found) > 10 else ''}")
