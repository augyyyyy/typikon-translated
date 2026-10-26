import json

p = r"C:\Users\augus\.gemini\antigravity\brain\bb3f56cd-feb9-4ffa-ac3c-d5170dd0aee0\.system_generated\logs\transcript_full.jsonl"
for line in open(p, encoding="utf-8"):
    d = json.loads(line)
    idx = d.get("step_index")
    t = d.get("thinking") or ""
    if any(k in t for k in ["p273", "p274", "p275", "p276", "p277", "p278", "p279", "p280"]):
        print(f"Step {idx}: thinking len {len(t)}")
