from pathlib import Path
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

for pno in range(701, 711):
    f = Path(f'scratch/cohort71_extracted/p{pno}.txt')
    text = f.read_text(encoding='utf-8')
    notes = re.findall(r'\[(\d+)\]', text)
    orig_pages = re.findall(r'\{с\.\s*\d+\}', text)
    print(f"=== Leaf p{pno} === (len={len(text)}, notes={notes}, orig_pages={orig_pages})")
