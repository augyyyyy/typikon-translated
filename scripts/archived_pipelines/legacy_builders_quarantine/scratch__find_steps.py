import json
from pathlib import Path

p = Path(r"C:\Users\augus\.gemini\antigravity\brain\6065af8a-b08e-4115-9081-aca661da1666\.system_generated\logs\transcript_full.jsonl")
with open(p, "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f]

for i in range(len(lines)):
    step = lines[i]
    step_idx = step.get("step_index")
    th = step.get("thinking", "")
    content = step.get("content", "")
    calls = step.get("tool_calls", [])
    if any(k in th for k in ["Table I", "Table II", "Table III", "ПАСХАЛІА", "ІНДИКТІОНЪ", "§. 221", "p311", "p312", "p313", "p314", "p315", "p316", "p317", "p318", "p319", "p320"]):
        print(f"Step {step_idx}: th_len={len(th)}, content_len={len(content)}")
