import os
import re

SCRATCH = r'e:\Google Antigravity\Projects\Translation\scratch'
FINAL_DIR = r'e:\Google Antigravity\Projects\Translation\Final'
os.makedirs(FINAL_DIR, exist_ok=True)

FILES = [
    "STITCHED_v3_dolnytsky_part1_structure.txt",
    "STITCHED_v3_dolnytsky_part2_general_rubrics.txt",
    "STITCHED_v3_dolnytsky_part3_menaion.txt",
    "STITCHED_v3_dolnytsky_part4_triodion.txt",
    "STITCHED_v3_dolnytsky_part5_temple.txt",
    "STITCHED_v3_dolnytsky_appendix.txt",
    "STITCHED_v3_footnotes.txt"
]

def clean_file(text):
    # 1. Normalize quotes to straight quotes
    # (MS Word can auto-format to smart quotes upon import)
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('‘', "'").replace('’', "'")
    
    # 2. Normalize em-dashes and hyphens based on convention
    text = text.replace('—', ' -- ').replace('–', ' -- ')
    text = re.sub(r'\s*--\s*', ' -- ', text)
    
    # 3. Clean up excessive spacing
    text = re.sub(r' +', ' ', text)
    
    # 4. Clean up trailing spaces on lines
    text = '\n'.join([line.rstrip() for line in text.split('\n')])
    
    return text

def main():
    print("="*60)
    print("PHASE 3: FINAL POLISH")
    print("="*60)
    
    for fname in FILES:
        in_path = os.path.join(SCRATCH, fname)
        if not os.path.exists(in_path):
            continue
            
        with open(in_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        clean_text = clean_file(text)
        
        # Determine the final output name
        # E.g. "STITCHED_v3_dolnytsky_part1_structure.txt" -> "Final_Dolnytsky_Part1_Structure.txt"
        base_name = fname.replace("STITCHED_v3_dolnytsky_", "Final_Dolnytsky_")
        base_name = base_name.replace("STITCHED_v3_", "Final_")
        
        out_path = os.path.join(FINAL_DIR, base_name)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(clean_text)
            
        print(f"Processed and moved to final: {base_name}")

if __name__ == '__main__':
    main()
