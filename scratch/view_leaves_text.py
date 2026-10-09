import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for pno in range(301, 311):
    f = Path(f"scratch/leaf_p{pno}_raw.txt")
    lines = [l.strip() for l in f.read_text(encoding='utf-8').splitlines() if l.strip()]
    print(f"==================== LEAF p{pno} (lines: {len(lines)}) ====================")
    text = " ".join(lines)
    # Print formatted paragraph-like view
    print(f.read_text(encoding='utf-8'))
