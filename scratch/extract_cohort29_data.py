import sys
from pathlib import Path
import re
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))
print("Total pages in PDF:", len(doc))

out_lines = []
for p in range(281, 291):
    txt = doc[p-1].get_text()
    out_lines.append(f"=== LEAF p{p} ===")
    out_lines.append(txt)
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    first_line = lines[0] if lines else 'EMPTY'
    last_line = lines[-1] if lines else 'EMPTY'
    print(f"p{p}: {len(txt)} chars, {len(lines)} lines | First: {first_line[:40]} | Last: {last_line[:40]}")

out_file = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort29_extracted_pdf_text.txt")
out_file.write_text("\n\n".join(out_lines), encoding="utf-8")
print(f"Extracted {out_file}, size = {out_file.stat().st_size} bytes")
