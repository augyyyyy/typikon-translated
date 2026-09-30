import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

docx_path = Path.home() / 'OneDrive/Desktop/Here is the revised translation of the Typikon.docx'
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# Read DOCX footnotes
docx_fns = {}
with zipfile.ZipFile(docx_path) as z:
    with z.open('word/footnotes.xml') as f:
        tree = ET.fromstring(f.read())
        for fn in tree.findall(f'.//{{{W_NS}}}footnote'):
            fid = fn.attrib.get(f'{{{W_NS}}}id')
            if fid not in ("-1", "0"):
                texts = [t.text for t in fn.findall(f'.//{{{W_NS}}}t') if t.text]
                docx_fns[int(fid)] = " ".join(" ".join(texts).split())

# Read Final_footnotes.txt
final_fns = {}
final_fn_path = Path('Final/Final_footnotes.txt')
for line in final_fn_path.read_text(encoding='utf-8').splitlines():
    m = re.match(r'^\[\^(\d+)\]:\s*(.*)', line)
    if m:
        final_fns[int(m.group(1))] = m.group(2).strip()

print(f"Total footnotes in DOCX: {len(docx_fns)} (min {min(docx_fns)}, max {max(docx_fns)})")
print(f"Total footnotes in Final_footnotes.txt: {len(final_fns)} (min {min(final_fns)}, max {max(final_fns)})")

# Check alignment
matches = 0
differing_text = 0
missing_in_docx = 0
for fid in sorted(final_fns.keys()):
    if fid in docx_fns:
        matches += 1
    else:
        missing_in_docx += 1

print(f"Matching IDs: {matches}")
print(f"IDs in Final_footnotes but missing in DOCX: {missing_in_docx}")

missing_ids = [fid for fid in final_fns if fid not in docx_fns]
print("Missing IDs:", missing_ids[:30], "..." if len(missing_ids) > 30 else "")
