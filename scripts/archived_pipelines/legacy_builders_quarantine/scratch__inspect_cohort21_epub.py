import zipfile, re, sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(epub_path)
notes_html = z.read("index_split_018.xhtml").decode("utf-8", errors="ignore")

out_notes = []
for i in range(494, 535):
    pattern = rf'id=["\']n5-{i}["\'][^>]*>(.*?)</div>'
    m = re.search(pattern, notes_html, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        clean = re.sub(r'\s+', ' ', clean)
        out_notes.append(f"[{i}]: {clean}")
    else:
        out_notes.append(f"[{i}]: NOT FOUND")

Path("scratch/cohort21_epub_notes.txt").write_text("\n".join(out_notes), encoding="utf-8")
print(f"Extracted {len(out_notes)} notes to scratch/cohort21_epub_notes.txt")
for line in out_notes[:15]:
    print(line[:120])
