import fitz
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
pdf_path = Path(r"E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

for c_idx, start_p in enumerate(range(911, 961, 10), start=91):
    end_p = min(start_p + 9, 960)
    cohort_notes = []
    headers = []
    for p in range(start_p, end_p + 1):
        txt = doc[p-1].get_text()
        notes = re.findall(r'\[(\d+)\]', txt)
        cohort_notes.extend(notes)
        for line in txt.splitlines():
            s = line.strip()
            if s.isupper() and len(s) > 4 and not s.startswith("==="):
                headers.append(s)
    uniq_headers = list(dict.fromkeys(headers))[:4]
    print(f"Cohort {c_idx} (leaves p{start_p}-p{end_p}): {len(cohort_notes)} notes (range {cohort_notes[0] if cohort_notes else 'none'}..{cohort_notes[-1] if cohort_notes else 'none'}). Headers: {uniq_headers}")
