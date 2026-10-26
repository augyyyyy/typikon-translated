import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for p in range(301, 311):
    txt = Path(f"scratch/leaf_p{p}_raw.txt").read_text(encoding="utf-8").strip()
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    first_few = " ".join(lines[:3])
    last_few = " ".join(lines[-3:])
    print(f"=== LEAF p{p} ===")
    print(f"  START: {first_few[:120]}")
    print(f"  END:   {last_few[-120:]}")
