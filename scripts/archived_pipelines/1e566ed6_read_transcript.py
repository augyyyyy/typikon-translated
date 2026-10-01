import json

transcript_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\.system_generated\logs\transcript_full.jsonl"

target = 'And under each Numerical Section, how is the material "in between" broken up correctly. What are these lines.'

found = False
with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if target in str(data.get("content", "")):
            found = True
            print(f"Found match at step {data.get('step_index')}:")
            print(f"Source: {data.get('source')}, Type: {data.get('type')}")
            print("Content excerpt:")
            print(data.get("content")[:1000])
            print("="*40)
            
if not found:
    print("Not found by exact match, searching for substring 'Numerical Section'...")
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            content = str(data.get("content", ""))
            if "Numerical Section" in content or "What are these lines" in content:
                print(f"Found match at step {data.get('step_index')}:")
                print(f"Source: {data.get('source')}, Type: {data.get('type')}")
                print(content[:1000])
                print("="*40)
