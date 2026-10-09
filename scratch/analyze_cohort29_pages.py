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
    txt = page.get_text()
    print(f"=== LEAF p{p} (PDF page {p}) ===")
    # Find original book page number if present in header/footer
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    header = lines[0] if lines else ""
    print(f"Header/first line: {header}")
    # Search for footnotes at the bottom of the page or numbers in brackets
    # Let's see bottom 10 lines
    print("--- Bottom lines ---")
    for l in lines[-8:]:
        print("  ", l)
    print()
