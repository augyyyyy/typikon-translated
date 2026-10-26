import sys
import re
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

txt = Path('scratch/pdf_text_cohort43.txt').read_text(encoding='utf-8')
leaves = txt.split('=== LEAF ')
for leaf in leaves:
    if not leaf.strip():
        continue
    parts = leaf.split('\n')
    header = parts[0].strip()
    print(f'=== {header} ===')
    page_markers = re.findall(r'\{[сc]\.\s*\d+\}', leaf)
    print('Page markers:', page_markers)
    non_empty = [p.strip() for p in parts[1:] if p.strip()]
    if non_empty:
        print('  First line:', non_empty[0][:80])
        print('  Last line:', non_empty[-1][:80])
    print()
