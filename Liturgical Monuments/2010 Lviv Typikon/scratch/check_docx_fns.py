import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

docx_path = Path.home() / 'OneDrive/Desktop/Here is the revised translation of the Typikon.docx'
with zipfile.ZipFile(docx_path) as z:
    with z.open('word/footnotes.xml') as f:
        tree = ET.fromstring(f.read())
        fns = tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footnote')
        print(f"Total footnotes in DOCX footnotes.xml: {len(fns)}")
        for fn in fns[:15]:
            fid = fn.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
            texts = [t.text for t in fn.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text]
            content = " ".join(texts)
            if fid not in ("-1", "0"):
                print(f"ID {fid}: {content[:100]}")
