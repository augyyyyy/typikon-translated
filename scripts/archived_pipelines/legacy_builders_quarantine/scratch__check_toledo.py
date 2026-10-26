import sys
from pathlib import Path
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))
page = doc[291] # p292
rects = page.search_for("Толедский")
print("Search rects for Толедский:", rects)
for r in rects:
    print(page.get_textbox(fitz.Rect(r.x0-50, r.y0-10, r.x1+300, r.y1+30)))
