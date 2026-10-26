import sys
import re
import fitz
import zipfile
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(epub_path)
html = z.read("index_split_009.xhtml").decode("utf-8", errors="ignore")

for p_idx in range(190, 200):
    p_num = p_idx + 1
    page = doc[p_idx]
    txt = page.get_text()
    print(f"=== LEAF p{p_num} ===")
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    print(f"First 2 lines: {lines[:2]}")
    print(f"Last 2 lines:  {lines[-2:]}")
