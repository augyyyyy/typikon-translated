#!/usr/bin/env python3
"""
Book Title Unification Script
Applies the uniform proper-name policy for all liturgical book titles:
- Greek titles: already correct (Octoechos, Triodion, etc.)
- Slavonic titles: convert English translations back to transliterated proper names
  - "Eye of the Church" -> "Tserkovne Oko"
  - "Service Book" -> "Sluzhebnik"
  - "Horo- and Prayer Book" -> "Chasoslovets i Molitvoslov"

First-occurrence glosses are added per-file.
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

final_dir = r'e:\Google Antigravity\Projects\Translation\Final'

# Replacements: (pattern, replacement, description)
# "Eye of the Church" -> "Tserkovne Oko" (simple)
# "Service Book" -> "Sluzhebnik" (need to avoid "Service Books" plural)
# "Horo- and Prayer Book" -> "Chasoslovets i Molitvoslov"

REPLACEMENTS = [
    # Eye of the Church -> Tserkovne Oko
    (r'\bEye of the Church\b', 'Tserkovne Oko'),
    # Service Books (plural) -> Sluzhebnyky
    (r'\bService Books\b', 'Sluzhebnyky'),
    # Service Book (singular) -> Sluzhebnik
    (r'\bService Book\b', 'Sluzhebnik'),
    # Horo- and Prayer Books (plural first)
    (r'\bHoro- and Prayer Books\b', 'Chasoslovtsi i Molitvoslovy'),
    # Horo- and Prayer Book (singular)
    (r'\bHoro- and Prayer Book\b', 'Chasoslovets i Molitvoslov'),
    # Also catch "Horo- or Prayer Book" variant
    (r'\bHoro- or Prayer Book\b', 'Chasoslovets i Molitvoslov'),
]

# First-occurrence glosses (added after the FIRST instance in each file)
GLOSSES = {
    'Tserkovne Oko': ' (lit. "Eye of the Church")',
    'Sluzhebnik': ' (lit. "Service Book")',
    'Sluzhebnyky': ' (lit. "Service Books")',
    'Chasoslovets i Molitvoslov': ' (lit. "Horo- and Prayer Book")',
    'Chasoslovtsi i Molitvoslovy': ' (lit. "Horo- and Prayer Books")',
}

# Stats
total_stats = {}

for name in sorted(os.listdir(final_dir)):
    if not name.endswith('.txt'):
        continue
    filepath = os.path.join(final_dir, name)
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    original = text
    file_stats = {}
    
    for pattern, replacement in REPLACEMENTS:
        count = len(re.findall(pattern, text))
        if count > 0:
            text = re.sub(pattern, replacement, text)
            file_stats[replacement] = count
    
    # Add first-occurrence glosses
    for term, gloss in GLOSSES.items():
        glossed = term + gloss
        if term in text and glossed not in text:
            # Only gloss the FIRST occurrence
            text = text.replace(term, glossed, 1)
    
    if text != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'\n=== {name} ===')
        for term, count in file_stats.items():
            print(f'  {term}: {count} replacements')
        total_stats[name] = file_stats
    else:
        print(f'\n=== {name} === (no changes)')

print('\n\n========== SUMMARY ==========')
grand = {}
for fname, stats in total_stats.items():
    for term, count in stats.items():
        grand[term] = grand.get(term, 0) + count
for term, count in grand.items():
    print(f'  {term}: {count} total replacements')
