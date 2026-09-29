import re
from pathlib import Path

md_path = Path('Final MD/Final_Dolnytsky_part2_general_rubrics.md')
md_lines = md_path.read_text(encoding='utf-8').splitlines()

# Find all footnote references and their line numbers
refs = []
for i, line in enumerate(md_lines):
    for m in re.finditer(r'\[\^(\d+)\]', line):
        refs.append((int(m.group(1)), i+1, line))

print(f"Total footnotes in Part 2 MD: {len(refs)}")
for idx in range(len(refs)-1):
    cur_fn, cur_l, cur_line = refs[idx]
    nxt_fn, nxt_l, nxt_line = refs[idx+1]
    if nxt_fn < cur_fn:
        print(f"\nBackward Jump! L{cur_l} [^{cur_fn}] -> L{nxt_l} [^{nxt_fn}] (jump of {cur_fn - nxt_fn})")
        print(f"  Line {cur_l}: {cur_line[:90]}")
        print(f"  Line {nxt_l}: {nxt_line[:90]}")
