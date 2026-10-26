import fitz
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

all_cohort_notes = []

for pno in range(160, 170):
    page_num = pno + 1
    page = doc[pno]
    text = page.get_text()
    # Find all footnote citations [N]
    citations = [int(x) for x in re.findall(r'\[(\d+)\]', text)]
    all_cohort_notes.extend(citations)
    # Find any page markers like {c. 166}
    page_markers = re.findall(r'\{[сc]\.?\s*\d+\}', text)
    print(f"Leaf p{page_num}: citations={citations}, page_markers={page_markers}")

print(f"Total citations across cohort 17: {len(all_cohort_notes)}")
print(f"Citations min={min(all_cohort_notes)}, max={max(all_cohort_notes)}")
# Check if citations are continuous
expected = list(range(min(all_cohort_notes), max(all_cohort_notes)+1))
missing = set(expected) - set(all_cohort_notes)
print(f"Missing in sequence: {missing}")
