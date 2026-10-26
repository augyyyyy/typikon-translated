import json
from pathlib import Path

p = Path(r"C:\Users\augus\.gemini\antigravity\brain\6065af8a-b08e-4115-9081-aca661da1666\.system_generated\logs\transcript_full.jsonl")
with open(p, "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f]

for idx in [41, 47, 53]:
    for l in lines:
        if l.get("step_index") == idx:
            out_p = Path(f"scratch/step_{idx}_dump.txt")
            out_p.write_text(l.get("thinking", "") + "\n\n" + l.get("content", ""), encoding="utf-8")
            print(f"Wrote {out_p} ({out_p.stat().st_size} bytes)")
