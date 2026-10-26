import sys
import fitz

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open('E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf')

for pno in [430, 431, 964, 965]:
    t = doc[pno].get_text()[:400]
    print(f'=== Page {pno+1} ===\n{t}\n')
