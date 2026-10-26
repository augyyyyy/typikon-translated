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
idx_end = txt.find("не выпевают (как и копты) ни в сутки, ни в неделю, а только некоторые")
if idx_end != -1:
    idx_end += len("не выпевают (как и копты) ни в сутки, ни в неделю, а только некоторые")
else:
    # let's search for "не выпевают"
    m = re.search(r"не выпевают.*", txt[idx_start:])
    if m:
        idx_end = idx_start + m.end()

print(f"Start: {idx_start}, End: {idx_end}, Len: {idx_end - idx_start}")
section = txt[idx_start:idx_end]

# Find all footnote links in this section
fn_links = re.findall(r'href=[\"\']index_split_\d+\.xhtml#(n\d+-\d+)[\"\']>\[?(\d+)\]?</a>', section)
print(f"Total footnote links found: {len(fn_links)}")
for target, num in fn_links:
    print(f"  Note link {num} -> {target}")

# Also find footnotes in fn_txt
fn_txt = z.read("index_split_019.xhtml").decode("utf-8", errors="ignore")
for target, num in fn_links:
    pat = rf'id=[\"\']{target}[\"\'][^>]*></a>\s*(.*?)(?:</div>|<div class="paragraph">)'
    m = re.search(pat, fn_txt, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        clean = re.sub(r'^\s*\[?\d+\]?\.?\s*', '', clean).strip()
        print(f"\n[{num} / {target}]: {clean}")
    else:
        print(f"\n[{num} / {target}]: NOT FOUND IN SPLIT 019")
