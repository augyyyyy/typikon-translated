from pathlib import Path
import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

for p in range(551, 561):
    f = Path(f'scratch/cohort56_extracted/p{p}.txt')
    txt = f.read_text(encoding='utf-8')
    print(f'=== p{p} (len {len(txt)}) ===')
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    for l in lines[:3]:
        print('  TOP:', l[:80])
    for l in lines[-2:]:
        print('  END:', l[:80])
    notes = re.findall(r'\[(\d+)\]', txt)
    orig_pages = re.findall(r'\{с\.\s*\d+\}', txt)
    print(f'  Notes found: {notes}')
    print(f'  Orig pages found: {orig_pages}')
