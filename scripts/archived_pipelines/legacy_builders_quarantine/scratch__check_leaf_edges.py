import sys
from pathlib import Path
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

for p in range(291, 301):
    page = doc[p-1]
    txt = page.get_text()
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    first_3 = lines[:3] if len(lines) >= 3 else lines
    last_3 = lines[-3:] if len(lines) >= 3 else lines
    print(f"=== LEAF p{p} (PDF page {p}) ===")
    print("  FIRST LINES:", " // ".join(first_3))
    print("  LAST LINES: ", " // ".join(last_3))
