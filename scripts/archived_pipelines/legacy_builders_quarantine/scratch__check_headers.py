import sys
from pathlib import Path
import fitz

sys.stdout.reconfigure(encoding='utf-8')

def main():
    doc = fitz.open(r"E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")
    for pno in range(751, 761):
        page = doc[pno - 1]
        rect = fitz.Rect(0, 0, page.rect.width, 100)
        header_text = page.get_text("text", clip=rect).strip().replace('\n', ' ')
        print(f"Leaf p{pno}: header='{header_text}'")

if __name__ == '__main__':
    main()
