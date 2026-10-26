import sys
from pathlib import Path
import re
import zipfile

sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))
txt = z.read("index_split_018.xhtml").decode("utf-8", errors="ignore")

# Let's see what notes are referenced in leaves 241-250
pdf_text = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort25_extracted_pdf_text.txt").read_text(encoding="utf-8")

notes_in_pdf = [int(x) for x in re.findall(r'\[(\d+)\]', pdf_text)]
print(f"Notes in PDF: min={min(notes_in_pdf)}, max={max(notes_in_pdf)}, count={len(notes_in_pdf)}")
print("Found notes in PDF:", sorted(set(notes_in_pdf)))

# Check all notes from min to max in EPUB
for n in range(min(notes_in_pdf), max(notes_in_pdf) + 1):
    m = re.search(rf'id=["\']n5-{n}["\'][^>]*></a>\s*(.*?)(?:</div>|<div class="paragraph">)', txt, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        clean = re.sub(r'^\s*\[?\d+\]?\.?\s*', '', clean).strip()
        print(f"[{n}] -> fn {n + 584}: {clean}")
    else:
        print(f"[{n}] -> fn {n + 584}: MISSING IN EPUB")

# Also let's find original page numbers
pages_in_pdf = re.findall(r'\{с\.\s*(\d+)\}', pdf_text)
print("\nOriginal pages found in PDF text:", pages_in_pdf)
