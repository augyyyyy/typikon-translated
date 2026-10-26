import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = Path(r'C:\Users\augus\.gemini\antigravity\brain\540274db-d170-4321-9789-715385cf6523\.system_generated\logs\transcript_full.jsonl')

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('step_index') == 180:
            thinking = obj.get('thinking', '')
            print(f'Thinking length: {len(thinking)}')
            # Search for draft or footnotes in thinking
            print('Thinking sample around draft:')
            for line_t in thinking.splitlines():
                if any(k in line_t for k in ['DRAFT', 'raw_draft', 'footnotes', 'Footnotes', '=== LEAF p442']):
                    print(line_t[:120])
            
            tool_calls = obj.get('tool_calls', [])
            print(f'Number of tool calls: {len(tool_calls)}')
            for i, tc in enumerate(tool_calls):
                cmd = tc.get('args', {}).get('CommandLine', '')
                print(f'Tool call {i}: length {len(cmd)}')
            break
