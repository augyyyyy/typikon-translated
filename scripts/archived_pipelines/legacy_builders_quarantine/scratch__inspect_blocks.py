import sys
import fitz
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf'
doc = fitz.open(pdf_path)

for pno in range(420, 430):
    page = doc[pno]
    blocks = page.get_text('blocks')
    print(f'=== Page {pno+1} ===')
    for b in blocks:
        # Check if block is near top or bottom or contains page number
        y0, y1 = b[1], b[3]
        text = b[4].strip().replace('\n', ' ')
        if y0 < 50 or y1 > page.rect.height - 50:
            print(f'  [y={y0:.1f}-{y1:.1f}] {text[:80]}')
        elif any(c in text for c in ['{с.', '{c.', 'с.']):
            print(f'  [marker in body] {text[:80]}')
