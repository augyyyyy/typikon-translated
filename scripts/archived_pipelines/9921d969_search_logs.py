import json
import re
import sys

# Force sys.stdout to be UTF-8
sys.stdout.reconfigure(encoding='utf-8')

log_path = r"C:\Users\augus\.gemini\antigravity\brain\9921d969-3a5c-4531-a4b6-3e899725121a\.system_generated\logs\transcript.jsonl"
with open(log_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        data = json.loads(line)
        content = data.get("content", "")
        if not content:
            continue
        c_lower = content.lower()
        if "general menaion" in c_lower or "forerunner" in c_lower:
            print(f"[{idx}] Source: {data.get('source')} | Type: {data.get('type')}")
            # print first 500 characters
            print(content[:500])
            print("-" * 80)
