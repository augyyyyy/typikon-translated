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
REGISTRY_FILE = PROJECT_ROOT / "Typikons" / "codex_registry.json"
STATE_FILE = PROJECT_ROOT / "Typikons" / "ACTIVE_ORCHESTRATOR_STATE.json"

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

    # Candidate root library paths across Windows drive mount points
    drive_candidates = [
        Path("E:/") / "Google Drive" / "Liturgical Library" / "3. Modern Service Books and Typikons" / "Typikon",
        Path("D:/") / "Google Drive" / "Liturgical Library" / "3. Modern Service Books and Typikons" / "Typikon",
        Path("C:/") / "Google Drive" / "Liturgical Library" / "3. Modern Service Books and Typikons" / "Typikon",
    ]

    for root_cand in drive_candidates:
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
    workspace_dir = PROJECT_ROOT / mon_info.get("workspace_dir", f"Typikons/{monument_id}")
    images_dir = workspace_dir / "Source Text" / "images"
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
        out_file = images_dir / f"p{p}.png"
        if out_file.exists() and not force:
            print(f"  [CACHED] Leaf p{p} -> {out_file.name} ({out_file.stat().st_size} bytes)")
            extracted_count += 1
            total_bytes += out_file.stat().st_size
            continue

        idx = p - 1  # 0-indexed PyMuPDF index
        page = doc[idx]
        pix = page.get_pixmap(dpi=dpi)
        pix.save(str(out_file))
        size = out_file.stat().st_size
        total_bytes += size
        extracted_count += 1
        print(f"  [RENDERED] Leaf p{p} (index {idx}) -> {out_file.name} ({size} bytes)")

    doc.close()
    print("=" * 65)
    print(f"Leaf extraction complete: {extracted_count} leaves verified in {images_dir.relative_to(PROJECT_ROOT)}")
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
