import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
final_dir = r'e:\Google Antigravity\Projects\Translation\Final'
for name in sorted(os.listdir(final_dir)):
    if not name.endswith('.txt'): continue
    with open(os.path.join(final_dir, name), 'r', encoding='utf-8') as f:
        text = f.read()
    if '[^3]' in text:
        for i, line in enumerate(text.split('\n'), 1):
            if '[^3]' in line:
                idx = line.index('[^3]')
                snippet = line[max(0,idx-50):idx+10]
                print(f'{name} line {i}: ...{snippet}...')
