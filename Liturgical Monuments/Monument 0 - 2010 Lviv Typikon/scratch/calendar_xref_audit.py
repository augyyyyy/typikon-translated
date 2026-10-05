#!/usr/bin/env python3
"""
Phase C: Calendar Symbol & Cross-Reference Tag Audit
=====================================================
1. Calendar Symbols: Scans Part 3 (Menaion) for service-rank descriptions
   and proposes/applies a text-tag scheme that can later be adapted to
   typographic symbols when the document is formatted.

2. Cross-References: Scans all Final files for literal page references
   ("on p. 154", "here on p. 157-158") and converts them to anchor tags
   that will enable true linking in the final formatted document.
"""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

final_dir = r'c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\Final'

# ========================================================
# PART 1: Service-Rank Tag Inventory
# ========================================================
# The 2010 source uses symbols for liturgical service ranks.
# In .txt format we use inline tags: [RANK:xxx]
# These are searchable, unambiguous, and machine-parseable.
#
# The original Dolnytsky symbols:
#   = (equal sign)     → Saint without Polyeleos (ordinary)
#   + (cross/plus)     → Saint with Polyeleos
#   Влк (abbreviation) → All-Night Vigil (Великая)
#   Тр (abbreviation)  → Doxology rank (Трезвон)
#   А-Є (letter range) → Calendar letter key
#
# Tag scheme for .txt:
#   [RANK:ORD]  = Ordinary service (without Polyeleos, "on 4" or "on 6")
#   [RANK:DOX]  = Doxology
#   [RANK:POL]  = Polyeleos
#   [RANK:VIG]  = All-Night Vigil
#   [RANK:FEAST] = Great Feast (of the Lord or Theotokos)

# Scan for current descriptive patterns
rank_patterns = [
    (r'\bSaint without Polyeleos\b', 'ORD'),
    (r'\bSaint with Polyeleos\b', 'POL'),
    (r'\bSaint with All-Night Vigil\b', 'VIG'),
    (r'\bSaint with Doxology\b', 'DOX'),
    (r'\bof.*Great.*(?:Doxology|type)\b', 'DOX'),
    (r'\bAll-Night Vigil is served\b', 'VIG'),
]

print("=" * 60)
print("SERVICE RANK PATTERN INVENTORY")
print("=" * 60)

for name in sorted(os.listdir(final_dir)):
    if not name.endswith('.txt'):
        continue
    filepath = os.path.join(final_dir, name)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    counts = {}
    for pat, tag in rank_patterns:
        c = sum(1 for l in lines if re.search(pat, l, re.IGNORECASE))
        if c > 0:
            counts[f'[RANK:{tag}]'] = c
    
    if counts:
        print(f'\n{name}:')
        for tag, c in sorted(counts.items()):
            print(f'  {tag}: {c} occurrences')

# ========================================================
# PART 2: Cross-Reference Inventory
# ========================================================
print("\n\n" + "=" * 60)
print("CROSS-REFERENCE PAGE NUMBER INVENTORY")
print("=" * 60)

# Pattern: "on p. NNN" or "on p. NNN-NNN"
page_ref_re = re.compile(r'(?:on|see|See) (?:the rule )?(?:given )?(?:before )?(?:here )?(?:on )?p\.\s*(\d+(?:-\d+)?)')

# Also: "here on p. NNN"
page_ref_re2 = re.compile(r'here on p\.\s*(\d+(?:-\d+)?)')

all_refs = {}
for name in sorted(os.listdir(final_dir)):
    if not name.endswith('.txt'):
        continue
    filepath = os.path.join(final_dir, name)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    file_refs = []
    for i, line in enumerate(lines, 1):
        for m in page_ref_re.finditer(line):
            file_refs.append((i, m.group(), m.group(1)))
    
    if file_refs:
        all_refs[name] = file_refs
        print(f'\n{name}: {len(file_refs)} page references')
        # Show unique page targets
        targets = sorted(set(r[2] for r in file_refs))
        print(f'  Targets: {", ".join(targets)}')

# Summary
total = sum(len(v) for v in all_refs.values())
all_targets = sorted(set(t for refs in all_refs.values() for _,_,t in refs))
print(f'\n--- TOTAL: {total} page references to {len(all_targets)} unique page targets ---')
print(f'Unique targets: {", ".join(all_targets[:30])}...' if len(all_targets) > 30 else f'Unique targets: {", ".join(all_targets)}')
