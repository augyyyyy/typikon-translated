import re

doc_txt_path = "doc_text_binary.txt"
out_path = "doc_search_results.txt"

with open(doc_txt_path, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

output = []

# 1. Look for question marks and display their context
output.append("--- MATCHES WITH QUESTION MARKS ---\n")
q_matches = []
for idx, line in enumerate(lines):
    if '?' in line:
        q_matches.append(f"Line {idx}: {line.strip()}\n")
output.extend(q_matches[:50])

# 2. Look for keywords like "питання", "зауваження", "note", "question"
output.append("\n--- MATCHES WITH KEYWORDS ---\n")
keywords = ['питання', 'зауваж', 'уваг', 'note', 'question', 'side']
kw_matches = []
for idx, line in enumerate(lines):
    if any(kw in line.lower() for kw in keywords):
        kw_matches.append(f"Line {idx}: {line.strip()}\n")
output.extend(kw_matches[:50])

with open(out_path, 'w', encoding='utf-8') as out_f:
    out_f.writelines(output)

print(f"Wrote search results to {out_path}")
