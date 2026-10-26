import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

draft = Path('Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Draft/1888_violakis_typikon_cohort44_raw_draft.md').read_text(encoding='utf-8')
parts = draft.split('=== LEAF ')
for p in parts[1:3]:
    print('=== LEAF ' + p[:400] + '\n...\n')
