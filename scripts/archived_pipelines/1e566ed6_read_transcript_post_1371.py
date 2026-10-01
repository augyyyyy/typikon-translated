import json

transcript_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\.system_generated\logs\transcript_full.jsonl"

steps_to_print = []
collecting = False
with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        idx = data.get("step_index", 0)
        if idx >= 1371:
            steps_to_print.append(data)
        if idx > 1395:
            break

for s in steps_to_print:
    print(f"Step {s.get('step_index')} | Source: {s.get('source')} | Type: {s.get('type')}")
    content = s.get("content", "")
    if content:
        # print up to 500 chars
        print("Content:")
        print(content[:600])
        print("-" * 50)
