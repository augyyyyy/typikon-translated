import re
import os

SCRATCH = r'e:\Google Antigravity\Projects\Translation\scratch'
RAW_PART5 = r'e:\Google Antigravity\Projects\Translation\RAW\RAW_PART5_TRANSLATION.txt'
EN_FOOTNOTES = r'e:\Google Antigravity\Projects\Translation\English Broken\footnotes.txt'

def compile_and_format_footnotes():
    print("Compiling footnotes 1-785...")
    
    footnotes = {}
    
    # 1. Parse footnotes 1-755 from the existing compiled file
    with open(EN_FOOTNOTES, 'r', encoding='utf-8') as f:
        en_text = f.read()
        
    pattern = re.compile(r'(?:^\^\[|^\s*\[|^¹)(\d+)?(?(1)\]|)(.*(?:\n(?!\^\[|\[|¹).*)*)', re.MULTILINE)
    for m in pattern.finditer(en_text):
        num = int(m.group(1)) if m.group(1) else 1
        text = m.group(2).strip()
        footnotes[num] = text
        
    # 2. Parse footnotes 756-785 from RAW_PART5
    with open(RAW_PART5, 'r', encoding='utf-8') as f:
        raw_text = f.read()
        
    pattern_raw = re.compile(r'^\[(\d+)\]\s+(.*(?:\n(?!\[\d+\]).*)*)', re.MULTILINE)
    for m in pattern_raw.finditer(raw_text):
        num = int(m.group(1))
        if num not in footnotes:
            footnotes[num] = m.group(2).strip()

    # Verify counts
    missing = set(range(1, 786)) - set(footnotes.keys())
    print(f"Loaded {len(footnotes)} unique footnotes.")
    if missing:
        print(f"WARNING: Still missing footnotes: {sorted(list(missing))}")
        
    # Prepare the compiled markdown file
    compiled_txt = []
    compiled_txt.append("# Translated Footnotes\n")
    for num in sorted(footnotes.keys()):
        # Replace internal newlines with spaces for single-line markdown footnotes if needed
        # MS Word handles multi-line markdown footnotes cleanly if indented, 
        # but flattening is safer for pure table-of-notes.
        text = footnotes[num].replace('\n', ' ').strip()
        # Some footnotes start with multiple spaces, remove them.
        text = re.sub(r'\s+', ' ', text)
        compiled_txt.append(f"[^{num}]: {text}")
        
    out_path = os.path.join(SCRATCH, "STITCHED_v3_footnotes.txt")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(compiled_txt))
        
    print(f"Saved compiled footnotes to: {out_path}")
    
    # 3. Update the 6 body files: Convert `^[N]` to `[^N]`
    files = [
        "STITCHED_v3_dolnytsky_part1_structure.txt",
        "STITCHED_v3_dolnytsky_part2_general_rubrics.txt",
        "STITCHED_v3_dolnytsky_part3_menaion.txt",
        "STITCHED_v3_dolnytsky_part4_triodion.txt",
        "STITCHED_v3_dolnytsky_part5_temple.txt",
        "STITCHED_v3_dolnytsky_appendix.txt"
    ]
    
    total_replaced = 0
    for fname in files:
        fpath = os.path.join(SCRATCH, fname)
        if not os.path.exists(fpath): continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content, count = re.subn(r'\^\[(\d+)\]', r'[^\1]', content)
        
        if count > 0:
            total_replaced += count
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            # Now append the footnotes that appear IN THIS FILE to the BOTTOM of the file
            # This makes the markdown renderer automatically populate them!
            file_footnotes = []
            for marker in set(re.findall(r'\[\^(\d+)\]', new_content)):
                num = int(marker)
                if num in footnotes:
                    text = re.sub(r'\s+', ' ', footnotes[num])
                    file_footnotes.append(f"[^{num}]: {text}")
                    
            if file_footnotes:
                file_footnotes.sort(key=lambda x: int(re.search(r'\^(\d+)', x).group(1)))
                with open(fpath, 'a', encoding='utf-8') as f:
                    f.write('\n\n' + '--'*20 + '\n')
                    f.write('\n'.join(file_footnotes))
                
        print(f"{fname}: Converted {count} markers and appended {len(file_footnotes)} definitions.")

    print(f"Total markers converted across all files: {total_replaced}")

if __name__ == '__main__':
    compile_and_format_footnotes()
