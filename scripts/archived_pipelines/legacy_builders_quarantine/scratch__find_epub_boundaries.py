import zipfile
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))

for part in ["index_split_012.xhtml", "index_split_013.xhtml"]:
    data = z.read(part).decode("utf-8", errors="ignore")
    # remove html tags
    clean = re.sub(r'<[^>]+>', ' ', data)
    clean = re.sub(r'\s+', ' ', clean)
    idx1 = clean.find("респонсорий молитвы")
    idx2 = clean.find("принадлежавшей монастырю св. Севастиана")
    print(f"{part}: idx1={idx1}, idx2={idx2}")
    if idx1 != -1:
        print(f"  Snippet near idx1: {clean[idx1-50:idx1+150]}")
    if idx2 != -1:
        print(f"  Snippet near idx2: {clean[idx2-50:idx2+150]}")
