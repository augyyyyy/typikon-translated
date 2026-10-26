import sys
from pathlib import Path
import fitz

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))

crops_to_check = [
    (248, "рассвета"),
    (248, "страх"),
    (248, "фасадов"),
    (250, "проводятся"),
    (244, "придерживает"),
    (247, "равноденствия"),
]

for leaf, word in crops_to_check:
    page = doc[leaf - 1]
    rects = page.search_for(word)
    if not rects:
        print(f"Could not find '{word}' on leaf {leaf}")
        continue
    r = rects[0]
    expanded_rect = fitz.Rect(r.x0 - 150, r.y0 - 15, r.x1 + 250, r.y1 + 15)
    pix = page.get_pixmap(clip=expanded_rect, dpi=300)
    out_crop = Path(f"scratch/crop_p{leaf}_{word}.png")
    pix.save(str(out_crop))
    print(f"Saved crop for leaf {leaf} '{word}' to {out_crop}")
