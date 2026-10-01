import os
import re

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
path = os.path.join(typikon_dir, "Final_Dolnytsky_part2_general_rubrics.md")

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

service_pattern = r'^(####\s*)?AT\s+(?:GREAT\s+|SMALL\s+|DAILY\s+|THE\s+)?(?:VESPERS|COMPLINE|MATINS|HOURS|LITURGY|MIDNIGHT\s+OFFICE)\b'

for idx, line in enumerate(lines):
    if re.search(service_pattern, line, re.IGNORECASE):
        print(f"Line {idx+1}: '{line}'")
