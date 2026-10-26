import os
import sys
from pathlib import Path
from PIL import Image

# Let's inspect Page_0981.jpg
img_path = Path(r"Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images\Page_0981.jpg")
if img_path.exists():
    im = Image.open(img_path)
    print(f"Image 981 size: {im.size}")
