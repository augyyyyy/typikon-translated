import os
import re

coded_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\all_horizontal_rules.txt"

matches = []
for file in os.listdir(coded_dir):
    if file.endswith('.md'):
        path = os.path.join(coded_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            # Match horizontal lines of underscores or dashes
            if re.match(r'^_{3,}$|^_{5,}.*|^-{3,}$|^-{5,}.*', line.strip()):
                matches.append(f"{file} | Line {idx+1}: {line.strip()}")

with open(output_path, "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(matches))

print(f"SUCCESS: Found {len(matches)} horizontal rule matches. Wrote to {output_path}")
