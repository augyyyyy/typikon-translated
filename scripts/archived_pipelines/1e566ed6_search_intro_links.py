import os
import re

path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_intro.md"
with open(path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if "(#" in line:
            print(f"{idx}: {line.strip()}")
