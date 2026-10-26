import os
import sys
from pathlib import Path
import fitz

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf')
pdf_path = Path(pdf_base)

if not pdf_path.exists():
    print(f"PDF not found: {pdf_path}")
else:
    doc = fitz.open(pdf_path)
    print(f"Total pages in doc: {len(doc)}")
    # Check page 981 to 990 (1-indexed page 981 is doc[980])
    for p in range(981, 991):
        page_idx = p - 1
        page = doc[page_idx]
        text = page.get_text()
        first_line = text.splitlines()[0] if text.splitlines() else ""
        last_lines = [l for l in text.splitlines() if l.strip()][-3:]
        print(f"--- Leaf p{p} (page_idx {page_idx}) ---")
        print(f"Length: {len(text)} chars, Lines: {len(text.splitlines())}")
        print(f"First line: {first_line}")
        print(f"Last lines: {last_lines}\n")
