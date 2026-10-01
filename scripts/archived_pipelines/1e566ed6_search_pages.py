import re

doc_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_utf8.txt"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\page_markers_results.txt"

try:
    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    lines = text.splitlines()
    matches = []
    
    # Match patterns like [123], [стор. 123], [стр. 123], стор. 123, стр. 123
    page_re = re.compile(r'(\[?\b(стор|стр)\b\.?\s*\d+\]?|\[\d+\])', re.IGNORECASE)
    
    for idx, line in enumerate(lines):
        if page_re.search(line):
            matches.append(f"Line {idx+1}: {line.strip()}")
            
    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(matches))
        
    print(f"SUCCESS: Found {len(matches)} page-related matches and wrote to {output_path}")

except Exception as e:
    print(f"Error: {e}")
