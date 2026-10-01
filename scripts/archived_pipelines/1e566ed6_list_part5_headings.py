import os

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
path = os.path.join(typikon_dir, "Final_Dolnytsky_part5_temple.md")

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
output_lines = []
for idx, line in enumerate(lines):
    if line.startswith("#"):
        output_lines.append(f"Line {idx+1}: '{line.strip()}'\n")

with open("part5_headings_output.txt", 'w', encoding='utf-8') as f:
    f.writelines(output_lines)
print("Done writing to part5_headings_output.txt")
