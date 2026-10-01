import os
import shutil
from pathlib import Path

binder_dir = r'E:\Google Drive\Parish Administration\St Josaphat Parish Choir Materials\Liturgical Booklets\02_Binder_1_The_Divine_Office'
artifacts_dir = r'C:\Users\augus\.gemini\antigravity\brain\9686e761-280f-434e-9d19-e1c17478fcc5'

print("--- PURGING OLD MD FILES ---")
for md_file in Path(binder_dir).rglob("*.md"):
    print(f"Deleting: {md_file}")
    md_file.unlink()

print("\n--- DEPLOYING NEW FILES ---")
target_mapping = {
    'Great_Vespers': r'1_The_Great_Ordo\1.1_Great_Vespers',
    'Daily_Vespers': r'2_The_Daily_Ordo\2.1_Daily_Vespers',
    'Small_Vespers': r'2_The_Daily_Ordo\2.1_Daily_Vespers',
    'Great_Matins': r'1_The_Great_Ordo\1.4_Great_Matins',
    'Daily_Matins': r'2_The_Daily_Ordo\2.4_Daily_Matins',
    'Great_Compline': r'1_The_Great_Ordo\1.2_Great_Compline',
    'Small_Compline': r'2_The_Daily_Ordo\2.2_Small_Compline',
    'Sunday_Midnight_Office': r'1_The_Great_Ordo\1.3_Sunday_Midnight_Office',
    'Daily_Midnight_Office': r'2_The_Daily_Ordo\2.3_Daily_Midnight_Office',
    'Saturday_Midnight_Office': r'2_The_Daily_Ordo\2.3_Daily_Midnight_Office',
    'First_Hour': r'2_The_Daily_Ordo\2.5_The_Hours',
    'Third_Hour': r'2_The_Daily_Ordo\2.5_The_Hours',
    'Sixth_Hour': r'2_The_Daily_Ordo\2.5_The_Hours',
    'Ninth_Hour': r'2_The_Daily_Ordo\2.5_The_Hours'
}

for prefix, rel_path in target_mapping.items():
    dest_dir = os.path.join(binder_dir, rel_path)
    
    for suffix in ['_Audit_Report.md', '_Edit_Script.md']:
        filename = prefix + suffix
        src = os.path.join(artifacts_dir, filename)
        dest = os.path.join(dest_dir, filename)
        
        if os.path.exists(src):
            shutil.copy2(src, dest)
            print(f"Deployed: {filename} -> {dest_dir}")
        else:
            print(f"ERROR: {filename} not found in artifacts!")

print("\nDEPLOYMENT COMPLETE.")
