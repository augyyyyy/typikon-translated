import os
import sys
from pathlib import Path
import fitz

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf')
pdf_path = Path(pdf_base)
doc = fitz.open(pdf_path)

raw_path = Path("scratch/cohort99_source_raw.txt")
raw_text = raw_path.read_text(encoding='utf-8')

raw_leaves = raw_text.split("=== LEAF ")
leaf_dict = {}
for part in raw_leaves[1:]:
    lines = part.strip().splitlines()
    header = lines[0].split()[0]  # e.g. p981
    content = "\n".join(lines[1:])
    leaf_dict[header] = content

for p in range(981, 991):
    leaf_id = f"p{p}"
    pdf_text = doc[p-1].get_text().strip()
    raw_content = leaf_dict.get(leaf_id, "").strip()
    print(f"=== {leaf_id} ===")
    print(f"PDF length: {len(pdf_text)} | Raw length: {len(raw_content)}")
