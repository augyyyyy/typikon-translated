import re

doc_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_utf8.txt"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\bracket_search_results.txt"

try:
    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    # Find anything inside square brackets or curly braces
    brackets = re.findall(r'\[([^\]]{3,})\]|\{([^\}]{3,})\}', text)
    
    out_lines = []
    for match in brackets:
        # Match is a tuple (square_bracket_content, curly_bracket_content)
        content = match[0] if match[0] else match[1]
        out_lines.append(content.strip())
        
    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(out_lines))
        
    print(f"SUCCESS: Found {len(out_lines)} bracketed segments and wrote to {output_path}")

except Exception as e:
    print(f"Error: {e}")
