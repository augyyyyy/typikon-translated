# Canonical Drive E Master Asset Vault & Extraction Playbook (`Rule 20`)

## 1. External Single Source of Truth (Drive E Master Vault)
- Drive E (`/Google Drive/Liturgical Library/`, specifically `/Google Drive/Liturgical Library/2. Historical Liturgical Texts/Typikons_and_Ordines/<Stem>/JPGs/` for historical Typika and the corresponding `<canonical_mirror_dir>/JPGs/` defined in `Liturgical Monuments/codex_registry.json`) is the immutable canonical master vault for all 300 DPI high-resolution page rasters across all monuments.
- **Standardized Raster Specification**:
  - **Resolution & Format**: 300 DPI JPEG (`Quality 92`).
  - **Filename Indexing**: 4-digit zero-padded physical PDF leaf coordinates (`Page_0001.jpg`, `Page_0002.jpg`, ..., `Page_{N:04d}.jpg`), matching the Chant Indexer spoke specification.
- **Exclusive Write-Ownership Carve-Out (`GLOBAL_SYSTEM_RULES.md` §7)**:
  - `Translation` is authorized to write extracted `Page_{p:04d}.jpg` rasters into the registered `<canonical_mirror_dir>/JPGs/` vault on Drive E for monuments in `Liturgical Monuments/codex_registry.json`.

## 2. Prohibition of Local Raster Bloat on Drive C (NTFS Junction Tiering)
- Multi-gigabyte image sets must **never** reside natively on Drive C, as OneDrive/cloud synchronization congests bandwidth and consumes local SSD capacity.
- Every monument workspace's image directory (`Liturgical Monuments/<Monument>/Source Text/images/` or `JPGs/`) must be mapped via an **NTFS Directory Junction** (`mklink /J`) pointing directly to its Drive E master vault directory.
- Verify or repair Drive E asset mirrors and junctions via:
  ```powershell
  py scripts/sync_drive_e_asset_mirror.py --verify
  ```

## 3. Two-Tier Extraction Hierarchy (`scripts/extract_cohort_leaves.py`)
`scripts/extract_cohort_leaves.py` enforces a deterministic 2-tier lookup when preparing a cohort:
1. **Tier 1 (Vault Cache Hit)**: Checks whether `Page_{p:04d}.jpg` already exists in the Drive E master vault (`> 1,000 bytes`). When present, PyMuPDF re-rendering from the source PDF is strictly prohibited.
2. **Tier 2 (Direct Vault Extraction)**: Renders only missing physical leaves from the source PDF at 300 DPI directly into the Drive E vault as quality-92 JPEGs (`Page_{p:04d}.jpg`).
3. **Ban on Hardlink Aliases (`p{p}.jpg` / `p{p}.png`)**: Creating `p{p}.jpg` or `p{p}.png` hardlink aliases on Drive E is strictly prohibited, because cloud sync clients upload hardlinks as duplicate multi-gigabyte files.

## 4. Drive E Recursive `.rglob()` Law (`GLOBAL_SYSTEM_RULES.md` §6.1)
- Because nested category folders inside the Drive E Liturgical Library may be reorganized at any time, all scripts scanning Drive E vaults (`scripts/extract_cohort_leaves.py`, `scripts/sync_drive_e_asset_mirror.py`, `scripts/verify_publication_edition.py`) must resolve leaf rasters and source PDFs dynamically via recursive `.rglob("Page_*.jpg")` and `.rglob(pdf_name)` searches rather than brittle single-level path joins.
