import json
import os
from pathlib import Path

brain_dir = Path(os.environ.get('USERPROFILE', '')) / '.gemini/antigravity/brain'

for cid, label in [
    ('f9ae38f4-dcfb-47ae-ba0c-2208ac10acec', 'Cohort #01'),
    ('0fc73f36-696b-4962-9b67-bdd997f76457', 'Cohort #04'),
    ('30578717-3293-4799-8386-e47463de5676', 'Cohort #20'),
    ('9c6e797c-65a3-47d7-b2f0-44485ac4e7d9', 'Cohort #29'),
]:
    sub_path = brain_dir / cid / '.system_generated/logs/transcript.jsonl'
    images_viewed = set()
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
                    p = str(args.get('AbsolutePath', '')).strip('"\'')
                    if p.lower().endswith(('.png', '.jpg', '.jpeg')):
                        images_viewed.add(Path(p).name)
    print(f"{label}: Viewed {len(images_viewed)} images -> {sorted(list(images_viewed))}")
