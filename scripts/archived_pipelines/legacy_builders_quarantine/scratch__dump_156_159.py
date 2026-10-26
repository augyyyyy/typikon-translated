import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\augus\.gemini\antigravity\brain\7153e055-b139-488b-ba66-90c1a4d194d9\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in [156, 157, 158, 159]:
    data = json.loads(lines[idx])
    print(f"=== LINE {idx} ===")
    print("Source:", data.get('source'))
    content = data.get('content') or ''
    print("Content:", content[:500])
    print("Tool calls:", data.get('tool_calls'))
