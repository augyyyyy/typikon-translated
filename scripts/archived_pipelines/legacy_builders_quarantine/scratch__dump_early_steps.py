import sys, json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
app_data = Path(r'C:\Users\augus\.gemini\antigravity\brain\6065af8a-b08e-4115-9081-aca661da1666\.system_generated\logs')
transcript_full_path = app_data / 'transcript_full.jsonl'

with open(transcript_full_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx in range(11, 35) or idx in range(164, 185):
            d = json.loads(line)
            source = d.get('source')
            stype = d.get('type')
            th = d.get('thinking', '') or ''
            ct = d.get('content', '') or ''
            calls = d.get('tool_calls', [])
            call_names = [c.get('name') for c in calls] if calls else []
            if th or ct or call_names:
                print(f"=== Step {idx}: source={source} type={stype} calls={call_names} ===")
                if th:
                    print(f"--- Thinking ({len(th)} chars) ---")
                    print(th[:500])
                    if len(th) > 500:
                        print("...")
                        print(th[-300:])
                if ct and source == 'MODEL':
                    print(f"--- Content ({len(ct)} chars) ---")
                    print(ct[:500])
                    if len(ct) > 500:
                        print("...")
                        print(ct[-300:])
