import fitz
from pathlib import Path

pdf_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
doc = fitz.open(str(pdf_path))
page = doc[247] # leaf 248 is index 247

# Crop the top half of leaf 248
rect = fitz.Rect(50, 50, page.rect.width - 50, 350)
pix = page.get_pixmap(clip=rect, dpi=200)
pix.save("scratch/p248_top.png")
print("Saved scratch/p248_top.png")
