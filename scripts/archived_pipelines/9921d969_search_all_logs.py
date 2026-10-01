import os
import json
import sys

# Force sys.stdout to be UTF-8
sys.stdout.reconfigure(encoding='utf-8')

brain_dir = r"C:\Users\augus\.gemini\antigravity\brain"
for conv_id in os.listdir(brain_dir):
    conv_dir = os.path.join(brain_dir, conv_id)
    if not os.path.isdir(conv_dir):
        continue
    log_path = os.path.join(conv_dir, ".system_generated", "logs", "transcript.jsonl")
    if not os.path.exists(log_path):
        continue
    
    with open(log_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            data = json.loads(line)
            content = data.get("content", "")
            if not content:
                continue
            c_lower = content.lower()
            if "general menaion" in c_lower and ("category" in c_lower or "categories" in c_lower or "badge" in c_lower or "forerunner" in c_lower):
                print(f"[{conv_id}][{idx}] Source: {data.get('source')} | Type: {data.get('type')}")
                print(content[:600])
                print("=" * 80)
