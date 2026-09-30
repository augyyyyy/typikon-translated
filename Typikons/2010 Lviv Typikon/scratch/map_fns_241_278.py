import zipfile, xml.etree.ElementTree as ET, sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# Extract paragraphs in Ukrainian docx containing footnotes 247 to 278
ua_docx = Path('scratch/Typyk_UHKC_ukr.docx')
fn_map = {}

with zipfile.ZipFile(ua_docx) as z:
    tree = ET.fromstring(z.read('word/document.xml'))
    for idx, p in enumerate(tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')):
        for fnref in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footnoteReference'):
            fn_id = fnref.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
            if fn_id and fn_id.isdigit():
                val = int(fn_id)
                if 241 <= val <= 278:
                    text = ''.join(p.itertext()).strip()
                    fn_map[val] = (idx, text)

print(f"Total footnotes mapped between 241 and 278: {len(fn_map)}")
for k in sorted(fn_map.keys()):
    p_idx, text = fn_map[k]
    print(f"FN {k} (P{p_idx}): {text[:90]}")
