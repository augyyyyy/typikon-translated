import sys
from pathlib import Path
import re
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))
txt = z.read("index_split_012.xhtml").decode("utf-8", errors="ignore")

idx_start = txt.find("Стефана Савваита")
idx_end = txt.find("не выпевают (как и копты)")
if idx_end != -1:
    idx_end += len("не выпевают (как и копты) ни в сутки, ни в неделю, а только некоторые")
section = txt[idx_start:idx_end]

for m in re.finditer(r'<a[^>]+href=[\"\']index_split_\d+\.xhtml#(n\d+-\d+)[\"\'][^>]*>(.*?)</a>', section):
    print(f"Target: {m.group(1)} | Text: '{m.group(2)}'")

# Also let's print the footnote texts from split 019
fn_txt = z.read("index_split_019.xhtml").decode("utf-8", errors="ignore")
notes_found = re.findall(r'<a[^>]+href=[\"\']index_split_\d+\.xhtml#(n\d+-\d+)[\"\']', section)
print(f"\nTotal notes found in section: {len(notes_found)}")
for nid in notes_found:
    pat = rf'id=[\"\']{nid}[\"\'][^>]*></a>\s*(.*?)(?:</div>|<div class="paragraph">)'
    m = re.search(pat, fn_txt, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        clean = re.sub(r'^\s*\[?\d+\]?\.?\s*', '', clean).strip()
        print(f"\n[{nid}]: {clean}")
