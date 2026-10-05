import re
import os

def check_missing_footnotes():
    en_footnotes_path = r'e:\Google Antigravity\Projects\Translation\English Broken\footnotes.txt'
    with open(en_footnotes_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extract all footnote numbers
    numbers = []
    # Pattern matches ^[n], [n], or ¹ at start of lines
    for m in re.finditer(r'(?:^\^\[|^\s*\[|^¹)(\d+)?(?(1)\]|)', text, re.MULTILINE):
        if m.group(1):
            numbers.append(int(m.group(1)))
        else:
            numbers.append(1)

    missing = set(range(1, 803)) - set(numbers)
    print(f'Missing {len(missing)} footnotes in English Broken/footnotes.txt.')

    # Let's search for these missing footnotes in the RAW files
    raw_dir = r'e:\Google Antigravity\Projects\Translation\RAW'
    found_in_raw = []
    for f in os.listdir(raw_dir):
        if not f.endswith('.txt'): continue
        path = os.path.join(raw_dir, f)
        with open(path, 'r', encoding='utf-8') as raw_file:
            raw_text = raw_file.read()
            # look for [N] or ^[N] followed by text at the start of a line
            for missing_num in missing:
                pattern = re.compile(rf'(?:^\^\[{missing_num}\]|^\s*\[{missing_num}\])(.*)', re.MULTILINE)
                for match in pattern.finditer(raw_text):
                    found_in_raw.append((missing_num, f, match.group(1).strip()[:100]))

    print(f'Found {len(found_in_raw)} of the missing footnotes in RAW files.')
    for fn in sorted(found_in_raw, key=lambda x: x[0]):
        print(f'[{fn[0]}] {fn[1]}: {fn[2]}')

if __name__ == "__main__":
    check_missing_footnotes()
