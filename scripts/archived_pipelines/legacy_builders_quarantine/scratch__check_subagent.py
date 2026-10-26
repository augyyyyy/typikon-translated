import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
p = Path(r"C:/Users/augus/.gemini/antigravity/brain/6551bd52-ad87-46e5-962b-4fc02ea07eb8/.system_generated/logs/transcript.jsonl")
if not p.exists():
    print("Transcript does not exist.")
    sys.exit(0)

lines = p.read_text(encoding='utf-8').strip().splitlines()
print(f"Total lines: {len(lines)}")
for line in lines[-6:]:
    d = json.loads(line)
    step_idx = d.get("step_index")
    stype = d.get("type")
    src = d.get("source")
    print(f"Step {step_idx} [{src} : {stype}]")
    if "tool_calls" in d:
        for tc in d["tool_calls"]:
            name = tc.get("name")
            args = tc.get("args", {})
            summary = tc.get("toolSummary") or tc.get("toolAction") or ""
            target = args.get("TargetFile") or args.get("CommandLine") or args.get("AbsolutePath") or ""
            print(f"  -> {name} ({summary}): {str(target)[:80]}")
    if d.get("content"):
        c = d["content"]
        if len(c) > 200:
            print(f"  Content preview: {c[:150]}...{c[-50:]}")
        else:
            print(f"  Content: {c}")
