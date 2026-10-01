import os
import shutil

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
files = [
    "Final_Dolnytsky_part1_structure.md",
    "Final_Dolnytsky_part2_general_rubrics.md",
    "Final_Dolnytsky_part3_menaion.md",
    "Final_Dolnytsky_part4_triodion.md",
    "Final_Dolnytsky_part5_temple.md",
    "Final_Dolnytsky_appendix.md",
    "Final_Dolnytsky_glossary.md"
]

for filename in files:
    backup_path = os.path.join(typikon_dir, "backup", filename)
    target_path = os.path.join(typikon_dir, filename)
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, target_path)
        print(f"Restored: {filename}")
