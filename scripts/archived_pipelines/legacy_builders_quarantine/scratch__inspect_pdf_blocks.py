from pathlib import Path
import os
import fitz

def main():
    pdf_base = os.environ.get('TRANSLATION_DATA', r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons')
    pdf_path = Path(pdf_base) / '1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf'
    
    doc = fitz.open(str(pdf_path))
    out_file = Path('scratch/cohort63_blocks.txt')
    
    with open(out_file, 'w', encoding='utf-8') as f:
        for pno in range(621, 631):
            page = doc[pno - 1]
            blocks = page.get_text('blocks')
            f.write(f"=== PAGE {pno} (Total blocks: {len(blocks)}) ===\n")
            for b in sorted(blocks, key=lambda x: (x[1], x[0])):
                # b: (x0, y0, x1, y1, text, block_no, block_type)
                clean_text = ' '.join(b[4].split())
                f.write(f"  [{b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}] {clean_text}\n")
            f.write("\n")

if __name__ == '__main__':
    main()
