import json
import sys

path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\.system_generated\logs\transcript.jsonl"
steps = []
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        steps.append(json.loads(line))

output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\last_steps.txt"
with open(output_path, "w", encoding="utf-8") as out:
    out.write(f"Total steps: {len(steps)}\n")
    user_indices = [idx for idx, step in enumerate(steps) if step.get('type') == 'USER_INPUT']
    out.write(f"Total user inputs: {len(user_indices)}\n")

    # Let's print the last 15 user inputs and the model's response to each
    for idx in user_indices[-15:]:
        step = steps[idx]
        out.write(f"\n================ USER INPUT STEP {step.get('step_index')} ================\n")
        out.write(str(step.get("content", "")) + "\n")
        
        # find subsequent MODEL response content (if any, before the next user input)
        next_user_idx = len(steps)
        for next_idx in user_indices:
            if next_idx > idx:
                next_user_idx = next_idx
                break
        
        # gather model outputs between idx and next_user_idx
        model_contents = []
        for j in range(idx + 1, next_user_idx):
            if steps[j].get('source') == 'MODEL' and steps[j].get('type') == 'PLANNER_RESPONSE':
                model_contents.append(steps[j].get('content', ''))
        if model_contents:
            out.write(f"---------------- MODEL RESPONSES ----------------\n")
            for mc in model_contents:
                out.write(str(mc) + "\n")
print("Done writing to last_steps.txt")


