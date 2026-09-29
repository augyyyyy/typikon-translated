import zipfile, xml.etree.ElementTree as ET, sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ua_docx = Path('scratch/Typyk_UHKC_ukr.docx')

fn_targets = [
    247, 248, 249, 250, 251, 252, 253, 254, 255, 256,
    259, 260, 261, 262, 263, 264, 265, 266, 267, 268,
    271, 272, 273, 274, 275, 276, 277, 278
]

with zipfile.ZipFile(ua_docx) as z:
    tree = ET.fromstring(z.read('word/document.xml'))
    for idx, p in enumerate(tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')):
        fns = [fnref.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id') 
               for fnref in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footnoteReference')]
        matched = [int(f) for f in fns if f and f.isdigit() and int(f) in fn_targets]
        if matched:
            text = ''.join(p.itertext()).strip()
            print(f"P{idx} -> FNs {matched}:")
            # print runs to see exact anchor word
            runs_repr = []
            for r in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r'):
                r_text = ''.join(r.itertext())
                r_fns = [fnref.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id') 
                         for fnref in r.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footnoteReference')]
                if r_fns:
                    runs_repr.append(f"[{r_text} -> FN {r_fns}]")
                elif r_text:
                    runs_repr.append(r_text)
            print("  Runs: " + "".join(runs_repr))
            print("-" * 60)
