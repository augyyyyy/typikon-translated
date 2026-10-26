import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

html = Path("scratch/epub_c31_markup.html").read_text(encoding="utf-8")

# Find all heading tags or strong paragraphs
headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html)
print(f"H tags: {headings}")

# Look for bold standalone lines or title-like classes
for m in re.finditer(r'<p[^>]*class=[\"\']([^\"\']*)[\"\'][^>]*>(.*?)</p>', html):
    cls, content = m.group(1), m.group(2)
    clean = re.sub(r'<[^>]+>', '', content).strip()
    if any(h in clean for h in ["Утреня", "Часы", "Вечерня", "Повечерие", "Венедикт", "чины", "Амвросианский", "Мозарабский", "Галликанский", "Церковный год", "Месяцесловы", "Малый римский"]):
        print(f"Class: {cls} | Text: {clean}")
