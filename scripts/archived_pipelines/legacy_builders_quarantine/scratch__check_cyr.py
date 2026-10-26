import re
from pathlib import Path

for fname in ["scratch/step_41_dump.txt", "scratch/step_47_dump.txt"]:
    p = Path(fname)
    if p.exists():
        text = p.read_text(encoding="utf-8")
        cyr_blocks = re.findall(r'[\u0400-\u04FF\s\d\.,:;«»\(\)\[\]\?\!\—\-\*\#\=\/]{50,}', text)
        print(f"{fname}: {len(cyr_blocks)} cyrillic blocks found")
        for i, b in enumerate(cyr_blocks[:5]):
            print(f"--- Block {i} ({len(b)} chars) ---")
            print(b[:300].strip())
