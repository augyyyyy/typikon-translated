import os
import fitz
from pathlib import Path

pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons')
pdf_path = Path(pdf_base) / '1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf'

doc = fitz.open(str(pdf_path))
print(f"Total pages: {len(doc)}")

for i in range(1010, len(doc)):
    txt = doc[i].get_text()
    first_line = txt.strip().split("\n")[0] if txt.strip() else "EMPTY"
    last_line = txt.strip().split("\n")[-1] if txt.strip() else "EMPTY"
    s1 = first_line[:50].encode('ascii', 'replace').decode('ascii')
    s2 = last_line[:50].encode('ascii', 'replace').decode('ascii')
    print(f"Page {i+1}: length={len(txt)} | start: {s1} | end: {s2}")
