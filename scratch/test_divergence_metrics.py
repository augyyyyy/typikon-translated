import json
import os
import re
from pathlib import Path
from collections import Counter

brain_dir = Path(os.environ.get('USERPROFILE', '')) / '.gemini/antigravity/brain'

test_cohort_ids = [
    ('Cohort #01', 'f9ae38f4-dcfb-47ae-ba0c-2208ac10acec'),
    ('Cohort #04', '0fc73f36-696b-4962-9b67-bdd997f76457'),
    ('Cohort #20', '30578717-3293-4799-8386-e47463de5676'),
    ('Cohort #29', '9c6e797c-65a3-47d7-b2f0-44485ac4e7d9'),
]

for label, cid in test_cohort_ids:
    sub_path = brain_dir / cid / '.system_generated/logs/transcript.jsonl'
    tool_counts = Counter()
    image_views = 0
    scratch_scripts_written = []
    gate_runs = 0
    gate_failures = 0
    
    with open(sub_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            row = json.loads(line)
            for tc in row.get('tool_calls', []):
                tname = tc.get('name')
                tool_counts[tname] += 1
                args = tc.get('args', {})
                if isinstance(args, str):
                    try: args = json.loads(args)
                    except: args = {}
                
                # Check image viewing
                if tname == 'view_file':
                    fpath = str(args.get('AbsolutePath', ''))
                    if fpath.lower().endswith(('.png', '.jpg', '.jpeg')):
                        image_views += 1
                
                # Check scratch script creation
                if tname in ('write_to_file', 'create_file'):
                    fpath = str(args.get('TargetFile', ''))
                    if 'scratch' in fpath or fpath.endswith('.py'):
                        scratch_scripts_written.append(Path(fpath).name)
                
                # Check gate runs
                if tname == 'run_command':
                    cmd = str(args.get('CommandLine', ''))
                    if any(k in cmd for k in ['lint_vocabulary', 'hieratic_pronoun', 'reconcile_footnotes', 'structural_audit', 'run_small_pause_gate']):
                        gate_runs += 1

            # Check if this row is tool output with error
            if row.get('type') == 'GENERIC':
                cnt = str(row.get('content', ''))
                if 'FAILED' in cnt or 'VIOLATION' in cnt or 'Exit code 1' in cnt:
                    if any(k in cnt for k in ['Gate', 'Linter', 'Audit', 'lint_vocabulary']):
                        gate_failures += 1

    print(f"\n--- {label} ({cid}) ---")
    print(f"  Tool counts: {dict(tool_counts)}")
    print(f"  Image views (view_file .png): {image_views}")
    print(f"  Scratch scripts created: {len(scratch_scripts_written)} -> {scratch_scripts_written[:4]}")
    print(f"  Gate executions: {gate_runs} (Detected Failures/Retries: {gate_failures})")
