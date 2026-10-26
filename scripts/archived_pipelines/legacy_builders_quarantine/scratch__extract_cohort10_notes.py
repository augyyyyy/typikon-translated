import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

step97 = Path(r"C:\Users\augus\.gemini\antigravity\brain\f226825a-f6a9-4f6d-9451-ef6f56dead8c\.system_generated\steps\97\content.md")
if not step97.exists():
    print("step97 not found")
    sys.exit(1)

txt = step97.read_text(encoding="utf-8")
pattern = r'<a id="note(\d+)"></a>\s*<div class="note"><a href="#note\1_return"><sup>\1</sup></a><p class="txt">(.*?)</p></div>'
matches = re.findall(pattern, txt, re.DOTALL)
print(f"Total notes found: {len(matches)}")
notes = dict(matches)

# Let's inspect available note keys
keys = sorted([int(k) for k in notes.keys()])
print(f"Key range: {min(keys)} to {max(keys)}")

# In cohort 9:
# i in range(75, 108):
# azbyka_num = str(i + 341)
# so for i=75: 75 + 341 = 416
# Let's check for i in range(108, 128): azbyka_num = i + 341
for i in range(108, 128):
    azbyka_num = str(i + 341)
    if azbyka_num in notes:
        clean = re.sub(r'<[^>]+>', '', notes[azbyka_num]).strip()
        print(f"Orig [{i}] (Azbyka {azbyka_num}): {clean}")
    else:
        print(f"Orig [{i}] (Azbyka {azbyka_num}): NOT FOUND")
