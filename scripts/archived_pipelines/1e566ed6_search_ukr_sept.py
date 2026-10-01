doc_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_utf8.txt"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\ukr_dividers_context.txt"

try:
    with open(doc_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    out_lines = []
    
    # Let's search for "12 ВЕРЕСНЯ" or "14 ВЕРЕСНЯ" (case-insensitive)
    for idx, line in enumerate(lines):
        if "12 ВЕРЕСНЯ" in line or "14 ВЕРЕСНЯ" in line or "12 вересня" in line.lower() or "14 вересня" in line.lower():
            start = max(0, idx - 8)
            end = min(len(lines), idx + 8)
            out_lines.append(f"=== MATCH AT LINE {idx+1} ===")
            for i in range(start, end):
                prefix = "-> " if i == idx else "   "
                out_lines.append(f"{prefix}Line {i+1}: {lines[i].strip()}")
            out_lines.append("")
            
    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(out_lines))
        
    print(f"SUCCESS: Wrote matches to {output_path}")
except Exception as e:
    print(f"Error: {e}")
