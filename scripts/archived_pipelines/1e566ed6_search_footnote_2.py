import os

footnotes_path = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_footnotes.md"

if not os.path.exists(footnotes_path):
    print("Footnotes file not found!")
    exit(1)

with open(footnotes_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.findall(r'^\[\^2\]:.*$', content, re.MULTILINE)
print("Matches for [^2]:")
for m in matches:
    print(m)

print("\nMatches for 'Excerpt from Appendix XXXI':")
matches_text = re.findall(r'^.*Excerpt from Appendix XXXI.*$', content, re.MULTILINE | re.IGNORECASE)
for m in matches_text:
    print(m)
