#!/usr/bin/env python3
"""
Phase 1 Terminology Unification - Known Standards
Fixes the 4 drift groups where the intended standard is already known.
"""
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')

final_dir = r'e:\Google Antigravity\Projects\Translation\Final'

# Replacements: (pattern, replacement, description)
FIXES = [
    # 1. Leavetaking -> Apodosis
    (r'\bLeavetaking\b', 'Apodosis', 'Leavetaking -> Apodosis'),
    (r'\bLeave-taking\b', 'Apodosis', 'Leave-taking -> Apodosis'),
    (r'\bLeave taking\b', 'Apodosis', 'Leave taking -> Apodosis'),
    (r'\bLEAVETAKING\b', 'APODOSIS', 'LEAVETAKING -> APODOSIS'),

    # 2. Prokeimenon -> Prokimenon
    (r'\bProkeimenon\b', 'Prokimenon', 'Prokeimenon -> Prokimenon'),
    (r'\bProkeimena\b', 'Prokimena', 'Prokeimena -> Prokimena'),
    (r'\bPROKEIMENON\b', 'PROKIMENON', 'PROKEIMENON -> PROKIMENON'),

    # 3. Irmos -> Heirmos (but NOT inside Irmologion -> Heirmologion)
    # Do Irmologion first (longer match), then Irmos
    (r'\bIrmologion\b', 'Heirmologion', 'Irmologion -> Heirmologion'),
    (r'\bIRMOLOGION\b', 'HEIRMOLOGION', 'IRMOLOGION -> HEIRMOLOGION'),
    (r'\bIrmoi\b', 'Heirmoi', 'Irmoi -> Heirmoi'),
    (r'\bIrmos\b', 'Heirmos', 'Irmos -> Heirmos'),
    (r'\bIRMOS\b', 'HEIRMOS', 'IRMOS -> HEIRMOS'),

    # 4. Katavasiae -> Katavasia (the -ae Latin plural to Greek singular/collective)
    (r'\bKatavasiae\b', 'Katavasias', 'Katavasiae -> Katavasias'),
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
    for pattern, replacement, desc in FIXES:
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
log_path = os.path.join(r'e:\Google Antigravity\Projects\Translation\scratch\reports', 'terminology_fix_phase1.json')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(log, f, indent=2, ensure_ascii=False)
print(f'Log saved to: {log_path}')
