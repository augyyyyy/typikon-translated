import json
from pathlib import Path

p = Path(r"C:\Users\augus\.gemini\antigravity\brain\c40d0340-aef8-4cd9-866a-867f4ec4f13e\.system_generated\logs\transcript_full.jsonl")
with open(p, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if idx == 51:
            data = json.loads(line)
            t = data.get("thinking", "")
            out_p = Path("scratch/step51_thinking.txt")
            out_p.write_text(t, encoding="utf-8")
            print(f"Wrote {len(t)} characters to {out_p}")
