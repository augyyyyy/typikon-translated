import sys
from pathlib import Path
import re
import zipfile

sys.stdout.reconfigure(encoding='utf-8')

pdf_text = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort25_extracted_pdf_text.txt").read_text(encoding="utf-8")
leaves_raw = re.split(r'=== LEAF (p\d+) ===', pdf_text)

leaf_data = {}
for i in range(1, len(leaves_raw), 2):
    lid = leaves_raw[i]
    content = leaves_raw[i+1].strip()
    leaf_data[lid] = content

# Print clean representation of each leaf
for lid in [f'p{p}' for p in range(241, 251)]:
    print(f"\n==================== {lid} ====================")
    lines = [l.strip() for l in leaf_data[lid].split('\n') if l.strip()]
    full = ' '.join(lines)
    full = re.sub(r'\s+', ' ', full)
    print(full[:300] + ' ... ' + full[-300:])
