import sys
import re
import fitz
import zipfile
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(epub_path)
html = z.read("index_split_009.xhtml").decode("utf-8", errors="ignore")

# Replace footnote links with [N]
text = re.sub(r'<a[^>]+href=["\']#n5-(\d+)["\'][^>]*>\[(\d+)\]</a>', r'[\1]', html)
# Remove unwanted tags
text = re.sub(r'<a[^>]+id=["\'](?:TOC|note)[^"\']*["\'][^>]*>.*?</a>', '', text)
# Convert </p>, <br/>, headings to newlines
text = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>', r'\n\n\1\n\n', text)
text = re.sub(r'</p>', '\n\n', text)
text = re.sub(r'<br[^>]*>', '\n', text)
text = re.sub(r'<[^>]+>', ' ', text)
# Unescape HTML entities
text = text.replace('&nbsp;', ' ').replace('&laquo;', '«').replace('&raquo;', '»').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
# Clean whitespace
text = re.sub(r'[ \t\xa0]+', ' ', text)

# Define exact boundary anchor phrases for each leaf from p191 to p200:
# p191 start: 'фивском), эфиопской'
# p192 start: 'Таковы были внешняя сторона и история'
# p193 start: 'словами: иди, тебя ожидает собрание'
# p194 start: 'бесплотного человека на осуждение нашу?'
# p195 start: 'формою буквы свойство наклонностей'
# p196 start: 'управление им), но ограничиваются о каждой'
# p197 start: 'Если эти службы могли казаться небольшими'
# p198 start: 'слуги и смотрители отдельно для каждого дома'
# p199 start: 'изгнанием из монастыря; наиболее употребительные епитимьи'
# p200 start: 'только больным (пр. 45). «Кто не захочет идти в трапезу'
# p201 start: 'братом чередным, стоящим впереди'

anchors = [
    (191, "фивском), эфиопской"),
    (192, "Таковы были внешняя сторона и история Пахомиевых"),
    (193, "словами: иди, тебя ожидает собрание"),
    (194, "бесплотного человека на осуждение нашу"),
    (195, "формою буквы свойство наклонностей"),
    (196, "управление им), но ограничиваются о каждой"),
    (197, "Если эти службы могли казаться небольшими"),
    (198, "слуги и смотрители отдельно для каждого дома"),
    (199, "изгнанием из монастыря; наиболее употребительные епитимьи"),
    (200, "только больным (пр. 45). «Кто не захочет идти в трапезу"),
    (201, "братом чередным, стоящим впереди"),
]

positions = []
for p_num, anchor in anchors:
    pos = text.find(anchor)
    if pos == -1:
        print(f"ERROR: Anchor not found for leaf p{p_num}: {anchor}")
    else:
        positions.append((p_num, pos))
        print(f"Found anchor for leaf p{p_num} at {pos}")

if len(positions) == len(anchors):
    print("All 11 anchors found successfully!")
