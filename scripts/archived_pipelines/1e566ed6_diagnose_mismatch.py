import os

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
backup_path = os.path.join(typikon_dir, "backup", "Final_Dolnytsky_part1_structure.md")

with open(backup_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize
content = content.replace('\r\n', '\n').replace('\n', '\r\n')

# Check first target: Matins header around line 138-142
idx1 = content.find("ORDER OF Great Matins")
if idx1 != -1:
    print("Found 'ORDER OF Great Matins' at index:", idx1)
    print("Excerpt:")
    print(repr(content[idx1:idx1+800]))
else:
    print("'ORDER OF Great Matins' not found")

# Check second target: RUBRIC FOR DEACONS
idx2 = content.find("RUBRIC FOR DEACONS")
if idx2 != -1:
    print("\nFound 'RUBRIC FOR DEACONS' at index:", idx2)
    print("Excerpt:")
    print(repr(content[idx2:idx2+800]))
else:
    print("'RUBRIC FOR DEACONS' not found")
