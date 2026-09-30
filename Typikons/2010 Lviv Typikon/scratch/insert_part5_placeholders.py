import os
import re

FINAL_DIR = r'e:\Google Antigravity\Projects\Translation\Final'
PART5_FILE = os.path.join(FINAL_DIR, 'Final_Dolnytsky_part5_temple.txt')

MARKERS = [
    r'(present here a table of all boundary keys)',
    r'(III\. PERPETUAL TABLE)',
    r'(\(Translator\'s Note: Pages 245-248 contain the massive numerical grids)'
]

def add_part5_placeholders():
    if not os.path.exists(PART5_FILE):
        return
        
    with open(PART5_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    adds = 0
    
    for marker in MARKERS:
        pattern = re.compile(r'(?<!\[INSERT DIAGRAM/TABLE HERE FROM ORIGINAL PDF\]\n\n)' + marker, re.IGNORECASE)
        matches = list(pattern.finditer(content))
        if matches:
            adds += len(matches)
            content = pattern.sub(r'\n\n[INSERT DIAGRAM/TABLE HERE FROM ORIGINAL PDF]\n\n\1', content)
            
    if adds > 0:
        with open(PART5_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added {adds} placeholders for Part 5 charts/tables.")
    else:
        print("No new placeholders needed or already inserted.")

if __name__ == '__main__':
    add_part5_placeholders()
