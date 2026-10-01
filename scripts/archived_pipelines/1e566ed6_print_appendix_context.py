import os
import re

appendix_path = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_appendix.md"

with open(appendix_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for "II. Rubric of Vespers without Vigil"
m = re.search(r'II\. Rubric of Vespers without Vigil', content)
if m:
    start_pos = m.start()
    # Print 500 characters before and 1000 characters after
    print("SURROUNDING TEXT FOR II:")
    print(content[max(0, start_pos - 1000) : min(len(content), start_pos + 1500)])
else:
    print("Not found II")
