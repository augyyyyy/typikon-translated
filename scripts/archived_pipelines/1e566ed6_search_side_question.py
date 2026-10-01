import json

path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\.system_generated\logs\transcript.jsonl"
steps = []
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        steps.append(json.loads(line))

output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\side_question_output.txt"
with open(output_path, "w", encoding="utf-8") as out:
    out.write(f"Total steps: {len(steps)}\n")
    for idx, step in enumerate(steps):
        if step.get('type') == 'USER_INPUT':
            content = step.get("content", "")
            if "side" in content.lower() or "typyk" in content.lower() or "google drive" in content.lower():
                out.write(f"\n================ USER INPUT STEP {step.get('step_index')} ================\n")
                out.write(content + "\n")
                # Find subsequent model responses
                for j in range(idx + 1, len(steps)):
                    next_step = steps[j]
                    if next_step.get('type') == 'USER_INPUT':
                        break
                    if next_step.get('source') == 'MODEL' and next_step.get('type') == 'PLANNER_RESPONSE':
                        out.write(f"--- MODEL RESPONSE (Step {next_step.get('step_index')}) ---\n")
                        out.write(next_step.get('content', '') + "\n")
print("Done writing search output.")
