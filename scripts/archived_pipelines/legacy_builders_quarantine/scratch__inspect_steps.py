import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = Path(r'C:\Users\augus\.gemini\antigravity\brain\540274db-d170-4321-9789-715385cf6523\.system_generated\logs\transcript_full.jsonl')

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get('step_index')
        if idx and 150 <= idx <= 180:
            calls = obj.get('tool_calls', [])
            call_names = [c.get('name') for c in calls] if calls else []
            step_type = obj.get('type')
            print(f'Step {idx}: {step_type} - {call_names}')
