import sys
from pathlib import Path
import zipfile
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(str(epub_path))
html = z.read("index_split_012.xhtml").decode("utf-8", errors="ignore")

# Find the start: where Maronite worship ends or "Богослужение Западной Церкви" begins
idx_start = html.find("Богослужение Западной Церкви")
# Let's find the start of leaf 291 text
idx_p291 = html.find("на полунощнице")
print("idx_start:", idx_start, "idx_p291:", idx_p291)

# Find where leaf 300 ends: "стих отверзения"
idx_p300_end = html.find("стих отверзения")
print("idx_p300_end:", idx_p300_end)

if idx_p291 != -1 and idx_p300_end != -1:
    sub = html[idx_p291-100:idx_p300_end+300]
    # replace tags with simple formatting or print
    print("Found snippet length:", len(sub))
    with open("scratch/epub_cohort30_raw.html", "w", encoding="utf-8") as f:
        f.write(sub)
    print("Wrote scratch/epub_cohort30_raw.html")
