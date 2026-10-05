import os
import re

FINAL_DIR = r'e:\Google Antigravity\Projects\Translation\Final'

# The exact or partial phrases indicating a diagram or table start
DIAGRAM_MARKERS = [
    r'Diagram:\s+At the Entrance',
    r'Diagram:\s+At the Narthex',
    r'Diagram:\s+At the Blessing of Loaves',
    r'Diagram:\s+At the Magnification',
    r'Diagram:\s+At the Little Entrance',
    r'Diagram:\s+Before the Little Entrance',
    r'Diagram:\s+At the High Throne',
    r'\[Diagram:\s+Communion of the Body',
    r'\[Diagram of the Lamb\]',
    r'diagram below:',
    r'^TABLE\s*\nThis table consists'  # Specific match for the Paschal table
]

def add_placeholders():
    print("Scanning Final files for diagram/table locations...")
    files = [f for f in os.listdir(FINAL_DIR) if f.endswith('.txt')]
    total_added = 0
    
    for fname in files:
        fpath = os.path.join(FINAL_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        file_adds = 0
        
        for marker in DIAGRAM_MARKERS:
            # We want to insert the placeholder exactly before the marker, 
            # ensuring we don't accidentally double-insert if the script is run twice.
            # Using negative lookbehind to prevent double insertion.
            pattern = re.compile(r'(?<!\[INSERT DIAGRAM/TABLE HERE FROM ORIGINAL PDF\]\n\n)(' + marker + r')', re.MULTILINE | re.IGNORECASE)
            
            # Find matches to count logically
            matches = list(pattern.finditer(new_content))
            if matches:
                file_adds += len(matches)
                new_content = pattern.sub(r'\n\n[INSERT DIAGRAM/TABLE HERE FROM ORIGINAL PDF]\n\n\1', new_content)
                
        if file_adds > 0:
            total_added += file_adds
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  {fname}: Added {file_adds} placeholders.")
            
    print(f"Total placeholders inserted: {total_added}")

if __name__ == '__main__':
    add_placeholders()
