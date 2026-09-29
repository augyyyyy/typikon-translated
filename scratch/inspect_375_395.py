from pathlib import Path
import re

txt_lines = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8').splitlines()
md_lines = Path('Final MD/Final_Dolnytsky_part3_menaion.md').read_text(encoding='utf-8').splitlines()

print("Footnotes 375 to 395 in Part 3 MD:")
for i, line in enumerate(md_lines):
    for m in re.finditer(r'\[\^(\d+)\]', line):
        fn = int(m.group(1))
        if 375 <= fn <= 395:
            print(f"MD L{i+1}: [^{fn}] - {line[:80]}")
