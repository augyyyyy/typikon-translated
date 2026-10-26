import sys
from pathlib import Path
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

for p in range(281, 291):
    page = doc[p-1]
    print(f"\n==================== LEAF p{p} (PDF page {p}) ====================")
    words = page.get_text("words")
    # Top words
    top_words = [w for w in words if w[1] < 60]
    print("TOP WORDS:", [(w[4], round(w[0], 1), round(w[1], 1)) for w in top_words])
    
    # Bottom words
    bottom_words = [w for w in words if w[1] > page.rect.height - 60]
    print("BOTTOM WORDS:", [(w[4], round(w[0], 1), round(w[1], 1)) for w in bottom_words])
    
    # Full text blocks
    blocks = page.get_text("blocks")
    print(f"TOTAL BLOCKS: {len(blocks)}")
    for i, b in enumerate(blocks):
        txt = b[4].strip().replace("\n", " ")
        print(f"  Block {i} (y0={round(b[1], 1)}, y1={round(b[3], 1)}): {txt[:100]} ... [len={len(txt)}]")
