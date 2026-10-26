import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\augus\.gemini\antigravity\brain\7153e055-b139-488b-ba66-90c1a4d194d9\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index')
        if idx in range(19, 39):
            th = data.get('thinking') or ''
            c = data.get('content') or ''
            media = data.get('media')
            print(f"Step {idx}: src={data.get('source')}, type={data.get('type')}, media={media}, th_len={len(th)}")
            if len(th) > 0:
                print(f"  Thinking snippet: {th[:250]}...")
