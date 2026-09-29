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

def norm(s):
    # Normalize dashes, quotes, and whitespace
    s = s.replace('–', '-').replace('—', '-').replace('’', "'").replace('‘', "'")
    s = s.replace('“', '"').replace('”', '"')
    return " ".join(s.lower().split())

txt = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8')
md = Path('Final MD/Final_Dolnytsky_part3_menaion.md').read_text(encoding='utf-8')
norm_txt = norm(txt)
norm_md = norm(md)

for fid in range(241, 281):
    found = False
    for p in paras:
        refs = p.findall(f'.//{{{W_NS}}}footnoteReference')
        for r in refs:
            if r.attrib.get(f'{{{W_NS}}}id') == str(fid):
                text_parts = [t.text for t in p.findall(f'.//{{{W_NS}}}t') if t.text]
                full_text = "".join(text_parts)
                # Find anchor offset
                curr = 0
                for c in p.iter():
                    if c.tag == f'{{{W_NS}}}t' and c.text:
                        curr += len(c.text)
                    elif c.tag == f'{{{W_NS}}}footnoteReference' and c.attrib.get(f'{{{W_NS}}}id') == str(fid):
                        break
                pre = full_text[max(0, curr-35):curr]
                post = full_text[curr:min(len(full_text), curr+35)]
                n_pre = norm(pre)
                in_t = n_pre in norm_txt
                in_m = n_pre in norm_md
                print(f"FN {fid:3d}: norm(pre)=[{n_pre}] -> in_txt={in_t}, in_md={in_m}")
                found = True
                break
        if found:
            break
