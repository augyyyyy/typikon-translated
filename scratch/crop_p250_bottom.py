import fitz
from pathlib import Path

pdf_path = "E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf"
doc = fitz.open(pdf_path)
page = doc[249]
rect = fitz.Rect(50, page.rect.height - 200, page.rect.width - 50, page.rect.height)
pix = page.get_pixmap(clip=rect, dpi=200)
pix.save("scratch/p250_bottom.png")
print("Saved scratch/p250_bottom.png")
