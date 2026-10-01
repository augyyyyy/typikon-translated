import os
import re

def clean_body_text(text):
    # Strip first 4 lines
    lines = text.split('\n')[4:]
    
    # Strip lines starting with #
    body_lines = [line for line in lines if not line.strip().startswith('#')]
    body_text = '\n'.join(body_lines)
    
    # Strip list bullet markers at start of lines
    body_text = re.sub(r'^\s*[o?•]\t', '', body_text, flags=re.MULTILINE)
    body_text = re.sub(r'^\s*[o?•]\s+', '', body_text, flags=re.MULTILINE)
    
    # Keep only letters
    cleaned = re.sub(r'[^a-zA-Z]', '', body_text)
    return cleaned.lower()

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
orig_path = os.path.join(typikon_dir, "backup", "Final_Dolnytsky_part2_general_rubrics.md")
form_path = os.path.join(typikon_dir, "Final_Dolnytsky_part2_general_rubrics.md")

with open(orig_path, 'r', encoding='utf-8') as f:
    orig = f.read()
with open(form_path, 'r', encoding='utf-8') as f:
    form = f.read()

orig_clean = clean_body_text(orig)
form_clean = clean_body_text(form)

if orig_clean == form_clean:
    print("SUCCESS: Part 2 body text matches perfectly!")
else:
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
    print(f"FAIL: Mismatch in body text at clean index {mismatch_idx}!")
    print(f"Original: ...{sample_orig}...")
    print(f"Formatted: ...{sample_form}...")
