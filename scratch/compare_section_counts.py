import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# Compare paragraph count per date/chapter in Part 3 (Menaion)
ua_p3 = Path('Ukrainian TXTs/Part 3.txt').read_text(encoding='utf-8')
en_p3 = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8')

# Extract sections matching dates like '1 ВЕРЕСНЯ', '2 ВЕРЕСНЯ', etc.
ua_sections = re.split(r'\n(?=\d+\s+[А-ЯЄІЇ]+)', ua_p3)
en_sections = re.split(r'\n(?=\d+\s+[A-Z]+)', en_p3)

print(f"Ukrainian Part 3 major date sections: {len(ua_sections)}")
print(f"English Part 3 major date sections: {len(en_sections)}")

# Match by index or name
for idx in range(min(len(ua_sections), len(en_sections), 30)):
    u_lines = [l for l in ua_sections[idx].splitlines() if l.strip()]
    e_lines = [l for l in en_sections[idx].splitlines() if l.strip()]
    u_title = u_lines[0] if u_lines else "EMPTY"
    e_title = e_lines[0] if e_lines else "EMPTY"
    diff = len(u_lines) - len(e_lines)
    if abs(diff) >= 3:
        print(f"Section {idx}: UA ({len(u_lines)} lines): \"{u_title[:30]}\" vs EN ({len(e_lines)} lines): \"{e_title[:30]}\" -> DIFF = {diff}")
