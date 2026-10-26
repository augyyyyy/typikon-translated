import sys
from pathlib import Path
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for p in range(331, 341):
    fpath = Path(f"scratch/leaf_p{p}_raw.txt")
    txt = fpath.read_text(encoding='utf-8')
    orig_pages = re.findall(r'\{с\.\s*(\d+)\}', txt)
    notes = re.findall(r'\[(\d+)\]', txt)
    print(f"=== LEAF p{p} (Orig p. {orig_pages}, Notes: {notes}) ===")
    lines = txt.splitlines()
    print(f"Total lines: {len(lines)}")
    # Print first 5 non-empty lines
    non_empty = [l for l in lines if l.strip()]
    for l in non_empty[:3]:
        print(f"  TOP: {l}")
    for l in non_empty[-3:]:
        print(f"  BTM: {l}")
    print()
