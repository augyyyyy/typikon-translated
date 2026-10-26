import zipfile, sys, re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

z = zipfile.ZipFile('E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/Source Epubs/skab_part1.epub')
content = z.read('index_split_009.xhtml').decode('utf-8', errors='ignore')

# Clean html tags but preserve paragraphs and spans
content = re.sub(r'<a href="[^"]*"[^>]*>(\[\d+\])</a>', r'\1', content)
content = re.sub(r'</p>|</div>', '\n\n', content)
content = re.sub(r'<h\d[^>]*>(.*?)</h\d>', r'\n\n### \1\n\n', content)
content = re.sub(r'<[^>]+>', '', content)
content = re.sub(r'[ \t]+', ' ', content)
content = re.sub(r'\n{3,}', '\n\n', content)

idx1 = content.find('братом чередным')
idx2 = content.find('имевшая такое же устройство, как Харитонова')
print(f'Length: {idx2 - idx1}')
cohort_text = content[idx1:idx2].strip()
Path('scratch/cohort21_epub_clean.txt').write_text(cohort_text, encoding='utf-8')
print('Wrote scratch/cohort21_epub_clean.txt')
