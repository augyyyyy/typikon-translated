import zipfile
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(epub_path)

all_text = ""
for name in z.namelist():
    if name.endswith('.xhtml') or name.endswith('.html'):
        data = z.read(name).decode('utf-8', errors='ignore')
        if 'n5-95' in data or 'n5-188' in data or 'id="n5-' in data:
            print(f"Found footnotes in {name}")
            all_text += "\n" + data

out_lines = []
missing = []
for i in range(95, 189):
    pattern = rf'id=["\']n5-{i}["\'][^>]*>(.*?)</div>'
    m = re.search(pattern, all_text, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        clean = re.sub(r'\s+', ' ', clean)
        out_lines.append(f"[{i}]: {clean}")
    else:
        # try search for numeric marker
        m2 = re.search(rf'id=["\'][^"\']*{i}["\'][^>]*>(.*?)</div>', all_text, re.DOTALL)
        if m2:
            clean = re.sub(r'<[^>]+>', '', m2.group(1)).strip()
            clean = re.sub(r'\s+', ' ', clean)
            out_lines.append(f"[{i}]: {clean}")
        else:
            out_lines.append(f"[{i}]: NOT FOUND")
            missing.append(i)

out_file = Path("scratch/russian_footnotes_95_188.txt")
out_file.write_text("\n".join(out_lines), encoding="utf-8")
print(f"Extracted {len(out_lines)} footnotes. Missing: {len(missing)}")
if missing:
    print("Missing indices:", missing)
