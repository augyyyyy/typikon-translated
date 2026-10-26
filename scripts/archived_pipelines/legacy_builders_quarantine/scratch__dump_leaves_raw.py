import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for p in range(161, 171):
    raw = Path(f"scratch/leaf_texts/p{p}.txt").read_text(encoding="utf-8")
    # Clean non-breaking spaces
    raw = raw.replace('\xa0', ' ')
    print(f"==================== LEAF p{p} ====================")
    print(raw)
