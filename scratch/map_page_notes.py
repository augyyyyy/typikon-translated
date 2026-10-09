import sys
from pathlib import Path
import re
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

for p in range(281, 291):
    txt = doc[p-1].get_text()
    notes_in_page = re.findall(r'\[(\d+)\]', txt)
    print(f"p{p}: {notes_in_page}")
    # print context of each note
    for n in notes_in_page:
        m = re.search(rf'(.{{0,40}}\[{n}\].{{0,40}})', txt.replace("\n", " "))
        if m:
            print(f"   [{n}]: {m.group(1)}")
