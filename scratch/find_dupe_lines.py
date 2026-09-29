from pathlib import Path
import re

txt_lines = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8').splitlines()
md_lines = Path('Final MD/Final_Dolnytsky_part3_menaion.md').read_text(encoding='utf-8').splitlines()

print("--- TXT ---")
for fn in [248, 277]:
    for i, l in enumerate(txt_lines):
        if f"[^{fn}]" in l:
            print(f"TXT L{i+1} ([^{fn}]): {l[:100]}")

print("\n--- MD ---")
for fn in [248, 250, 251, 252, 277]:
    found = False
    for i, l in enumerate(md_lines):
        if f"[^{fn}]" in l:
            print(f"MD L{i+1} ([^{fn}]): {l[:100]}")
            found = True
    if not found:
        print(f"MD: [^{fn}] NOT FOUND!")
