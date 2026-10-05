import zipfile, xml.etree.ElementTree as ET, sys, re, json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# 1. Load the deterministic audit report JSON
report_path = Path('scratch/reports/deterministic_audit_report.json')
with open(report_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

unanchored_fn_ids = []
for iss in data['issues']:
    if iss['category'] == 'Footnote Bijectivity' and 'never referenced' in iss['message']:
        m = re.search(r'\[\^(\d+)\]', iss['message'])
        if m:
            unanchored_fn_ids.append(m.group(1))

print(f"Total unanchored footnote definitions to investigate: {len(unanchored_fn_ids)}")

# 2. Find their exact locations in scratch/Typyk_UHKC_ukr.docx
ua_docx = Path('scratch/Typyk_UHKC_ukr.docx')
with zipfile.ZipFile(ua_docx) as z:
    tree = ET.fromstring(z.read('word/document.xml'))
    curr_heading = 'TOP'
    found_locations = {}
    for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        text = ''.join(p.itertext()).strip()
        if re.match(r'^\d+\s+[А-ЯЄІЇ]+', text) or text.startswith('ЧАСТИНА') or text.startswith('ГЛАВА') or text.startswith('УСТАВ') or text.startswith('ПРИМІТКА') or 'ВЕРЕСНЯ' in text or 'ЖОВТНЯ' in text:
            curr_heading = text
        for fnref in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footnoteReference'):
            fn_id = fnref.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
            if fn_id in unanchored_fn_ids:
                found_locations[fn_id] = (curr_heading, text[:70])

print(f"Successfully mapped {len(found_locations)} dropped footnotes back to their Ukrainian source dates:")
for fn_id in sorted(found_locations.keys(), key=lambda x: int(x))[:30]:
    heading, snippet = found_locations[fn_id]
    print(f"  Footnote [^{fn_id}]: Under \"{heading[:35]}\" -> Context: \"{snippet}\"")
