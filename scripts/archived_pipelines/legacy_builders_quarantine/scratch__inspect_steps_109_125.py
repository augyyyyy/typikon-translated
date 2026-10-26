import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = Path(r'C:\Users\augus\.gemini\antigravity\brain\540274db-d170-4321-9789-715385cf6523\.system_generated\logs\transcript_full.jsonl')

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get('step_index')
        if idx in (109, 125):
            print(f'=== Step {idx} (type: {obj.get("type")}) ===')
            calls = obj.get('tool_calls', [])
            for c in calls:
                print('Tool call:', c.get('name'))
                args = c.get('args', {})
                for k, v in args.items():
                    if isinstance(v, str) and len(v) > 100:
                        print(f'  arg {k}: len {len(v)}: {v[:100]}...')
                    else:
                        print(f'  arg {k}: {v}')
