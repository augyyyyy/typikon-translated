import sys, zipfile, xml.etree.ElementTree as ET
from pathlib import Path

docx_path = Path.home() / 'OneDrive/Desktop/Here is the revised translation of the Typikon.docx'
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
with zipfile.ZipFile(docx_path) as z:
    with z.open('word/document.xml') as f:
        tree = ET.fromstring(f.read())
paras = tree.findall(f'.//{{{W_NS}}}p')
for j in range(1985, 1996):
    texts = [t.text for t in paras[j].findall(f'.//{{{W_NS}}}t') if t.text]
    refs = [r.attrib.get(f'{{{W_NS}}}id') for r in paras[j].findall(f'.//{{{W_NS}}}footnoteReference')]
    clean = " ".join(" ".join(texts).split())
    print(f"P{j} (refs={refs}): {clean[:90]}")
