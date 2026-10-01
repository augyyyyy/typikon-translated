import re

doc_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_utf8.txt"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\ukr_all_questions.txt"

try:
    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    lines = text.splitlines()
    matches = []
    
    # Search for "питання", "запитання", "відповідь" (case-insensitive)
    kw_re = re.compile(r'(питання|запитання|відповідь|відповіді|увага|примітка)', re.IGNORECASE)
    
    for idx, line in enumerate(lines):
        if kw_re.search(line):
            matches.append(f"Line {idx+1}: {line.strip()}")
            
    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(matches))
        
    print(f"SUCCESS: Found {len(matches)} matching lines and wrote to {output_path}")

except Exception as e:
    print(f"Error: {e}")
