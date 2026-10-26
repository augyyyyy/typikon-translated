import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
lines = md_path.read_text(encoding='utf-8').splitlines()

for i, l in enumerate(lines):
    if "ON TUESDAY, WEDNESDAY AND FRIDAY" in l:
        print(f"Fixing Tuesday, Wednesday and Friday numbering at line {i+1}")
        # line i+2 is Everything according to... only: 1. Instead of
        # line i+4 is 9. On Lord I have cried
        lines[i+4] = lines[i+4].replace("9. **On", "2. **On")
        lines[i+6] = lines[i+6].replace("10. **Entrance:**", "3. **Entrance:**")
        lines[i+8] = lines[i+8].replace("11. After", "4. After")
        break

for i, l in enumerate(lines):
    if "ON WEDNESDAY EVENING, IF THE FEAST FALLS ON THURSDAY" in l:
        print(f"Fixing Wednesday evening numbering at line {i+1}")
        lines[i+2] = lines[i+2].replace("12. **On", "1. **On")
        break

md_path.write_text('\n'.join(lines), encoding='utf-8')
print("Successfully fixed final Part 3 numbering bugs!")
