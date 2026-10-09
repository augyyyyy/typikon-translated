import os
import sys
import re
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

raw_path = Path("scratch/cohort99_source_raw.txt")
raw_text = raw_path.read_text(encoding='utf-8')

for target in ["324", "325", "326", "438", "439", "440", "216", "620", "155"]:
    print(f"--- Searching for {target} ---")
    pos = 0
    while True:
        idx = raw_text.find(target, pos)
        if idx == -1:
            break
        start = max(0, idx - 50)
        end = min(len(raw_text), idx + 100)
        snippet = raw_text[start:end].replace('\n', ' ')
        print(f"Found at {idx}: {snippet}")
        pos = idx + len(target)
