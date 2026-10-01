import os

part1_path = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_part1_structure.md"

if not os.path.exists(part1_path):
    print("Part 1 file not found!")
    exit(1)

with open(part1_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.findall(r'\[\^2\]', content)
print(f"Found {len(matches)} occurrences of [^2] in Part 1:")
for m in re.finditer(r'\[\^2\]', content):
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 50)
    print(repr(content[start:end]))
