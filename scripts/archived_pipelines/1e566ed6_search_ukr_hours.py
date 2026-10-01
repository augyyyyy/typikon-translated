doc_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_utf8.txt"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\ukr_hours_context.txt"

try:
    with open(doc_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines):
        # Skip the Table of Contents (first 300 lines)
        if idx < 300:
            continue
        if "ЧИН ЗВИЧАЙНИХ ЧАСІВ" in line or "ЗВИЧАЙНИХ ЧАСІВ" in line:
            start = max(0, idx - 10)
            end = min(len(lines), idx + 20)
            out_lines = []
            for i in range(start, end):
                out_lines.append(f"{i+1}: {lines[i].strip()}")
            with open(output_path, "w", encoding="utf-8") as f_out:
                f_out.write("\n".join(out_lines))
            print(f"SUCCESS: Wrote context starting from line {start+1} to {output_path}")
            break
except Exception as e:
    print(f"Error: {e}")
