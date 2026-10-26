import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\augus\.gemini\antigravity\brain\7153e055-b139-488b-ba66-90c1a4d194d9\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index')
        if idx in [40, 42, 44, 46, 48, 50]:
            c = data.get('content') or ''
            print(f"=== STEP {idx} (len {len(c)}) ===")
            print(c[:300])
            print("...\n")
            with open(f"scratch/step_{idx}_content.txt", "w", encoding="utf-8") as out:
                out.write(c)
