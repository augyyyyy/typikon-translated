import os
import sys
import io

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_part5_temple.md"
with open(path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if line.strip().startswith('#'):
            print(f"{idx}: {line.strip()}")
