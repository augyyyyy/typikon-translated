import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

md_path = Path('Final MD/Final_Dolnytsky_part4_triodion.md')
lines = md_path.read_text(encoding='utf-8').splitlines()

# 1. Meatfare Saturday Vespers (L88-95)
for i, l in enumerate(lines):
    if l.startswith('6. At the end: Troparion for the dead'):
        print(f"Fixing Meatfare Saturday Vespers L{i+1}")
        lines[i] = lines[i].replace("6. At the end", "5. At the end")
        lines[i+2] = lines[i+2].replace("7. \"Have mercy", "6. \"Have mercy")
        break

# 2. Archcathedral Notes (L498-502)
for i, l in enumerate(lines):
    if l.startswith('> **Notes**') and i < 600:
        print(f"Fixing Archcathedral Notes L{i+1}")
        lines[i+2] = re.sub(r'^8\.\s+', '1. ', lines[i+2])
        lines[i+4] = re.sub(r'^9\.\s+', '2. ', lines[i+4])
        break

# 3. 17th Kathisma & Praises (L760-768)
for i, l in enumerate(lines):
    if "5. **Praises (Lauds):** Stichera of the Praises, Martyria" in l:
        print(f"Fixing Praises and Doxology L{i+1}")
        lines[i] = lines[i].replace("5. **Praises", "6. **Praises")
        lines[i+2] = lines[i+2].replace("6. **After", "7. **After")
        break

# 4. Great Thursday Matins (L1218-1236)
for i, l in enumerate(lines):
    if "##### At Matins" in l and i > 1200 and i < 1250:
        print(f"Fixing Great Thursday Matins L{i+1}")
        lines[i+2] = re.sub(r'^1\.\t', '1. ', lines[i+2])
        lines[i+4] = lines[i+4].replace("1. **On", "2. **On")
        lines[i+6] = lines[i+6].replace("2. **Troparia:", "3. **Troparia:")
        lines[i+8] = lines[i+8].replace("3. There will", "4. There will")
        lines[i+10] = lines[i+10].replace("4. **Canons:", "5. **Canons:")
        lines[i+16] = lines[i+16].replace("6. **Praises", "6. **Praises")
        lines[i+18] = lines[i+18].replace("7. \"It is", "7. \"It is")
        lines[i+20] = lines[i+20].replace("6. Priest:", "8. Priest:")
        break

# 5. Shroud Notes (L1385-1392)
for i, l in enumerate(lines):
    if l.startswith('> **Notes**') and i > 1350 and i < 1400:
        print(f"Fixing Shroud Notes L{i+1}")
        lines[i+2] = re.sub(r'^7\.\s+', '1. ', lines[i+2])
        lines[i+4] = re.sub(r'^8\.\s+', '2. ', lines[i+4])
        break

md_path.write_text('\n'.join(lines), encoding='utf-8')
print("Successfully fixed all remaining Triodion list numbering issues!")
