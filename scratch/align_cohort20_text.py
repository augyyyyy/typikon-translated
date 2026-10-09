import sys
import re
import zipfile
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(epub_path)
html = z.read("index_split_009.xhtml").decode("utf-8", errors="ignore")

# Let's clean up html to plain text while keeping page markers {с. 203} and note links
# Replace <br/> and </p> with newlines
text = re.sub(r'<a[^>]+id=["\'](?:TOC|note)[^"\']*["\'][^>]*>.*?</a>', '', html)
# replace footnote markers
text = re.sub(r'<a[^>]+href=["\']#n5-(\d+)["\'][^>]*>\[(\d+)\]</a>', r'[\1]', text)
# remove all other tags
text = re.sub(r'<[^>]+>', ' ', text)
# normalize whitespace except newlines
text = re.sub(r'[ \t\xa0]+', ' ', text)
text = re.sub(r'\n\s+', '\n', text)
text = re.sub(r'\n+', '\n', text)

# Find the start of leaf 191:
# On leaf 190 end: "...мемфисском и"
# On leaf 191 start: "фивском), эфиопской и арабской..."
start_idx = text.find('фивском), эфиопской')
print("Found start_idx:", start_idx)

# Find end of leaf 200:
# Leaf 200 end: "(для молитвы после пения псалма) нужно было не иначе, как вс"
# Leaf 201 start: "тав по знаку аввы" or "знак авва ударом руки (пр. 6) о пол."
end_idx = text.find('нужно было не иначе, как встав по знаку аввы')
if end_idx == -1:
    end_idx = text.find('нужно было не иначе')
print("Found end_idx:", end_idx)

cohort_text = text[start_idx:end_idx + 80]
print("Cohort text length:", len(cohort_text))
print("Sample start:\n", cohort_text[:300])
print("Sample end:\n", cohort_text[-300:])
