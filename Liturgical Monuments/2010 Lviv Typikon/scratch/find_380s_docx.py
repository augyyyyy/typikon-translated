import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

docx_path = Path.home() / 'OneDrive/Desktop/Here is the revised translation of the Typikon.docx'
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

with zipfile.ZipFile(docx_path) as z:
    with z.open('word/document.xml') as f:
        tree = ET.fromstring(f.read())

paras = tree.findall(f'.//{{{W_NS}}}p')
for fid in [380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393]:
    for idx, p in enumerate(paras):
        refs = p.findall(f'.//{{{W_NS}}}footnoteReference')
        if any(r.attrib.get(f'{{{W_NS}}}id') == str(fid) for r in refs):
            texts = [t.text for t in p.findall(f'.//{{{W_NS}}}t') if t.text]
            clean = " ".join(" ".join(texts).split())
            print(f"DOCX FN {fid:3d} (para {idx:4d}): {clean[:90]}")
            break
