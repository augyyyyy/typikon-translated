import os
import re

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
master_path = os.path.join(typikon_dir, "Dolnytsky_Typikon_Master.md")

with open(master_path, 'r', encoding='utf-8') as f:
    content = f.read()

def slugify(text):
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9\s\-]', '', slug)
    slug = slug.replace(' ', '-')
    slug = re.sub(r'-+', '-', slug)
    return slug

headings = re.findall(r'^#+\s+(.*)$', content, re.MULTILINE)
anchors = set(slugify(h) for h in headings)

print("TOTAL HEADINGS FOUND:", len(headings))
print("TOTAL ANCHORS GENERATED:", len(anchors))
print("\nFirst 10 Headings:")
for h in headings[:10]:
    print(f"  Raw: '{h}' | Slug: '{slugify(h)}'")

# Let's check some specific headings
targets = [
    "1.1 On the Constituent Parts of the Divine Service",
    "1.2 Vespers",
    "1.2.1 Order of Great Vespers with All-Night Vigil"
]
print("\nChecking Specific Targets:")
for t in targets:
    found = False
    for h in headings:
        if t.lower() in h.lower():
            print(f"  Match found: Raw: '{h}' | Slug: '{slugify(h)}'")
            found = True
    if not found:
        print(f"  No match found for: '{t}'")
