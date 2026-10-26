import json

with open(r'C:\Users\augus\.gemini\antigravity\brain\7153e055-b139-488b-ba66-90c1a4d194d9\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index')
        if idx is not None and 50 <= idx <= 76:
            calls = [c['name'] for c in data.get('tool_calls', [])]
            print(f"Step {idx}: {data.get('source')}, {data.get('type')}, calls={calls}, th={len(data.get('thinking') or '')}, c={len(data.get('content') or '')}")
