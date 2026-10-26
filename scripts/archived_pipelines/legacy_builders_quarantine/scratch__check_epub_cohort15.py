import zipfile
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
if epub_path.exists():
    z = zipfile.ZipFile(epub_path)
    namelist = z.namelist()
    print("EPUB file list:", len(namelist), "files")
    
    for n in sorted(namelist):
        if n.endswith(('.xhtml', '.html')):
            content = z.read(n).decode('utf-8', errors='ignore')
            matches = re.findall(r'id=["\'](n5-\d+)["\']', content)
            if matches:
                print(f"{n}: found {len(matches)} notes: {matches[0]} ... {matches[-1]}")
else:
    print("EPUB not found!")
