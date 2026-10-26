import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\augus\.gemini\antigravity\brain\7153e055-b139-488b-ba66-90c1a4d194d9\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index')
        if idx is not None and 18 <= idx <= 40:
            th = data.get('thinking') or ''
            c = data.get('content') or ''
            print(f"Step {idx}: src={data.get('source')}, th_len={len(th)}, c_len={len(c)}")
