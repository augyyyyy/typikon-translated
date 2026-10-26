import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

raw_pdf_text = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort25_extracted_pdf_text.txt").read_text(encoding="utf-8")
leaves_raw = re.split(r'=== LEAF (p\d+) ===', raw_pdf_text)

leaf_data = {}
for i in range(1, len(leaves_raw), 2):
    lid = leaves_raw[i]
    content = leaves_raw[i+1].strip()
    leaf_data[lid] = content

# Also inspect EPUB text for leaves 241-250
import zipfile
epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))
txt = z.read("index_split_010.xhtml").decode("utf-8", errors="ignore")

# Find headings in EPUB
for h in re.findall(r'<h\d[^>]*>(.*?)</h\d>', txt):
    print("EPUB H:", re.sub(r'<[^>]+>', '', h))

# Find class="title" or similar in EPUB
for p in re.findall(r'<p class="title[^"]*">(.*?)</p>', txt):
    print("EPUB P TITLE:", re.sub(r'<[^>]+>', '', p))

for p in re.findall(r'<p class="heading[^"]*">(.*?)</p>', txt):
    print("EPUB P HEADING:", re.sub(r'<[^>]+>', '', p))
