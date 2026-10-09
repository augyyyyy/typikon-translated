import fitz
import sys
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf"
doc = fitz.open(pdf_path)

headings = [
    (243, "Великая пятница"),
    (245, "Великая суббота"),
    (246, "Пасха"),
    (250, "Пасхальная седмица"),
]

for leaf, h in headings:
    page = doc[leaf - 1]
    rects = page.search_for(h)
    if rects:
        r = rects[0]
        expanded = fitz.Rect(r.x0 - 50, r.y0 - 20, r.x1 + 50, r.y1 + 20)
        pix = page.get_pixmap(clip=expanded, dpi=150)
        pix.save(f"scratch/crop_h_{leaf}.png")
        print(f"Leaf {leaf}: {h} found and cropped")
    else:
        print(f"Leaf {leaf}: {h} NOT found")
