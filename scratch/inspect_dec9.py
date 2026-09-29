import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

ua_p3 = Path('Ukrainian TXTs/Part 3.txt').read_text(encoding='utf-8')
en_p3 = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8')

# Find December 9 in both
ua_match = re.search(r'9 ГРУДНЯ.*?(?=\d+\s+[А-ЯЄІЇ]+|\Z)', ua_p3, re.DOTALL)
en_match = re.search(r'9 DECEMBER.*?(?=\d+\s+[A-Z]+|\Z)', en_p3, re.DOTALL)

if ua_match and en_match:
    u_text = ua_match.group(0)
    e_text = en_match.group(0)
    print(f"UA Dec 9 characters: {len(u_text)}, lines: {len(u_text.splitlines())}")
    print(f"EN Dec 9 characters: {len(e_text)}, lines: {len(e_text.splitlines())}")
    
    print("\nUA Dec 9 Headings:")
    for l in u_text.splitlines():
        if 'УСТАВ' in l or 'ВЕРЕСНЯ' in l or 'ГРУДНЯ' in l or 'НЕДІЛ' in l or 'СЕДМИЧ' in l or l.startswith('I.') or l.startswith('II.'):
            print("  UA:", l.strip())
            
    print("\nEN Dec 9 Headings:")
    for l in e_text.splitlines():
        if 'RULE' in l or 'DECEMBER' in l or 'SUNDAY' in l or 'WEEKDAY' in l or l.startswith('I.') or l.startswith('II.'):
            print("  EN:", l.strip())
