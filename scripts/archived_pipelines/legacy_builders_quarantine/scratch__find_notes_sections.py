import sys
import fitz

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open('E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf')

for pno in range(425, 450):
    t = doc[pno].get_text()
    for line in t.split('\n'):
        if 'II в' in line or 'II век' in line or 'Век апостольский' in line:
            print(f'Page {pno+1}: {line}')
