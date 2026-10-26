import os
import fitz
from pathlib import Path

pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons')
pdf_path = Path(pdf_base) / '1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf'

doc = fitz.open(str(pdf_path))

for i in range(950, 965):
    txt = doc[i].get_text()
    first_line = txt.strip().split("\n")[0] if txt.strip() else "EMPTY"
    s1 = first_line[:60].encode('ascii', 'replace').decode('ascii')
    print(f"Page {i+1}: len={len(txt)} | start: {s1}")
