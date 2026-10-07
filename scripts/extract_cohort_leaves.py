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
STATE_FILE = PROJECT_ROOT / "Liturgical Monuments" / "ACTIVE_ORCHESTRATOR_STATE.json"

DRIVE_CANDIDATES = [
    Path("E:/") / "Google Drive" / "Liturgical Library" / "3. Modern Service Books and Typikons" / "Typikon",
    Path("D:/") / "Google Drive" / "Liturgical Library" / "3. Modern Service Books and Typikons" / "Typikon",
    Path("C:/") / "Google Drive" / "Liturgical Library" / "3. Modern Service Books and Typikons" / "Typikon",
]

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

    # Check environment variables
    env_dir = os.environ.get("HISTORICAL_TYPIKONS_DIR")
    if env_dir:
        cand = Path(env_dir) / Path(relative_pdf_path).name
        if cand.exists():
            return cand

    for root_cand in DRIVE_CANDIDATES:
        cand = root_cand / relative_pdf_path
        if cand.exists():
            return cand
        cand_flat = root_cand / Path(relative_pdf_path).name
        if cand_flat.exists():
            return cand_flat
        cand_hist = root_cand / "Historical Typikons" / Path(relative_pdf_path).name
        if cand_hist.exists():
            return cand_hist

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

    state: Dict[str, Any] = {}
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)

    if not monument_id:
        monument_id = state.get("monument_id", "1891_lviv_synod")

    if monument_id not in monuments:
        raise ValueError(f"Unknown monument '{monument_id}'. Available: {list(monuments.keys())}")

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
        vault_jpg_dir = vault_root / mon_info["canonical_mirror_dir"] / "JPGs"
        vault_jpg_dir.mkdir(parents=True, exist_ok=True)

    # Automatically establish NTFS directory junction if images_dir is not yet a junction
    is_junc = False
    try:
        is_junc = images_dir.exists() and (os.stat(images_dir).st_file_attributes & 0x400 != 0)
    except (OSError, AttributeError):
        pass

    if vault_jpg_dir and not is_junc:
        if not images_dir.exists():
            images_dir.parent.mkdir(parents=True, exist_ok=True)
            try:
                cmd = ["cmd.exe", "/c", "mklink", "/J", str(images_dir.resolve()), str(vault_jpg_dir.resolve())]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"  [JUNCTION] Linked {images_dir.name} -> {vault_jpg_dir}")
            except (subprocess.CalledProcessError, OSError) as e:
                print(f"  [Warning] Could not establish NTFS junction: {e}", file=sys.stderr)
                images_dir.mkdir(parents=True, exist_ok=True)
        else:
            # If already exists as normal directory, keep it
            pass
    elif not vault_jpg_dir and not images_dir.exists():
        images_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = resolve_pdf_path(rel_pdf, custom_pdf)
    print(f"Opening source codex: {pdf_path.name}")
    doc = fitz.open(str(pdf_path))
    total_doc_pages = len(doc)
    print(f"Total physical pages in document: {total_doc_pages}")

    # Determine start and end page
    if start_page is None or end_page is None:
        cohort_size = mon_info.get("default_cohort_size", 20)
        c_num = cohort_num if cohort_num else 1
        state_range = parse_range_from_state(state, c_num)
        if state_range:
            start_page, end_page = state_range
        else:
            start_page = ((c_num - 1) * cohort_size) + 1
            end_page = min(total_doc_pages, c_num * cohort_size)

    if start_page < 1 or end_page > total_doc_pages or start_page > end_page:
        doc.close()
        raise ValueError(f"Invalid page bounds: start={start_page}, end={end_page}, total={total_doc_pages}")

    print(f"Extraction target: leaves p{start_page} to p{end_page} ({end_page - start_page + 1} leaves) @ {dpi} DPI")
    extracted_count = 0
    total_bytes = 0

    for p in range(start_page, end_page + 1):
        target_vault_canon = vault_jpg_dir / f"Page_{p:04d}.jpg" if vault_jpg_dir else None
        target_vault_alias_png = vault_jpg_dir / f"p{p}.png" if vault_jpg_dir else None
        target_vault_alias_jpg = vault_jpg_dir / f"p{p}.jpg" if vault_jpg_dir else None
        target_local_png = images_dir / f"p{p}.png"
        target_local_jpg = images_dir / f"p{p}.jpg"

        # Tier 1: Check existing files
        found_file = None
        for cand in [target_vault_canon, target_vault_alias_png, target_vault_alias_jpg, target_local_png, target_local_jpg]:
            if cand and cand.exists() and cand.stat().st_size > 1000:
                found_file = cand
                break

        if found_file and not force:
            print(f"  [CACHED] Leaf p{p} -> {found_file.name} ({found_file.stat().st_size} bytes)")
            extracted_count += 1
            total_bytes += found_file.stat().st_size
            continue

        idx = p - 1  # 0-indexed PyMuPDF index
        page = doc[idx]
        pix = page.get_pixmap(dpi=dpi)

        # Tier 2: Render to Drive E: vault as JPEG Quality 92 if available, else local PNG
        if vault_jpg_dir and target_vault_canon:
            pix.save(str(target_vault_canon), output="jpeg", jpg_quality=92)
            # Create compatibility hardlinks
            if target_vault_alias_png and not target_vault_alias_png.exists():
                try:
                    os.link(str(target_vault_canon), str(target_vault_alias_png))
                except (OSError, FileExistsError):
                    pass
            if target_vault_alias_jpg and not target_vault_alias_jpg.exists():
                try:
                    os.link(str(target_vault_canon), str(target_vault_alias_jpg))
                except (OSError, FileExistsError):
                    pass
            out_file = target_vault_canon
            tier_label = "VAULT_RENDERED_E"
        else:
            out_file = target_local_png
            pix.save(str(out_file))
            tier_label = "LOCAL_RENDERED_C"

        size = out_file.stat().st_size
        total_bytes += size
        extracted_count += 1
        print(f"  [{tier_label}] Leaf p{p} (index {idx}) -> {out_file.name} ({size} bytes)")

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
