import os

part1_path = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_part1_structure.md"

with open(part1_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
m = re.search(r'### 1\.5\.3 Order of Daily Matins', content)
if m:
    start_pos = m.start()
    # Find next section "#### Note on a Non-Polyeleos" or similar
    end_m = re.search(r'#### Note on a Non-Polyeleos', content[start_pos:])
    if end_m:
        end_pos = start_pos + end_m.start()
    else:
        end_pos = start_pos + 2000
    print(repr(content[start_pos:end_pos]))
else:
    print("Not found!")
