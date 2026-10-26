import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for p in range(331, 341):
    fpath = Path(f"scratch/leaf_p{p}_raw.txt")
    lines = [l.strip() for l in fpath.read_text(encoding='utf-8').splitlines()]
    # recombine into paragraphs while preserving original markers
    print(f"==================== LEAF p{p} ====================")
    txt = "\n".join(lines)
    print(txt)
    print("\n")
