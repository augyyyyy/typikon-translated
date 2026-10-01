doc_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_utf8.txt"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\ukr_first_100.txt"

try:
    with open(doc_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    out_lines = []
    # Take first 200 lines to see headers, table of contents, and early text
    for i in range(min(len(lines), 200)):
        out_lines.append(f"Line {i+1}: {lines[i].strip()}")
        
    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(out_lines))
        
    print(f"SUCCESS: Wrote first 200 lines to {output_path}")

except Exception as e:
    print(f"Error: {e}")
