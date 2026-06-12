#!/usr/bin/env python3
"""
Searches and fixes terminology in the new MD-based Typikon directory:
C:/Users/augus/OneDrive/Documents/Google Antigravity/Projects/Typikon Coded/Data/Service Books/Typikon
"""
import os
import re
import sys

# Configure standard output to use UTF-8
sys.stdout.reconfigure(encoding='utf-8')

target_dir = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"

print(f"Target Directory: {target_dir}")

replacements = [
    # 1. Tserkovne Oko (lit. "Eye of the Church") -> Tserkovne Oko
    (r'Tserkovne Oko \(lit\. "Eye of the Church"\)', 'Tserkovne Oko'),
    
    # 2. Megalynaria -> Magnifications
    (r'\bMegalynaria\b', 'Magnifications'),
    (r'\bmegalynaria\b', 'magnifications'),
]

# First, count occurrences of canonical and Slavonic terms
canonical_terms = ["Tserkovne Oko", "Magnification", "Magnifications", "Gradual", "Stepenna", "Eye of the Church", "Megalynaria"]
print("\n--- Term Counts in Target Files ---")
for term in canonical_terms:
    total_count = 0
    for fname in sorted(os.listdir(target_dir)):
        if not fname.endswith('.md'):
            continue
        # Skip matrices/glossaries
        if fname in ['vocabulary_standardization_matrix.md', 'Final_Dolnytsky_glossary.md']:
            continue
        fpath = os.path.join(target_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        count = len(re.findall(r'\b' + re.escape(term) + r'\b', content, re.I))
        if count > 0:
            print(f"  {term} in {fname}: {count}")
            total_count += count
    print(f"  [Total for '{term}': {total_count}]\n")


# Next, apply the fixes
print("\n--- Applying Replacements ---")
total_changes = 0
for fname in sorted(os.listdir(target_dir)):
    if not fname.endswith('.md'):
        continue
    # Skip standard matrices/glossaries from auto-fixes so we preserve explanations
    if fname in ['vocabulary_standardization_matrix.md', 'Final_Dolnytsky_glossary.md']:
        continue
    
    fpath = os.path.join(target_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified_content = content
    file_changes = {}
    
    for pattern, replacement in replacements:
        matches = list(re.finditer(pattern, modified_content))
        if matches:
            count = len(matches)
            modified_content = re.sub(pattern, replacement, modified_content)
            file_changes[pattern] = count
            total_changes += count
            
    if file_changes:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"=== {fname} ===")
        for pattern, count in file_changes.items():
            print(f"  Replaced '{pattern}': {count} time(s)")

print(f"\nTOTAL REPLACEMENTS APPLIED: {total_changes}")
