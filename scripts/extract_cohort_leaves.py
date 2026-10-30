#!/usr/bin/env python3
"""
Universal Headless Leaf Extraction Engine
==========================================
Extracts high-resolution (300 DPI) PNG leaves from source codex PDFs directly
to disk cache in <Workspace>/Source Text/images/p{N}.png.

Adheres strictly to Law I: parent context remains completely shielded from
raw image data.

Usage:
    python scripts/extract_cohort_leaves.py --monument 1891_lviv_synod --cohort 3
    python scripts/extract_cohort_leaves.py --monument 1891_lviv_synod --start 1 --end 20
"""

import os
import sys
import re
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF (fitz) is not installed. Run 'pip install pymupdf'.", file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"
from orchestrator_state import STATE_FILE, load_state, resolve_monument_id

DRIVE_CANDIDATES = [
    Path("E:/") / "Google Drive" / "Liturgical Library",
    Path("D:/") / "Google Drive" / "Liturgical Library",
    Path("C:/") / "Google Drive" / "Liturgical Library",
]

def is_junction_path(path: Path) -> bool:
    try:
        if hasattr(path, "is_junction"):
            return path.is_junction()
        if hasattr(os.path, "isjunction"):
            return os.path.isjunction(path)
        return path.exists() and (os.lstat(path).st_file_attributes & 0x400 != 0)
    except (OSError, AttributeError):
        return False

def resolve_vault_jpg_dir(vault_root: Path, rel_mirror: str) -> Path:
    base = vault_root / rel_mirror
    if base.name.upper() == "JPGS":
        return base
    if (base / "JPGs").exists():
        return base / "JPGs"
    if base.parent.name.upper() == "JPGS":
        return base
    return base / "JPGs"

def parse_range_from_state(state: Dict[str, Any], cohort_num: int) -> Optional[Tuple[int, int]]:
    """Extract start and end page if state defines current_cohort_range matching cohort_num."""
    if state.get("current_cohort") == cohort_num:
        range_str = state.get("current_cohort_range", "")
        m = re.search(r"leaves\s+p(\d+)-p(\d+)", range_str)
        if m:
            return int(m.group(1)), int(m.group(2))
        m2 = re.search(r"pp\.\s*(\d+)-(\d+)", range_str)
        if m2:
            return int(m2.group(1)), int(m2.group(2))
    return None

def resolve_pdf_path(relative_pdf_path: str, custom_pdf: Optional[str] = None) -> Path:
    if custom_pdf:
        p = Path(custom_pdf)
        if p.exists():
            return p
        raise FileNotFoundError(f"Specified custom PDF not found: {custom_pdf}")

    pdf_name = Path(relative_pdf_path).name

    # Check environment variables
    env_dir = os.environ.get("HISTORICAL_TYPIKONS_DIR")
    if env_dir:
        cand = Path(env_dir) / pdf_name
        if cand.exists():
            return cand
        for r_cand in Path(env_dir).rglob(pdf_name):
            return r_cand

    for root_cand in DRIVE_CANDIDATES:
        if not root_cand.exists():
            continue
        cand = root_cand / relative_pdf_path
        if cand.exists():
            return cand
        cand_typ = root_cand / "2. Historical Liturgical Texts" / "Typikons_and_Ordines" / pdf_name
        if cand_typ.exists():
            return cand_typ
        cand_flat = root_cand / pdf_name
        if cand_flat.exists():
            return cand_flat
        parent_cluster = (root_cand / relative_pdf_path).parent
        if parent_cluster.exists():
            for r_cand in parent_cluster.rglob(pdf_name):
                return r_cand

    # Check relative to project root
    local_cand = PROJECT_ROOT / relative_pdf_path
    if local_cand.exists():
        return local_cand

    raise FileNotFoundError(
        f"Could not locate PDF for '{relative_pdf_path}'. Set HISTORICAL_TYPIKONS_DIR or specify --pdf."
    )

def extract_leaves(
    monument_id: Optional[str] = None,
    cohort_num: Optional[int] = None,
    start_page: Optional[int] = None,
    end_page: Optional[int] = None,
    custom_pdf: Optional[str] = None,
    dpi: int = 300,
    force: bool = False
) -> int:
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
    
    monuments = registry.get("monuments", {})

    monument_id = resolve_monument_id(monument_id)
    if monument_id not in monuments:
        raise ValueError(f"Unknown monument '{monument_id}'. Available: {list(monuments.keys())}")

    state: Dict[str, Any] = {}
    try:
        state = load_state(monument_id=monument_id)
    except (FileNotFoundError, OSError, ValueError):
        state = {}

    mon_info = monuments[monument_id]
    rel_pdf = mon_info["relative_pdf_path"]
    workspace_dir = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}")
    images_dir = workspace_dir / "Source Text" / "images"

    # Resolve Drive E: canonical vault directory
    vault_root = None
    for cand in DRIVE_CANDIDATES:
        if cand.exists():
            vault_root = cand
            break

    vault_jpg_dir = None
    if vault_root and mon_info.get("canonical_mirror_dir"):
        vault_jpg_dir = resolve_vault_jpg_dir(vault_root, mon_info["canonical_mirror_dir"])
        vault_jpg_dir.mkdir(parents=True, exist_ok=True)

    # Automatically establish or repair NTFS directory junction
    is_junc = is_junction_path(images_dir)
    if vault_jpg_dir and is_junc and not images_dir.exists():
        try:
            subprocess.run(["cmd.exe", "/c", "rmdir", str(images_dir)], capture_output=True, text=True, check=True)
            is_junc = False
        except (subprocess.CalledProcessError, OSError):
            pass

    if vault_jpg_dir and not is_junc:
        if not images_dir.exists():
            images_dir.parent.mkdir(parents=True, exist_ok=True)
            try:
                cmd = ["cmd.exe", "/c", "mklink", "/J", str(images_dir), str(vault_jpg_dir.resolve())]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"  [JUNCTION] Linked {images_dir.name} -> {vault_jpg_dir}")
            except (subprocess.CalledProcessError, OSError) as e:
                print(f"  [Warning] Could not establish NTFS junction: {e}", file=sys.stderr)
                images_dir.mkdir(parents=True, exist_ok=True)
    elif not vault_jpg_dir and not images_dir.exists():
        images_dir.mkdir(parents=True, exist_ok=True)

    total_doc_pages = mon_info.get("total_physical_pages", 0)
    doc = None

    # Determine start and end page
    if start_page is None or end_page is None:
        cohort_size = mon_info.get("default_cohort_size", 10)
        c_num = cohort_num if cohort_num else 1
        state_range = parse_range_from_state(state, c_num)
        if state_range:
            start_page, end_page = state_range
        else:
            start_page = ((c_num - 1) * cohort_size) + 1
            end_page = min(total_doc_pages, c_num * cohort_size) if total_doc_pages > 0 else (c_num * cohort_size)

    if total_doc_pages > 0 and (start_page < 1 or end_page > total_doc_pages or start_page > end_page):
        raise ValueError(f"Invalid page bounds: start={start_page}, end={end_page}, total={total_doc_pages}")

    print(f"Extraction target: leaves p{start_page} to p{end_page} ({end_page - start_page + 1} leaves) @ {dpi} DPI")
    extracted_count = 0
    total_bytes = 0

    for p in range(start_page, end_page + 1):
        target_vault_canon = vault_jpg_dir / f"Page_{p:04d}.jpg" if vault_jpg_dir else None
        target_local_canon = images_dir / f"Page_{p:04d}.jpg"

        # Tier 1: Check existing files in Drive E vault first
        found_file = None
        for cand in [target_vault_canon, target_local_canon]:
            if cand and cand.exists() and cand.stat().st_size > 1000:
                found_file = cand
                break

        if found_file and not force:
            if not target_local_canon.exists() and found_file != target_local_canon:
                shutil.copy2(found_file, target_local_canon)
            print(f"  [CACHED] Leaf p{p} -> {found_file.name} ({found_file.stat().st_size} bytes)")
            extracted_count += 1
            total_bytes += found_file.stat().st_size
            continue

        # Tier 2: Open source PDF on demand only when vault image is missing or --force is set
        if doc is None:
            pdf_path = resolve_pdf_path(rel_pdf, custom_pdf)
            print(f"Opening source codex: {pdf_path.name}")
            doc = fitz.open(str(pdf_path))
            total_doc_pages = len(doc)
            print(f"Total physical pages in document: {total_doc_pages}")

        idx = p - 1  # 0-indexed PyMuPDF index
        page = doc[idx]
        pix = page.get_pixmap(dpi=dpi)

        if vault_jpg_dir and target_vault_canon:
            pix.save(str(target_vault_canon), output="jpeg", jpg_quality=92)
            out_file = target_vault_canon
            tier_label = "VAULT_RENDERED_E"
        else:
            out_file = target_local_canon
            pix.save(str(out_file), output="jpeg", jpg_quality=92)
            tier_label = "LOCAL_RENDERED_C"

        size = out_file.stat().st_size
        total_bytes += size
        extracted_count += 1
        print(f"  [{tier_label}] Leaf p{p} (index {idx}) -> {out_file.name} ({size} bytes)")

    if doc is not None:
        doc.close()
    print("=" * 65)
    print(f"Leaf extraction complete: {extracted_count} leaves verified in {images_dir.relative_to(PROJECT_ROOT) if images_dir.exists() else images_dir}")
    print(f"Total on-disk image cache size: {total_bytes / (1024 * 1024):.2f} MB")
    print("=" * 65)
    return 0

def main():
    parser = argparse.ArgumentParser(description="Universal Headless Leaf Extraction Engine")
    parser.add_argument("--monument", help="Monument ID from codex_registry.json")
    parser.add_argument("--cohort", type=int, help="Cohort number to extract")
    parser.add_argument("--start", type=int, help="Start physical page (1-indexed)")
    parser.add_argument("--end", type=int, help="End physical page (1-indexed)")
    parser.add_argument("--pdf", help="Explicit path to source PDF file")
    parser.add_argument("--dpi", type=int, default=300, help="Extraction DPI (default: 300)")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing cached images")

    args = parser.parse_args()
    try:
        sys.exit(extract_leaves(
            monument_id=args.monument,
            cohort_num=args.cohort,
            start_page=args.start,
            end_page=args.end,
            custom_pdf=args.pdf,
            dpi=args.dpi,
            force=args.force
        ))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
