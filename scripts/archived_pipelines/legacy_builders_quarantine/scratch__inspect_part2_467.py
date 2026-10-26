from pathlib import Path
import os
import fitz

def main():
    pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons')
    p = Path(pdf_base) / '1913-Skaballanovich-Tolkovy-Typikon-Part2-Exposition.pdf'
    doc = fitz.open(str(p))
    out = []
    out.append(f"Total pages in 1913 Part 2: {len(doc)}")
    
    for i in range(450, len(doc)):
        txt = doc[i].get_text()
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        first_line = lines[0] if lines else "EMPTY"
        last_line = lines[-1] if lines else "EMPTY"
        out.append(f"PDF Page {i+1} (index {i}): lines={len(lines)}, first={repr(first_line)[:50]}, last={repr(last_line)[:50]}")
        if "466" in txt or "467" in txt or "468" in txt or "ДЕВЯТЫЙ" in txt:
            out.append(f"   --- Match on PDF Page {i+1} ---")
            out.append(txt[:300])

    Path('scratch/part2_scan.txt').write_text('\n'.join(out), encoding='utf-8')
    print("Wrote scratch/part2_scan.txt successfully")

if __name__ == '__main__':
    main()
