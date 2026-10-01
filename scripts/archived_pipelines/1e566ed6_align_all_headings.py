import os
import re

def slugify(text):
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9\s\-]', '', slug)
    slug = slug.replace(' ', '-')
    slug = re.sub(r'-+', '-', slug)
    return slug

def is_month_heading(text):
    months = ["September", "October", "November", "December", "January", "February", "March", "April", "May", "June", "July", "August"]
    cleaned = text.strip()
    # Matches e.g. "3.4 December" or "3.10 June"
    pattern = r'^\d+\.\d+\s+(?:' + '|'.join(months) + r')$'
    return bool(re.match(pattern, cleaned, re.IGNORECASE))

def match_date_in_heading(date_str, heading):
    m = re.match(r'(\d+(?:-\d+)?)\s+(.*)', date_str)
    if not m:
        return False
    day, month = m.group(1), m.group(2)
    # Ensure the day digit in the heading is not preceded by a dot
    pattern = r'(?<!\.)\b' + re.escape(day) + r'\s+' + re.escape(month) + r'\b'
    return bool(re.search(pattern, heading.lower()))

def is_already_aligned(heading):
    return bool(re.match(r'^\d+\.\d+(\.\d+)*\b', heading.strip()))

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

# We will load the contents of all files
file_contents = {}
for filename in files:
    path = os.path.join(typikon_dir, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            file_contents[filename] = f.read()

def normalize_heading(h):
    # Normalize for comparison (remove punctuation, lower, collapse spaces)
    h_norm = h.lower().strip()
    h_norm = re.sub(r'[^a-z0-9\s]', '', h_norm)
    return ' '.join(h_norm.split())

# Reconcile headings
aligned_count = 0
for text, link in toc_links:
    # Try to find a match
    slug = slugify(text)
    # Check if link exists
    found = False
    for filename, content in file_contents.items():
        # Find all headings in content (only levels 2 and 3)
        headings = re.findall(r'^#{2,3}\s+(.*)$', content, re.MULTILINE)
        for h in headings:
            if slugify(h) == link:
                found = True
                break
        if found:
            break
            
    if found:
        continue
        
    # If the TOC text is a month heading, try to match it directly by month name
    if is_month_heading(text):
        m = re.match(r'^\d+\.\d+\s+(.*)$', text.strip())
        if m:
            month_name = m.group(1).lower().strip()
            matched_h = None
            matched_file = None
            for filename, content in file_contents.items():
                headings = re.findall(r'^#{2,3}\s+(.*)$', content, re.MULTILINE)
                for h in headings:
                    if h.lower().strip() == month_name:
                        matched_h = h
                        matched_file = filename
                        break
                if matched_h:
                    break
            if matched_h:
                old_h_esc = re.escape(matched_h)
                pattern = r'^(#{2,3})\s+' + old_h_esc + r'\s*$'
                level_match = re.search(pattern, file_contents[matched_file], re.MULTILINE)
                if level_match:
                    level = level_match.group(1)
                    new_h = f"{level} {text}"
                    file_contents[matched_file], count = re.subn(pattern, new_h, file_contents[matched_file], flags=re.MULTILINE)
                    if count > 0:
                        print(f"ALIGNED MONTH: '{text}' -> '{matched_h}' in {matched_file}")
                        aligned_count += 1
                        continue

    # Not found! Let's search for a close heading match
    # 1. Try date-based match (e.g. "26 October" or "26 OCTOBER" or "26-28 December")
    # Extract date pattern from TOC text, skipping month headings
    date_match = None
    if not is_month_heading(text):
        date_match = re.search(r'(?<!\.)\b(\d+(?:-\d+)?\s+(?:September|October|November|December|January|February|March|April|May|June|July|August))', text, re.IGNORECASE)
        
    if date_match:
        date_str = date_match.group(1).lower()
        # Find heading containing this date
        matched_h = None
        matched_file = None
        for filename, content in file_contents.items():
            headings = re.findall(r'^#{2,3}\s+(.*)$', content, re.MULTILINE)
            for h in headings:
                if is_already_aligned(h):
                    continue
                if match_date_in_heading(date_str, h):
                    matched_h = h
                    matched_file = filename
                    break
            if matched_h:
                break
                
        if matched_h:
            # Replace
            old_h_esc = re.escape(matched_h)
            # Find heading level
            pattern = r'^(#{2,3})\s+' + old_h_esc + r'\s*$'
            level_match = re.search(pattern, file_contents[matched_file], re.MULTILINE)
            if level_match:
                level = level_match.group(1)
                new_h = f"{level} {text}"
                file_contents[matched_file], count = re.subn(pattern, new_h, file_contents[matched_file], flags=re.MULTILINE)
                if count > 0:
                    print(f"ALIGNED DATE: '{text}' -> '{matched_h}' in {matched_file}")
                    aligned_count += 1
                    continue
                    
    # 2. Try match by section number prefix (e.g. "4.1.2")
    num_match = re.match(r'^(\d+(?:\.\d+)+)\b', text)
    if num_match:
        num = num_match.group(1)
        # Search for a heading that starts with this number or contains it
        matched_h = None
        matched_file = None
        for filename, content in file_contents.items():
            headings = re.findall(r'^#{2,3}\s+(.*)$', content, re.MULTILINE)
            for h in headings:
                h_clean = h.strip()
                h_num_match = re.match(r'^(\d+(?:\.\d+)*)\b', h_clean)
                if h_num_match and h_num_match.group(1) == num:
                    matched_h = h
                    matched_file = filename
                    break
                if is_already_aligned(h):
                    continue
                # Or if it's in Part 2 and heading has sequential number
                if filename == "Final_Dolnytsky_part2_general_rubrics.md" and num.startswith("2."):
                    rubric_num = num.split(".")[-1]
                    if rubric_num.isdigit():
                        r_val = int(rubric_num)
                        if r_val <= 7:
                            # Outside a feast
                            if h_clean.startswith(f"{r_val}. ") or h_clean.startswith(f"{r_val}.\t") or h_clean.startswith(f"SAINT WITH") or h_clean.startswith(f"SAINT WITHOUT"):
                                # check if words match
                                if normalize_heading(text.replace(num, ""))[5:15] in normalize_heading(h):
                                    matched_h = h
                                    matched_file = filename
                                    break
                        else:
                            # Within a feast
                            r_within = r_val - 7
                            if h_clean.startswith(f"{r_within}. ") or h_clean.startswith(f"{r_within}.\t") or h_clean.startswith("FOREFEAST") or h_clean.startswith("AFTERFEAST") or h_clean.startswith("APODOSIS"):
                                if normalize_heading(text.replace(num, ""))[5:15] in normalize_heading(h):
                                    matched_h = h
                                    matched_file = filename
                                    break
            if matched_h:
                break
                
        if matched_h:
            # Replace
            old_h_esc = re.escape(matched_h)
            pattern = r'^(#{2,3})\s+' + old_h_esc + r'\s*$'
            level_match = re.search(pattern, file_contents[matched_file], re.MULTILINE)
            if level_match:
                level = level_match.group(1)
                new_h = f"{level} {text}"
                file_contents[matched_file], count = re.subn(pattern, new_h, file_contents[matched_file], flags=re.MULTILINE)
                if count > 0:
                    print(f"ALIGNED NUMBER: '{text}' -> '{matched_h}' in {matched_file}")
                    aligned_count += 1
                    continue

# Write updated files
for filename, content in file_contents.items():
    path = os.path.join(typikon_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Successfully aligned {aligned_count} headings.")
