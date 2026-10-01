import os
import re

path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_appendix.md"
with open(path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        line_stripped = line.strip()
        if "Rubric" in line_stripped or "Liturgy" in line_stripped:
            if idx > 216:
                print(f"{idx}: {line_stripped[:80]}")
