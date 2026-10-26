import sys
from pathlib import Path
import zipfile
import re
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Try epub
epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
if epub_path.exists():
    z = zipfile.ZipFile(str(epub_path))
    for fname in z.namelist():
        if fname.endswith(".xhtml") or fname.endswith(".html"):
            content = z.read(fname).decode("utf-8", errors="ignore")
            # look for note anchors
            if 'id="n6-17"' in content or 'id="n-17"' in content or 'id="note17"' in content or '>17<' in content:
                print(f"Found 17 in {fname}")

# Let's inspect the PDF around page 505-507
pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))
print(f"Total pages in PDF: {len(doc)}")

# Look around pages 500-515
for pno in range(500, 515):
    txt = doc[pno].get_text()
    if "17]" in txt or "17." in txt or "18]" in txt or "26]" in txt or "34]" in txt:
        print(f"Page {pno+1} might have notes: {txt[:100]}...")
