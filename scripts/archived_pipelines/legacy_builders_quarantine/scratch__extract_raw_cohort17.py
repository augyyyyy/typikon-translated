import fitz
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

for pno in range(160, 170):
    page_num = pno + 1
    page = doc[pno]
    text = page.get_text()
    out_path = Path(f"scratch/leaf_texts/p{page_num}.txt")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"Leaf p{page_num}: {len(text)} chars written to {out_path}")
