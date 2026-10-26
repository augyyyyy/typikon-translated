import sys
from pathlib import Path
import fitz
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

print("=== LEAF SUMMARY p331 - p340 ===")
for p in range(331, 341):
    txt = doc[p-1].get_text()
    notes = re.findall(r'\[(\d+)\]', txt)
    orig_pages = re.findall(r'\{с\.\s*(\d+)\}', txt)
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    first_line = lines[0] if lines else ''
    last_line = lines[-1] if lines else ''
    print(f"Leaf p{p}: Orig: {orig_pages}, Notes: {notes}, Chars: {len(txt)}")
    print(f"   First: {first_line}")
    print(f"   Last:  {last_line}")
