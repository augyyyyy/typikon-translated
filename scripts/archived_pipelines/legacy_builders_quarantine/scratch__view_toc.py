import sys
from pathlib import Path
import re

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

p = Path(r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\..\..\..\..\..\..\.gemini\antigravity\brain\f226825a-f6a9-4f6d-9451-ef6f56dead8c\.system_generated\steps\69\content.md")
txt = p.read_text(encoding="utf-8")
for i, line in enumerate(txt.splitlines()):
    if '<a href="./' in line:
        m = re.search(r'href="\./([^"]+)"[^>]*><span class="([^"]+)">\s*([^<]+)\s*<', line)
        if m:
            ch, cls, title = m.groups()
            if cls == "h2o":
                print(f"Chapter {ch}: {title}")
