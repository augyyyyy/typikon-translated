import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

for p in range(241, 251):
    txt = Path(f"scratch/p{p}_source_raw.txt").read_text(encoding="utf-8")
    greek = re.findall(r'[\u0370-\u03ff\u1f00-\u1fff]+', txt)
    latin = re.findall(r'[A-Za-z]+', txt)
    print(f"p{p}:")
    if greek:
        print(f"  Greek: {greek}")
    if latin:
        # Filter common words
        print(f"  Latin: {latin}")
