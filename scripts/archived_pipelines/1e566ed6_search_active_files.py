import os

coded_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\active_search_results.txt"

matches = []
for file in os.listdir(coded_dir):
    if file.endswith('.md'):
        path = os.path.join(coded_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            if "Royal Hours are transferred" in line or "22 or 23 December" in line:
                matches.append(f"{file} | Line {idx+1}: {line.strip()}")

with open(output_path, "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(matches))

print(f"SUCCESS: Found {len(matches)} matches. Wrote to {output_path}")
