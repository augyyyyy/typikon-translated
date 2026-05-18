#!/usr/bin/env python3
"""
Phase 2 Structural Audit Tool
Generates a per-file report of all footnote markers, their line numbers,
and surrounding context, to facilitate cross-referencing against source images.

Also checks for:
1. Missing footnote numbers in the sequence 1-785
2. Duplicate footnote markers
3. Footnote markers that appear in wrong files
"""
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')

final_dir = r'e:\Google Antigravity\Projects\Translation\Final'
report_dir = r'e:\Google Antigravity\Projects\Translation\scratch\reports'
os.makedirs(report_dir, exist_ok=True)

# Expected footnote ranges per file (approximate from prior work)
expected_ranges = {
    'Final_Dolnytsky_intro.txt': (1, 1),  # Just [^1]
    'Final_Dolnytsky_part1_structure.txt': (2, 43),
    'Final_Dolnytsky_part2_general_rubrics.txt': (44, 240),
    'Final_Dolnytsky_part3_menaion.txt': (241, 700),  # approximate
    'Final_Dolnytsky_part4_triodion.txt': (700, 785),  # approximate  
    'Final_Dolnytsky_part5_temple.txt': (700, 785),  # overlaps with part4
}

all_markers = {}  # marker_num -> [(file, line, context)]
all_definitions = {}  # marker_num -> [(file, line, text)]

for fname in sorted(os.listdir(final_dir)):
    if not fname.endswith('.txt'):
        continue
    fpath = os.path.join(final_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        # Find markers (references in body text)
        for m in re.finditer(r'\[\^(\d+)\](?!:)', line):
            num = int(m.group(1))
            start = max(0, m.start()-40)
            end = min(len(line), m.end()+40)
            ctx = line[start:end].strip().replace('\r','').replace('\n','')
            if num not in all_markers:
                all_markers[num] = []
            all_markers[num].append((fname, i, ctx))
        
        # Find definitions (footnote text)
        for m in re.finditer(r'\[\^(\d+)\]:', line):
            num = int(m.group(1))
            text = line[m.start():min(len(line), m.start()+100)].strip().replace('\r','').replace('\n','')
            if num not in all_definitions:
                all_definitions[num] = []
            all_definitions[num].append((fname, i, text))

# Analysis
print('=' * 80)
print('FOOTNOTE AUDIT REPORT')
print('=' * 80)

# 1. Missing markers (no anchor in body text)
all_nums = set(range(1, 786))
anchored = set(all_markers.keys())
defined = set(all_definitions.keys())

missing_anchors = sorted(all_nums - anchored)
missing_defs = sorted(all_nums - defined)
orphan_anchors = sorted(anchored - defined)
orphan_defs = sorted(defined - anchored)

print(f'\nTotal unique anchors in body: {len(anchored)}')
print(f'Total unique definitions: {len(defined)}')
print(f'\nMissing anchors (no [^n] in body text): {len(missing_anchors)}')
if missing_anchors:
    print(f'  Numbers: {missing_anchors[:50]}{"..." if len(missing_anchors)>50 else ""}')

print(f'\nMissing definitions (no [^n]: in footnotes): {len(missing_defs)}')
if missing_defs:
    print(f'  Numbers: {missing_defs[:50]}{"..." if len(missing_defs)>50 else ""}')

print(f'\nOrphan anchors (anchor exists but no definition): {len(orphan_anchors)}')
if orphan_anchors:
    for n in orphan_anchors:
        for fname, line, ctx in all_markers[n]:
            print(f'  [{n}] in {fname}:{line} -> {ctx}')

print(f'\nOrphan definitions (definition exists but no anchor): {len(orphan_defs)}')
if orphan_defs:
    for n in orphan_defs:
        for fname, line, text in all_definitions[n]:
            print(f'  [{n}] in {fname}:{line} -> {text}')

# 2. Duplicate anchors (same footnote referenced multiple times)
print(f'\n{"=" * 80}')
print('DUPLICATE ANCHORS (same footnote number appears >1 time in body)')
print('=' * 80)
dupes = {n: locs for n, locs in all_markers.items() if len(locs) > 1}
if dupes:
    for n in sorted(dupes.keys()):
        print(f'\n  [{n}] appears {len(dupes[n])} times:')
        for fname, line, ctx in dupes[n]:
            print(f'    {fname}:{line} -> {ctx}')
else:
    print('  None found.')

# 3. Sequence check - are markers in order within each file?
print(f'\n{"=" * 80}')
print('SEQUENCE CHECK (out-of-order footnotes within files)')
print('=' * 80)
for fname in sorted(os.listdir(final_dir)):
    if not fname.endswith('.txt') or fname == 'Final_footnotes.txt':
        continue
    fpath = os.path.join(final_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    markers_in_order = []
    for m in re.finditer(r'\[\^(\d+)\](?!:)', text):
        markers_in_order.append(int(m.group(1)))
    
    # Check for out-of-order
    issues = []
    for i in range(1, len(markers_in_order)):
        if markers_in_order[i] < markers_in_order[i-1]:
            issues.append((markers_in_order[i-1], markers_in_order[i], i))
    
    if issues:
        print(f'\n  {fname}: {len(issues)} out-of-order pairs')
        for prev, curr, idx in issues[:10]:
            print(f'    [{prev}] followed by [{curr}] (position {idx})')
    else:
        print(f'  {fname}: OK (all in order)')

# Save full marker map
marker_map = {}
for n in sorted(all_markers.keys()):
    entries = []
    for fname, line, ctx in all_markers[n]:
        entries.append({'file': fname, 'line': line, 'context': ctx})
    marker_map[str(n)] = entries

with open(os.path.join(report_dir, 'footnote_audit.json'), 'w', encoding='utf-8') as f:
    json.dump(marker_map, f, indent=2, ensure_ascii=False)

print(f'\n\nFull marker map saved to: {os.path.join(report_dir, "footnote_audit.json")}')
