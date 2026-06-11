#!/usr/bin/env python3
"""
Final Terminology Corrections:
1. "Tserkovne Oko (lit. \"Eye of the Church\")" -> "Tserkovne Oko" globally in .txt files.
2. "Megalynaria" -> "Magnifications" globally in .txt files (specifically Part 2 and Footnotes).
"""
import os
import re

# Resolve directories relative to this script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(script_dir)
final_dir = os.path.join(workspace_dir, 'Final')

print(f"Workspace Directory: {workspace_dir}")
print(f"Final Directory: {final_dir}")

replacements = [
    # 1. Tserkovne Oko (lit. "Eye of the Church") -> Tserkovne Oko
    (r'Tserkovne Oko \(lit\. "Eye of the Church"\)', 'Tserkovne Oko'),
    
    # 2. Megalynaria -> Magnifications
    (r'\bMegalynaria\b', 'Magnifications'),
    (r'\bmegalynaria\b', 'magnifications'),
]

total_changes = 0

for fname in sorted(os.listdir(final_dir)):
    if not fname.endswith('.txt'):
        continue
    fpath = os.path.join(final_dir, fname)
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
        print(f"\n=== {fname} ===")
        for pattern, count in file_changes.items():
            print(f"  Replaced '{pattern}': {count} time(s)")

print(f"\nTOTAL CHANGES APPLIED: {total_changes}")
