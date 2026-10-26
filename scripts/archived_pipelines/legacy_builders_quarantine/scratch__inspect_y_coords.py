import sys
from pathlib import Path
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

for p in range(281, 291):
    page = doc[p-1]
    # In the PDF, is there a separator line or footnotes at the bottom?
    # Let's inspect all text blocks with their bounding boxes
    print(f"\n==================== LEAF p{p} (PDF page {p}) ====================")
    blocks = page.get_text("blocks")
    for b in blocks:
        # print y coordinates and first line of text
        txt_lines = b[4].strip().splitlines()
        first_line = txt_lines[0] if txt_lines else ""
        last_line = txt_lines[-1] if txt_lines else ""
        print(f"y0={b[1]:.1f}, y1={b[3]:.1f}, lines={len(txt_lines)}: '{first_line[:50]}' ... '{last_line[:50]}'")
