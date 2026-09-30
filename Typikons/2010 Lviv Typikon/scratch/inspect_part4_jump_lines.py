from pathlib import Path
import re

md_lines = Path('Final MD/Final_Dolnytsky_part4_triodion.md').read_text(encoding='utf-8').splitlines()

targets = [484, 490, 492, 510, 517, 521, 529, 535, 548, 561, 566, 572, 624, 638, 639, 643, 651]

for fn in targets:
    for i, l in enumerate(md_lines):
        if f"[^{fn}]" in l:
            print(f"MD L{i+1} [^{fn}]: {l[:90]}")
