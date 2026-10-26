import sys
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

fmd = Path('Liturgical Monuments/Monument 1 - 1891 Lviv Synod/Final MD')

def search_text(cohort_name, keywords):
    p = fmd / cohort_name
    if not p.exists():
        print(f"File {cohort_name} not found")
        return
    txt = p.read_text(encoding='utf-8', errors='ignore')
    print(f'=== {cohort_name} ===')
    for kw in keywords:
        matches = [m.start() for m in re.finditer(re.escape(kw), txt, re.IGNORECASE)]
        print(f'Keyword "{kw}": {len(matches)} matches')
        for idx in matches[:3]:
            start = max(0, idx - 120)
            end = min(len(txt), idx + 120)
            print(f'  ...{txt[start:end].replace(chr(10), " ")}...')

search_text('1891_synod_cohort1.md', ['Chrysostom', 'Acts', 'Homily XXI', 'departed', 'Panakhyda', 'Parastas'])
search_text('1891_synod_cohort6.md', ['Apostolic', 'Canon', 'excommunicate', 'heretic', 'Zamość'])
search_text('1891_synod_cohort12.md', ['Damascus', 'De Fide', 'Orthodoxa', 'Matthew', '28:20', 'commanded'])
search_text('1891_synod_cohort14.md', ['Sirach', 'Ecclesiasticus', 'Timothy', '3:5', '2:4', 'warreth', 'house'])
