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

leaf_texts = {}
for i in range(10):
    p_num = positions[i][0]
    p_start = positions[i][1]
    p_end = positions[i+1][1]
    raw_leaf = text[p_start:p_end].strip()
    
    # clean up multiple empty lines
    cleaned = re.sub(r'\n{3,}', '\n\n', raw_leaf)
    leaf_texts[p_num] = cleaned
    
    notes = re.findall(r'\[(\d+)\]', cleaned)
    p_markers = re.findall(r'\{[сc]\.?\s*\d+\}', cleaned)
    print(f"=== LEAF p{p_num} (len={len(cleaned)}) ===")
    print(f"  Notes: {notes}")
    print(f"  Page markers: {p_markers}")
    print(f"  Start: {cleaned[:60]}")
    print(f"  End:   {cleaned[-60:]}\n")
