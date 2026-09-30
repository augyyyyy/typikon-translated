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
        pre = full_text[max(0, found_idx-50):found_idx]
        post = full_text[found_idx:min(len(full_text), found_idx+50)]
        return pre, post, full_text
    return None, None, None

part3_jumps = [313, 317, 342, 356, 361, 367, 389, 380, 382, 402, 433]

for fid in part3_jumps:
    for idx, p in enumerate(paras):
        pre, post, full = get_exact_context(p, fid)
        if pre is not None:
            pre_clean = " ".join(pre.split())
            post_clean = " ".join(post.split())
            # Find closest heading before this paragraph
            heading = ""
            for k in range(idx, max(-1, idx-20), -1):
                p_k = " ".join("".join(t.text for t in paras[k].findall(f'.//{{{W_NS}}}t') if t.text).split())
                if any(m in p_k.upper() for m in ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'DECEMBER', 'NOVEMBER', 'OCTOBER', 'SEPTEMBER', 'CASE', 'RULE']):
                    heading = p_k
                    break
            print(f"FN {fid:3d} (para {idx:4d}) [{heading[:50]}]: PRE: [{pre_clean}] | POST: [{post_clean}]")
            break
