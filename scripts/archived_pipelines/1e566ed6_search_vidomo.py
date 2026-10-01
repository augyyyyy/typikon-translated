import re

doc_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_utf8.txt"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\ukr_vidomo_context.txt"

try:
    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    lines = text.splitlines()
    matches = []
    
    # Search for "відомо" (case-insensitive)
    kw_re = re.compile(r'відомо', re.IGNORECASE)
    
    for idx, line in enumerate(lines):
        if kw_re.search(line):
            start = max(0, idx - 4)
            end = min(len(lines), idx + 5)
            matches.append(f"=== MATCH AT LINE {idx+1} ===")
            for i in range(start, end):
                prefix = "-> " if i == idx else "   "
                matches.append(f"{prefix}Line {i+1}: {lines[i].strip()}")
            matches.append("") # empty line separator
            
    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(matches))
        
    print(f"SUCCESS: Found {len(matches)//11} occurrences and wrote to {output_path}")

except Exception as e:
    print(f"Error: {e}")
