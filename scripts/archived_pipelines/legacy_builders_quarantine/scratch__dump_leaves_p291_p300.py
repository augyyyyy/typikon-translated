import sys
from pathlib import Path
import fitz
import zipfile
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

with open("scratch/leaves_p291_p300_pdf.txt", "w", encoding="utf-8") as f:
    for p in range(291, 301):
        txt = doc[p-1].get_text()
        f.write(f"=== LEAF p{p} ===\n")
        f.write(txt)
        f.write("\n\n")

print("Wrote scratch/leaves_p291_p300_pdf.txt")
