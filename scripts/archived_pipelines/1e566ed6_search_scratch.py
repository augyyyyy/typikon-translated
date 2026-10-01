import os

scratch_dir = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch"

for root, dirs, files in os.walk(scratch_dir):
    for file in files:
        if file.endswith('.py') or file.endswith('.txt') or file.endswith('.md'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if "apply_citation" in content:
                    print(f"Found reference in: {path}")
            except Exception as e:
                pass
