doc_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_utf8.txt"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\ukr_search_output.txt"

try:
    with open(doc_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines):
        if "царські маси" in line or "22 ми 23 грудня" in line:
            start = max(0, idx - 15)
            end = min(len(lines), idx + 15)
            out_lines = []
            for i in range(start, end):
                out_lines.append(f"{i+1}: {lines[i].strip()}")
            with open(output_path, "w", encoding="utf-8") as f_out:
                f_out.write("\n".join(out_lines))
            print(f"SUCCESS: Wrote context lines {start+1} to {end} to {output_path}")
            break
except Exception as e:
    print(f"Error: {e}")
