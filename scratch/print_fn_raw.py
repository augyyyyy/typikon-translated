import sys
from pathlib import Path
import re

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

p = Path(r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\..\..\..\..\..\..\.gemini\antigravity\brain\f226825a-f6a9-4f6d-9451-ef6f56dead8c\.system_generated\steps\97\content.md")
txt = p.read_text(encoding="utf-8")

notes = dict(re.findall(r'<a id="note(\d+)"><\/a>\s*<div class="note"><a href="#note\1_return"><sup>\1<\/sup><\/a><p class="txt">(.*?)<\/p><\/div>', txt, re.DOTALL))

for i in range(75, 108):
    azbyka_num = str(i + 341)
    cohort_fn = i - 75 + 415
    content = notes.get(azbyka_num, "NOT FOUND")
    clean = re.sub(r'<[^>]+>', '', content).strip()
    print(f"[^{cohort_fn}]: /* Orig. note [{i}] */ {clean}\n")
