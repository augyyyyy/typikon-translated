import json

transcript_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\.system_generated\logs\transcript_full.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        content = str(data.get("content", ""))
        if "media__" in content or "1781275" in content or "178125" in content:
            print(f"=== STEP {data.get('step_index')} (Source: {data.get('source')}) ===")
            print(content[:1000])
            print("="*80)
