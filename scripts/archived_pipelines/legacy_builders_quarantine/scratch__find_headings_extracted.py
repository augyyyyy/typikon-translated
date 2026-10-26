import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

txt = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort20_extracted_pdf_text.txt").read_text(encoding='utf-8')

for leaf in txt.split('=== LEAF '):
    if not leaf.strip():
        continue
    header = leaf.split('\n')[0]
    lines = leaf.split('\n')
    print(f"=== {header} ===")
    for l in lines[1:]:
        l_s = l.strip()
        if 0 < len(l_s) < 60 and not l_s.startswith('[') and not l_s.startswith('{'):
            # check if it looks like a heading
            if any(w in l_s for w in ['строй', 'Устав', 'Правила', 'киновии', 'Пахоми']):
                print("   HEADING CANDIDATE:", l_s)
