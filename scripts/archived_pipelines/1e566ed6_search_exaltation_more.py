import os

part3_path = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_part3_menaion.md"

with open(part3_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find "Universal Exaltation of the Precious Cross"
import re
m = re.search(r'### 3\.1\.4.*', content)
if m:
    start_pos = m.start()
    # Print lines from start_pos + 3000 to start_pos + 10000
    print(content[start_pos + 2000 : start_pos + 8000])
