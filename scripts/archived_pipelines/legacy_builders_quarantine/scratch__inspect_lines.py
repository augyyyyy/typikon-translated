import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

user_home = Path(os.environ.get('USERPROFILE', ''))
transcript_full_path = user_home / '.gemini' / 'antigravity' / 'brain' / '6065af8a-b08e-4115-9081-aca661da1666' / '.system_generated' / 'logs' / 'transcript_full.jsonl'

lines = open(transcript_full_path, encoding='utf-8').readlines()
for l_idx in [41, 89, 172, 232, 244, 250]:
    if l_idx < len(lines):
        data = json.loads(lines[l_idx])
        typ = data.get('type')
        th = data.get('thinking', '') or ''
        c = data.get('content', '') or ''
        print(f"=== LINE {l_idx} (type={typ}) ===")
        print(f"thinking len: {len(th)}, content len: {len(c)}")
        if th:
            print("thinking preview:", th[:200].replace('\n', ' '))
        if c:
            print("content preview:", c[:200].replace('\n', ' '))
