import fitz
from pathlib import Path

pdf_path = Path(r"E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

out_path = Path("scratch/raw_pdf_text_p821_p830.txt")
with open(out_path, "w", encoding="utf-8") as f:
    for page_num in range(821, 831):
        # 0-indexed in fitz
        page = doc[page_num - 1]
        text = page.get_text()
        f.write(f"=== LEAF p{page_num} ===\n")
        f.write(text.strip())
        f.write("\n\n")

print(f"Extracted pages 821-830 to {out_path}")
