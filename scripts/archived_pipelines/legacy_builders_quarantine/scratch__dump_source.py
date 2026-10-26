import re
import fitz
from pathlib import Path

# Load PDF
pdf_path = Path(r"E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(pdf_path)

# Let's write an assembler that reads the text of each page, fixes OCR line wraps, but preserves original words, headers, and footnote markers
# We will inspect each page carefully.

out_file = Path("scratch/draft_source_83.txt")

with open(out_file, "w", encoding="utf-8") as f:
    for p in range(821, 831):
        f.write(f"=== LEAF p{p} ===\n")
        page = doc[p - 1]
        text = page.get_text()
        f.write(text.strip())
        f.write("\n\n")

print("Dumped draft source text.")
