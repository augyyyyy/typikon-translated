import zipfile
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path('E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub')
z = zipfile.ZipFile(str(epub_path))

for name in z.namelist():
    if name.endswith('.xhtml'):
        raw = z.read(name).decode('utf-8', errors='ignore')
        if '599' in raw:
            for m in re.finditer(r'(.{0,50}599.{0,50})', raw):
                clean = re.sub(r'\s+', ' ', m.group(0))
                print(f"{name}: {clean}")
