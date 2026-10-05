import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

docx_path = Path.home() / 'OneDrive/Desktop/Here is the revised translation of the Typikon.docx'
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

with zipfile.ZipFile(docx_path) as z:
    with z.open('word/document.xml') as f:
        tree = ET.fromstring(f.read())

paras = tree.findall(f'.//{{{W_NS}}}p')
print(f"Total paragraphs in document.xml: {len(paras)}")

# Collect paragraphs with footnote references
fn_refs = []
for p_idx, p in enumerate(paras):
    refs = p.findall(f'.//{{{W_NS}}}footnoteReference')
    if refs:
        # Get full text of this paragraph
        p_text = "".join(t.text for t in p.findall(f'.//{{{W_NS}}}t') if t.text)
        for r in refs:
            fid = r.attrib.get(f'{{{W_NS}}}id')
            fn_refs.append((int(fid), p_idx, p_text))

print(f"Total footnote references in document.xml: {len(fn_refs)}")
# Let's inspect references from id 235 to 285
for fid, p_idx, p_text in sorted(fn_refs, key=lambda x: x[0]):
    if 240 <= fid <= 280:
        clean = " ".join(p_text.split())
        print(f"ID {fid} (p {p_idx}): {clean[:120]}")
