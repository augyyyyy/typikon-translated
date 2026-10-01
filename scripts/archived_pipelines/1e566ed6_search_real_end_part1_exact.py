doc_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_real_word.txt"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\ukr_part1_end_real.txt"

try:
    with open(doc_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    found = False
    for idx, line in enumerate(lines):
        if idx < 300:
            continue
        if "ПРО ВЕЧІРНЮ З ЛІТУРГІЄЮ" in line:
            found = True
            start = max(0, idx - 15)
            end = min(len(lines), idx + 25)
            out_lines = []
            for i in range(start, end):
                out_lines.append(f"{i+1}: {lines[i].strip()}")
            with open(output_path, "w", encoding="utf-8") as f_out:
                f_out.write("\n".join(out_lines))
            print(f"SUCCESS: Wrote context from line {start+1} to {end} to {output_path}")
            break
    if not found:
        print("Not found 'ПРО ВЕЧІРНЮ З ЛІТУРГІЄЮ' in body")
except Exception as e:
    print(f"Error: {e}")
