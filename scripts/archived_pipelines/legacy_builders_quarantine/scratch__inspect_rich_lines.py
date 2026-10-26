import sys, json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
app_data = Path(r'C:\Users\augus\.gemini\antigravity\brain\6065af8a-b08e-4115-9081-aca661da1666\.system_generated\logs')
transcript_full_path = app_data / 'transcript_full.jsonl'

target_lines = [250, 252, 254, 278, 280, 282, 286, 292]

with open(transcript_full_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx in target_lines:
            data = json.loads(line)
            c = data.get('content', '')
            print(f"=== Line {idx}: length={len(c)} ===")
            print(c[:400])
            print("...")
            print(c[-300:])
