import os
import sys
import re
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

raw_text = Path("scratch/cohort99_source_raw.txt").read_text(encoding='utf-8')

# Fix known OCR typos in raw text
text = raw_text
text = text.replace('Luﬂ', 'Lüft')
text = text.replace('Мансвегпов', 'Мансветов')
text = text.replace('obserwat.', 'observat.')
text = text.replace('11, 119.', 'II, 119.')
text = text.replace('ΰμνωι', 'ὕμνοι')
text = text.replace('(Сип.)', '(Син.)')
text = text.replace('Τυπικών ркп.', 'Τυπικόν ркп.')

parts = text.split("=== LEAF ")
clean_blocks = []

for part in parts[1:]:
    lines = part.strip().splitlines()
    leaf_id = lines[0].strip().split()[0]
    raw_lines = lines[1:]
    
    paras = []
    curr_para = []
    
    for l in raw_lines:
        line_s = l.strip()
        if not line_s:
            continue
        
        is_new_note = False
        m = re.match(r'^(\d{3})\.\s*(.*)', line_s)
        if m:
            num = int(m.group(1))
            if 268 <= num <= 457:
                is_new_note = True
        
        if is_new_note:
            if curr_para:
                paras.append(" ".join(curr_para))
                curr_para = []
            curr_para.append(line_s)
        else:
            if not curr_para:
                curr_para.append(line_s)
            else:
                if curr_para[-1].endswith('-') or curr_para[-1].endswith('—'):
                    if curr_para[-1].endswith('-'):
                        curr_para[-1] = curr_para[-1][:-1] + line_s
                    else:
                        curr_para[-1] = curr_para[-1] + " " + line_s
                else:
                    curr_para.append(line_s)
                    
    if curr_para:
        paras.append(" ".join(curr_para))
        
    leaf_text = f"=== LEAF {leaf_id} ===\n" + "\n".join(paras)
    clean_blocks.append(leaf_text)

source_content = "\n\n".join(clean_blocks) + "\n"

target_file = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/1910_skaballanovich_typikon_cohort99_source.txt")
target_file.parent.mkdir(parents=True, exist_ok=True)
target_file.write_text(source_content, encoding='utf-8')

print(f"Written source file: {target_file}, size: {len(source_content)} chars")
