import os

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
path = os.path.join(typikon_dir, "backup", "Final_Dolnytsky_part2_general_rubrics.md")

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    line_str = line.strip()
    # If the line is in uppercase and is not empty, and doesn't start with #
    if line_str.isupper() and len(line_str) > 5 and not line_str.startswith('#'):
        # Skip AT COMPLINE, AT VESPERS etc.
        if not any(word in line_str for word in ["AT ", "THE ", "HOURS", "LITURGY", "COMPLINE", "MIDNIGHT", "MATINS"]):
            print(f"L{i+1}: {line_str}")
