import os
import sys
import re

base_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded"
dolnytsky_path = os.path.join(base_dir, 'Data', 'Service Books', 'Typikon', 'Dolnytsky_Typikon_Master.md')
ordo_path = os.path.join(base_dir, 'Data', 'Service Books', 'Typikon', 'Ordo', 'Ordo_Celebrationis_1996_CLEAN.md')
out_path = r"C:\Users\augus\.gemini\antigravity\brain\e5ff2e9a-16b3-401d-bdc1-57dd450d6e62\scratch\scour_results.txt"

p1 = re.compile(r'\b(monast\w*|parish\w*|monk\w*|secular\w*|cloisters?|lavra|skete|parochi\w*)\b', re.I)
p2 = re.compile(r'(in parish churches|in monasteries|monastic practice|parish practice|parish usage|monastic usage|ancient custom|ancient rule|according to our custom|with us today|which today we usually do not take|local custom)', re.I)

out_lines = []

def analyze(name, path):
    out_lines.append(f"==================================================")
    out_lines.append(f"       ANALYZING: {name}")
    out_lines.append(f"==================================================")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    paras = content.split('\n\n')
    matches = []
    for idx, p in enumerate(paras):
        p_str = p.strip()
        if not p_str:
            continue
        m1 = p1.search(p_str)
        m2 = p2.search(p_str)
        if m1 or m2:
            matches.append({
                'idx': idx,
                'matched_terms': list(set([m.group(0) for m in [m1, m2] if m])),
                'text': p_str
            })

    out_lines.append(f"Found {len(matches)} matching paragraphs.")
    for i, m in enumerate(matches):
        out_lines.append(f"\n--- Match {i+1} [Terms: {', '.join(m['matched_terms'])}] ---")
        out_lines.append(m['text'])

analyze("Dolnytsky Typikon Master", dolnytsky_path)
analyze("Ordo Celebrationis 1996", ordo_path)

with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print(f"Wrote {len(out_lines)} lines to {out_path}")
