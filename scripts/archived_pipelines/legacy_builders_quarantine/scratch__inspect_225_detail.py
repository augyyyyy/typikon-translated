import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = Path(r'C:\Users\augus\.gemini\antigravity\brain\540274db-d170-4321-9789-715385cf6523\.system_generated\logs\transcript_full.jsonl')

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get('step_index')
        if idx in (225, 226, 247, 248):
            print(f'=== Step {idx} (type: {obj.get("type")}) ===')
            if obj.get('tool_calls'):
                for c in obj['tool_calls']:
                    args = c.get('args', {})
                    print('TargetFile:', args.get('TargetFile'))
                    print('Length of CodeContent:', len(args.get('CodeContent', '')))
            if obj.get('content'):
                print('Content:', obj.get('content')[:300])
