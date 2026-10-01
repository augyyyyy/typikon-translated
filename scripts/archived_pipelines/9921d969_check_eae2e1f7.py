import json
import sys
import os

# Force sys.stdout to be UTF-8
sys.stdout.reconfigure(encoding='utf-8')

log_path = r"C:\Users\augus\.gemini\antigravity\brain\eae2e1f7-7ebf-4e30-81e3-0cce897ae257\.system_generated\logs\transcript_full.jsonl"
if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            data = json.loads(line)
            if data.get("source") != "USER_EXPLICIT":
                continue
            content = data.get("content", "")
            if not content:
                continue
            c_lower = content.lower()
            if "category" in c_lower or "categories" in c_lower or "general menaion" in c_lower or "forerunner" in c_lower:
                print(f"[eae2e1f7][{idx}] User Msg:")
                print(content[:600])
                print("=" * 80)
else:
    print("Log not found at", log_path)
