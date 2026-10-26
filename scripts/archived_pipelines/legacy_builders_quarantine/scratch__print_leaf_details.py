import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

for p in range(241, 251):
    txt = Path(f"scratch/p{p}_source_raw.txt").read_text(encoding="utf-8")
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    print(f"============================== LEAF p{p} ({len(lines)} lines) ==============================")
    # Print the full text reconstructed into paragraphs
    # Lines ending without hyphen or with hyphen:
    text_blocks = []
    curr = []
    for l in lines:
        curr.append(l)
    print('\n'.join(lines))
