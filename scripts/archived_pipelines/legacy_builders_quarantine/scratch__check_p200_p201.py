import sys
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf"
doc = fitz.open(pdf_path)

p200 = doc[199].get_text()
p201 = doc[200].get_text()

print("P200 last 5 lines:")
for l in p200.strip().split('\n')[-5:]:
    print("  ", repr(l))

print("P201 first 5 lines:")
for l in p201.strip().split('\n')[:5]:
    print("  ", repr(l))
