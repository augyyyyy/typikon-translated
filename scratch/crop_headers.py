from PIL import Image
from pathlib import Path

img_dir = Path('Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/images')

for pno in range(511, 521):
    img_path = img_dir / f"Page_{pno:04d}.jpg"
    img = Image.open(img_path)
    w, h = img.size
    # crop top 150 pixels and bottom 150 pixels
    top = img.crop((0, 0, w, 150))
    bottom = img.crop((0, h - 150, w, h))
    # We can save small thumbnails or check where the page number is
    # Let's save crops to scratch
    out_dir = Path('scratch/crops')
    out_dir.mkdir(parents=True, exist_ok=True)
    top.save(out_dir / f"p{pno}_top.jpg")
    bottom.save(out_dir / f"p{pno}_bottom.jpg")

print("Saved top and bottom crops for p511-p520")
