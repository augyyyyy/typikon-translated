import json
import os
from pathlib import Path

brain_dir = Path(os.environ.get('USERPROFILE', '')) / '.gemini/antigravity/brain'
parent_transcript = brain_dir / 'b0cb1fdd-acd4-4d72-9ecf-0a57d18d2da2/.system_generated/logs/transcript.jsonl'

if not parent_transcript.exists():
    print(f"Parent transcript not found: {parent_transcript}")
    exit(1)

with open(parent_transcript, 'r', encoding='utf-8') as f:
    lines = [json.loads(line) for line in f if line.strip()]

print(f"Total steps in parent: {len(lines)}")

subagents = []
for idx, entry in enumerate(lines):
    for tc in entry.get('tool_calls', []):
        if tc.get('name') == 'invoke_subagent':
            next_step = lines[idx + 1] if idx + 1 < len(lines) else {}
            subagents.append({
                'step_index': entry.get('step_index'),
                'created_at': entry.get('created_at'),
                'args': tc.get('args'),
                'result': next_step.get('content')
            })

print(f"Total invoke_subagent calls: {len(subagents)}")
for idx, s in enumerate(subagents, 1):
    res = str(s['result'])[:100]
    print(f"Cohort #{idx} (Step {s['step_index']}, {s['created_at']}): Return='{res}'")

