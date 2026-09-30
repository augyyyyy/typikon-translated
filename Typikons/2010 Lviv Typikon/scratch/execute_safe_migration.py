import os
import shutil
import subprocess
from pathlib import Path

root = Path('.').resolve()
dest_dir = root / "Typikons" / "2010 Lviv Typikon"

# Target root items to migrate into dest_dir
items_to_migrate = [
    # Deliverables
    "Final",
    "Final MD",
    
    # Metadata & Audits
    "_brain",
    "Audit_Reports",
    "visual_audit_log.md",
    "comprehensive_audit.md",
    
    # Scripts & Tools
    "scratch",
    "typikon_deepseek_verifier.py",
    "typikon_deepseek_image_verifier.py",
    
    # Primary Source Corpora & Raw Scans
    "Ukrainian Original",
    "Ukrainian PDFs",
    "Ukrainian TXTs",
    "Typyk UHKC pdf jpgs",
    "English Broken",
    "English OC 1996",
    "Resources"
]

print("=" * 80)
print("EXECUTING DETERMINISTIC REORGANIZATION INTO Typikons/2010 Lviv Typikon/")
print("=" * 80)

# 1. Pre-flight file list
pre_files = {}
for item in items_to_migrate:
    src_path = root / item
    if not src_path.exists():
        continue
    if src_path.is_file():
        pre_files[src_path.relative_to(root)] = src_path.stat().st_size
    else:
        for f in src_path.rglob('*'):
            if f.is_file():
                pre_files[f.relative_to(root)] = f.stat().st_size

print(f"Pre-flight file count: {len(pre_files)} files ({sum(pre_files.values()):,} bytes)")

# 2. Get list of all tracked files
git_files_raw = subprocess.check_output(['git', 'ls-files'], encoding='utf-8')
tracked_files = set(p.replace('\\', '/') for p in git_files_raw.splitlines() if p.strip())

# 3. Create destination folder
dest_dir.mkdir(parents=True, exist_ok=True)
print(f"Created destination directory: {dest_dir.relative_to(root)}")

# 4. Migrate item by item
for item_name in items_to_migrate:
    src_item = root / item_name
    if not src_item.exists():
        print(f"Skipping non-existent: {item_name}")
        continue
        
    dst_item = dest_dir / item_name
    
    if src_item.is_file():
        rel_str = str(src_item.relative_to(root)).replace('\\', '/')
        dst_item.parent.mkdir(parents=True, exist_ok=True)
        if rel_str in tracked_files:
            cmd = ['git', 'mv', str(src_item.relative_to(root)), str(dst_item.relative_to(root))]
            subprocess.check_call(cmd)
            print(f"  [GIT MV] {src_item.name} -> {dst_item.relative_to(root)}")
        else:
            shutil.move(str(src_item), str(dst_item))
            print(f"  [FS MOVE] {src_item.name} -> {dst_item.relative_to(root)}")
    else:
        # Directory migration
        # Check if ANY file inside is tracked
        dir_rel = str(src_item.relative_to(root)).replace('\\', '/')
        has_tracked = any(tf.startswith(dir_rel + '/') or tf == dir_rel for tf in tracked_files)
        has_untracked = False
        for f in src_item.rglob('*'):
            if f.is_file():
                f_rel = str(f.relative_to(root)).replace('\\', '/')
                if f_rel not in tracked_files:
                    has_untracked = True
                    break
                    
        if has_tracked and not has_untracked:
            # Entire directory is tracked, single git mv
            dst_item.parent.mkdir(parents=True, exist_ok=True)
            cmd = ['git', 'mv', str(src_item.relative_to(root)), str(dst_item.relative_to(root))]
            subprocess.check_call(cmd)
            print(f"  [GIT MV DIR] {src_item.name}/ -> {dst_item.relative_to(root)}/")
        elif not has_tracked:
            # Entire directory is untracked/ignored, single filesystem move
            dst_item.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_item), str(dst_item))
            print(f"  [FS MOVE DIR] {src_item.name}/ -> {dst_item.relative_to(root)}/")
        else:
            # Mixed directory: move file by file
            dst_item.mkdir(parents=True, exist_ok=True)
            # Find all files
            all_child_files = [f for f in src_item.rglob('*') if f.is_file()]
            for f in all_child_files:
                f_rel_from_src = f.relative_to(src_item)
                target_f = dst_item / f_rel_from_src
                target_f.parent.mkdir(parents=True, exist_ok=True)
                
                f_rel_from_root = str(f.relative_to(root)).replace('\\', '/')
                if f_rel_from_root in tracked_files:
                    cmd = ['git', 'mv', str(f.relative_to(root)), str(target_f.relative_to(root))]
                    subprocess.check_call(cmd)
                else:
                    shutil.move(str(f), str(target_f))
                    
            # Remove any empty source directory shells
            shutil.rmtree(str(src_item), ignore_errors=True)
            print(f"  [MIXED MOVE DIR] {src_item.name}/ ({len(all_child_files)} files) -> {dst_item.relative_to(root)}/")

# 5. Post-flight verification
print("\n" + "=" * 80)
print("POST-FLIGHT VERIFICATION & ASSERTION")
print("=" * 80)

post_files = {}
for f in dest_dir.rglob('*'):
    if f.is_file():
        post_files[f.relative_to(dest_dir)] = f.stat().st_size

print(f"Post-flight file count: {len(post_files)} files ({sum(post_files.values()):,} bytes)")
print(f"Pre-flight file count:  {len(pre_files)} files ({sum(pre_files.values()):,} bytes)")

assert len(post_files) == len(pre_files), f"Count mismatch! {len(post_files)} != {len(pre_files)}"
assert sum(post_files.values()) == sum(pre_files.values()), f"Byte mismatch! {sum(post_files.values())} != {sum(pre_files.values())}"

print("\nSUCCESS: Exact metric equality asserted (zero byte loss, zero missing files).")
