import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\augus\.gemini\antigravity\brain\7153e055-b139-488b-ba66-90c1a4d194d9\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index')
        if idx in [51, 53, 55, 57, 59, 61]:
            calls = data.get('tool_calls', [])
            for c in calls:
                print(f"Step {idx}: tool={c.get('name')}, args={c.get('args')}")
