import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = Path(r'C:\Users\augus\.gemini\antigravity\brain\540274db-d170-4321-9789-715385cf6523\.system_generated\logs\transcript_full.jsonl')

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get('step_index')
        s = json.dumps(obj)
        if '=== LEAF p441 ===' in s and obj.get('type') == 'PLANNER_RESPONSE':
            print(f'Step {idx} has LEAF p441 in PLANNER_RESPONSE')
