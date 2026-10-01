import os
import sys

def main():
    typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
    debug_txt = os.path.join(typikon_dir, "all_headings_debug.txt")
    
    with open(debug_txt, 'r', encoding='utf-8') as f:
        content = f.read()
        
    enc = sys.stdout.encoding or 'utf-8'
    
    parts = content.split("========================================")
    for i in range(len(parts)):
        part = parts[i]
        if any(f in part for f in ["part5_temple", "appendix", "glossary"]):
            print("========================================")
            print(part.strip().encode(enc, errors='replace').decode(enc))
            if i + 1 < len(parts):
                next_lines = parts[i+1].splitlines()
                to_print = "\n".join(next_lines[:50])
                print(to_print.encode(enc, errors='replace').decode(enc))
                if len(next_lines) > 50:
                    print(f"... and {len(next_lines)-50} more lines")

if __name__ == "__main__":
    main()
