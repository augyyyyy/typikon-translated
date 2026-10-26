import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_text = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort25_extracted_pdf_text.txt").read_text(encoding="utf-8")
leaves_raw = re.split(r'=== LEAF (p\d+) ===', pdf_text)

leaf_data = {}
for i in range(1, len(leaves_raw), 2):
    lid = leaves_raw[i]
    content = leaves_raw[i+1].strip()
    leaf_data[lid] = content

for lid in [f'p{p}' for p in range(241, 251)]:
    with open(f"scratch/{lid}_source_raw.txt", "w", encoding="utf-8") as f:
        f.write(leaf_data[lid])

print("Wrote scratch/p241_source_raw.txt through scratch/p250_source_raw.txt")
