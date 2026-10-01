import os

coded_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
keywords = ["22", "23", "royal", "pre-feast", "eve", "question", "answer"]

matches = []
for file in os.listdir(coded_dir):
    if file.endswith('.md'):
        path = os.path.join(coded_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            line_lower = line.lower()
            if ("22" in line_lower or "23" in line_lower) and ("december" in line_lower or "royal" in line_lower or "pre-feast" in line_lower):
                matches.append(f"{file}:{idx+1}: {line.strip()}")
            elif "question:" in line_lower or "answer:" in line_lower:
                matches.append(f"{file}:{idx+1} [Q/A]: {line.strip()}")

print("Matches found:")
for m in matches[:50]:
    print(m)
