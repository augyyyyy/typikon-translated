from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')

for pno in range(701, 711):
    f = Path(f'scratch/cohort71_extracted/p{pno}.txt')
    lines = f.read_text(encoding='utf-8').splitlines()
    print(f'=== p{pno} === (first 3 lines, last 2 lines, total lines {len(lines)})')
    for l in lines[:3]:
        print('  ', l[:100])
    print('   ...')
    for l in lines[-2:]:
        print('  ', l[:100])
