import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

for p in [243, 248, 249, 250]:
    txt = Path(f"scratch/p{p}_source_raw.txt").read_text(encoding="utf-8")
    for idx, line in enumerate(txt.split('\n')):
        if any(c in line for c in ['ἀ', 'ἐ', 'π', 'λ', 'φ', 'titulus', 'frontium', 'indulgentia', 'vigilat', 'attenduntur']):
            print(f"p{p}:{idx+1}: {line}")
