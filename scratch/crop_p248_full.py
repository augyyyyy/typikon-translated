import fitz

pdf_path = "E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf"
doc = fitz.open(pdf_path)
page = doc[247]
# full width rect
rect = fitz.Rect(0, 50, page.rect.width, 400)
pix = page.get_pixmap(clip=rect, dpi=200)
pix.save("scratch/p248_top_full.png")
print("Saved scratch/p248_top_full.png")
