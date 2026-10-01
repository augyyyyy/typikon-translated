import os
import re

def clean_paragraph(text):
    # Keep only alphanumeric chars
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text)
    return cleaned.lower()

def verify_paragraphs(orig_path, form_path):
    with open(orig_path, 'r', encoding='utf-8') as f:
        orig_content = f.read()
    with open(form_path, 'r', encoding='utf-8') as f:
        form_content = f.read()
        
    # Split by double newlines or lines to get paragraphs
    orig_paragraphs = [p.strip() for p in re.split(r'\n\s*\n', orig_content) if p.strip()]
    
    # We clean the entire formatted content to search in it
    form_clean_all = clean_paragraph(form_content)
    
    missing_count = 0
    for i, p in enumerate(orig_paragraphs):
        # Skip headings and page numbers
        if p.startswith('#') or len(p) < 10:
            continue
        # Also skip table of contents blocks
        if "Saint without Polyeleos on Sunday" in p and len(p) < 300:
            continue
            
        p_clean = clean_paragraph(p)
        if p_clean not in form_clean_all:
            # Let's check if there is a partial mismatch or split paragraphs
            # We split the paragraph into sentences and check
            sentences = [s.strip() for s in re.split(r'[.!?]', p) if len(s.strip()) > 15]
            sentence_missing = False
            for s in sentences:
                s_clean = clean_paragraph(s)
                if s_clean not in form_clean_all:
                    sentence_missing = True
                    print(f"MISSING SENTENCE in paragraph {i+1}: {s}")
            if sentence_missing:
                missing_count += 1
                print(f"MISSING PARAGRAPH {i+1} (length {len(p)}):\n{p}\n")
                
    if missing_count == 0:
        print(f"SUCCESS: All text paragraphs from {os.path.basename(orig_path)} are present in the formatted file.")
    else:
        print(f"FAILED: {missing_count} missing paragraph(s) in formatted file.")

if __name__ == "__main__":
    typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
    verify_paragraphs(
        os.path.join(typikon_dir, "backup", "Final_Dolnytsky_part2_general_rubrics.md"),
        os.path.join(typikon_dir, "Final_Dolnytsky_part2_general_rubrics.md")
    )
