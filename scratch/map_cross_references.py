import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Load all 67 refs
with open('scratch/reports/ref_tokens_67.json', 'r', encoding='utf-8') as f:
    refs = json.load(f)

print(f"Total refs: {len(refs)}")
by_file = {}
for r in refs:
    by_file.setdefault(r['file'], []).append(r)

for fname, items in by_file.items():
    print(f"\n=== {fname} ({len(items)}) ===")
    for it in items:
        ref_str = it['ref']
        line_no = it['line']
        txt = it['line_text']
        print(f"  L{line_no:4d} [{ref_str:12s}]: {txt[:90]}")
