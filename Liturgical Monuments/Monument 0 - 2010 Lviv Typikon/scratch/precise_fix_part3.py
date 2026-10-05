import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
lines = md_path.read_text(encoding='utf-8').splitlines()

# 1. Fix L248-255 (Renovation on Sunday)
# Find line with "3 readings to the Renovation."
for i, l in enumerate(lines):
    if "3 readings to the Renovation." in l:
        print(f"Fixing Renovation on Sunday at line {i+1}")
        lines[i] = "3. **Readings:** 3 readings to the Renovation."
        lines[i+2] = "4. **Aposticha:** At the Aposticha – Resurrectional stichera; Glory: to the Renovation, Both now: of the Forefeast"
        lines[i+4] = "5. **Troparia:** After the Trisagion – Resurrectional Troparion, Glory: to the Renovation, Both now: of the Forefeast"
        lines[i+6] = "6. **Dismissal:** Great Dismissal with Resurrectional commemoration"
        break

# 2. Fix L1150-1170 (Nativity/Theophany Eve Vespers)
for i, l in enumerate(lines):
    if l.startswith('The Priest, having put on an epitrachelion and having gone out before the Holy Doors'):
        print(f"Fixing Nativity Eve Vespers at line {i+1}")
        lines[i] = "1. " + lines[i]
        lines[i+2] = "2. " + lines[i+2]
        lines[i+4] = re.sub(r'^3\.\t', '3. ', lines[i+4])
        # line i+6 is 4. On Lord I have cried
        lines[i+8] = "5. **Entrance:** " + lines[i+8]
        lines[i+10] = "6. " + lines[i+10]
        lines[i+12] = "7. " + lines[i+12]
        lines[i+14] = "8. " + lines[i+14]
        lines[i+16] = "9. " + lines[i+16]
        lines[i+18] = "10. " + lines[i+18]
        break

# 3. Fix L1800 (Synaxis of Forerunner on Sunday)
for i, l in enumerate(lines):
    if "#### II. SYNAXIS OF THE FORERUNNER ON SUNDAY" in l:
        print(f"Fixing Synaxis of Forerunner at line {i+1}")
        lines[i+2] = "1. **Kathisma:** *“Blessed is the man”*, as usual."
        lines[i+4] = lines[i+4].replace("3. **On", "2. **On")
        lines[i+6] = lines[i+6].replace("4. **Aposticha:**", "3. **Aposticha:**")
        lines[i+8] = "4. **Troparia:** " + lines[i+8]
        break

# 4. Fix Cheesefare Saturday Finding of Head
for i, l in enumerate(lines):
    if "2. FINDING OF THE PRECIOUS HEAD" in l and "ON CHEESEFARE SATURDAY" in lines[i+2]:
        print(f"Fixing Cheesefare Saturday Finding at line {i+1}")
        lines[i+6] = "1. **Kathisma:** *“Blessed is the man”* (according to the rule – 1st antiphon)."
        lines[i+8] = lines[i+8].replace("1. **On", "2. **On")
        lines[i+10] = lines[i+10].replace("2. **Entrance:**", "3. **Entrance:**")
        lines[i+12] = lines[i+12].replace("3. **Aposticha:**", "4. **Aposticha:**")
        lines[i+14] = lines[i+14].replace("4. **Troparia:**", "5. **Troparia:**")
        lines[i+16] = lines[i+16].replace("5. Litany", "6. Litany")
        lines[i+18] = re.sub(r'^7\.\t', '7. ', lines[i+18])
        break

# 5. Fix Finding on Monday (L2806)
for i, l in enumerate(lines):
    if "ON SUNDAY EVENING," in l and "IF THE FEAST FALLS ON MONDAY" in lines[i+2]:
        print(f"Fixing Finding on Monday at line {i+1}")
        lines[i+4] = "1. **Kathisma:** *“Blessed is the man”* (according to the rule – 1st antiphon)."
        lines[i+6] = lines[i+6].replace("4. **On", "2. **On")
        lines[i+8] = lines[i+8].replace("5. **Entrance:**", "3. **Entrance:**")
        lines[i+10] = lines[i+10].replace("6. **Aposticha:**", "4. **Aposticha:**")
        lines[i+12] = "5. **Troparia:** " + lines[i+12].replace("7. After", "After")
        lines[i+14] = lines[i+14].replace("8. Litany", "6. Litany")
        break

md_path.write_text('\n'.join(lines), encoding='utf-8')
print("Successfully wrote updated Final MD/Final_Dolnytsky_part3_menaion.md!")
