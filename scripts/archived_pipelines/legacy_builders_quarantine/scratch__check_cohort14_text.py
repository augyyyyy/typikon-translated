import zipfile
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(epub_path)
fn_text = z.read("index_split_018.xhtml").decode("utf-8", errors="ignore")

for i in range(13, 47):
    pattern = rf'id="n5-{i}"[^>]*>(.*?)</div>'
    m = re.search(pattern, fn_text, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        print(f"[{i}]: {clean}")
    else:
        print(f"[{i}]: NOT FOUND")
