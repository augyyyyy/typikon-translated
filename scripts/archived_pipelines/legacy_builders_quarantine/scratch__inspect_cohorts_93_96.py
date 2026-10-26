import fitz
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
pdf_path = Path(r"E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

def inspect_range(start_p, end_p):
    for p in range(start_p, end_p + 1):
        txt = doc[p-1].get_text()
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        notes = re.findall(r'\[(\d+)\]', txt)
        print(f"p{p} (notes {notes}):")
        for line in lines[:3]:
            print(f"   {line}")

print("=== COHORT 95 (p941-p950) ===")
inspect_range(941, 950)
print("\n=== COHORT 96 (p951-p960) ===")
inspect_range(951, 960)
