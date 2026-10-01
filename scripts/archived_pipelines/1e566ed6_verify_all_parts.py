import os
import re

def clean_text(text):
    # Strip markdown formatting, symbols, numbers (to ignore TOC additions), and spaces
    # We want to make sure the core textual words are identical.
    cleaned = re.sub(r'[^a-zA-Z]', '', text)
    return cleaned.lower()

def verify_file(orig_path, form_path):
    if not os.path.exists(orig_path):
        return f"SKIP: Original file not found: {orig_path}"
    if not os.path.exists(form_path):
        return f"SKIP: Formatted file not found: {form_path}"
        
    with open(orig_path, 'r', encoding='utf-8') as f:
        orig = f.read()
    with open(form_path, 'r', encoding='utf-8') as f:
        form = f.read()
        
    orig_clean = clean_text(orig)
    form_clean = clean_text(form)
    
    if orig_clean == form_clean:
        return f"SUCCESS: {os.path.basename(orig_path)} matches perfectly! (clean length: {len(orig_clean)})"
    else:
        # Find first mismatch
        min_len = min(len(orig_clean), len(form_clean))
        mismatch_idx = -1
        for i in range(min_len):
            if orig_clean[i] != form_clean[i]:
                mismatch_idx = i
                break
        if mismatch_idx == -1:
            mismatch_idx = min_len
            
        sample_orig = orig_clean[max(0, mismatch_idx-30):mismatch_idx+50]
        sample_form = form_clean[max(0, mismatch_idx-30):mismatch_idx+50]
        return (f"FAIL: {os.path.basename(orig_path)} has mismatch at index {mismatch_idx}!\n"
                f"Original: ...{sample_orig}...\n"
                f"Formatted: ...{sample_form}...")

if __name__ == "__main__":
    typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
    files = [
        "Final_Dolnytsky_part1_structure.md",
        "Final_Dolnytsky_part2_general_rubrics.md",
        "Final_Dolnytsky_part3_menaion.md",
        "Final_Dolnytsky_part4_triodion.md",
        "Final_Dolnytsky_part5_temple.md",
        "Final_Dolnytsky_appendix.md"
    ]
    
    for filename in files:
        orig_path = os.path.join(typikon_dir, "backup", filename)
        form_path = os.path.join(typikon_dir, filename)
        print(verify_file(orig_path, form_path))
