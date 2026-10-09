import sys
from pathlib import Path
import re
import zipfile
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))
fn_txt = z.read("index_split_019.xhtml").decode("utf-8", errors="ignore")

print("--- FOOTNOTES IN EPUB ---")
for i in range(28, 55):
    target = f"n6-{i}"
    pat = rf'id=[\"\']{target}[\"\'][^>]*></a>\s*(.*?)(?:</div>|<div class="paragraph">)'
    m = re.search(pat, fn_txt, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        print(f"[{i}]: {clean}")
    else:
        print(f"[{i}]: NOT FOUND")

print("\n--- LEAF PAGE NOTES AND ORIG PAGES IN MASTER PDF ---")
pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))
for p in range(291, 301):
    txt = doc[p-1].get_text()
    notes = re.findall(r'\[(\d+)\]', txt)
    orig_pages = re.findall(r'\{с\.\s*(\d+)\}', txt)
    print(f"Leaf p{p}: Orig pages {orig_pages}, Notes {notes}")
