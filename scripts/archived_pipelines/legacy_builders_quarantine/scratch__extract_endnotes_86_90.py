import os
import fitz
from pathlib import Path

pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons')
pdf_path = Path(pdf_base) / '1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf'

doc = fitz.open(str(pdf_path))
out_lines = []

# Pages 1008 to 1014 (0-indexed: 1007 to 1013)
for page_num in range(1007, min(1014, len(doc))):
    p = doc[page_num]
    text = p.get_text()
    out_lines.append(f"--- PAGE {page_num + 1} ---\n")
    out_lines.append(text)

out_path = Path("scratch") / "cohort86_90_endnotes_raw.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print(f"Extracted pages 1008-1014 to {out_path}")
