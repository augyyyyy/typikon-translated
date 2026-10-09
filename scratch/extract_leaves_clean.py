import sys
import re
import fitz
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

leaves_text = {}
for p_idx in range(190, 200):
    p_num = p_idx + 1
    page = doc[p_idx]
    # get text as blocks
    blocks = page.get_text("blocks")
    cleaned_blocks = []
    for b in blocks:
        b_txt = b[4].strip()
        # skip page numbers if separate block
        if b_txt.isdigit() and len(b_txt) <= 4:
            continue
        cleaned_blocks.append(b_txt)
    leaves_text[p_num] = cleaned_blocks

# Let's see how many blocks each leaf has
for p_num, blist in leaves_text.items():
    print(f"p{p_num}: {len(blist)} blocks")
