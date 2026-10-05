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

missing_ids = [
    29, 35, 36, 41, 88, 104, 146, 149, 192, 217, 218, 223,
    300, 338, 339, 345, 359, 360, 362, 379, 392, 399, 406, 444, 450,
    502, 516, 518, 519, 545, 547, 576, 579, 623, 640
]

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

print(f"Extracting anchor contexts for {len(missing_ids)} missing footnotes from DOCX:")
for fid in missing_ids:
    found = False
    for p_idx, p in enumerate(paras):
        pre, post, full = get_exact_context(p, fid)
        if pre is not None:
            pre_clean = " ".join(pre.split())
            post_clean = " ".join(post.split())
            print(f"FN {fid:3d} (para {p_idx:4d}): PRE: [{pre_clean}] | POST: [{post_clean}]")
            found = True
            break
    if not found:
        print(f"FN {fid:3d}: NOT FOUND IN DOCX XML!")
