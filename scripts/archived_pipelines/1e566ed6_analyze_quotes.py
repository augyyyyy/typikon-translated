import os

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"

files = [
    "Final_Dolnytsky_part2_general_rubrics.md",
    "Final_Dolnytsky_part3_menaion.md",
    "Final_Dolnytsky_part4_triodion.md",
    "Final_Dolnytsky_part5_temple.md",
    "Final_Dolnytsky_appendix.md"
]

for filename in files:
    path = os.path.join(typikon_dir, filename)
    if not os.path.exists(path):
        continue
    print(f"\n=== SAMPLES FROM {filename} ===")
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    count = 0
    for i, line in enumerate(lines):
        if '"' in line:
            print(f"L{i+1}: {line.strip()[:150]}")
            count += 1
            if count >= 10:
                break
