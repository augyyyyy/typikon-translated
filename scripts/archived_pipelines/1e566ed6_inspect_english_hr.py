import os

coded_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"

for file in sorted(os.listdir(coded_dir)):
    if file.endswith('.md') and not file.startswith('Dolnytsky_Typikon_Master'):
        path = os.path.join(coded_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        count = 0
        for idx, line in enumerate(lines):
            if "________________________________________" in line:
                count += 1
                print(f"=== Match {count} in {file} (Line {idx+1}) ===")
                start = max(0, idx - 4)
                end = min(len(lines), idx + 5)
                for i in range(start, end):
                    prefix = "-> " if i == idx else "   "
                    print(f"{prefix}{i+1}: {lines[i].strip()}")
                print()
                if count >= 3:
                    break
