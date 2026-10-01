import os
import re

path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_appendix.md"
with open(path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        line_stripped = line.strip()
        # Match lines starting with a Roman numeral like "I.", "II.", "III." etc., followed by uppercase
        # We also want to capture if there is a '#' in front or not
        if re.match(r'^(?:#+\s*)?[IVXLCDM]+\.\s+[A-Z]', line_stripped):
            print(f"{idx}: {line_stripped}")
