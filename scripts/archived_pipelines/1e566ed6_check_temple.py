import os

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
path = os.path.join(typikon_dir, "Final_Dolnytsky_part5_temple.md")

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip().startswith('"') or line.strip().endswith('"'):
        sanitized = line.strip()[:120].encode('ascii', 'replace').decode('ascii')
        print(f"L{i+1}: {sanitized}")
