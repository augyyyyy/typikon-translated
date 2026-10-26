import sys, json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
app_data = Path(r'C:\Users\augus\.gemini\antigravity\brain\6065af8a-b08e-4115-9081-aca661da1666\.system_generated\logs')
transcript_full_path = app_data / 'transcript_full.jsonl'

with open(transcript_full_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx >= 330:
            data = json.loads(line)
            calls = data.get('tool_calls', [])
            for c in calls:
                print(f"Step {idx}: {c.get('name')}")
                cmd = c.get('args', {}).get('CommandLine')
                if cmd:
                    print(f"   CMD: {cmd}")
                p = c.get('args', {}).get('AbsolutePath')
                if p:
                    print(f"   PATH: {p}")
