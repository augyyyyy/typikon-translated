import json
from pathlib import Path

p = Path(r"C:\Users\augus\.gemini\antigravity\brain\6065af8a-b08e-4115-9081-aca661da1666\.system_generated\logs\transcript_full.jsonl")
with open(p, "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f]

for i, l in enumerate(lines):
    th = l.get("thinking", "")
    content = l.get("content", "")
    full = th + "\n" + content
    # check for transcription of p311, p312, etc.
    for p_num in range(311, 321):
        if f"p{p_num}" in full and ("===" in full or "<!-- LEAF:" in full or "ПАСХАЛ" in full):
            print(f"Step {l.get('step_index')}: mentions p{p_num}, len={len(full)}")
            break
