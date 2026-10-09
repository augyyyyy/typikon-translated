import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

src = Path('Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/1910_skaballanovich_typikon_cohort25_source.txt').read_text(encoding='utf-8')

leaves = re.findall(r'=== LEAF (p\d+) ===', src)
print("Leaves:", leaves)

pages = re.findall(r'\{с\.\s*(\d+)\}', src)
print("Original pages:", pages)

notes = [int(x) for x in re.findall(r'\[(\d+)\]', src)]
print(f"Notes count: {len(notes)}, min: {min(notes)}, max: {max(notes)}")
missing_notes = [n for n in range(733, 775) if n not in notes]
print("Missing notes:", missing_notes)

headings = re.findall(r'^###\s+(.*)$', src, re.MULTILINE)
print("Headings:", headings)
