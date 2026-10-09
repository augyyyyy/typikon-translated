import sys
from pathlib import Path
import fitz

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

crops_to_check = [
    (243, "ἀπαγγέλειν"),
    (248, "ἀγροпνοῦσι"),
    (248, "паннох"),
    (248, "frontium"),
    (249, "λαμποφορία"),
    (249, "φωταγογία"),
    (249, "ἀγία"),
    (250, "attenduntur"),
]

for leaf, word in crops_to_check:
    page = doc[leaf - 1]
    rects = page.search_for(word)
    if not rects:
        # try searching partial or nearby words
        print(f"Could not find exact text '{word}' on leaf {leaf}")
        continue
    r = rects[0]
    # expand rect slightly to see surrounding context
    expanded_rect = fitz.Rect(r.x0 - 50, r.y0 - 10, r.x1 + 50, r.y1 + 10)
    pix = page.get_pixmap(clip=expanded_rect, dpi=300)
    out_crop = Path(f"scratch/crop_p{leaf}_{word[:5]}.png")
    pix.save(str(out_crop))
    print(f"Saved crop for leaf {leaf} '{word}' to {out_crop}")
