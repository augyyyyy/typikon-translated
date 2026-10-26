import json
from pathlib import Path

p = Path(r"C:\Users\augus\.gemini\antigravity\brain\db11b78e-b866-44a1-8bfa-88d700d02897\.system_generated\logs\transcript_full.jsonl")
for i, line in enumerate(p.read_text(encoding="utf-8").splitlines()):
    obj = json.loads(line)
    for t in obj.get("tool_calls", []):
        name = t.get("name")
        args = t.get("args", {})
        if name == "run_command":
            cmd = args.get("CommandLine", "").strip().replace("\n", " ")[:120]
            print(f"step {i}: run_command -> {cmd}")
        elif name == "view_file":
            print(f"step {i}: view_file -> {args.get('AbsolutePath', '')}")
        elif name == "write_to_file":
            print(f"step {i}: write_to_file -> {args.get('TargetFile', '')}")
        elif name == "send_message":
            print(f"step {i}: send_message -> {args.get('Recipient', '')}")
        else:
            print(f"step {i}: {name}")
