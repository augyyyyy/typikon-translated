import zipfile
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))
data = z.read("index_split_012.xhtml").decode("utf-8", errors="ignore")

# Find 'apertinonis' which was on leaf p300
pos_aper = data.find("apertinonis")
print(f"apertinonis pos: {pos_aper}")

if pos_aper != -1:
    snippet = data[pos_aper:pos_aper+300]
    print(f"After apertinonis: {snippet}")

# Find 'Севастиан'
pos_sev = data.find("Севастиан")
print(f"Севастиан pos: {pos_sev}")
if pos_sev != -1:
    snippet_end = data[pos_sev:pos_sev+300]
    print(f"Around Севастиан: {snippet_end}")

# Now get the exact segment
start_idx = data.find("респонсорий", pos_aper)
end_idx = data.find("и", data.find("n6-59", pos_sev)) + 1
print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx != -1 and end_idx != -1:
    segment = data[start_idx:end_idx]
    Path("scratch/epub_c31_markup.html").write_text(segment, encoding="utf-8")
    print(f"Successfully wrote scratch/epub_c31_markup.html ({len(segment)} chars)")
