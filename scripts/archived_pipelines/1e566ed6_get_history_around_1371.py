import json

transcript_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\.system_generated\logs\transcript_full.jsonl"

steps = []
with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        idx = data.get("step_index", 0)
        if 1360 <= idx <= 1380:
            steps.append(data)

# Write output to file safely
out_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\history_context.txt"
with open(out_path, "w", encoding="utf-8") as f_out:
    for s in steps:
        f_out.write(f"=== STEP {s.get('step_index')} (Source: {s.get('source')}, Type: {s.get('type')}) ===\n")
        f_out.write(s.get("content", ""))
        f_out.write("\n\n" + "="*80 + "\n\n")

print(f"SUCCESS: Wrote steps 1360-1380 to {out_path}")
