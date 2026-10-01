import os
import re

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
files = [
    "Final_Dolnytsky_part1_structure.md",
    "Final_Dolnytsky_part2_general_rubrics.md",
    "Final_Dolnytsky_part3_menaion.md",
    "Final_Dolnytsky_part4_triodion.md",
    "Final_Dolnytsky_part5_temple.md",
    "Final_Dolnytsky_appendix.md",
    "Final_Dolnytsky_glossary.md"
]

def parse_header_number(title):
    # Extracts numbers like "1.1", "1.2.1" from heading start
    m = re.match(r'^(\d+(?:\.\d+)*)\b', title.strip())
    if m:
        return [int(x) for x in m.group(1).split('.')]
    return None

def clean_title(title):
    # Remove existing numbers/bullets from heading text
    cleaned = title.strip()
    # Remove leading numbering like "1.1 ", "1. ", "1.\t", "V. "
    cleaned = re.sub(r'^(\d+(?:\.\d+)*[\.\t\s]*)+', '', cleaned)
    # Remove roman numerals like "I. ", "V. "
    cleaned = re.sub(r'^[IVXLCDM]+\.[\t\s]*', '', cleaned)
    # Remove leading tabs/bullets
    cleaned = cleaned.strip(" \t.*")
    return cleaned

output_lines = []

for filename in files:
    path = os.path.join(typikon_dir, filename)
    if not os.path.exists(path):
        continue
    
    output_lines.append(f"\n=== SIMULATION FOR {filename} ===\n")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.splitlines()
    
    # Track hierarchy state
    h1_val = None
    h2_val = None
    h3_val = None
    h4_val = 0
    h5_val = 0
    
    # Determine default h1_val based on filename if not found in file
    if "part1" in filename:
        h1_val = 1
    elif "part2" in filename:
        h1_val = 2
    elif "part3" in filename:
        h1_val = 3
    elif "part4" in filename:
        h1_val = 4
    elif "part5" in filename:
        h1_val = 5
    elif "appendix" in filename:
        h1_val = 6
    elif "glossary" in filename:
        h1_val = 7
        
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped.startswith("#"):
            continue
            
        # Count heading level
        level = len(line_stripped) - len(line_stripped.lstrip('#'))
        title = line_stripped.lstrip('#').strip()
        
        # Parse existing prefix if present
        existing_nums = parse_header_number(title)
        
        if level == 1:
            # H1 defines a new Part
            if "PART I" in title.upper():
                h1_val = 1
            elif "PART II" in title.upper():
                h1_val = 2
            elif "PART III" in title.upper():
                h1_val = 3
            elif "PART IV" in title.upper():
                h1_val = 4
            elif "PART V" in title.upper():
                h1_val = 5
            elif "APPENDIX" in title.upper():
                h1_val = 6
            elif "GLOSSARY" in title.upper():
                h1_val = 7
            h2_val = None
            h3_val = None
            h4_val = 0
            h5_val = 0
            output_lines.append(f"H1: {line_stripped}\n")
            
        elif level == 2:
            # H2
            if existing_nums:
                # E.g. "1.1" -> h1_val=1, h2_val=1
                if len(existing_nums) >= 2:
                    h1_val, h2_val = existing_nums[0], existing_nums[1]
                else:
                    h2_val = existing_nums[0]
            else:
                if h2_val is None:
                    h2_val = 1
                else:
                    h2_val += 1
            h3_val = None
            h4_val = 0
            h5_val = 0
            
            clean_t = clean_title(title)
            new_title = f"## {h1_val}.{h2_val} {clean_t}"
            output_lines.append(f"  H2: '{line_stripped}' -> '{new_title}'\n")
            
        elif level == 3:
            # H3
            if existing_nums:
                if len(existing_nums) >= 3:
                    h1_val, h2_val, h3_val = existing_nums[0], existing_nums[1], existing_nums[2]
                elif len(existing_nums) == 2:
                    h2_val, h3_val = existing_nums[0], existing_nums[1]
                else:
                    h3_val = existing_nums[0]
            else:
                if h3_val is None:
                    h3_val = 1
                else:
                    h3_val += 1
            h4_val = 0
            h5_val = 0
            
            clean_t = clean_title(title)
            new_title = f"### {h1_val}.{h2_val}.{h3_val} {clean_t}"
            output_lines.append(f"    H3: '{line_stripped}' -> '{new_title}'\n")
            
        elif level == 4:
            # H4
            h4_val += 1
            h5_val = 0
            
            clean_t = clean_title(title)
            # Use current h3 if available, else h2
            if h3_val is not None:
                parent_prefix = f"{h1_val}.{h2_val}.{h3_val}"
            else:
                parent_prefix = f"{h1_val}.{h2_val}"
            new_title = f"#### {parent_prefix}.{h4_val} {clean_t}"
            output_lines.append(f"      H4: '{line_stripped}' -> '{new_title}'\n")
            
        elif level == 5:
            # H5
            h5_val += 1
            
            clean_t = clean_title(title)
            # Use current h4 if available, else h3, else h2
            if h4_val > 0:
                if h3_val is not None:
                    parent_prefix = f"{h1_val}.{h2_val}.{h3_val}.{h4_val}"
                else:
                    parent_prefix = f"{h1_val}.{h2_val}.{h4_val}"
            elif h3_val is not None:
                parent_prefix = f"{h1_val}.{h2_val}.{h3_val}"
            else:
                parent_prefix = f"{h1_val}.{h2_val}"
                
            new_title = f"##### {parent_prefix}.{h5_val} {clean_t}"
            output_lines.append(f"        H5: '{line_stripped}' -> '{new_title}'\n")

with open("simulation_output.txt", 'w', encoding='utf-8') as f:
    f.writelines(output_lines)
print("Done writing to simulation_output.txt")
