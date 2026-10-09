import fitz
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
pdf_path = Path(r"E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

all_text = []
for p in range(1014, 1023):
    txt = doc[p-1].get_text()
    all_text.append(f"--- PAGE {p} ---\n" + txt)

out_file = Path("scratch/cohort91_96_endnotes_raw.txt")
out_file.write_text("\n".join(all_text), encoding='utf-8')
print(f"Extracted {len(all_text)} endnote pages to {out_file} ({out_file.stat().st_size} bytes)")
