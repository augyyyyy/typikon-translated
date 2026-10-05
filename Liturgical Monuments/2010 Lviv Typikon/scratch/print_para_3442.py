import zipfile, xml.etree.ElementTree as ET, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
docx_path = Path.home() / 'OneDrive/Desktop/Here is the revised translation of the Typikon.docx'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
with zipfile.ZipFile(docx_path) as z:
    with z.open('word/document.xml') as f:
        tree = ET.fromstring(f.read())
p = tree.findall(f'.//{{{W_NS}}}p')[3442]
for child in p.iter():
    if child.tag == f'{{{W_NS}}}t':
        print(f'TEXT: {child.text}')
    elif child.tag == f'{{{W_NS}}}footnoteReference':
        fid = child.attrib.get(f'{{{W_NS}}}id')
        print(f'>>> FN REF: {fid} <<<')
