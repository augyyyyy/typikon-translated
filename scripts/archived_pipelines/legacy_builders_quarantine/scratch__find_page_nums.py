import sys
from pathlib import Path
import re
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

for p in range(281, 291):
    page = doc[p-1]
    # Check rect at top (y < 60) and bottom (y > 700)
    rect_top = fitz.Rect(0, 0, page.rect.width, 60)
    top_text = page.get_text("text", clip=rect_top).strip()
    rect_bottom = fitz.Rect(0, page.rect.height - 60, page.rect.width, page.rect.height)
    bottom_text = page.get_text("text", clip=rect_bottom).strip()
    print(f"p{p}: TOP='{top_text}' | BOTTOM='{bottom_text}'")
