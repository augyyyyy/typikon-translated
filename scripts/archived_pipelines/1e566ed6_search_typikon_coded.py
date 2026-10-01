import os

coded_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
keywords = ["question", "side", "питання"]

matches = []

for root, dirs, files in os.walk(coded_dir):
    for file in files:
        if file.endswith('.md') or file.endswith('.txt'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                for idx, line in enumerate(lines):
                    if any(kw in line.lower() for kw in keywords):
                        # Filter out common false positives like "inside" or "outside" unless they contain the word "question"
                        if "side" in line.lower() and not any(w in line.lower() for w in ["inside", "outside", "sideline"]):
                            matches.append(f"{file}:{idx+1}: {line.strip()}\n")
                        elif "question" in line.lower() or "питання" in line.lower():
                            matches.append(f"{file}:{idx+1}: {line.strip()}\n")
            except Exception as e:
                pass

out_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\coded_search_results.txt"
with open(out_path, 'w', encoding='utf-8') as out_f:
    out_f.writelines(matches)

print(f"Wrote {len(matches)} matches to {out_path}")
