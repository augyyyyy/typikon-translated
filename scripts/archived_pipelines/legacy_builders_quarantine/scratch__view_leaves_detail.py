import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for p in range(161, 171):
    raw = Path(f"scratch/leaf_texts/p{p}.txt").read_text(encoding="utf-8")
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    print(f"=== PHYSICAL LEAF p{p} (lines: {len(lines)}) ===")
    print("\n".join(lines[:12]))
    print("...")
    print("\n".join(lines[-8:]))
    print()
