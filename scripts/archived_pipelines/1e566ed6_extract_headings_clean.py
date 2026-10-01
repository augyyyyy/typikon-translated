import os
import sys

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
files = [
    "Final_Dolnytsky_part1_structure.md",
    "Final_Dolnytsky_part2_general_rubrics.md",
    "Final_Dolnytsky_part3_menaion.md",
    "Final_Dolnytsky_part4_triodion.md",
    "Final_Dolnytsky_part5_temple.md"
]

output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\headings_report.txt"

with open(output_path, 'w', encoding='utf-8') as out_f:
    out_f.write("=== EXTRACTED HEADINGS REPORT ===\n")
    for fn in files:
        path = os.path.join(typikon_dir, fn)
        out_f.write(f"\n=================== FILE: {fn} ===================\n")
        if not os.path.exists(path):
            out_f.write(f"Error: {fn} not found.\n")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check for actual markdown headers of level 1, 2, 3
            if line.startswith("#") and not line.startswith("#####"):
                out_f.write(f"L{i+1}: {line}\n")
            elif line.isupper() and len(line) < 100 and not any(c in line for c in ['"', '[', ']', '(', ')', '*', '†', ':', '.', '-']):
                out_f.write(f"L{i+1}: [CAPS] {line}\n")
            elif any(month in line for month in ["SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST"]):
                if len(line) < 100 and not line.startswith("Note") and not line.startswith("Everything"):
                    out_f.write(f"L{i+1}: [MONTH-DATE] {line}\n")
                    
print("Report generated successfully.")
