import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parent.parent

txt_lines = (root / 'Final/Final_Dolnytsky_part2_general_rubrics.txt').read_text(encoding='utf-8').splitlines()
md_lines = (root / 'Final MD/Final_Dolnytsky_part2_general_rubrics.md').read_text(encoding='utf-8').splitlines()

print("--- TXT matches for 112 and 115 ---")
for idx, l in enumerate(txt_lines):
    if '[^112]' in l or '[^115]' in l:
        print(f"TXT L{idx+1}: {l}")

print("\n--- MD match for 123 ---")
for idx, l in enumerate(md_lines):
    if '[^123]' in l:
        print(f"MD L{idx+1}: {l}")

print("\n--- TXT matches for 192 and 217 ---")
for idx, l in enumerate(txt_lines):
    if '[^192]' in l or '[^217]' in l:
        print(f"TXT L{idx+1}: {l}")
