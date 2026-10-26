import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

raw_pdf_text = Path('Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort24_extracted_pdf_text.txt').read_text(encoding='utf-8')
leaves_raw = re.split(r'=== LEAF (p\d+) ===', raw_pdf_text)

headings = [
    'Богослужение Четыредесятницы',
    'Оглашение в Четыредесятницу',
    'Покаяние и причащение в Четыредесятницу',
    'Законы о Четыредесятнице',
    'Предпоследняя неделя Четыредесятницы',
    'Страстная неделя',
    'Суббота Лазарева',
    'Вербное воскресенье',
    'Первые дни страстной седмицы',
    'Великий четверг'
]

source_leaves = {}

for i in range(1, len(leaves_raw), 2):
    lid = leaves_raw[i]
    content = leaves_raw[i+1].strip()
    
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
        
        # Check if line is one of the headings
        if l in headings:
            if curr_para:
                cleaned_paras.append(' '.join(curr_para))
                curr_para = []
            cleaned_paras.append(f'### {l}')
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
    
    source_leaves[lid] = leaf_text

output_lines = []
for lid in [f'p{p}' for p in range(231, 241)]:
    output_lines.append(f'=== LEAF {lid} ===')
    output_lines.append(source_leaves[lid])
    output_lines.append('')

final_source = '\n'.join(output_lines).strip() + '\n'

out_path = Path('Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/1910_skaballanovich_typikon_cohort24_source.txt')
out_path.write_text(final_source, encoding='utf-8')
print(f"Wrote {out_path}, size = {out_path.stat().st_size} bytes")
