#!/usr/bin/env python3
"""
Ships all finalized translation files to the Hub's inbox:
C:/Users/augus/OneDrive/Documents/Google Antigravity/Projects/Typikon Coded/Data/Inbox/
"""
import os
import shutil

# Directories
script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(script_dir)
final_dir = os.path.join(workspace_dir, 'Final')
inbox_dir = "C:/Users/augus/OneDrive/Documents/Google Antigravity/Projects/Typikon Coded/Data/Inbox"

print(f"Source Final Dir: {final_dir}")
print(f"Destination Inbox Dir: {inbox_dir}")

# Ensure destination exists
os.makedirs(inbox_dir, exist_ok=True)

files_to_copy = [
    f for f in os.listdir(final_dir)
    if os.path.isfile(os.path.join(final_dir, f)) and f.lower() != 'desktop.ini'
]

print(f"\nFound {len(files_to_copy)} files to ship:")
for f in files_to_copy:
    src = os.path.join(final_dir, f)
    dst = os.path.join(inbox_dir, f)
    shutil.copy2(src, dst)
    print(f"  Copied: {f} -> {dst}")

print("\nShipping completed successfully!")
