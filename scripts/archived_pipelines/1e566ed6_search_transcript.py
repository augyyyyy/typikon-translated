import json

log_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\.system_generated\logs\transcript.jsonl"
out_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\search_results_transcript.txt"

matches = []
with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        data = json.loads(line)
        content = data.get('content', '')
        step_type = data.get('type', '')
        
        # Search for words of interest
        if any(term in content.lower() for term in ['uhkc', 'typyk', 'original doc', 'original document']):
            matches.append(f"Step {idx} ({step_type}): {content}\n")

with open(out_path, 'w', encoding='utf-8') as out_f:
    out_f.writelines(matches)
print(f"Wrote {len(matches)} matches to {out_path}")
