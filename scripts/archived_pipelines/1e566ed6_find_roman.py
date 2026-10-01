import os
import re

path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_appendix.md"
with open(path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        line_stripped = line.strip()
        # Match Roman numerals at the beginning of a line
        m = re.match(r'^([IVXLCDM]+)\b', line_stripped)
        if m:
            print(f"{idx}: {line_stripped}")
