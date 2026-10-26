import sys
import re
from pathlib import Path
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_path = Path("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub")
z = zipfile.ZipFile(epub_path)
html = z.read("index_split_009.xhtml").decode("utf-8", errors="ignore")

# Find text between note 439 and note 495
start_pos = html.find('n5-439')
end_pos = html.find('n5-495')

cohort20_html = html[start_pos:end_pos]

# find all h1, h2, h3, h4, h5, or class="title" or <b> / <strong> / <p class="...
headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', cohort20_html, re.DOTALL)
print("Headings in h tags:", headings)

# Also check for p with class title or strong
p_titles = re.findall(r'<p[^>]*class=["\'][^"\']*title[^"\']*["\'][^>]*>(.*?)</p>', cohort20_html, re.DOTALL)
print("Paragraph titles:", p_titles)

# Also check bold lines in cohort20_html
bolds = re.findall(r'<b>(.*?)</b>', cohort20_html)
print("Bolds count:", len(bolds))
for b in bolds:
    if len(b) > 10 and len(b) < 100:
        print("  Bold candidate heading:", b)
