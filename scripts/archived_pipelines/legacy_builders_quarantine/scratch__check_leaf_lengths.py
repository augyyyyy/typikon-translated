import sys
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for p in range(301, 311):
    raw = Path(f"scratch/leaf_p{p}_raw.txt").read_text(encoding="utf-8")
    # replace multiple spaces and line breaks within paragraphs
    # but preserve structural headings
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    text = "\n".join(lines)
    print(f"Leaf p{p}: length {len(text)} chars")
