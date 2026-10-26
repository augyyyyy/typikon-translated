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

# Check paragraph splits in EPUB vs PDF for each leaf
import zipfile
epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))
epub_text = z.read("index_split_010.xhtml").decode("utf-8", errors="ignore")

for p in range(241, 251):
    lid = f"p{p}"
    print(f"\n==================== {lid} ====================")
    # let's see how many paragraphs are in the raw leaf
    lines = leaf_data[lid].split('\n')
    print(f"Lines count: {len(lines)}")
