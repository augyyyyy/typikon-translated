import sys
from pathlib import Path
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))
p300_text = doc[299].get_text()
print("Length of p300 text:", len(p300_text))
print("Last 200 characters of p300 text:")
print(repr(p300_text[-200:]))
print("Raw p300 text:")
print(p300_text)

# Also check p301 to see how it connects
p301_text = doc[300].get_text()
print("First 200 characters of p301 text:")
print(repr(p301_text[:200]))
print(p301_text[:200])
