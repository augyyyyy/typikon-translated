import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

raw_pdf_text = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort25_extracted_pdf_text.txt").read_text(encoding="utf-8")
leaves_raw = re.split(r'=== LEAF (p\d+) ===', raw_pdf_text)

leaf_data = {}
for i in range(1, len(leaves_raw), 2):
    lid = leaves_raw[i]
    content = leaves_raw[i+1].strip()
    leaf_data[lid] = content

for lid in [f'p{p}' for p in range(241, 251)]:
    print(f"============================== {lid} ==============================")
    lines = leaf_data[lid].split('\n')
    for idx, l in enumerate(lines[:15]):
        print(f"{idx+1}: {l}")
    print("...")
    for idx, l in enumerate(lines[-10:]):
        print(f"{len(lines)-10+idx+1}: {l}")
