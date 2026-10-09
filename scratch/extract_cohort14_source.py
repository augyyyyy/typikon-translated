import fitz
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

leaves_text = {}
for p in range(130, 140):
    leaf_num = p + 1
    text = doc[p].get_text()
    leaves_text[leaf_num] = text

for leaf_num, text in leaves_text.items():
    print(f"=== LEAF p{leaf_num} ===")
    print(f"Length: {len(text)} chars, Lines: {len(text.splitlines())}")
    print("--- FIRST 200 CHARS ---")
    print(text[:200].strip())
    print("--- LAST 200 CHARS ---")
    print(text[-200:].strip())
    print()
