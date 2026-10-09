import sys
from pathlib import Path
import fitz
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

full_notes_text = ""
for pno in [504, 505, 506]:
    full_notes_text += doc[pno].get_text() + "\n"

# Let's extract notes 17 through 34
notes = {}
for i in range(17, 35):
    # Pattern to find start of note i and start of note i+1
    pat = rf'(?:^|\n)\s*{i}\.\s*(.*?)(?=(?:^|\n)\s*{i+1}\.\s*|\Z)'
    m = re.search(pat, full_notes_text, re.DOTALL)
    if m:
        txt = m.group(1).strip()
        # clean line breaks inside note
        clean = " ".join(l.strip() for l in txt.splitlines() if l.strip())
        notes[i] = clean
        print(f"[{i}]: {clean[:80]}... (len {len(clean)})")
    else:
        print(f"[{i}]: NOT FOUND")

out_file = Path("scratch/cohort34_russian_notes.txt")
with open(out_file, "w", encoding="utf-8") as f:
    for i in range(17, 35):
        f.write(f"[{i}] {notes.get(i, '')}\n\n")
print(f"Wrote notes to {out_file}")
