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
        pre = full_text[max(0, found_idx-50):found_idx]
        post = full_text[found_idx:min(len(full_text), found_idx+50)]
        return pre, post, full_text
    return None, None, None

for fid in range(310, 325):
    for idx, p in enumerate(paras):
        pre, post, full = get_exact_context(p, fid)
        if pre is not None:
            pre_clean = " ".join(pre.split())
            post_clean = " ".join(post.split())
            print(f"FN {fid:3d} (para {idx:4d}): PRE: [{pre_clean}] | POST: [{post_clean}]")
            break
