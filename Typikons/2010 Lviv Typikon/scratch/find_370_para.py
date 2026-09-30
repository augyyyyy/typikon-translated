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

def get_exact_context(p_elem, fid_target):
    full_text_parts = []
    found_idx = None
    curr_len = 0
    for child in p_elem.iter():
        if child.tag == f'{{{W_NS}}}t' and child.text:
            full_text_parts.append(child.text)
            curr_len += len(child.text)
        elif child.tag == f'{{{W_NS}}}footnoteReference':
            fid = child.attrib.get(f'{{{W_NS}}}id')
            if fid and int(fid) == fid_target:
                found_idx = curr_len
    if found_idx is not None:
        full_text = "".join(full_text_parts)
        pre = full_text[max(0, found_idx-60):found_idx]
        post = full_text[found_idx:min(len(full_text), found_idx+60)]
        return pre, post, full_text
    return None, None, None

for idx, p in enumerate(paras):
    pre, post, full = get_exact_context(p, 370)
    if pre:
        print(f"FN 370 is at paragraph {idx}!")
        for j in range(max(0, idx-4), min(len(paras), idx+5)):
            texts = [t.text for t in paras[j].findall(f'.//{{{W_NS}}}t') if t.text]
            combined = " ".join(" ".join(texts).split())
            print(f"  P{j}: {combined[:90]}")
        break
