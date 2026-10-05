import os

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
output_file = os.path.join(typikon_dir, "Dolnytsky_Typikon_Master.md")

file_order = [
    "Final_Dolnytsky_intro.md",
    "Final_Dolnytsky_part1_structure.md",
    "Final_Dolnytsky_part2_general_rubrics.md",
    "Final_Dolnytsky_part3_menaion.md",
    "Final_Dolnytsky_part4_triodion.md",
    "Final_Dolnytsky_part5_temple.md",
    "Final_Dolnytsky_appendix.md",
    "Final_Dolnytsky_glossary.md",
    "Final_footnotes.md"
]

print("Compiling Master Document...")
with open(output_file, 'w', encoding='utf-8', newline='') as out_f:
    out_f.write("# The Typikon of the Ruthenian Catholic Church\n")
    out_f.write("## 1899 Edition (Rev. Isydor Dolnytsky)\n")
    out_f.write("\n*Translated into Formal Liturgical English*\n\n")
    out_f.write("---\n\n")

    for filename in file_order:
        filepath = os.path.join(typikon_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found.")
            continue
            
        print(f"Reading {filename}...")
        with open(filepath, 'r', encoding='utf-8') as in_f:
            content = in_f.read()
            
        # We do not inject redundant level 1 headers since the source files 
        # now start with their own clean level 1 headers (e.g. # PART I: ...).
        # We only prepend # Introduction for the intro file if desired.
        if "intro" in filename:
            out_f.write("\n\n# Introduction\n\n")
            
        out_f.write(content)
        out_f.write("\n\n<div style=\"page-break-after: always;\"></div>\n\n")

print(f"Master document created successfully at: {output_file}")
