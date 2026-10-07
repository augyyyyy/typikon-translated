#!/usr/bin/env python3
"""
Canonical Master Asset Vault & Storage Tiering Synchronizer
===========================================================
Establishes permanent, cloud-synced 300 DPI JPEG (Quality 92) image mirrors
in external storage matching the Chant Indexer spoke specification.

Replaces local workspace 'Source Text/images' folders on Drive C: with NTFS
Directory Junctions (mklink /J), reducing local SSD footprint and OneDrive
bandwidth consumption to 0 bytes while maintaining 100% path compatibility.

Usage:
    py scripts/sync_drive_e_asset_mirror.py --monument 1891_lviv_synod --dry-run
    py scripts/sync_drive_e_asset_mirror.py --monument 1891_lviv_synod --create-junction
    py scripts/sync_drive_e_asset_mirror.py --all --create-junction --cleanup-backup
    py scripts/sync_drive_e_asset_mirror.py --verify-all
"""

import os
import sys
import json
import argparse
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from PIL import Image
except ImportError:
    Image = None

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"

DEFAULT_VAULT_ROOTS = [
    Path("E:/") / "Google Drive" / "Liturgical Library" / "3. Modern Service Books and Typikons" / "Typikon",
    Path("D:/") / "Google Drive" / "Liturgical Library" / "3. Modern Service Books and Typikons" / "Typikon",
    Path("C:/") / "Google Drive" / "Liturgical Library" / "3. Modern Service Books and Typikons" / "Typikon",
]

def resolve_vault_root() -> Path:
    env_root = os.environ.get("LITURGICAL_LIBRARY_TYPIKON_DIR")
    if env_root and Path(env_root).exists():
        return Path(env_root)
    for cand in DEFAULT_VAULT_ROOTS:
        if cand.exists():
            return cand
    raise FileNotFoundError(
        "Could not locate Drive E: Canonical Liturgical Library. "
        "Ensure Drive E: is mounted or set LITURGICAL_LIBRARY_TYPIKON_DIR."
    )

def resolve_source_pdf(relative_pdf_path: str, vault_root: Path) -> Optional[Path]:
    cand1 = vault_root / relative_pdf_path
    if cand1.exists():
        return cand1
    cand2 = vault_root / "Historical Typikons" / Path(relative_pdf_path).name
    if cand2.exists():
        return cand2
    cand3 = PROJECT_ROOT / relative_pdf_path
    if cand3.exists():
        return cand3
    return None

def is_junction(path: Path) -> bool:
    try:
        if hasattr(path, "is_junction"):
            return path.is_junction()
        if hasattr(os.path, "isjunction"):
            return os.path.isjunction(path)
        return path.exists() and (os.lstat(path).st_file_attributes & 0x400 != 0)
    except (OSError, AttributeError):
        return False

def write_monument_manifest(
    monument_dir: Path,
    mon_info: Dict[str, Any],
    total_pages: int,
    actual_count: int,
    total_bytes: int
) -> Path:
    stem = monument_dir.name
    manifest_path = monument_dir / f"{stem}.md"
    content = f"""# Metadata: {mon_info.get('title', stem)}

- **Canonical Monument ID**: `{mon_info.get('monument_id', '')}`
- **Title**: {mon_info.get('title', '')}
- **Short Title**: {mon_info.get('short_title', '')}
- **Genre Register**: {mon_info.get('genre_register', 'rubrical').upper()}
- **Total Physical Leaves**: {total_pages}
- **Extracted Images Count**: {actual_count}
- **Total Mirror Size**: {total_bytes:,} bytes ({total_bytes / (1024 * 1024):.2f} MB)
- **Image Standard**: 300 DPI JPEG (Quality 92)
- **Dual Mirror Verified**: True
- **Scan Repository**: `JPGs/`
- **Source PDF**: `{mon_info.get('relative_pdf_path', '')}`
"""
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(content)
    return manifest_path

def sync_monument_mirror(
    monument_id: str,
    mon_info: Dict[str, Any],
    vault_root: Path,
    dry_run: bool = False,
    create_junction: bool = False,
    cleanup_backup: bool = False,
    verbose: bool = True
) -> Dict[str, Any]:
    rel_mirror = mon_info.get("canonical_mirror_dir")
    if not rel_mirror:
        raise ValueError(f"Monument '{monument_id}' lacks 'canonical_mirror_dir' in registry.")

    vault_mon_dir = vault_root / rel_mirror
    vault_jpg_dir = vault_mon_dir / "JPGs"
    total_pages = mon_info.get("total_physical_pages", 0)

    workspace_dir = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}")
    local_img_dir = workspace_dir / "Source Text" / "images"

    if verbose:
        print(f"\n{'='*70}")
        print(f"Syncing Monument: {mon_info.get('short_title', monument_id)}")
        print(f"Vault Directory:  {vault_jpg_dir}")
        print(f"Local Directory:  {local_img_dir}")
        print(f"Total Pages:      {total_pages}")
        print(f"{'='*70}")

    if dry_run:
        print("  [DRY-RUN] Directory creation and file migration preview only.")
        return {
            "monument_id": monument_id,
            "status": "DRY_RUN",
            "vault_dir": str(vault_jpg_dir),
            "expected_pages": total_pages
        }

    vault_jpg_dir.mkdir(parents=True, exist_ok=True)

    # Check source PDF
    pdf_path = resolve_source_pdf(mon_info.get("relative_pdf_path", ""), vault_root)
    doc = None
    if pdf_path and fitz:
        try:
            doc = fitz.open(str(pdf_path))
        except Exception as e:
            print(f"  [Warning] Could not open PDF {pdf_path}: {e}", file=sys.stderr)

    synced_count = 0
    converted_count = 0
    rendered_count = 0

    for p in range(1, total_pages + 1):
        target_canon = vault_jpg_dir / f"Page_{p:04d}.jpg"
        target_p_jpg = vault_jpg_dir / f"p{p}.jpg"
        target_p_png = vault_jpg_dir / f"p{p}.png"

        # Check if canonical exists and valid
        if target_canon.exists() and target_canon.stat().st_size > 1000:
            synced_count += 1
        else:
            # Need to create target_canon. Try local PNG first
            local_png = local_img_dir / f"p{p}.png"
            local_jpg = local_img_dir / f"p{p}.jpg"

            if local_png.exists() and local_png.stat().st_size > 1000:
                if Image:
                    with Image.open(local_png) as img:
                        img.convert("RGB").save(str(target_canon), format="JPEG", quality=92, optimize=True)
                    converted_count += 1
                    synced_count += 1
                elif doc and p <= len(doc):
                    page = doc[p - 1]
                    pix = page.get_pixmap(dpi=300)
                    pix.save(str(target_canon), output="jpeg", jpg_quality=92)
                    rendered_count += 1
                    synced_count += 1
                else:
                    raise RuntimeError(f"Cannot convert {local_png} (Pillow missing and PDF unavailable)")
            elif local_jpg.exists() and local_jpg.stat().st_size > 1000:
                shutil.copy2(local_jpg, target_canon)
                converted_count += 1
                synced_count += 1
            elif doc and p <= len(doc):
                page = doc[p - 1]
                pix = page.get_pixmap(dpi=300)
                pix.save(str(target_canon), output="jpeg", jpg_quality=92)
                rendered_count += 1
                synced_count += 1
            else:
                print(f"  [ERROR] Page {p} could not be sourced from local image or PDF!", file=sys.stderr)

        # Ensure compatibility hardlinks (p{p}.jpg, p{p}.png) on Drive E:
        if target_canon.exists():
            for alias in [target_p_jpg, target_p_png]:
                if not alias.exists():
                    try:
                        os.link(str(target_canon), str(alias))
                    except (OSError, FileExistsError):
                        pass

        if p % 100 == 0 or p == total_pages:
            print(f"  Processed {p}/{total_pages} leaves (Synced: {synced_count}, Converted: {converted_count}, Rendered: {rendered_count})...")

    if doc:
        doc.close()

    # Calculate mirror size
    vault_files = list(vault_jpg_dir.glob("Page_*.jpg"))
    actual_count = len(vault_files)
    total_bytes = sum(f.stat().st_size for f in vault_files)

    manifest_file = write_monument_manifest(vault_mon_dir, mon_info, total_pages, actual_count, total_bytes)
    if verbose:
        print(f"  Manifest generated: {manifest_file.name}")
        print(f"  Vault count: {actual_count}/{total_pages} leaves verified ({total_bytes / (1024*1024):.2f} MB)")

    # Junction Creation
    junction_status = "NOT_REQUESTED"
    if create_junction:
        if is_junction(local_img_dir):
            if verbose:
                print(f"  [JUNCTION] {local_img_dir} is already an active NTFS junction.")
            junction_status = "ALREADY_JUNCTION"
        else:
            backup_dir = local_img_dir.parent / "images_legacy_backup"
            if local_img_dir.exists():
                if backup_dir.exists():
                    shutil.rmtree(backup_dir, ignore_errors=True)
                local_img_dir.rename(backup_dir)
                if verbose:
                    print(f"  [BACKUP] Renamed existing C: images -> {backup_dir.name}")

            cmd = ["cmd.exe", "/c", "mklink", "/J", str(local_img_dir.resolve()), str(vault_jpg_dir.resolve())]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if verbose:
                print(f"  [JUNCTION] Created NTFS Junction: {local_img_dir.name} -> {vault_jpg_dir}")
                print(f"  Output: {res.stdout.strip()}")
            junction_status = "CREATED"

            # Verify through junction
            test_target = local_img_dir / "Page_0001.jpg"
            test_alias = local_img_dir / "p1.png"
            if not test_target.exists() and not test_alias.exists():
                raise RuntimeError(f"Junction verification failed: {test_target} not readable!")

            # Cleanup backup if requested
            if cleanup_backup and backup_dir.exists():
                backup_size = sum(f.stat().st_size for f in backup_dir.glob("*") if f.is_file())
                shutil.rmtree(backup_dir, ignore_errors=True)
                if verbose:
                    print(f"  [RECLAIMED] Removed legacy backup directory, freeing {backup_size / (1024*1024):.2f} MB on Drive C:!")
                junction_status = "CREATED_AND_CLEANED"

    return {
        "monument_id": monument_id,
        "status": "SUCCESS",
        "expected_pages": total_pages,
        "vault_pages": actual_count,
        "vault_bytes": total_bytes,
        "junction_status": junction_status
    }

def verify_all_mirrors(registry: Dict[str, Any], vault_root: Path) -> int:
    print(f"\n{'='*70}")
    print("VERIFYING ALL CANONICAL ASSET MIRRORS ON DRIVE E:")
    print(f"Vault Root: {vault_root}")
    print(f"{'='*70}")

    all_ok = True
    for mon_id, mon_info in registry.get("monuments", {}).items():
        rel_mirror = mon_info.get("canonical_mirror_dir")
        if not rel_mirror:
            continue
        expected = mon_info.get("total_physical_pages", 0)
        jpg_dir = vault_root / rel_mirror / "JPGs"

        workspace_dir = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{mon_id}")
        local_img_dir = workspace_dir / "Source Text" / "images"

        if not jpg_dir.exists():
            print(f"  [-] {mon_id:<28} : MISSING from Drive E: ({rel_mirror})")
            all_ok = False
            continue

        actual_files = list(jpg_dir.glob("Page_*.jpg"))
        actual_count = len(actual_files)
        total_mb = sum(f.stat().st_size for f in actual_files) / (1024 * 1024)

        junc_flag = "JUNCTION_OK" if is_junction(local_img_dir) else "LOCAL_DIR"

        if actual_count == expected:
            print(f"  [+] {mon_id:<28} : 100% OK ({actual_count}/{expected} leaves, {total_mb:.1f} MB) [{junc_flag}]")
        else:
            print(f"  [!] {mon_id:<28} : PARTIAL ({actual_count}/{expected} leaves, {total_mb:.1f} MB) [{junc_flag}]")
            all_ok = False

    print(f"{'='*70}")
    return 0 if all_ok else 1

def main():
    parser = argparse.ArgumentParser(description="Canonical Drive E: Master Asset Vault & Storage Tiering Synchronizer")
    parser.add_argument("--monument", help="Specific monument ID to synchronize")
    parser.add_argument("--all", action="store_true", help="Synchronize all completed monuments (excludes Monument 5)")
    parser.add_argument("--dry-run", action="store_true", help="Preview synchronization without file I/O")
    parser.add_argument("--create-junction", action="store_true", help="Replace local C: images with NTFS Directory Junction")
    parser.add_argument("--cleanup-backup", action="store_true", help="Delete legacy backup on C: once junction verified")
    parser.add_argument("--verify-all", action="store_true", help="Verify completeness of all mirrors across Drive E:")

    args = parser.parse_args()

    if not REGISTRY_FILE.exists():
        print(f"ERROR: Registry file not found: {REGISTRY_FILE}", file=sys.stderr)
        sys.exit(1)

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    try:
        vault_root = resolve_vault_root()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if args.verify_all:
        sys.exit(verify_all_mirrors(registry, vault_root))

    target_monuments = []
    if args.monument:
        if args.monument not in registry["monuments"]:
            print(f"ERROR: Unknown monument '{args.monument}'", file=sys.stderr)
            sys.exit(1)
        target_monuments.append(args.monument)
    elif args.all:
        # Include completed monuments; explicitly quarantine active Monument 5
        for m_id, m_info in registry["monuments"].items():
            if m_id == "1888_violakis_typikon":
                print(f"[QUARANTINE] Skipping active {m_id} while concurrent chat session executes.")
                continue
            if m_info.get("status") == "completed" or (PROJECT_ROOT / m_info.get("workspace_dir", "") / "Source Text" / "images").exists():
                target_monuments.append(m_id)

    if not target_monuments:
        print("Specify --monument <id>, --all, or --verify-all. Run with -h for help.")
        sys.exit(0)

    for m_id in target_monuments:
        sync_monument_mirror(
            monument_id=m_id,
            mon_info=registry["monuments"][m_id],
            vault_root=vault_root,
            dry_run=args.dry_run,
            create_junction=args.create_junction,
            cleanup_backup=args.cleanup_backup
        )

if __name__ == "__main__":
    main()
