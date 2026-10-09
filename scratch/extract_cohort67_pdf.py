from pathlib import Path
import os
import fitz

def main():
    pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons')
    pdf_path = Path(pdf_base) / '1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf'
    
    if not pdf_path.exists():
        print(f"Error: {pdf_path} does not exist.")
        return

    doc = fitz.open(str(pdf_path))
    
    out_dir = Path('scratch/cohort67_extracted')
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for pno in range(661, 671):
        page_idx = pno - 1  # 0-indexed
        page = doc[page_idx]
        text = page.get_text()
        out_file = out_dir / f"p{pno}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Leaf p{pno}: {len(text)} characters extracted")

    # Extract footnote pages 985 to 988
    for pno in range(984, 989):
        page_idx = pno - 1
        page = doc[page_idx]
        text = page.get_text()
        out_file = out_dir / f"notes_p{pno}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Notes page p{pno}: {len(text)} characters extracted")

    # Check images in Source Text/images
    img_dir = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/images")
    for pno in range(661, 671):
        found = []
        for name in [f"Page_{pno:04d}.jpg", f"p{pno}.png", f"p{pno}.jpg"]:
            if (img_dir / name).exists():
                found.append(name)
        print(f"Leaf p{pno} images: {found}")

if __name__ == '__main__':
    main()
