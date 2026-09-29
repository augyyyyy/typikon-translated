from pathlib import Path
import re

txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

# Check which footnotes from 247 to 278 are missing in TXT or MD
for fn in range(247, 279):
    tag = f"[^{fn}]"
    in_txt = tag in txt
    in_md = tag in md
    if not (in_txt and in_md):
        print(f"FN {fn}: in_txt={in_txt}, in_md={in_md}")
