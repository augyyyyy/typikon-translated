import os
import sys
from pathlib import Path
import fitz

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf')
doc = fitz.open(pdf_base)

# Let's inspect bottom of p982 (page 981 in 0-indexed)
p982 = doc[981].get_text()
print("Bottom of p982:")
print("\n".join(p982.splitlines()[-5:]))

print("\nTop of p983:")
p983 = doc[982].get_text()
print("\n".join(p983.splitlines()[:5]))
