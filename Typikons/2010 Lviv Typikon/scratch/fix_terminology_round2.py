#!/usr/bin/env python3
"""
Phase 1 Terminology Unification - Round 2
Catches lowercase variants missed in round 1.
"""
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')

final_dir = r'e:\Google Antigravity\Projects\Translation\Final'

def smart_replace(text, pattern, replacement, flags=0):
    """Replace with count tracking."""
    matches = list(re.finditer(pattern, text, flags))
    count = len(matches)
    if count:
        text = re.sub(pattern, replacement, text, flags=flags)
    return text, count

log = {}
total_changes = 0

for fname in sorted(os.listdir(final_dir)):
    if not fname.endswith('.txt'):
        continue
    fpath = os.path.join(final_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    file_changes = {}
    original = text

    # Irmos/Irmoi lowercase variants
    # Must do longer patterns first (irmologion before irmos)
    
    # irmologion -> Heirmologion (any case)
    def fix_irmologion(m):
        word = m.group(0)
        if word.isupper():
            return 'HEIRMOLOGION'
        elif word[0].isupper():
            return 'Heirmologion'
        else:
            return 'heirmologion'
    text, c = smart_replace(text, r'\birmologion\b', '', re.IGNORECASE)
    if c:
        # redo properly
        text = original  # reset
    
    # Actually let's just do targeted replacements
    text = original

    fixes = [
        # lowercase irmos -> heirmos (the big miss)
        (r'\birmologion\b', 'heirmologion', 'irmologion -> heirmologion'),
        (r'\bIrmologion\b', 'Heirmologion', 'Irmologion -> Heirmologion'),  
        (r'\birmoi\b', 'heirmoi', 'irmoi -> heirmoi'),
        (r'\birmos\b', 'heirmos', 'irmos -> heirmos'),
        
        # lowercase leavetaking
        (r'\bleavetaking\b', 'apodosis', 'leavetaking -> apodosis'),
        (r'\bleave-taking\b', 'apodosis', 'leave-taking -> apodosis'),
        
        # lowercase prokeimenon
        (r'\bprokeimenon\b', 'prokimenon', 'prokeimenon -> prokimenon'),
        (r'\bprokeimena\b', 'prokimena', 'prokeimena -> prokimena'),
    ]

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
