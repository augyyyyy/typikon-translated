import os
import sys

# Set stream encoding for Windows console compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
files = [
    "Final_Dolnytsky_part1_structure.md",
    "Final_Dolnytsky_part2_general_rubrics.md",
    "Final_Dolnytsky_part3_menaion.md",
    "Final_Dolnytsky_part4_triodion.md",
    "Final_Dolnytsky_part5_temple.md",
    "Final_Dolnytsky_appendix.md"
]

print("--- EXTRACTING HEADINGS ---")
for fn in files:
    path = os.path.join(typikon_dir, fn)
    print(f"\n===== FILE: {fn} =====")
    if not os.path.exists(path):
        print(f"Error: {fn} not found.")
        continue
        
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        # Check for markdown headers
        if line.startswith("#"):
            print(f"Line {i+1}: {line}")
        # Check for capitalized lines that might be headings (if short)
        elif line.isupper() and len(line) < 120 and not any(c in line for c in ['"', '[', ']', '(', ')', '*', '†']):
            print(f"Line {i+1}: [CAPS] {line}")
        # Check for specific patterns
        elif any(month in line for month in ["SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST"]):
            if len(line) < 100 and not line.startswith("Note") and not line.startswith("Everything"):
                print(f"Line {i+1}: [MONTH-DATE] {line}")
