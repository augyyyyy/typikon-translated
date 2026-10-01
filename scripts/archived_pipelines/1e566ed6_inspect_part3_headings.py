import os

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
path = os.path.join(typikon_dir, "Final_Dolnytsky_part3_menaion.md")

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
h2 = ""
h3 = ""
output_lines = []

h4_count = 0
h5_count = 0

for line in lines:
    if line.startswith("## "):
        h2 = line
    elif line.startswith("### "):
        h3 = line
    elif line.startswith("#### "):
        h4_count += 1
        output_lines.append(f"H4: {line.strip()} (under H3: {h3.strip() if h3 else h2.strip()})\n")
    elif line.startswith("##### "):
        h5_count += 1
        output_lines.append(f"  H5: {line.strip()} (under H3: {h3.strip() if h3 else h2.strip()})\n")

output_lines.append(f"\nSummary: H4={h4_count}, H5={h5_count}\n")

with open("part3_headings_output.txt", 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Done. Found {h4_count} H4s and {h5_count} H5s. Wrote to part3_headings_output.txt")
