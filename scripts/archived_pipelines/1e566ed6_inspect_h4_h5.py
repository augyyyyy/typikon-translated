import os
import re

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
files = [
    "Final_Dolnytsky_part1_structure.md",
    "Final_Dolnytsky_part2_general_rubrics.md",
    "Final_Dolnytsky_part3_menaion.md",
    "Final_Dolnytsky_part4_triodion.md",
    "Final_Dolnytsky_part5_temple.md",
    "Final_Dolnytsky_appendix.md",
    "Final_Dolnytsky_glossary.md"
]

output_lines = []

for filename in files:
    path = os.path.join(typikon_dir, filename)
    if not os.path.exists(path):
        continue
    output_lines.append(f"\n========================================\nFILE: {filename}\n========================================\n")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track the current heading context
    lines = content.splitlines()
    h2 = ""
    h3 = ""
    for line in lines:
        if line.startswith("## "):
            h2 = line
        elif line.startswith("### "):
            h3 = line
        elif line.startswith("#### "):
            output_lines.append(f"  H4: {line.strip()} (under {h3.strip() if h3 else h2.strip()})\n")
        elif line.startswith("##### "):
            output_lines.append(f"  H5: {line.strip()} (under {h3.strip() if h3 else h2.strip()})\n")

output_path = "h4_h5_list.txt"
with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)
print("Done writing to h4_h5_list.txt")
