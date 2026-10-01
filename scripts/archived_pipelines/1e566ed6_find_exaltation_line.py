path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon\Final_Dolnytsky_part3_menaion.md"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "Universal Exaltation" in line or "14 September" in line:
        print(f"Line {idx+1}: {line.strip()}")
