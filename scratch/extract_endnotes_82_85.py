import os
import fitz
from pathlib import Path

pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons')
pdf_path = Path(pdf_base) / '1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf'

doc = fitz.open(str(pdf_path))
out_lines = []

# Pages 1003 to 1008 (0-indexed: 1002 to 1007)
for page_num in range(1002, min(1008, len(doc))):
    p = doc[page_num]
    text = p.get_text()
    out_lines.append(f"--- PAGE {page_num + 1} ---\n")
    out_lines.append(text)

out_path = Path("scratch") / "cohort82_85_endnotes_raw.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print(f"Extracted pages 1003-1008 to {out_path} ({len(out_lines)} blocks)")
