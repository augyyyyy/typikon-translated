from pathlib import Path
from PIL import Image

def main():
    img_dir = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/images")
    for pno in range(751, 761):
        f = img_dir / f"p{pno}.png"
        if f.exists():
            im = Image.open(f)
            print(f"p{pno}.png: size={im.size}, mode={im.mode}")
        else:
            print(f"p{pno}.png: NOT FOUND")

if __name__ == '__main__':
    main()
