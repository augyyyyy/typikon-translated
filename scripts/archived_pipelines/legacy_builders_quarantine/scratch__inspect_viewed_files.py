import json
import os
from pathlib import Path
from collections import Counter

brain_dir = Path(os.environ.get('USERPROFILE', '')) / '.gemini/antigravity/brain'
sub_path = brain_dir / 'f9ae38f4-dcfb-47ae-ba0c-2208ac10acec' / '.system_generated/logs/transcript.jsonl'

viewed_files = []
with open(sub_path, 'r', encoding='utf-8') as f:
    for line in f:
        if not line.strip(): continue
        row = json.loads(line)
        for tc in row.get('tool_calls', []):
            if tc.get('name') == 'view_file':
                args = tc.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args)
                    except: args = {}
                viewed_files.append(args.get('AbsolutePath'))

print("Cohort 1 viewed files sample:")
for vf in viewed_files[:10]:
    print(" ", vf)
print(f"Total files viewed: {len(viewed_files)}")
