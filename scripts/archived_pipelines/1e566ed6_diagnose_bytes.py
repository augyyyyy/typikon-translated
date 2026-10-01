with open(r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\backup\Final_Dolnytsky_part1_structure.md", 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Matins text representation:")
for i in range(137, 144):
    print(f"Line {i}:", repr(lines[i]))

print("\nBullet points representation (Line 193):")
print(repr(lines[193]))
for c in lines[193]:
    print(c, hex(ord(c)))
