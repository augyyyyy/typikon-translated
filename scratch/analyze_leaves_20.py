import sys
import re
import fitz
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

for page_idx in range(190, 200): # physical pages 191 to 200
    p_num = page_idx + 1
    page = doc[page_idx]
    txt = page.get_text()
    
    # find note markers like [440], [441] etc.
    notes = re.findall(r'\[(\d+)\]', txt)
    # find page markers like {с. 203}
    orig_pages = re.findall(r'\{[сc]\.?\s*\d+\}', txt)
    
    first_line = txt.strip().split('\n')[0] if txt.strip() else ""
    last_line = txt.strip().split('\n')[-1] if txt.strip() else ""
    
    print(f"=== LEAF p{p_num} ===")
    print(f"  Notes on page: {notes}")
    print(f"  Orig page markers: {orig_pages}")
    print(f"  First line: {first_line[:60]}")
    print(f"  Last line:  {last_line[:60]}")
    print(f"  Char count: {len(txt)}")
