import os
import re

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
intro_path = os.path.join(typikon_dir, "Final_Dolnytsky_intro.md")

with open(intro_path, 'r', encoding='utf-8') as f:
    intro_content = f.read()

toc_links = re.findall(r'\[([^\]]+)\]\(#([^\)]+)\)', intro_content)

# Find 2.6
target_text = None
target_link = None
for text, link in toc_links:
    if '2.6' in text:
        target_text = text
        target_link = link
        break

print(f"Target Text: '{target_text}'")
print(f"Target Link: '{target_link}'")

# Load file
part2_path = os.path.join(typikon_dir, "Final_Dolnytsky_part2_general_rubrics.md")
with open(part2_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's run slugify
def slugify(text):
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9\s\-]', '', slug)
    slug = slug.replace(' ', '-')
    slug = re.sub(r'-+', '-', slug)
    return slug

def is_already_aligned(heading):
    return bool(re.match(r'^\d+\.\d+(\.\d+)*\b', heading.strip()))

headings = re.findall(r'^#{2,3}\s+(.*)$', content, re.MULTILINE)
print("Total headings in Part 2:", len(headings))

# Let's search for matches
num_match = re.match(r'^(\d+(?:\.\d+)+)\b', target_text)
if num_match:
    num = num_match.group(1)
    print(f"Number Prefix: '{num}'")
    for h in headings:
        h_clean = h.strip()
        if h_clean.startswith(num + " ") or h_clean.startswith(num + ".") or h_clean.startswith(num + "\t"):
            print(f"Matched Heading: '{h}'")
            print(f"is_already_aligned('{h}'): {is_already_aligned(h)}")
            # Check replacement pattern
            old_h_esc = re.escape(h)
            pattern = r'^(#{2,3})\s+' + old_h_esc + r'\s*$'
            level_match = re.search(pattern, content, re.MULTILINE)
            print(f"Level Match: {level_match is not None}")
            if level_match:
                print(f"Level: '{level_match.group(1)}'")
