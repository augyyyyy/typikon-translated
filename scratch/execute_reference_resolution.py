import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Load the verified concordance
with open('scratch/reports/page_concordance_master.json', 'r', encoding='utf-8') as f:
    concordance = json.load(f)

# Ensure the 4 overrides are present
concordance['p468'] = {
    'target_file': 'Final_Dolnytsky_part5_temple.md',
    'heading': 'Temple Of A Saint On One Of The Lenten Days',
    'slug': 'temple-of-a-saint-on-one-of-the-lenten-days'
}
concordance['p204'] = {
    'target_file': 'Final_Dolnytsky_part3_menaion.md',
    'heading': '3.5.9 January: Apodosis of Theophany',
    'slug': '359-january-apodosis-of-theophany'
}

ref_pattern = re.compile(r'(\b(?:pp?\.?\s*\d+(?:-\d+)?))\s*\[[→\->]?REF:([^\]]+)\]')

def resolve_for_md(match, current_filename):
    page_str = match.group(1)
    ref_key = match.group(2)
    
    target = concordance.get(ref_key)
    if not target:
        ref_k2 = f"p{ref_key}" if not ref_key.startswith('p') else ref_key[1:]
        target = concordance.get(ref_k2)
    
    if not target or target.get('target_file') == 'EXTERNAL':
        return page_str
    
    tf = target['target_file']
    slug = target['slug']
    if tf == current_filename:
        return f"[{page_str}](#{slug})"
    else:
        return f"[{page_str}]({tf}#{slug})"

# 1. Update Final MD files
print("Applying resolutions to Final MD/...")
total_md_subs = 0
for md_path in sorted(Path('Final MD').glob('*.md')):
    content = md_path.read_text(encoding='utf-8')
    new_content, count = ref_pattern.subn(lambda m: resolve_for_md(m, md_path.name), content)
    if count > 0:
        md_path.write_text(new_content, encoding='utf-8')
        print(f"  {md_path.name}: replaced {count} references")
        total_md_subs += count

print(f"Total Final MD replacements: {total_md_subs}")

# 2. Update Final TXT files (strip [→REF:...], retain plain page numbers)
print("\nApplying resolutions to Final/...")
total_txt_subs = 0
for txt_path in sorted(Path('Final').glob('*.txt')):
    content = txt_path.read_text(encoding='utf-8')
    new_content, count = ref_pattern.subn(r'\1', content)
    if count > 0:
        txt_path.write_text(new_content, encoding='utf-8')
        print(f"  {txt_path.name}: replaced {count} references")
        total_txt_subs += count

print(f"Total Final TXT replacements: {total_txt_subs}")
