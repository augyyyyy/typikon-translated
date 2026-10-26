import sys
from pathlib import Path
import re
import zipfile

sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))
txt = z.read("index_split_018.xhtml").decode("utf-8", errors="ignore")

notes = {}
for n in range(733, 775):
    m = re.search(rf'id=["\']n5-{n}["\'][^>]*></a>\s*(.*?)(?:</div>|<div class="paragraph">)', txt, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        clean = re.sub(r'^\s*\[?\d+\]?\.?\s*', '', clean).strip()
        notes[n] = clean
    else:
        notes[n] = "MISSING"

with open("scratch/cohort25_raw_notes.txt", "w", encoding="utf-8") as f:
    for n in range(733, 775):
        fn_en = n + 584
        f.write(f"[{n}] (EN [^{fn_en}]) {notes[n]}\n\n")

print(f"Dumped {len(notes)} notes to scratch/cohort25_raw_notes.txt")
