import sys
import json
from pathlib import Path

# Force UTF-8
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

p = Path('../Typikon Coded/json_db/synodal_footnotes.json')
if not p.exists():
    print(f"File not found: {p}")
    sys.exit(1)

data = json.loads(p.read_text(encoding='utf-8'))
print(f"Total footnotes in synodal_footnotes.json: {len(data)}")

targets = ["241", "242", "278", "360", "406", "502", "775", "784"]
for tid in targets:
    if tid in data:
        fn = data[tid]
        print(f"ID {tid}: typikon_part={fn.get('typikon_part')}, section={fn.get('section')}, text_en length={len(fn.get('text_en',''))}, anchors={fn.get('anchors')}")
