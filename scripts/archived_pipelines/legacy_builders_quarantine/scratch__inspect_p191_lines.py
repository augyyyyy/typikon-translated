import sys
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf"
doc = fitz.open(pdf_path)

txt = doc[190].get_text()
for i, line in enumerate(txt.split('\n')):
    print(f"{i:2d}: {repr(line)}")
