import re
import json
import os

def parse_en_footnotes(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Pattern matches ^[n], [n], or ¹ at start of lines
    pattern = re.compile(r'(?:^\^\[(\d+)\]|^\s*\[(\d+)\]|^¹)', re.MULTILINE)
    matches = list(pattern.finditer(content))
    notes = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(content)
        note_content = content[start:end].strip()
        # Extract numbering if exist
        num = match.group(1) or match.group(2) or '1'
        # Remove the marker from start of the string to get the text
        clean_text = re.sub(r'^(?:\^\[\d+\]|\[\d+\]|¹)\s*', '', note_content)
        notes.append({'orig_num': num, 'text': clean_text, 'full_note': note_content})
    return notes

def parse_ua_footnotes(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    notes = []
    for i, line in enumerate(lines):
        text = line.strip()
        if text:
            notes.append({'num': i + 1, 'text': text})
    return notes

def reconcile():
    en_path = 'e:/Google Antigravity/Projects/Translation/English Broken/footnotes.txt'
    ua_path = 'e:/Google Antigravity/Projects/Translation/Ukrainian TXTs/Footnotes.txt'
    
    en_notes = parse_en_footnotes(en_path)
    ua_notes = parse_ua_footnotes(ua_path)
    
    print(f"Loaded {len(en_notes)} English notes and {len(ua_notes)} Ukrainian notes.")
    
    mapping = []
    # Initial naive 1-to-1 mapping to see divergence
    # We will use the [n] in English as a hint
    
    en_map = {int(n['orig_num']): n for n in en_notes if n['orig_num'].isdigit()}
    # Correction for the '¹' case which is index 1
    if not 1 in en_map and en_notes and '¹' in en_notes[0]['full_note']:
        en_map[1] = en_notes[0]

    report = []
    for i in range(1, len(ua_notes) + 1):
        ua_note = ua_notes[i-1]
        en_note = en_map.get(i)
        
        status = "MATCH" if en_note else "MISSING"
        report.append({
            'ua_num': i,
            'ua_text': ua_note['text'][:100],
            'en_text': en_note['text'][:100] if en_note else "---",
            'status': status
        })

    with open('e:/Google Antigravity/Projects/Translation/scratch/footnote_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    missing_count = sum(1 for r in report if r['status'] == "MISSING")
    print(f"Report generated. Missing English notes found: {missing_count}")

if __name__ == "__main__":
    reconcile()
