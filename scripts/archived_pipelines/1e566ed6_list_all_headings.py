import os
import re

def main():
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
    
    output_report = os.path.join(typikon_dir, "all_headings_debug.txt")
    lines_out = []
    
    for filename in files:
        path = os.path.join(typikon_dir, filename)
        if not os.path.exists(path):
            continue
            
        lines_out.append(f"\n========================================\nFILE: {filename}\n========================================")
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.splitlines() if hasattr(f, 'splitlines') else f.read().splitlines()
            
        for i, line in enumerate(lines):
            line_str = line.strip()
            # If it's a markdown heading
            if line_str.startswith('#'):
                lines_out.append(f"  Line {i+1:4d}: [MD] {line_str}")
            # If it looks like a heading (e.g. short, uppercase, or starts with numbers)
            elif len(line_str) > 0 and len(line_str) < 80:
                # Check if it is ALL CAPS
                is_all_caps = line_str.isupper() and any(c.isalpha() for c in line_str)
                # Check if it starts with section number
                starts_with_num = bool(re.match(r'^\d+\.\d+(\.\d+)?\b', line_str))
                
                if is_all_caps or starts_with_num:
                    lines_out.append(f"  Line {i+1:4d}: [POTENTIAL] {line_str}")
                    
    with open(output_report, 'w', encoding='utf-8') as f_out:
        f_out.write("\n".join(lines_out))
    print(f"Report written to: {output_report}")

if __name__ == "__main__":
    main()
