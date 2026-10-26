import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\augus\.gemini\antigravity\brain\7153e055-b139-488b-ba66-90c1a4d194d9\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index')
        if idx == 59:
            th = data.get('thinking') or ''
            with open('scratch/step59_thinking.txt', 'w', encoding='utf-8') as out:
                out.write(th)
            print("Wrote scratch/step59_thinking.txt, len =", len(th))
            break
