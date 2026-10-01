import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

log_path = os.path.join(
    r"C:\Users\augus\.gemini\antigravity\brain\9921d969-3a5c-4531-a4b6-3e899725121a",
    ".system_generated",
    "logs",
    "transcript_full.jsonl"
)

summary_path = os.path.join(
    r"C:\Users\augus\.gemini\antigravity\brain\9921d969-3a5c-4531-a4b6-3e899725121a",
    "scratch",
    "chat_recap.txt"
)

with open(log_path, "r", encoding="utf-8") as f, open(summary_path, "w", encoding="utf-8") as out:
    for idx, line in enumerate(f):
        data = json.loads(line)
        source = data.get("source")
        type_ = data.get("type")
        content = data.get("content", "")
        
        # We look for user requests
        if source == "USER_EXPLICIT" and type_ == "USER_INPUT":
            out.write(f"=== TURN {idx} | USER_INPUT ===\n")
            out.write(content.strip() + "\n\n")
        
        # We look for final responses from the model to the user
        # In a step-by-step trajectory, model responses of type PLANNER_RESPONSE (which are not just intermediate thoughts)
        # or when the content is present and it doesn't contain tool calls, or just general planner responses.
        # Let's write any MODEL responses that have content and no tool calls, or just print content if it's longer.
        elif source == "MODEL" and type_ == "PLANNER_RESPONSE" and content:
            # Check if this step has any tool calls
            tool_calls = data.get("tool_calls", [])
            # If it's a final response or a significant thought
            if not tool_calls:
                out.write(f"=== TURN {idx} | MODEL_RESPONSE ===\n")
                # write first 1000 characters of response
                out.write(content.strip()[:1000] + "\n")
                if len(content) > 1000:
                    out.write(f"... [TRUNCATED {len(content)-1000} chars]\n")
                out.write("\n")

print(f"Recap summary written to {summary_path}")
