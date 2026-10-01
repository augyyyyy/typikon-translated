import os

search_dir = r"E:\Google Drive\Liturgical Library\Typikon and Service Books\Typikon"
output_file = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\folder_contents.txt"

if os.path.exists(search_dir):
    files = os.listdir(search_dir)
    with open(output_file, "w", encoding="utf-8") as f:
        for item in files:
            f.write(f"{item}\n")
    print(f"SUCCESS: Wrote {len(files)} file names to {output_file}")
else:
    print(f"Directory does not exist: {search_dir}")
