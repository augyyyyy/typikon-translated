import sys, json, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
app_data = Path(r'C:\Users\augus\.gemini\antigravity\brain\6065af8a-b08e-4115-9081-aca661da1666\.system_generated\logs')
transcript_full_path = app_data / 'transcript_full.jsonl'

# Look through thinking and content in steps for leaves p311 - p320
found_transcriptions = {}
with open(transcript_full_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        data = json.loads(line)
        th = data.get('thinking', '') or ''
        ct = data.get('content', '') or ''
        text = th + '\n' + ct
        for leaf in range(311, 321):
            tag = f'p{leaf}'
            if f'LEAF {tag}' in text or f'LEAF: {tag}' in text or f'=== LEAF {tag} ===' in text or f'<!-- LEAF: {tag} -->' in text:
                if leaf not in found_transcriptions:
                    found_transcriptions[leaf] = []
                found_transcriptions[leaf].append(idx)

for leaf, steps in found_transcriptions.items():
    print(f"Leaf p{leaf}: seen in steps {steps}")
