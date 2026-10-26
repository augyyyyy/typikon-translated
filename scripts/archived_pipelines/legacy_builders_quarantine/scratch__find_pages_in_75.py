import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/step75_thinking.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pages = ['241', '242', '243', '244', '245', '246', '247', '248', '249', '250']
for p in pages:
    matches = [m.start() for m in re.finditer(r'(?:p\.?\s*' + p + r'|page\s*' + p + r'|p' + p + r')', text, re.I)]
    print(f"Page {p} matches at: {matches}")
