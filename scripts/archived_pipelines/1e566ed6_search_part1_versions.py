import os
import re

projects_dir = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects"

for root, dirs, files in os.walk(projects_dir):
    for file in files:
        if file == "Final_Dolnytsky_part1_structure.md":
            path = os.path.join(root, file)
            print(f"Found file: {path}")
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Find the Order of Daily Matins section
            m = re.search(r'Order of Daily Matins', content, re.IGNORECASE)
            if m:
                print("  Daily Matins text snippet:")
                # print next 1000 characters
                snippet = content[m.start():m.start()+1500]
                print(snippet)
                print("="*60)
