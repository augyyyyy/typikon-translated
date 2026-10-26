import sys
from pathlib import Path
import re

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

p = Path(r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\..\..\..\..\..\..\.gemini\antigravity\brain\f226825a-f6a9-4f6d-9451-ef6f56dead8c\.system_generated\steps\97\content.md")
txt = p.read_text(encoding="utf-8")

matches = [m.start() for m in re.finditer(r'note416', txt)]
for m in matches:
    print(f"Match at {m}:\n{txt[max(0, m-50):min(len(txt), m+150)]}\n---")
