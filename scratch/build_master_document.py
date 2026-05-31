import os

final_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\Final"
output_file = os.path.join(final_dir, "Dolnytsky_Typikon_Master.md")

file_order = [
    "Final_Dolnytsky_intro.txt",
    "Final_Dolnytsky_part1_structure.txt",
    "Final_Dolnytsky_part2_general_rubrics.txt",
    "Final_Dolnytsky_part3_menaion.txt",
    "Final_Dolnytsky_part4_triodion.txt",
    "Final_Dolnytsky_part5_temple.txt",
    "Final_Dolnytsky_appendix.txt",
    "Final_Dolnytsky_glossary.md",
    "Final_footnotes.txt"
]

print("Compiling Master Document...")
with open(output_file, 'w', encoding='utf-8') as out_f:
    out_f.write("# The Typikon of the Ruthenian Catholic Church\n")
    out_f.write("## 1899 Edition (Rev. Isydor Dolnytsky)\n")
    out_f.write("\n*Translated into Formal Liturgical English*\n\n")
    out_f.write("---\n\n")

    for filename in file_order:
        filepath = os.path.join(final_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found.")
            continue
            
        print(f"Reading {filename}...")
        with open(filepath, 'r', encoding='utf-8') as in_f:
            content = in_f.read()
            
        # Add a title if it's not already in the file (just for structure)
        if "intro" in filename:
            out_f.write("\n\n# Introduction\n\n")
        elif "part1" in filename:
            out_f.write("\n\n# Part I: Structure of Services\n\n")
        elif "part2" in filename:
            out_f.write("\n\n# Part II: General Rubrics\n\n")
        elif "part3" in filename:
            out_f.write("\n\n# Part III: The Menaion\n\n")
        elif "part4" in filename:
            out_f.write("\n\n# Part IV: The Triodion\n\n")
        elif "part5" in filename:
            out_f.write("\n\n# Part V: The Temple and Calendar\n\n")
        elif "appendix.txt" in filename:
            out_f.write("\n\n# Appendix\n\n")
        elif "footnotes" in filename:
            out_f.write("\n\n# Footnotes\n\n")
            
        out_f.write(content)
        out_f.write("\n\n<div style=\"page-break-after: always;\"></div>\n\n")

print(f"Master document created successfully at: {output_file}")
