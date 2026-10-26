import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\augus\.gemini\antigravity\brain\7153e055-b139-488b-ba66-90c1a4d194d9\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index')
        th = data.get('thinking') or ''
        c = data.get('content') or ''
        if len(th) > 500:
            print(f"Step {idx}: thinking len = {len(th)}")
        if len(c) > 2000 and data.get('source') == 'MODEL' and not c.startswith('Created At:'):
            print(f"Step {idx}: content len = {len(c)}")
