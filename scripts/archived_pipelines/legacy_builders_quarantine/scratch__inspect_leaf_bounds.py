import os
import sys
import re
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

raw_text = Path("scratch/cohort99_source_raw.txt").read_text(encoding='utf-8')

# Split into leaves
parts = raw_text.split("=== LEAF ")
for part in parts[1:]:
    lines = part.strip().splitlines()
    header = lines[0]
    body = "\n".join(lines[1:])
    print(f"=== LEAF {header} ===")
    # Print first 2 and last 2 lines
    sublines = [l for l in lines[1:] if l.strip()]
    for l in sublines[:2]:
        print(f"  TOP: {l}")
    for l in sublines[-2:]:
        print(f"  BOT: {l}")
