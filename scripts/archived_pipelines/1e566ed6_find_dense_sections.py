import os
import sys
import io
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
files = [
    "Final_Dolnytsky_part1_structure.md",
    "Final_Dolnytsky_part2_general_rubrics.md",
    "Final_Dolnytsky_part3_menaion.md",
    "Final_Dolnytsky_part4_triodion.md",
    "Final_Dolnytsky_part5_temple.md",
    "Final_Dolnytsky_appendix.md"
]

print("Auditing for dense, un-split prose sections...")

for filename in files:
    path = os.path.join(src_dir, filename)
    if not os.path.exists(path):
        continue
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split the file by headings to analyze each section
    sections = re.split(r'^(#+ .*)$', content, flags=re.MULTILINE)
    
    current_h3 = None
    h4_or_h5_present = False
    paragraphs = []
    
    # We iterate through the split blocks. The split will alternatingly be:
    # [non-heading content, heading_line, non-heading content, heading_line...]
    # If a heading matches H3, we check the following block for H4 or H5,
    # and count its paragraphs.
    for i in range(1, len(sections), 2):
        heading = sections[i].strip()
        body = sections[i+1] if i+1 < len(sections) else ""
        
        level = len(heading) - len(heading.lstrip('#'))
        
        if level == 3:
            # We found a new H3. Let's analyze the previous H3 first
            if current_h3 and not h4_or_h5_present:
                p_count = len([p for p in paragraphs if p.strip()])
                if p_count > 3:
                    print(f"[{filename}] Dense Section under '{current_h3}' with {p_count} paragraphs and no sub-headers:")
                    # print first 2 paragraphs as preview
                    previews = [p.strip()[:100] + "..." for p in paragraphs if p.strip()][:2]
                    for p in previews:
                        print(f"    * {p}")
            
            current_h3 = heading
            h4_or_h5_present = False
            # Split body by double newlines to count paragraphs
            paragraphs = body.split('\n\n')
            
        elif level in [4, 5]:
            if current_h3:
                h4_or_h5_present = True

    # Check last section
    if current_h3 and not h4_or_h5_present:
        p_count = len([p for p in paragraphs if p.strip()])
        if p_count > 3:
            print(f"[{filename}] Dense Section under '{current_h3}' with {p_count} paragraphs and no sub-headers:")
            previews = [p.strip()[:100] + "..." for p in paragraphs if p.strip()][:2]
            for p in previews:
                print(f"    * {p}")
