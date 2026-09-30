import os
import subprocess
from pathlib import Path

root = Path('.').resolve()
dest_parent = root / "Typikons" / "2010 Lviv Typikon"

items_to_move = [
    # Tracked directories
    "Final",
    "Final MD",
    "_brain",
    "Audit_Reports",
    "Ukrainian Original",
    "scratch",
    
    # Untracked/Ignored source directories
    "Ukrainian PDFs",
    "Ukrainian TXTs",
    "Typyk UHKC pdf jpgs",
    "English Broken",
    "English OC 1996",
    "Resources",
    
    # Root files
    "visual_audit_log.md",
    "comprehensive_audit.md",
    "typikon_deepseek_verifier.py",
    "typikon_deepseek_image_verifier.py"
]

items_to_stay_at_root = [
    ".agents",
    ".git",
    ".gitignore",
    "4 Liturgical Books",
    "__pycache__",
    "desktop.ini",
    "Typikons"
]

print("=" * 80)
print("REORGANIZATION PRE-FLIGHT AUDIT & INVENTORY MANIFEST")
print("=" * 80)

total_files_to_move = 0
total_bytes_to_move = 0
tracked_files_to_move = 0
untracked_files_to_move = 0

# Get all git-tracked files
git_files_raw = subprocess.check_output(['git', 'ls-files'], encoding='utf-8')
git_tracked_set = set(p.replace('\\', '/') for p in git_files_raw.splitlines() if p.strip())

print(f"\nTarget Destination: {dest_parent}\n")
print(f"{'Item Name':<35} | {'Type':<6} | {'Files':<8} | {'Size (MB)':<10} | {'Git Status':<12}")
print("-" * 80)

manifest_lines = []

for name in items_to_move:
    item_path = root / name
    if not item_path.exists():
        print(f"WARNING: {name} does not exist!")
        continue
    
    if item_path.is_file():
        file_count = 1
        size = item_path.stat().st_size
        rel_path = name.replace('\\', '/')
        is_tracked = rel_path in git_tracked_set
        git_status = "Tracked" if is_tracked else "Untracked"
        if is_tracked:
            tracked_files_to_move += 1
        else:
            untracked_files_to_move += 1
        total_files_to_move += 1
        total_bytes_to_move += size
        print(f"{name:<35} | {'FILE':<6} | {file_count:<8} | {size / (1024*1024):<10.2f} | {git_status:<12}")
        manifest_lines.append((str(item_path.relative_to(root)), str((dest_parent / name).relative_to(root)), git_status))
    else:
        # Directory
        f_count = 0
        d_size = 0
        t_count = 0
        u_count = 0
        for f in item_path.rglob('*'):
            if f.is_file():
                f_count += 1
                f_size = f.stat().st_size
                d_size += f_size
                rel_p = str(f.relative_to(root)).replace('\\', '/')
                if rel_p in git_tracked_set:
                    t_count += 1
                else:
                    u_count += 1
        total_files_to_move += f_count
        total_bytes_to_move += d_size
        tracked_files_to_move += t_count
        untracked_files_to_move += u_count
        status_summary = f"{t_count} trk / {u_count} untrk"
        print(f"{name:<35} | {'DIR':<6} | {f_count:<8} | {d_size / (1024*1024):<10.2f} | {status_summary:<12}")
        manifest_lines.append((str(item_path.relative_to(root)), str((dest_parent / name).relative_to(root)), status_summary))

print("-" * 80)
print(f"TOTALS TO MOVE:")
print(f"  Total Files:     {total_files_to_move}")
print(f"  Tracked Files:   {tracked_files_to_move}")
print(f"  Untracked Files: {untracked_files_to_move}")
print(f"  Total Size:      {total_bytes_to_move / (1024*1024):.2f} MB ({total_bytes_to_move:,} bytes)")
print("=" * 80)
