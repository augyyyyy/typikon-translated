import json
import os
import re
from pathlib import Path
from datetime import datetime

brain_dir = Path(os.environ.get('USERPROFILE', '')) / '.gemini/antigravity/brain'
parent_id = 'b0cb1fdd-acd4-4d72-9ecf-0a57d18d2da2'
parent_log = brain_dir / parent_id / '.system_generated/logs/transcript.jsonl'

with open(parent_log, 'r', encoding='utf-8') as f:
    parent_steps = [json.loads(line) for line in f if line.strip()]

cohorts = []
for idx, entry in enumerate(parent_steps):
    for tc in entry.get('tool_calls', []):
        if tc.get('name') == 'invoke_subagent':
            next_step = parent_steps[idx + 1] if idx + 1 < len(parent_steps) else {}
            content = next_step.get('content', '')
            match = re.search(r'"conversationId":\s*"([a-f0-9\-]+)"', content)
            cid = match.group(1) if match else None
            cohorts.append({
                'cohort_index': len(cohorts) + 1,
                'parent_step': entry.get('step_index'),
                'dispatched_at': entry.get('created_at'),
                'conversation_id': cid
            })

print(f"Discovered {len(cohorts)} subagent cohorts.")
total_sub_steps = 0
for c in cohorts:
    cid = c['conversation_id']
    sub_path = brain_dir / cid / '.system_generated/logs/transcript.jsonl' if cid else None
    exists = sub_path.exists() if sub_path else False
    lines_count = 0
    t_start = None
    t_end = None
    if exists:
        with open(sub_path, 'r', encoding='utf-8') as sf:
            for l in sf:
                if not l.strip(): continue
                lines_count += 1
                row = json.loads(l)
                if not t_start:
                    t_start = row.get('created_at')
                t_end = row.get('created_at')
        total_sub_steps += lines_count
    
    # Calculate duration
    dur_str = "N/A"
    if t_start and t_end:
        try:
            d1 = datetime.fromisoformat(t_start.replace('Z', '+00:00'))
            d2 = datetime.fromisoformat(t_end.replace('Z', '+00:00'))
            dur_mins = (d2 - d1).total_seconds() / 60.0
            dur_str = f"{dur_mins:.1f}m"
        except Exception:
            pass

    print(f"Cohort #{c['cohort_index']:02d}: ID={cid} | Steps={lines_count:3d} | Duration={dur_str:>6s} | Start={t_start}")
print(f"\nTotal subagent steps across all cohorts: {total_sub_steps}")
