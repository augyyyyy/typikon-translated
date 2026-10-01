import os
import re

intro_path = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_intro.md"

if not os.path.exists(intro_path):
    print("Intro file not found!")
    exit(1)

with open(intro_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all links starting with appendix or containing the word appendix/rubric in link
matches = re.findall(r'\[[^\]]*\]\([^\)]*appendix[^\)]*\)', content, re.IGNORECASE)
print("Appendix links in TOC:")
for m in matches:
    print(m)

# Find all links containing 6.1
matches_61 = re.findall(r'\[[^\]]*\]\([^\)]*6\.1[^\)]*\)', content, re.IGNORECASE)
print("\n6.1 links in TOC:")
for m in matches_61:
    print(m)
