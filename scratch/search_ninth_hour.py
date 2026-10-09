from pathlib import Path
import os
import fitz

def main():
    pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons')
    p = Path(pdf_base) / '1913-Skaballanovich-Tolkovy-Typikon-Part2-Exposition.pdf'
    doc = fitz.open(str(p))
    
    out = []
    for i in range(len(doc)):
        txt = doc[i].get_text()
        if "ДЕВЯТЫЙ ЧАС" in txt or "Девятый час" in txt:
            out.append(f"Match 'ДЕВЯТЫЙ ЧАС' on page {i+1} (index {i}):\n{txt[:400]}\n---")
        if "Характер службы" in txt:
            out.append(f"Match 'Характер службы' on page {i+1} (index {i}):\n{txt[:400]}\n---")

    Path('scratch/search_ninth_hour.txt').write_text('\n'.join(out), encoding='utf-8')
    print(f"Found {len(out)} matches.")

if __name__ == '__main__':
    main()
