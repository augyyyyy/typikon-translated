import re
from pathlib import Path

p = Path("scratch/raw_pdf_text_p821_p830.txt")
with open(p, "r", encoding="utf-8") as f:
    content = f.read()

leaves = content.split("=== LEAF ")
for leaf_block in leaves[1:]:
    lines = leaf_block.split("\n")
    leaf_header = lines[0].strip()
    text = "\n".join(lines[1:])
    print(f"Leaf {leaf_header}: {len(text)} chars")
