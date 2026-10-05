import os

root_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects"
exclude_dirs = {".git", "__pycache__", "Conversation_History", "Pre Update Chats", ".venv"}
exclude_extensions = {".png", ".jpg", ".jpeg", ".pdf", ".ini", ".zip", ".exe", ".pyc", ".png.metadata.json"}

found_files = []

for root, dirs, files in os.walk(root_dir):
    # Prune excluded directories in-place so os.walk does not descend into them
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        if any(file.endswith(ext) for ext in exclude_extensions):
            continue
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if 'gemini' in content.lower():
                    found_files.append(filepath)
                    print(f"FOUND: {filepath}")
        except Exception as e:
            pass

print(f"\nSearch complete. Found {len(found_files)} files containing 'gemini'.")
