import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\augus\.gemini\antigravity\brain\7153e055-b139-488b-ba66-90c1a4d194d9\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        idx = data.get('step_index')
        if idx in [157, 159]:
            print(f"Line {i}: step {idx}, src={data.get('source')}, content_len={len(data.get('content') or '')}")
