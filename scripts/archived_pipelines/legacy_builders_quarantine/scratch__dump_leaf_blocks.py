import sys
import re
from pathlib import Path
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

for p_idx in range(190, 200):
    p_num = p_idx + 1
    page = doc[p_idx]
    # get text preserving layout
    blocks = page.get_text("blocks")
    print(f"==================== LEAF p{p_num} ====================")
    for b in blocks:
        text = b[4].strip()
        # skip header/footer page numbers if any
        if text.isdigit() and len(text) <= 3:
            continue
        print(text)
        print("---")
