import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/step75_thinking.txt', 'r', encoding='utf-8') as f:
    text = f.read()

for fn in range(248, 271):
    matches = [m.start() for m in re.finditer(str(fn), text)]
    print(f"Footnote {fn}: matches at {matches}")
    for idx in matches:
        start = max(0, idx - 100)
        end = min(len(text), idx + 200)
        print(f"   [{idx}]: {text[start:end]!r}")
