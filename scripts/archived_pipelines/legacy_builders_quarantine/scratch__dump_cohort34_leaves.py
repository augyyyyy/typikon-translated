import sys
from pathlib import Path
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

for pno in range(330, 340):
    leaf_num = pno + 1
    txt = doc[pno].get_text()
    out_file = Path(f"scratch/leaf_p{leaf_num}_raw.txt")
    out_file.write_text(txt, encoding="utf-8")
    print(f"Dumped leaf p{leaf_num}: {len(txt)} chars")
