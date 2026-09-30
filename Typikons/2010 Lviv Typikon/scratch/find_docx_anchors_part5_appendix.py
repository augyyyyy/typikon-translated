import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import re

docx_path = Path.home() / 'OneDrive/Desktop/Here is the revised translation of the Typikon.docx'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

with zipfile.ZipFile(docx_path) as z:
    with z.open('word/document.xml') as f:
        tree = ET.fromstring(f.read())

paras = tree.findall(f'.//{{{W_NS}}}p')

def find_anchors():
    for p_idx, p in enumerate(paras):
        p_text = ''.join(p.itertext()).strip()
        # Find footnoteReference
        for fn in p.findall(f'.//{{{W_NS}}}footnoteReference'):
            fid = fn.attrib.get(f'{{{W_NS}}}id')
            if fid:
                num = int(fid)
                if num >= 650:
                    print(f"XML FN {num:3d} in para {p_idx:4d}: {p_text[:100]}")
        # Find bracketed numbers
        # If the paragraph is not purely a list of footnote definitions
        for m in re.finditer(r'(\^\[\d+\]|\[\d+\])', p_text):
            num = int(re.search(r'\d+', m.group()).group())
            if 660 <= num <= 785:
                # check if this is an anchor (i.e. not the definition starting at index 0 or right after period)
                # print context
                start = m.start()
                context = p_text[max(0, start-40):min(len(p_text), start+50)]
                print(f"Anchor candidate [{num}] at para {p_idx:4d} pos {start:3d}: ...{context}...")

if __name__ == '__main__':
    find_anchors()
