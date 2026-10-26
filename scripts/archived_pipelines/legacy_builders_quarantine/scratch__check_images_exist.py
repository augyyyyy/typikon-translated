import sys
from pathlib import Path
from PIL import Image
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Check images directory
img_dir = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/images")
for p in range(281, 291):
    img_p = img_dir / f"p{p}.png"
    if not img_p.exists():
        img_p = img_dir / f"p{p}.jpg"
    print(f"p{p}: {img_p.name} exists={img_p.exists()}, size={img_p.stat().st_size if img_p.exists() else 0}")
