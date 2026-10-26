import json
from pathlib import Path

p = Path(r"C:\Users\augus\.gemini\antigravity\brain\6065af8a-b08e-4115-9081-aca661da1666\.system_generated\logs\transcript_full.jsonl")
with open(p, "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f]

for l in lines:
    if l.get("step_index") == 89:
        Path("scratch/step_89_dump.txt").write_text(l.get("content", ""), encoding="utf-8")
        print("Wrote scratch/step_89_dump.txt")
