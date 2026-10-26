import json
from pathlib import Path

p = Path(r"C:\Users\augus\.gemini\antigravity\brain\6065af8a-b08e-4115-9081-aca661da1666\.system_generated\logs\transcript_full.jsonl")
with open(p, "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f]

for l in lines[40:75]:
    step_idx = l.get("step_index")
    tc = l.get("tool_calls", [])
    th = l.get("thinking", "")
    for c in tc:
        if c:
            print(f"Step {step_idx}: {c.get('name')} {c.get('args', {}).get('AbsolutePath', '')} {c.get('args', {}).get('CommandLine', '')}")
