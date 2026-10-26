import sys
import re
import fitz
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

for page_idx in range(195, 201): # physical pages 196 to 201
    p_num = page_idx + 1
    page = doc[page_idx]
    txt = page.get_text()
    print(f"=== LEAF p{p_num} ===")
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    for l in lines:
        if any(w in l for w in ['{с.', '[', 'пр.', 'Правил', 'ГЛАВА', 'Устав']):
            print("  ", l[:100])
