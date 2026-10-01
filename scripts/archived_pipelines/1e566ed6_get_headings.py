import os
typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
path = os.path.join(typikon_dir, "Final_Dolnytsky_part2_general_rubrics.md")
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
headings = [line.strip() for line in content.splitlines() if line.startswith('##')]
out_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\part2_headings.txt"
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(headings))
print("Saved part2 headings to", out_path)
