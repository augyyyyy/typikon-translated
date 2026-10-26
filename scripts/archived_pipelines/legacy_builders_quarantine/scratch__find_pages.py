import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

for pno in range(750, 762):
    p = Path(f'scratch/cohort76_extracted/p{pno}.txt')
    if not p.exists():
        continue
    content = p.read_text(encoding='utf-8')
    matches = re.findall(r'\{[сc]\.?\s*\d+\}', content)
    print(f"p{pno}: {matches}")
