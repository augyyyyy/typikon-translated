import os
import re

path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_appendix.md"
with open(path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if idx > 345:
            line_stripped = line.strip()
            if line_stripped.startswith('####') or line_stripped.startswith('#####'):
                # Check if it doesn't start with a paragraph number like "##### 97."
                m = re.match(r'^#####\s+\d+\b', line_stripped)
                if not m:
                    print(f"{idx}: {line_stripped}")
                else:
                    # If it starts with a small number (e.g. 1 to 5), it might be a sub-heading
                    num = int(re.match(r'^#####\s+(\d+)\b', line_stripped).group(1))
                    if num < 10:
                        print(f"{idx}: [SUB] {line_stripped}")
