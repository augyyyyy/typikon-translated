import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_path = r"C:\Users\augus\.gemini\antigravity\brain\9921d969-3a5c-4531-a4b6-3e899725121a\System_generated\logs\transcript_full.jsonl"
# Note: folder name might be case-sensitive or not on Windows, but the standard path has '.system_generated'
import os
log_path = os.path.join(r"C:\Users\augus\.gemini\antigravity\brain\9921d969-3a5c-4531-a4b6-3e899725121a", ".system_generated", "logs", "transcript_full.jsonl")

with open(log_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if idx in (795, 885):
            data = json.loads(line)
            print(f"[{idx}] Source: {data.get('source')} | Type: {data.get('type')}")
            print(data.get('content'))
            print("=" * 80)
