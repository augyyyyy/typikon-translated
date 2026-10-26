import fitz
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
pdf_path = Path(r"E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

for p in range(881, 911):
    txt = doc[p-1].get_text()
    notes = re.findall(r'\[(\d+)\]', txt)
    orig_pages = re.findall(r'\{с\.\s*(\d+)\}', txt)
    lines = [l.strip() for l in txt.splitlines() if l.strip()][:2]
    preview = " // ".join(lines)
    print(f"p{p} (Orig {orig_pages}): {preview} -> notes {notes}")
