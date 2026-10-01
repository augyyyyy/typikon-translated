import os
import re

def clean_paragraph(text):
    # Keep only alphanumeric chars
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text)
    return cleaned.lower()

def verify_paragraphs(orig_path, form_path, out_file):
    if not os.path.exists(orig_path):
        out_file.write(f"SKIP: Original file not found: {orig_path}\n")
        return
    if not os.path.exists(form_path):
        out_file.write(f"SKIP: Formatted file not found: {form_path}\n")
        return
        
    with open(orig_path, 'r', encoding='utf-8') as f:
        orig_content = f.read()
    with open(form_path, 'r', encoding='utf-8') as f:
        form_content = f.read()
        
    orig_paragraphs = [p.strip() for p in re.split(r'\n\s*\n', orig_content) if p.strip()]
    form_clean_all = clean_paragraph(form_content)
    
    missing_count = 0
    
    out_file.write(f"\n========================================\nFile: {os.path.basename(orig_path)}\n========================================")
    for i, p in enumerate(orig_paragraphs):
        if p.startswith('#') or len(p) < 15:
            continue
        if len(p) < 300 and ("Saint without Polyeleos on Sunday" in p or "Vesting of Sacred Robes" in p):
            continue
            
        p_clean = clean_paragraph(p)
        if p_clean not in form_clean_all:
            # Check which sentences/clauses are missing
            sentences = [s.strip() for s in re.split(r'[.!?]', p) if len(s.strip()) > 15]
            missing_sentences = []
            for s in sentences:
                s_clean = clean_paragraph(s)
                if s_clean not in form_clean_all:
                    missing_sentences.append(s)
            
            if missing_sentences:
                missing_count += 1
                out_file.write(f"\nMissing in Paragraph {i+1} (length {len(p)}):\n")
                out_file.write(f"  Snippet: {p[:150]}...\n")
                out_file.write("  Missing parts:\n")
                for ms in missing_sentences:
                    out_file.write(f"    - {ms}\n")

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
    
    out_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\detailed_diff_output.txt"
    with open(out_path, 'w', encoding='utf-8') as out_file:
        for filename in files:
            orig_path = os.path.join(typikon_dir, "backup", filename)
            form_path = os.path.join(typikon_dir, filename)
            verify_paragraphs(orig_path, form_path, out_file)
    print("Done writing detailed diff.")
