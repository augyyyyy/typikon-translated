import os

part4_path = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_part4_triodion.md"

with open(part4_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
headings = re.findall(r'^#+.*$', content, re.MULTILINE)
print("Part 4 Headings:")
for h in headings:
    print(h)
