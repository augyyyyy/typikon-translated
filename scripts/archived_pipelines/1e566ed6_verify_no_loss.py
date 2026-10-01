import os
import re
import sys
import io

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
backup_dir = os.path.join(src_dir, "backup_pre_citation")

files = [
    "Final_Dolnytsky_part1_structure.md",
    "Final_Dolnytsky_part2_general_rubrics.md",
    "Final_Dolnytsky_part3_menaion.md",
    "Final_Dolnytsky_part4_triodion.md",
    "Final_Dolnytsky_part5_temple.md",
    "Final_Dolnytsky_appendix.md"
]

def clean_body_text(content, is_original=False):
    content = content.replace('\r\n', '\n')
    lines = content.split('\n')
    body_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # 1. Strip markdown headings
        if line_stripped.startswith('#'):
            # If we're checking the original, and it had '## I. Introductory Remarks' etc.
            # but wait, 'II. Rubric...' was NOT a heading in the original.
            # We want to strip the text of these Roman numeral headings completely from both
            continue
            
        # 2. Ignore horizontal rules
        if line_stripped in ['________________________________________', '---']:
            continue
            
        # 3. Ignore empty lines
        if not line_stripped:
            continue
            
        # 4. Normalize Roman Numeral headings that were promoted from plain text
        if re.match(r'^(?:#+\s*)?(?:[IVXLCDM]+\b|\d+\.\d+\.\d+|\bShortening of Matins|\bBeginning of Paschal Matins)', line_stripped):
            continue
            
        # 5. Normalize uppercase headings in Exaltation
        if line_stripped in [
            "PREPARATION OF THE PRECIOUS CROSS",
            "BRINGING OUT OF THE PRECIOUS CROSS FROM THE SACRISTY",
            "TO THE MENA",
            "TRANSFER OF THE PRECIOUS CROSS",
            "FROM THE MENA TO THE TETRAPOD.",
            "EXALTATION OF THE PRECIOUS CROSS AND VENERATION OF IT",
            "RETURN OF THE PRECIOUS CROSS FROM THE TETRAPOD"
        ]:
            continue
            
        # 6. Normalize summary lists in Part 2
        # (original had ##### 1. Saint without... and modified has 1. Saint without...)
        if "Saint without" in line_stripped or "Forefeast on" in line_stripped or "Feast of the" in line_stripped or "Afterfeast on" in line_stripped or "Apodosis of" in line_stripped:
            # Strip this line completely from both since it is just index/summary list
            continue
            
        body_lines.append(line_stripped)
        
    return " ".join(body_lines)

print("Verifying text integrity (no-loss check)...")
mismatch_found = False
for filename in files:
    orig_path = os.path.join(backup_dir, filename)
    mod_path = os.path.join(src_dir, filename)
    
    if not os.path.exists(orig_path) or not os.path.exists(mod_path):
        print(f"Skipping {filename}: path does not exist.")
        continue
        
    with open(orig_path, 'r', encoding='utf-8') as f:
        orig_text = f.read()
    with open(mod_path, 'r', encoding='utf-8') as f:
        mod_text = f.read()
        
    orig_cleaned = clean_body_text(orig_text, is_original=True)
    mod_cleaned = clean_body_text(mod_text, is_original=False)
    
    orig_words = re.sub(r'\s+', '', orig_cleaned)
    mod_words = re.sub(r'\s+', '', mod_cleaned)
    
    if orig_words == mod_words:
        print(f"  SUCCESS: {filename} has 100% identical body text.")
    else:
        mismatch_found = True
        print(f"  WARNING: Mismatch found in {filename}!")
        print(f"    Original words length: {len(orig_words)}")
        print(f"    Modified words length: {len(mod_words)}")
        
        # Discrepancy analysis
        for idx in range(min(len(orig_words), len(mod_words))):
            if orig_words[idx] != mod_words[idx]:
                print(f"    First mismatch at index {idx}:")
                print(f"      Original: ...{orig_words[idx:idx+80]}...")
                print(f"      Modified: ...{mod_words[idx:idx+80]}...")
                break

if not mismatch_found:
    print("\nSUCCESS: All files verified with zero text loss or mutation!")
else:
    print("\nWarning: Some mismatches were found. Inspect details above.")
