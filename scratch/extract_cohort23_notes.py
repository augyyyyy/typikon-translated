import zipfile
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path('E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub')
z = zipfile.ZipFile(str(epub_path))
txt = z.read('index_split_018.xhtml').decode('utf-8', errors='ignore')

notes = {}
missing = []

for n in range(599, 676):
    # Pattern to match note block: <div class="paragraph"><a name="n5-599"...
    # or just between <a name="n5-{n}" ... and </div>
    m = re.search(rf'<a[^>]+id=["\']n5-{n}["\'][^>]*></a>\s*(.*?)(?:</div>|<div class="paragraph">)', txt, re.DOTALL)
    if not m:
        m = re.search(rf'id=["\']n5-{n}["\'][^>]*></a>\s*(.*?)(?:</div>|<div class="paragraph">)', txt, re.DOTALL)
    if m:
        raw_html = m.group(1)
        clean = re.sub(r'<[^>]+>', '', raw_html).strip()
        # Clean up leading numbers or brackets if any (e.g. "599. ")
        clean = re.sub(r'^\s*\[?\d+\]?\.?\s*', '', clean).strip()
        notes[n] = clean
    else:
        missing.append(n)

print(f"Extracted {len(notes)} notes. Missing: {missing}")

out_path = Path('scratch/cohort23_epub_notes.txt')
with open(out_path, 'w', encoding='utf-8') as f:
    for n in range(599, 676):
        if n in notes:
            f.write(f"[{n}] {notes[n]}\n")
        else:
            f.write(f"[{n}] MISSING\n")

print(f"Wrote {out_path}")
