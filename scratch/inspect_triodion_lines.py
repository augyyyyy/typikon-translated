import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

md_lines = Path('Final MD/Final_Dolnytsky_part4_triodion.md').read_text(encoding='utf-8').splitlines()
txt_lines = Path('Final/Final_Dolnytsky_part4_triodion.txt').read_text(encoding='utf-8').splitlines()

problem_lines = [95, 264, 268, 348, 494, 570, 574, 760, 1234, 1326, 1330, 1380, 1594, 1596]

for lno in problem_lines:
    print(f"--- Triodion MD Line {lno} ---")
    start = max(0, lno - 4)
    end = min(len(md_lines), lno + 3)
    for j in range(start, end):
        print(f"  MD L{j+1}: {repr(md_lines[j][:60])}")
