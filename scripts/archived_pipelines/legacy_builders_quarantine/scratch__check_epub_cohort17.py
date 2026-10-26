import zipfile
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(epub_path)
epub_html = z.read("index_split_008.xhtml").decode("utf-8", errors="ignore")

# Print occurrences of Greek or key phrases in epub_html around these topics
print("Length of epub_html:", len(epub_html))
for word in ["Музей", "Claudianus", "Мир всем", "Вонмем", "proschomen", "Hermas", "Иулитты", "рукоплеска", "Златоуст"]:
    found = len(re.findall(re.escape(word), epub_html, re.IGNORECASE))
    print(f"Word '{word}': {found} occurrences in EPUB")
