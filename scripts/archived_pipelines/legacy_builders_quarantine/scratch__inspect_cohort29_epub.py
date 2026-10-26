import sys
from pathlib import Path
import re
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))
txt = z.read("index_split_012.xhtml").decode("utf-8", errors="ignore")
idx = txt.find("Стефана Савваита")
section = txt[idx:]
links = re.findall(r'href=[\"\']index_split_(\d+)\.xhtml#(n\d+-\d+)[\"\']', section)
print("Footnote links count:", len(links))
print("First 10 links:", links[:10])
print("Last 10 links:", links[-10:])

# Let's inspect where these footnotes point
fn_split = f"index_split_{links[0][0]}.xhtml"
fn_txt = z.read(fn_split).decode("utf-8", errors="ignore")

for split_id, note_id in links:
    pattern = rf'id=[\"\']{note_id}[\"\'][^>]*></a>\s*(.*?)(?:</div>|<div class="paragraph">)'
    m = re.search(pattern, fn_txt, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        clean = re.sub(r'^\s*\[?\d+\]?\.?\s*', '', clean).strip()
        print(f"[{note_id}] {clean[:100]}...")
    else:
        print(f"[{note_id}] NOT FOUND")
