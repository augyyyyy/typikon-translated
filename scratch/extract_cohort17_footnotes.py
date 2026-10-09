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
        if 'id="n5-' in data or "id='n5-" in data:
            print(f"Found notes in {name}")
            all_text += "\n" + data

# Find all n5- footnote ids
all_ids = re.findall(r'id=["\']n5-(\d+)["\']', all_text)
if all_ids:
    int_ids = sorted([int(x) for x in set(all_ids)])
    print(f"Total n5 notes: {len(int_ids)}, min={min(int_ids)}, max={max(int_ids)}")
    # Find which ones are between 180 and 320
    cohort_ids = [x for x in int_ids if 189 <= x <= 300]
    print(f"Notes between 189 and 300: {cohort_ids}")

# Let's inspect footnote 189..290
out_lines = []
for i in range(189, 300):
    pattern = rf'id=["\']n5-{i}["\'][^>]*>(.*?)</div>'
    m = re.search(pattern, all_text, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        clean = re.sub(r'\s+', ' ', clean)
        out_lines.append(f"[{i}]: {clean}")

Path("scratch/russian_footnotes_cohort17.txt").write_text("\n".join(out_lines), encoding="utf-8")
print(f"Wrote {len(out_lines)} footnotes to scratch/russian_footnotes_cohort17.txt")
