import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\augus\.gemini\antigravity\brain\7153e055-b139-488b-ba66-90c1a4d194d9\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index')
        txt = json.dumps(data)
        if 'p241' in txt:
            calls = [c.get('name') for c in data.get('tool_calls', [])]
            print(f"Step {idx}: src={data.get('source')}, calls={calls}, th_len={len(data.get('thinking') or '')}, content_len={len(data.get('content') or '')}")
