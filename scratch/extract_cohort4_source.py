import sys
import fitz
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path(r"E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

out_path = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/1910_skaballanovich_typikon_cohort4_source.txt")
out_path.parent.mkdir(parents=True, exist_ok=True)

with open(out_path, "w", encoding="utf-8") as f:
    for p in range(30, 40):
        leaf_num = p + 1
        page_text = doc[p].get_text()
        f.write(f"=== LEAF p{leaf_num} ===\n")
        f.write(page_text.strip())
        f.write("\n\n")

print(f"Written source text to {out_path} ({out_path.stat().st_size} bytes)")
