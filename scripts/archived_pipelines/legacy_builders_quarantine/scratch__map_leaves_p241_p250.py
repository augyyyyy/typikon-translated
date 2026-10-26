import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_text = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort25_extracted_pdf_text.txt").read_text(encoding="utf-8")
leaves_raw = re.split(r'=== LEAF (p\d+) ===', pdf_text)

for i in range(1, len(leaves_raw), 2):
    lid = leaves_raw[i]
    content = leaves_raw[i+1].strip()
    pages = re.findall(r'\{с\.\s*(\d+)\}', content)
    notes = re.findall(r'\[(\d+)\]', content)
    print(f"{lid}: Original page markers={pages}, Footnote markers={notes}")
