import os

list_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\h4_h5_list.txt"

if not os.path.exists(list_path):
    print("h4_h5_list.txt not found!")
    exit(1)

with open(list_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
m = re.search(r'===+.*part4.*===+', content, re.IGNORECASE)
if m:
    start_pos = m.start()
    end_m = re.search(r'===+.*part5.*===+', content, re.IGNORECASE)
    if end_m:
        end_pos = start_pos + end_m.start()
    else:
        end_pos = len(content)
    print("Part 4 Headings:")
    print(content[start_pos:end_pos])
else:
    print("Part 4 not found!")
