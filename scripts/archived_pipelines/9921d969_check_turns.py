import json
import sys

# Force sys.stdout to be UTF-8
sys.stdout.reconfigure(encoding='utf-8')

log_path = r"C:\Users\augus\.gemini\antigravity\brain\9921d969-3a5c-4531-a4b6-3e899725121a\.system_generated\logs\transcript_full.jsonl"
with open(log_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if 790 <= idx <= 920:
            data = json.loads(line)
            content = data.get("content", "")
            if not content:
                continue
            print(f"[{idx}] Source: {data.get('source')} | Type: {data.get('type')}")
            print(content[:500])
            print("=" * 80)
