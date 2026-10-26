import zipfile
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(epub_path)
fn_text = z.read("index_split_018.xhtml").decode("utf-8", errors="ignore")

out_lines = []
for i in range(47, 96):
    pattern = rf'id=["\']n5-{i}["\'][^>]*>(.*?)</div>'
    m = re.search(pattern, fn_text, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        # normalize whitespace
        clean = re.sub(r'\s+', ' ', clean)
        out_lines.append(f"[{i}]: {clean}")
    else:
        out_lines.append(f"[{i}]: NOT FOUND")

Path("scratch/russian_footnotes_47_95.txt").write_text("\n".join(out_lines), encoding="utf-8")
print(f"Wrote {len(out_lines)} footnotes to scratch/russian_footnotes_47_95.txt")
for line in out_lines[:10]:
    print(line[:80])
