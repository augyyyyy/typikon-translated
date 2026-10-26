import os
import sys
import re
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

raw_path = Path("scratch/cohort99_source_raw.txt")
raw_text = raw_path.read_text(encoding='utf-8')

# Check potential OCR errors across all leaves
suspicious = [
    r'Luﬂ',
    r'Мансвегпов',
    r'Сип\.',
    r'Сев\.',
    r'Тмуитск',
    r'obserwat',
    r'11, 119',
    r'ΰμνωι',
    r'Τυπικών',
    r'εκτείναте',
    r'εти'
]

for pat in suspicious:
    matches = list(re.finditer(pat, raw_text))
    print(f"Pattern '{pat}': {len(matches)} matches")
    for m in matches:
        start = max(0, m.start() - 30)
        end = min(len(raw_text), m.end() + 30)
        print(f"  Context: {raw_text[start:end].replace(chr(10), ' ')}")
