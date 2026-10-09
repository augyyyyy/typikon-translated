import sys
from pathlib import Path
import re
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))
fn_txt = z.read("index_split_019.xhtml").decode("utf-8", errors="ignore")

for i in range(15, 28):
    target = f"n6-{i}"
    pat = rf'id=[\"\']{target}[\"\'][^>]*></a>\s*(.*?)(?:</div>|<div class="paragraph">)'
    m = re.search(pat, fn_txt, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        clean = re.sub(r'^\s*\[?\d+\]?\.?\s*', '', clean).strip()
        fn_idx = 1504 + (i - 15)
        print(f"[^{fn_idx}] (source n6-{i}): {clean}\n")
    else:
        print(f"n6-{i}: NOT FOUND")
