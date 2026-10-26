import sys
from pathlib import Path
import re
import zipfile

sys.stdout.reconfigure(encoding='utf-8')

raw_pdf_text = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort25_extracted_pdf_text.txt").read_text(encoding="utf-8")

leaves_raw = re.split(r'=== LEAF (p\d+) ===', raw_pdf_text)

leaf_data = {}
for i in range(1, len(leaves_raw), 2):
    lid = leaves_raw[i]
    content = leaves_raw[i+1].strip()
    leaf_data[lid] = content

# Check footnotes referenced in the text or found in epub
epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))

# Let's inspect the split file where the main text is
# Let's search which split files contain the text for leaves 241-250
for name in z.namelist():
    if name.endswith('.xhtml') and 'split' in name:
        txt = z.read(name).decode('utf-8', errors='ignore')
        if 'Великая пятница' in txt or 'Великая суббота' in txt:
            print(f"Found in {name}")

for lid in [f'p{p}' for p in range(241, 251)]:
    content = leaf_data[lid]
    first_line = content.split('\n')[0] if content else ''
    last_line = content.split('\n')[-1] if content else ''
    # find page markers
    p_markers = re.findall(r'(\d+)', first_line)
    orig_p = re.findall(r'(\d{2,3})', content[:50])
    print(f"\n--- {lid} --- (length {len(content)})")
    print(f"Start: {content[:120]!r}")
    print(f"End: {content[-120:]!r}")
