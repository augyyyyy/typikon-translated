import sys
import re
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
text = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>', r'\n\n\1\n\n', text)
text = re.sub(r'</p>', '\n\n', text)
text = re.sub(r'<br[^>]*>', '\n', text)
text = re.sub(r'<[^>]+>', ' ', text)
text = text.replace('&nbsp;', ' ').replace('&laquo;', '«').replace('&raquo;', '»').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
# normalize spaces around brackets
text = re.sub(r'\[\s*(\d+)\s*\]', r'[\1]', text)
# normalize double dot in page markers
text = re.sub(r'\{[сc]\.\.\s*(\d+)\}', r'{с. \1}', text)
text = re.sub(r'\{[сc]\.\s*(\d+)\}', r'{с. \1}', text)
text = re.sub(r'[ \t\xa0]+', ' ', text)

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
    positions.append((p_num, pos))

all_found_notes = []
for i in range(10):
    p_num = positions[i][0]
    p_start = positions[i][1]
    p_end = positions[i+1][1]
    cleaned = text[p_start:p_end].strip()
    notes = re.findall(r'\[(\d+)\]', cleaned)
    p_markers = re.findall(r'\{[сc]\.?\s*\d+\}', cleaned)
    all_found_notes.extend([int(n) for n in notes])
    print(f"Leaf p{p_num}: Notes={notes} | Pages={p_markers}")

print(f"\nTotal notes found across leaves p191-p200: {len(all_found_notes)}")
print(f"Min note: {min(all_found_notes)}, Max note: {max(all_found_notes)}")
expected = list(range(440, 495))
missing = set(expected) - set(all_found_notes)
extra = set(all_found_notes) - set(expected)
print(f"Missing from 440..494: {sorted(list(missing))}")
print(f"Extra: {sorted(list(extra))}")
