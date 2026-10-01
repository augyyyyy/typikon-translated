import json
from pathlib import Path

def main():
    p = Path("C:/Users/augus/.gemini/antigravity/brain/960bb940-280e-4e01-8bf8-55bdfe4cfe4d/.system_generated/logs/transcript.jsonl")
    if not p.exists():
        print("Transcript does not exist")
        return
        
    with open(p, "r", encoding="utf-8") as f:
        for i in range(3):
            line = f.readline()
            if not line:
                break
            try:
                data = json.loads(line)
                print(f"--- Line {i+1} ---")
                print("Keys:", data.keys())
                print("Source:", data.get("source"))
                print("Type:", data.get("type"))
                content = data.get("content", "")
                if content:
                    print("Content preview:", content[:200])
                tool_calls = data.get("tool_calls", [])
                if tool_calls:
                    print("Tool calls:", len(tool_calls))
            except Exception as e:
                print(f"Error parsing line: {e}")

if __name__ == "__main__":
    main()
