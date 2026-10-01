import os
import re

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
intro_path = os.path.join(typikon_dir, "Final_Dolnytsky_intro.md")

with open(intro_path, 'r', encoding='utf-8') as f:
    intro_content = f.read()

toc_links = re.findall(r'\[([^\]]+)\]\(#([^\)]+)\)', intro_content)

files = [
    "Final_Dolnytsky_part1_structure.md",
    "Final_Dolnytsky_part2_general_rubrics.md",
    "Final_Dolnytsky_part3_menaion.md",
    "Final_Dolnytsky_part4_triodion.md",
    "Final_Dolnytsky_part5_temple.md",
    "Final_Dolnytsky_appendix.md",
    "Final_Dolnytsky_glossary.md"
]

file_contents = {}
for filename in files:
    path = os.path.join(typikon_dir, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            file_contents[filename] = f.read()

def slugify(text):
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9\s\-]', '', slug)
    slug = slug.replace(' ', '-')
    slug = re.sub(r'-+', '-', slug)
    return slug

def is_month_heading(text):
    months = ["September", "October", "November", "December", "January", "February", "March", "April", "May", "June", "July", "August"]
    cleaned = text.strip()
    pattern = r'^\d+\.\d+\s+(?:' + '|'.join(months) + r')$'
    return bool(re.match(pattern, cleaned, re.IGNORECASE))

def is_already_aligned(heading):
    return bool(re.match(r'^\d+\.\d+(\.\d+)*\b', heading.strip()))

# Trace for '2.6'
for text, link in toc_links:
    if '2.6' not in text:
        continue
        
    print(f"--- TRACING: {text} ---")
    slug = slugify(text)
    print(f"slug: {slug}")
    
    # Check if link exists
    found = False
    for filename, content in file_contents.items():
        headings = re.findall(r'^#{2,3}\s+(.*)$', content, re.MULTILINE)
        for h in headings:
            if slugify(h) == link:
                found = True
                print(f"Found exact match: '{h}' in {filename}")
                break
        if found:
            break
            
    print(f"found: {found}")
    if found:
        continue
        
    if is_month_heading(text):
        print("is_month_heading is True")
        continue
        
    # Number matching
    num_match = re.match(r'^(\d+(?:\.\d+)+)\b', text)
    print(f"num_match: {num_match is not None}")
    if num_match:
        num = num_match.group(1)
        print(f"num: {num}")
        matched_h = None
        matched_file = None
        for filename, content in file_contents.items():
            headings = re.findall(r'^#{2,3}\s+(.*)$', content, re.MULTILINE)
            for h in headings:
                h_clean = h.strip()
                if h_clean.startswith(num + " ") or h_clean.startswith(num + ".") or h_clean.startswith(num + "\t"):
                    matched_h = h
                    matched_file = filename
                    print(f"Found heading startswith num: '{h}' in {filename}")
                    break
                if is_already_aligned(h):
                    continue
            if matched_h:
                break
                
        print(f"matched_h: '{matched_h}' in {matched_file}")
        if matched_h:
            old_h_esc = re.escape(matched_h)
            pattern = r'^(#{2,3})\s+' + old_h_esc + r'\s*$'
            level_match = re.search(pattern, file_contents[matched_file], re.MULTILINE)
            print(f"level_match: {level_match is not None}")
            if level_match:
                level = level_match.group(1)
                new_h = f"{level} {text}"
                print(f"pattern: {pattern}")
                print(f"new_h: {new_h}")
                res_content, count = re.subn(pattern, new_h, file_contents[matched_file], flags=re.MULTILINE)
                print(f"re.subn count: {count}")
