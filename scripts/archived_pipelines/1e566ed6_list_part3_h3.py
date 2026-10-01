import os

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
path = os.path.join(typikon_dir, "Final_Dolnytsky_part3_menaion.md")

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
for idx, line in enumerate(lines):
    if line.startswith("### "):
        print(f"Line {idx+1}: '{line.strip()}'")
