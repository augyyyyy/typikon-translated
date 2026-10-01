import os
import re

def clean_text(text):
    # Strip bullet markers, numbers, formatting syntax, and spaces
    text = re.sub(r'^\s*[-*o?•\d.#]+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-zA-Z0-9]', '', text)
    cleaned = text.lower()
    # Strip speaker tag words
    for speaker in ['priest', 'deacon', 'firstdeacon', 'seconddeacon', 'deacons', 'choir', 'reader', 'laity']:
        cleaned = cleaned.replace(speaker, '')
    return cleaned

def check_file(orig_path, form_path):
    if not os.path.exists(orig_path) or not os.path.exists(form_path):
        return
        
    with open(orig_path, 'r', encoding='utf-8') as f:
        orig = f.read()
    with open(form_path, 'r', encoding='utf-8') as f:
        form = f.read()
        
    # Remove markdown formatting characters from form for easier substring search
    form_clean = re.sub(r'[*_#`>]', '', form)
    form_clean_all = clean_text(form_clean)
    
    orig_paragraphs = [p.strip() for p in re.split(r'\n\s*\n', orig) if p.strip()]
    
    missing_sentences = []
    
    for i, p in enumerate(orig_paragraphs):
        # Skip top level headings
        if p.startswith('#') or len(p.strip()) < 10:
            continue
            
        # Split paragraph into sentences/clauses
        # Avoid splitting on abbreviations like St., e.g., i.e., etc., vs., vs
        # We split by periods followed by space, or newlines
        lines = p.split('\n')
        for line in lines:
            line = line.strip()
            # Remove bullet prefixes
            line_cleaned = re.sub(r'^\s*[-*o?•\d.#]+\s*', '', line)
            if len(line_cleaned) < 15:
                continue
            
            # Check sentence by sentence
            sentences = [s.strip() for s in re.split(r'(?<!St)(?<!e\.g)(?<!i\.e)(?<!etc)\.\s+', line_cleaned) if len(s.strip()) > 15]
            for s in sentences:
                s_clean = clean_text(s)
                if s_clean not in form_clean_all:
                    # Let's check if there is a close match by looking at a smaller substring
                    words = s.split()
                    if len(words) > 5:
                        sub = "".join(words[2:5])
                        sub_clean = clean_text(sub)
                        if sub_clean in form_clean_all:
                            # It's probably modified slightly, which counts as change/loss of wording
                            missing_sentences.append((i+1, s, "Modified/Rephrased"))
                        else:
                            missing_sentences.append((i+1, s, "Completely Missing"))
                    else:
                        missing_sentences.append((i+1, s, "Completely Missing"))
                        
    if missing_sentences:
        print(f"\n--- {os.path.basename(orig_path)}: {len(missing_sentences)} potential text mismatches ---")
        for p_num, s, status in missing_sentences[:10]: # Print first 10
            print(f"  [Para {p_num}] {status}:")
            print(f"    Original: {repr(s)}")
    else:
        print(f"--- {os.path.basename(orig_path)}: Perfect match! ---")

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
    for f in files:
        orig = os.path.join(typikon_dir, "backup", f)
        form = os.path.join(typikon_dir, f)
        check_file(orig, form)
