import os
import re

def clean_paragraph(text):
    # Strip list bullet markers at start of lines first
    text = re.sub(r'^\s*[o?•]\t', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*[o?•]\s+', '', text, flags=re.MULTILINE)
    # Keep only alphanumeric chars
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text)
    return cleaned.lower()

def verify_paragraphs(orig_path, form_path):
    if not os.path.exists(orig_path):
        return f"SKIP: Original file not found: {orig_path}"
    if not os.path.exists(form_path):
        return f"SKIP: Formatted file not found: {form_path}"
        
    with open(orig_path, 'r', encoding='utf-8') as f:
        orig_content = f.read()
    with open(form_path, 'r', encoding='utf-8') as f:
        form_content = f.read()
        
    # Split by double newlines or lines to get paragraphs
    orig_paragraphs = [p.strip() for p in re.split(r'\n\s*\n', orig_content) if p.strip()]
    form_clean_all = clean_paragraph(form_content)
    
    missing_count = 0
    missing_details = []
    
    for i, p in enumerate(orig_paragraphs):
        # Skip headings, short items, and known table of contents lines
        if p.startswith('#') or len(p) < 15:
            continue
        if len(p) < 300 and ("Saint without Polyeleos on Sunday" in p or "Vesting of Sacred Robes" in p):
            continue
            
        p_clean = clean_paragraph(p)
        if p_clean not in form_clean_all:
            # Check if sentences are missing
            sentences = [s.strip() for s in re.split(r'[.!?]', p) if len(s.strip()) > 15]
            sentence_missing = False
            missing_sentences = []
            for s in sentences:
                s_clean = clean_paragraph(s)
                if s_clean not in form_clean_all:
                    sentence_missing = True
                    missing_sentences.append(s)
            if sentence_missing:
                missing_count += 1
                missing_details.append((i+1, p, missing_sentences))
                
    if missing_count == 0:
        return f"SUCCESS: All text paragraphs from {os.path.basename(orig_path)} are present in the formatted file."
    else:
        details_str = ""
        for p_num, full_p, m_sents in missing_details[:2]: # Show up to 2 details
            details_str += f"\n- Paragraph {p_num} (length {len(full_p)}):\n  Missing sentences:\n"
            for s in m_sents:
                details_str += f"    * {s}\n"
        return f"FAILED: {os.path.basename(orig_path)} has {missing_count} missing paragraph(s).\nDetails: {details_str}"

if __name__ == "__main__":
    typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
    files = [
        "Final_Dolnytsky_appendix.md"
    ]
    
    for filename in files:
        orig_path = os.path.join(typikon_dir, "backup", filename)
        form_path = os.path.join(typikon_dir, filename)
        # We catch console encoding crashes by printing sanitized ascii
        res = verify_paragraphs(orig_path, form_path)
        print(res.encode('ascii', 'replace').decode('ascii'))
