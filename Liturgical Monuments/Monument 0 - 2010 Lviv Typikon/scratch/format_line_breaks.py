import os
import re

FINAL_DIR = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\Final"
TYPIKON_DIR = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"

def is_header(line):
    line = line.strip()
    if not line: return False
    # Horizontal rule
    if line.startswith('_____'): return True
    # All caps (with spaces), more than 3 chars
    if re.match(r'^[A-Z\s]+$', line) and len(line) > 3: return True
    # "ORDER OF..."
    if line.startswith("ORDER OF") or line.startswith("ON THE"): return True
    # Numbered section (1. Name)
    if re.match(r'^\d{1,2}\.\s+[A-Z]', line): return True
    # Roman numeral section (I. Name)
    if re.match(r'^(I|II|III|IV|V|VI|VII|VIII|IX|X)\.\s+[A-Z]', line): return True
    # Parts (PART I)
    if line.startswith("PART "): return True
    return False

def format_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        # Always keep empty lines if they already exist
        if not line.strip():
            new_lines.append(line)
            continue
            
        # If it's a header, and the previous line in new_lines is not empty, add an empty line
        if is_header(line):
            if new_lines and new_lines[-1].strip():
                # Don't add blank line if the previous line was also a header? 
                # Actually, the user says "blank lines between sections make it easier to read".
                # Let's add a blank line.
                new_lines.append("")
        
        new_lines.append(line)
        
    # Now normalize multiple blank lines to a single blank line
    text = '\n'.join(new_lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Save back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

files_to_process = []
for file in os.listdir(FINAL_DIR):
    if file.endswith('.txt') and "footnotes" not in file:
        files_to_process.append(os.path.join(FINAL_DIR, file))

for file in os.listdir(TYPIKON_DIR):
    if file.endswith('.txt'):
        files_to_process.append(os.path.join(TYPIKON_DIR, file))

for f in set(files_to_process):
    print("Formatting", f)
    format_file(f)
