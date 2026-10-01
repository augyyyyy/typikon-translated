doc1 = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_utf8.txt"
doc2 = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_real_word.txt"

with open(doc1, "r", encoding="utf-8") as f1:
    t1 = f1.read()
    
with open(doc2, "r", encoding="utf-8") as f2:
    t2 = f2.read()

lines = t2.splitlines()
q_lines = []
for idx, line in enumerate(lines):
    if "?" in line:
        q_lines.append(f"Line {idx+1}: {line.strip()}")

output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\comparison_results.txt"
with open(output_path, "w", encoding="utf-8") as f_out:
    f_out.write(f"DOCX extracted text length: {len(t1)}\n")
    f_out.write(f"DOC COM extracted text length: {len(t2)}\n")
    f_out.write(f"Found {len(q_lines)} question marks in DOC COM extracted text:\n")
    for q in q_lines:
        f_out.write(f"{q}\n")

print("SUCCESS: Wrote comparison results to file.")
