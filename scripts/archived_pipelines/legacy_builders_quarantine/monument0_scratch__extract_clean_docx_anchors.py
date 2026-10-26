import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

docx_path = Path.home() / 'OneDrive/Desktop/Here is the revised translation of the Typikon.docx'
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

with zipfile.ZipFile(docx_path) as z:
    with z.open('word/document.xml') as f:
        tree = ET.fromstring(f.read())

paras = tree.findall(f'.//{{{W_NS}}}p')

def get_full_para_with_tag(p_elem):
    # Return (full_text_with_tags, {fid: (pre_str, post_str)})
    text_parts = []
    fns_in_para = []
    curr_len = 0
    for child in p_elem.iter():
        if child.tag == f'{{{W_NS}}}t' and child.text:
            text_parts.append(child.text)
            curr_len += len(child.text)
        elif child.tag == f'{{{W_NS}}}footnoteReference':
            fid = child.attrib.get(f'{{{W_NS}}}id')
            if fid not in ("-1", "0"):
                fns_in_para.append((int(fid), curr_len))
    
    full_text = "".join(text_parts)
    results = {}
    for fid, offset in fns_in_para:
        pre = full_text[max(0, offset-30):offset]
        post = full_text[offset:min(len(full_text), offset+30)]
        results[fid] = (pre, post, full_text)
    return results

all_fn_data = {}
for p_idx, p in enumerate(paras):
    para_fns = get_full_para_with_tag(p)
    for fid, (pre, post, full_text) in para_fns.items():
        all_fn_data[fid] = (p_idx, pre, post, full_text)

txt = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8')
md = Path('Final MD/Final_Dolnytsky_part3_menaion.md').read_text(encoding='utf-8')

print("Analyzing footnotes 241 to 280:")
for fid in range(241, 281):
    if fid in all_fn_data:
        p_idx, pre, post, full = all_fn_data[fid]
        clean_pre = " ".join(pre.split())
        clean_post = " ".join(post.split())
        
        # Check if pre is in txt and md
        in_txt = clean_pre in txt or pre in txt
        in_md = clean_pre in md or pre in md
        print(f"FN {fid:3d} (p {p_idx:4d}): PRE: [{clean_pre}] | in_txt={in_txt}, in_md={in_md}")
    else:
        print(f"FN {fid:3d}: NOT IN DOCX!")
