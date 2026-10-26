import sys
from pathlib import Path
import re
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))
txt = z.read("index_split_012.xhtml").decode("utf-8", errors="ignore")

for p in range(295, 306):
    m = re.search(rf'\{{с\.?\s*{p}\}}', txt)
    if m:
        start = max(0, m.start() - 100)
        end = min(len(txt), m.end() + 100)
        snippet = txt[start:end].replace("\n", " ")
        snippet = re.sub(r'<[^>]+>', '', snippet)
        print(f"Page {p} at {m.start()}: {snippet}\n")
    else:
        print(f"Page {p}: NOT FOUND\n")
