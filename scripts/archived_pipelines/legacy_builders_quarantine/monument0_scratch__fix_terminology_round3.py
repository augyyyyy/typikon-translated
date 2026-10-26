#!/usr/bin/env python3
"""
Phase 1 Terminology Unification - Round 3
Fixes the remaining 4 drift groups based on research + user decision.

1. Church Eye / Tserkovne Oko -> Eye of the Church (academic standard)
2. Pochayiv -> Pochaiv (official Ukrainian transliteration)
3. Trephologion -> Anthologion (same book, Greek standard)
4. Krylos/Kryloi -> Kliros/Kliroi (user choice)
"""
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')

final_dir = r'e:\Google Antigravity\Projects\Translation\Final'

fixes = [
    # 1. Church Eye -> Eye of the Church
    (r'\bChurch Eye\b', 'Eye of the Church', 'Church Eye -> Eye of the Church'),
    (r'\bCHURCH EYE\b', 'EYE OF THE CHURCH', 'CHURCH EYE -> EYE OF THE CHURCH'),
    
    # Tserkovne Oko -> Eye of the Church
    (r'\bTserkovne Oko\b', 'Eye of the Church', 'Tserkovne Oko -> Eye of the Church'),
    (r'\bTSERKOVNE OKO\b', 'EYE OF THE CHURCH', 'TSERKOVNE OKO -> EYE OF THE CHURCH'),
    
    # 2. Pochayiv -> Pochaiv (official standard)
    (r'\bPochayiv\b', 'Pochaiv', 'Pochayiv -> Pochaiv'),
    (r'\bPOCHAYIV\b', 'POCHAIV', 'POCHAYIV -> POCHAIV'),
    
    # 3. Trephologion -> Anthologion (same book)
    (r'\bTrephologion\b', 'Anthologion', 'Trephologion -> Anthologion'),
    (r'\bTREPHOLOGION\b', 'ANTHOLOGION', 'TREPHOLOGION -> ANTHOLOGION'),
    (r'\btrephologion\b', 'anthologion', 'trephologion -> anthologion'),
    
    # 4. Krylos -> Kliros, Kryloi -> Kliroi (user choice)
    (r'\bKrylos\b', 'Kliros', 'Krylos -> Kliros'),
    (r'\bkrylos\b', 'kliros', 'krylos -> kliros'),
    (r'\bKryloi\b', 'Kliroi', 'Kryloi -> Kliroi'),
    (r'\bkryloi\b', 'kliroi', 'kryloi -> kliroi'),
    (r'\bKRYLOS\b', 'KLIROS', 'KRYLOS -> KLIROS'),
]

log = {}
total_changes = 0

for fname in sorted(os.listdir(final_dir)):
    if not fname.endswith('.txt'):
        continue
    fpath = os.path.join(final_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    file_changes = {}
    for pattern, replacement, desc in fixes:
        matches = list(re.finditer(pattern, text))
        if matches:
            count = len(matches)
            text = re.sub(pattern, replacement, text)
            file_changes[desc] = count
            total_changes += count

    if file_changes:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(text)
        log[fname] = file_changes
        print(f'\n=== {fname} ===')
        for desc, count in file_changes.items():
            print(f'  {desc}: {count}')

print(f'\n\nTOTAL CHANGES: {total_changes}')

# Save log
log_path = os.path.join(r'e:\Google Antigravity\Projects\Translation\scratch\reports', 'terminology_fix_round3.json')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(log, f, indent=2, ensure_ascii=False)
print(f'Log saved to: {log_path}')
