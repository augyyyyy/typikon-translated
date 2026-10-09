import sys
from pathlib import Path
import re

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

p = Path(r"C:\Users\augus\.gemini\antigravity\brain\f226825a-f6a9-4f6d-9451-ef6f56dead8c\.system_generated\steps\69\content.md")
txt = p.read_text(encoding="utf-8")
for i, line in enumerate(txt.splitlines()):
    if "век" in line.lower() or "завещ" in line.lower() or "href=" in line:
        if "href" in line:
            print(f"L{i}: {line[:120]}")
