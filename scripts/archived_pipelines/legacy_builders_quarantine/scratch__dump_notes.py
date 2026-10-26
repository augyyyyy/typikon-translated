import sys
from pathlib import Path
import re

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

p = Path(r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\..\..\..\..\..\..\.gemini\antigravity\brain\f226825a-f6a9-4f6d-9451-ef6f56dead8c\.system_generated\steps\97\content.md")
txt = p.read_text(encoding="utf-8")

notes = re.findall(r'<a id="note(\d+)"><\/a>\s*<div class="note"><a href="#note\1_return"><sup>\1<\/sup><\/a><p class="txt">(.*?)<\/p><\/div>', txt, re.DOTALL)
print(f"Total extracted notes: {len(notes)}")

for num, content in notes:
    n = int(num)
    if 410 <= n <= 455:
        clean = re.sub(r'<[^>]+>', '', content).strip()
        print(f"Note {n}:\n{clean}\n")
