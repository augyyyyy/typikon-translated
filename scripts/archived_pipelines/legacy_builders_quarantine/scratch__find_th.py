import json
from pathlib import Path

p = Path(r"C:\Users\augus\.gemini\antigravity\brain\6065af8a-b08e-4115-9081-aca661da1666\.system_generated\logs\transcript_full.jsonl")
with open(p, "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f]

for l in lines:
    th = l.get("thinking", "")
    idx = l.get("step_index")
    if len(th) > 0:
        print(f"Step {idx}: len={len(th)}")
