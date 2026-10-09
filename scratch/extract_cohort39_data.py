import sys
import os
from pathlib import Path
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Resolve PDF path via environment variable or relative path
env_dir = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons')
pdf_path = Path(env_dir) / '1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf'

if not pdf_path.exists():
    raise FileNotFoundError(f"PDF not found at {pdf_path}")

doc = fitz.open(pdf_path)

# Extract pages 381 to 390
out_dir = Path('scratch')
out_dir.mkdir(parents=True, exist_ok=True)

pages_file = out_dir / 'cohort39_extracted_pages.txt'
with open(pages_file, 'w', encoding='utf-8') as f:
    for p in range(381, 391):
        txt = doc[p - 1].get_text()
        f.write(f"=== LEAF p{p} ===\n")
        f.write(txt)
        f.write("\n\n")

print(f"Extracted pages 381-390 to {pages_file}")

# Extract notes pages 520 to 523
notes_file = out_dir / 'cohort39_extracted_notes.txt'
with open(notes_file, 'w', encoding='utf-8') as f:
    for p in range(520, 524):
        txt = doc[p - 1].get_text()
        f.write(f"=== NOTES PAGE {p} ===\n")
        f.write(txt)
        f.write("\n\n")

print(f"Extracted notes pages 520-523 to {notes_file}")
