import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

cmd = Path('scratch/step_180_cmd.txt').read_text(encoding='utf-8')
# Print lines around the start and end of SOURCE_TEXT
lines = cmd.splitlines()
print(f'Total lines: {len(lines)}')
print('\n--- First 30 lines ---')
for l in lines[:30]:
    print(l)

print('\n--- Last 30 lines ---')
for l in lines[-30:]:
    print(l)
