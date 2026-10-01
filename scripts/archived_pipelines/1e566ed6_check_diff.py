import os
import re

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

out_lines = []

for filename in files:
    backup_path = os.path.join(typikon_dir, "backup", filename)
    current_path = os.path.join(typikon_dir, filename)
    if not os.path.exists(backup_path) or not os.path.exists(current_path):
        continue
    
    with open(backup_path, 'r', encoding='utf-8') as f:
        backup_lines = f.readlines()
    with open(current_path, 'r', encoding='utf-8') as f:
        current_lines = f.readlines()
        
    backup_h_with_idx = [(i, line.strip()) for i, line in enumerate(backup_lines) if line.strip().startswith('#')]
    current_h_with_idx = [(i, line.strip()) for i, line in enumerate(current_lines) if line.strip().startswith('#')]
    
    diffs = []
    # Match headings by contents or by exact line-by-line index
    # Let's print headings that are present in current but not in backup, or modified.
    # To see modifications, let's just find lines where the exact line number from backup had a heading,
    # but the heading text changed in the current file.
    # Since alignment doesn't add/remove lines (or very few), we can check if the heading at backup line `i`
    # matches the heading at current line `i`.
    
    # Create a map of line number to heading text in backup
    backup_h_map = {i: line.strip() for i, line in enumerate(backup_lines) if line.strip().startswith('#')}
    current_h_map = {i: line.strip() for i, line in enumerate(current_lines) if line.strip().startswith('#')}
    
    for i, b_h in backup_h_map.items():
        if i in current_h_map:
            c_h = current_h_map[i]
            if b_h != c_h:
                diffs.append(f"Line {i+1}: BACKUP: '{b_h}'\n         CURRENT: '{c_h}'")
        else:
            diffs.append(f"Line {i+1}: BACKUP: '{b_h}'\n         CURRENT: (No heading at this line, current has: '{current_lines[i].strip() if i < len(current_lines) else 'EOF'}')")
            
    # Check if there are any new headings in current that were not in backup
    for i, c_h in current_h_map.items():
        if i not in backup_h_map:
            diffs.append(f"Line {i+1}: CURRENT NEW HEADING: '{c_h}'\n         BACKUP had: '{backup_lines[i].strip() if i < len(backup_lines) else 'EOF'}'")
            
    if diffs:
        out_lines.append(f"\n=== {filename} Headings Diff ===")
        out_lines.extend(diffs)

out_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\headings_diff.txt"
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))
print(f"Diff saved to {out_path}")
