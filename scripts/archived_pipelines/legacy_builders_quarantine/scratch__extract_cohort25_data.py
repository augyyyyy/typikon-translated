import sys
from pathlib import Path
import re
import zipfile
import fitz

sys.stdout.reconfigure(encoding='utf-8')

# Open PDF
pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))
print("Total pages in PDF:", len(doc))

out_lines = []
for p in range(241, 251):
    out_lines.append(f"=== LEAF p{p} ===")
    out_lines.append(doc[p-1].get_text())

out_file = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort25_extracted_pdf_text.txt")
out_file.write_text("\n\n".join(out_lines), encoding="utf-8")
print(f"Extracted {out_file}, size = {out_file.stat().st_size} bytes")

# Check EPUB notes
epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
if epub_path.exists():
    z = zipfile.ZipFile(str(epub_path))
    txt = z.read("index_split_018.xhtml").decode("utf-8", errors="ignore")
    found_notes = [int(x) for x in re.findall(r'id=["\']n5-(\d+)["\']', txt)]
    print(f"EPUB notes in split_018: total={len(found_notes)}, min={min(found_notes)}, max={max(found_notes)}")
    # Print notes starting at 733
    for n in range(733, 760):
        m = re.search(rf'id=["\']n5-{n}["\'][^>]*></a>\s*(.*?)(?:</div>|<div class="paragraph">)', txt, re.DOTALL)
        if m:
            clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            clean = re.sub(r'^\s*\[?\d+\]?\.?\s*', '', clean).strip()
            print(f"Note {n}: {clean[:80]}...")
