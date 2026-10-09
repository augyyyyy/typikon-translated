import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Read the extracted PDF text
raw_pdf_text = Path('Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort23_extracted_pdf_text.txt').read_text(encoding='utf-8')
leaves_raw = re.split(r'=== LEAF (p\d+) ===', raw_pdf_text)

# We will build clean leaf-by-leaf Russian source text
# Formatting:
# === LEAF p{N} ===
# Paragraphs separated by blank lines, unwrapping line breaks within paragraphs
# Preserving {с. N} markers and section headings

source_leaves = {}

for i in range(1, len(leaves_raw), 2):
    lid = leaves_raw[i]
    content = leaves_raw[i+1].strip()
    
    # Split into lines and reconstruct clean paragraphs
    lines = content.split('\n')
    cleaned_paras = []
    curr_para = []
    
    for line in lines:
        l = line.strip()
        if not l:
            if curr_para:
                cleaned_paras.append(' '.join(curr_para))
                curr_para = []
            continue
        
        # Check if line is a header like а) ..., в) ..., Воскресенье, Суббота, etc.
        if l in ['а)\xa0Неусыпающих и б)\xa0Студийский.', 'в)\xa0Спудеи Константинопольские', 
                 'Церковный год в IV–V вв.', 'Воскресенье', 'Суббота', 'Среда и пятница',
                 'Четыредесятница. Удлинение предпасхального поста', 'Образ пощения']:
            if curr_para:
                cleaned_paras.append(' '.join(curr_para))
                curr_para = []
            cleaned_paras.append(l)
            continue
            
        curr_para.append(l)
        
    if curr_para:
        cleaned_paras.append(' '.join(curr_para))
        
    # Reassemble text for this leaf
    leaf_text = '\n\n'.join(cleaned_paras)
    # Clean multiple spaces and non-breaking spaces
    leaf_text = re.sub(r'[ \t\xa0]+', ' ', leaf_text)
    # Normalize {с. N} formatting
    leaf_text = re.sub(r'\{с\.\s*(\d+)\}', r'{с. \1}', leaf_text)
    
    # Make sure section headers have ### in source where appropriate
    leaf_text = leaf_text.replace('в) Спудеи Константинопольские', '### в) Спудеи Константинопольские')
    leaf_text = leaf_text.replace('Церковный год в IV–V вв.', '### Церковный год в IV–V вв.')
    leaf_text = leaf_text.replace('Воскресенье', '### Воскресенье')
    leaf_text = leaf_text.replace('Суббота', '### Суббота')
    leaf_text = leaf_text.replace('Среда и пятница', '### Среда и пятница')
    leaf_text = leaf_text.replace('Четыредесятница. Удлинение предпасхального поста', '### Четыредесятница. Удлинение предпасхального поста')
    leaf_text = leaf_text.replace('Образ пощения', '### Образ пощения')
    
    source_leaves[lid] = leaf_text.strip()

out_path = Path('Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/1910_skaballanovich_typikon_cohort23_source.txt')

with open(out_path, 'w', encoding='utf-8') as f:
    for p in range(221, 231):
        lid = f'p{p}'
        f.write(f'=== LEAF {lid} ===\n')
        f.write(source_leaves[lid] + '\n\n')

print(f"Wrote {out_path}, size: {out_path.stat().st_size} bytes")
