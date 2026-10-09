import os
import sys
import re
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

raw_text = Path("scratch/cohort99_source_raw.txt").read_text(encoding='utf-8')

# Split by leaves
parts = raw_text.split("=== LEAF ")
clean_leaves = {}

for part in parts[1:]:
    lines = part.strip().splitlines()
    leaf_id = lines[0].strip() # e.g. "p981 ===" -> "p981"
    leaf_num = leaf_id.split()[0]
    content_lines = lines[1:]
    
    # We want to reconstruct clean notes for this leaf
    # A new note starts with a number followed by period and space (e.g. "268. ", "310. ")
    # or the text before the first note is the continuation from the previous leaf.
    clean_leaves[leaf_num] = content_lines

print("Leaves extracted:", list(clean_leaves.keys()))
