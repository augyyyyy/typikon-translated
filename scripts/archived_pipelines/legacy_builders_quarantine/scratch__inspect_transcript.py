import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

p = r"C:\Users\augus\.gemini\antigravity\brain\bb3f56cd-feb9-4ffa-ac3c-d5170dd0aee0\.system_generated\logs\transcript_full.jsonl"

for line in open(p, encoding="utf-8"):
    d = json.loads(line)
    idx = d.get("step_index")
    content = d.get("content") or ""
    thinking = d.get("thinking") or ""
    all_text = content + thinking
    for q in ["unctio renum", "szőnyeg rá varrt sassal", "Benedictiones consecrativae", "Чинъ благословенія дѣтей", "Мюллер"]:
        if q in all_text:
            print(f"Step {idx} contains '{q}' (type={d.get('type')}, content_len={len(content)}, thinking_len={len(thinking)})")
            break
