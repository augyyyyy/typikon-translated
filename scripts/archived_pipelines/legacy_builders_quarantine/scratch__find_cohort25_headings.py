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

# Check where headings might appear:
for lid in [f'p{p}' for p in range(241, 251)]:
    lines = leaf_data[lid].split('\n')
    for l in lines:
        l_s = l.strip()
        # Headings are typically short lines without ending punctuation, or centered/bold
        if l_s in [
            'Великий четверг',
            'Великая пятница',
            'Великая суббота',
            'Пасха',
            'Пасхальная седмица',
            'Фомина неделя'
        ] or (len(l_s) < 40 and not l_s.endswith('.') and not l_s.endswith(',') and not l_s.endswith(';') and not l_s.endswith(':') and not l_s.startswith('[') and not l_s.endswith(']')):
            print(f"{lid}: {l_s}")
