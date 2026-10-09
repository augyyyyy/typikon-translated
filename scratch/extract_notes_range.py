from pathlib import Path
import os
import fitz

def main():
    pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons')
    p = Path(pdf_base) / '1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf'
    doc = fitz.open(str(p))
    
    out = []
    for pno in range(968, 975):
        page = doc[pno-1]
        txt = page.get_text()
        out.append(f"=== PAGE {pno} ===")
        out.append(txt)
    
    Path('scratch/notes_p968_p974.txt').write_text('\n'.join(out), encoding='utf-8')
    print("Wrote scratch/notes_p968_p974.txt")

if __name__ == '__main__':
    main()
