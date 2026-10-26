import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

cmd = Path('scratch/step_180_cmd.txt').read_text(encoding='utf-8')
# Find SOURCE_TEXT = '''...'''
m = re.search(r"SOURCE_TEXT = '''(.*?)'''\s*Path\(", cmd, re.DOTALL)
if not m:
    print('SOURCE_TEXT match not found')
    # Try finding between === LEAF p441 === and === LEAF p450 ===
    m2 = re.search(r"(=== LEAF p441 ===.*?)\'\s*Path\(", cmd, re.DOTALL)
    if m2:
        print('Found via fallback pattern')
        source_text = m2.group(1)
    else:
        print('Fallback also failed')
        sys.exit(1)
else:
    source_text = m.group(1)

print(f'Length of extracted source text: {len(source_text)}')
leaves = re.split(r"(=== LEAF p\d{3} ===)", source_text)
print(f'Number of splits: {len(leaves)}')
for i in range(1, len(leaves), 2):
    leaf_hdr = leaves[i]
    leaf_body = leaves[i+1] if i+1 < len(leaves) else ''
    print(f'\n{leaf_hdr} (body length {len(leaf_body)}):')
    print(leaf_body[:250].strip())
