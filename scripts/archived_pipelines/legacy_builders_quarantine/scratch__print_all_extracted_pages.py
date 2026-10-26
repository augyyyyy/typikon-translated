from pathlib import Path
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

for p in range(551, 561):
    txt = Path(f'scratch/cohort56_extracted/p{p}.txt').read_text(encoding='utf-8')
    print(f"\n==================== LEAF p{p} (len {len(txt)}) ====================")
    print(txt)
