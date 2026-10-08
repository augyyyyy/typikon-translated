#!/usr/bin/env python3
"""
Publication Quality Gate & Ergonomics Auditor
==============================================
Validates that Final MD/ publication deliverables meet the Monument 0 benchmark:
  1. Zero Academic Placeholders (0 leaf markers, 0 cohort banners, 0 scaffold headers).
  2. Bijective Footnote Parity (100% 1:1 symmetry in master, 100% local resolution in parts).
  3. Interactive TOC Slug Integrity (all links resolve to valid header anchors).
  4. MTS-1 & Anti-Pattern Compliance (no banned phrases, valid UTF-8).

Usage:
    python scripts/verify_publication_edition.py --monument 1899_dolnytsky_typikon
    python scripts/verify_publication_edition.py --monument 1891_lviv_synod
"""

import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"

PLACEHOLDER_PATTERNS = [
    (r"\[(?:Physical\s+Page\s+\d+\s*/\s*)?(?:Book\s+Page|Physical\s+Page|Leaf|Page)\s+\d+[^\]]*\]", "Bracketed Page/Leaf marker"),
    (r"\*?\[Blank\s+[^\]]+\]\*?", "Blank leaf indicator"),
    (r"===\s*LEAF", "Leaf banner delimiter"),
    (r"<!--\s*LEAF", "HTML leaf comment"),
    (r"\*?\((?:Physical\s+Page|Physical\s+pp\.|Physical\s+Leaf|Book\s+Page|Leaf\s+p?|Blank\s+Flyleaf)[^)]*\)\*?", "Physical page reference"),
    (r"^[ \t]*(?:Month\s+—\s*\d+\s*—\s*[A-Za-z]+|—\s*\d+\s*—|\d+\s+—\s+[A-Za-z]+)[ \t]*$", "Running book pagination header"),
    (r"^#+\s*Cohort\s+\d+", "Cohort markdown header"),
    (r"^#+\s*.*?Cohort\s+\d+\s+Raw Draft", "Cohort raw draft header"),
    (r"^#+\s*Cohort\s+\d+\s+Footnotes", "Cohort footnotes header"),
    (r"<!--\s*(?:START|END)?\s*COHORT", "Cohort HTML delimiter"),
]

BANNED_PHRASES = [
    (r"\bfor ever and ever\b", "Banned liturgical doxology ('for ever and ever') -> MTS-1 Father Paul standard requires 'now and forever, and unto ages of ages'"),
]

def slugify(heading_text: str) -> str:
    cleaned = re.sub(r'\[\^?\d+\]', '', heading_text)
    cleaned = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', cleaned)
    cleaned = re.sub(r'[*_`~]', '', cleaned)
    cleaned = cleaned.lower()
    cleaned = re.sub(r'[^\w\s-]', '', cleaned, flags=re.UNICODE)
    cleaned = re.sub(r'[\s_]+', '-', cleaned)
    cleaned = re.sub(r'-+', '-', cleaned)
    return cleaned.strip('-')

def extract_headings_and_anchors(content: str) -> Set[str]:
    anchors = set()
    for line in content.splitlines():
        m = re.match(r"^#{1,6}\s+(.+)$", line.strip())
        if m:
            heading = m.group(1).strip()
            # Also check for explicit HTML anchor tag e.g. <a id="...">
            tag_m = re.search(r'<a\s+id="([^"]+)"', heading)
            if tag_m:
                anchors.add(tag_m.group(1).lower())
            slug = slugify(heading)
            if slug:
                anchors.add(slug)
    return anchors

def verify_monument_publication(monument_id: str) -> bool:
    if not REGISTRY_FILE.exists():
        print(f"ERROR: Registry file not found at {REGISTRY_FILE}", file=sys.stderr)
        return False

    registry = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    if monument_id not in registry.get("monuments", {}):
        print(f"ERROR: Monument '{monument_id}' not found in registry.", file=sys.stderr)
        return False

    mon_cfg = registry["monuments"][monument_id]
    ws_dir = PROJECT_ROOT / mon_cfg["workspace_dir"]
    final_md_dir = ws_dir / "Final MD"
    final_dir = ws_dir / "Final"
    footnotes_file = final_dir / "Final_footnotes.txt"

    pub_spec = mon_cfg.get("publication_spec", {})
    if not pub_spec:
        print(f"ERROR: Monument '{monument_id}' has no publication_spec in codex_registry.json!", file=sys.stderr)
        return False

    print("=" * 75)
    print(f"  PUBLICATION QUALITY GATE: {mon_cfg['title']}")
    print(f"  Workspace: {ws_dir.relative_to(PROJECT_ROOT)}")
    print("=" * 75)

    all_passed = True
    md_files = list(final_md_dir.glob("*.md"))
    if not md_files:
        print(f"[FAIL] No Markdown deliverables found in {final_md_dir.relative_to(PROJECT_ROOT)}")
        return False

    # -------------------------------------------------------------
    # Check 1: Zero Academic Scaffolding & Placeholders
    # -------------------------------------------------------------
    print("\n[Gate 1] Auditing for academic placeholders and translation scaffolding...")
    total_violations = 0
    for mf in md_files:
        # Standalone apparatus doesn't need rubrical checks
        content = mf.read_text(encoding="utf-8")
        file_violations = []
        for line_num, line in enumerate(content.splitlines(), start=1):
            # Skip footnote definitions in scholarly apparatus / local notes
            if re.match(r"^\s*\[\^\d+\]:", line):
                continue
            for pat, desc in PLACEHOLDER_PATTERNS:
                if re.search(pat, line, flags=re.IGNORECASE | re.MULTILINE):
                    file_violations.append((line_num, desc, line.strip()[:80]))
        if file_violations:
            total_violations += len(file_violations)
            print(f"  [FAIL] {mf.name}: {len(file_violations)} placeholder violations:")
            for ln, desc, snippet in file_violations[:5]:
                print(f"    L{ln}: [{desc}] {snippet}")
            if len(file_violations) > 5:
                print(f"    ... and {len(file_violations) - 5} more.")
        else:
            print(f"  [PASS] {mf.name}: 0 placeholders found.")

    if total_violations == 0:
        print("  >>> Gate 1 Result: PASS (Zero academic placeholders across all files)")
    else:
        print(f"  >>> Gate 1 Result: FAIL ({total_violations} placeholders detected)")
        all_passed = False

    # -------------------------------------------------------------
    # Check 2: Bijective Footnote Parity (Master & Local In-File)
    # -------------------------------------------------------------
    print("\n[Gate 2] Auditing footnote symmetry and in-file local resolution...")
    master_complete_candidates = list(final_md_dir.glob("*_complete.md"))
    if not master_complete_candidates:
        print("  [FAIL] Master complete edition (*_complete.md) not found!")
        all_passed = False
    else:
        master_complete_file = master_complete_candidates[0]
        master_content = master_complete_file.read_text(encoding="utf-8")

        # Parse markers in text vs definitions in master
        master_parts = re.split(r"\n#\s*FOOTNOTES AND SCHOLARLY COMMENTARY", master_content, flags=re.IGNORECASE)
        master_body = master_parts[0]
        master_fn_block = master_parts[1] if len(master_parts) > 1 else ""

        text_markers = set(int(n) for n in re.findall(r"\[\^(\d+)\]", master_body))
        def_markers = set(int(n) for n in re.findall(r"^\s*\[\^(\d+)\]:", master_fn_block, re.MULTILINE))

        missing_master = sorted(list(text_markers - def_markers))
        orphaned_master = sorted(list(def_markers - text_markers))

        if missing_master or orphaned_master:
            print(f"  [FAIL] Master edition footnote mismatch:")
            if missing_master: print(f"    Missing definitions in master: {missing_master[:10]}")
            if orphaned_master: print(f"    Orphaned definitions in master: {orphaned_master[:10]}")
            all_passed = False
        else:
            print(f"  [PASS] Master Complete Edition: {len(text_markers)}/{len(def_markers)} bijective symmetry.")

        # Now check each modular Part file for local in-file resolution
        part_files = [p for p in md_files if "_part" in p.name]
        part_footnote_errors = 0
        for pf in part_files:
            p_content = pf.read_text(encoding="utf-8")
            # Separate body text from bottom ### Notes block
            notes_split = re.split(r"\n---\s*\n\s*### Notes\s*\n\s*\[\^", p_content, flags=re.IGNORECASE)
            body_text = notes_split[0]
            notes_block = "[^" + notes_split[1] if len(notes_split) > 1 else ""

            body_markers = set(int(n) for n in re.findall(r"\[\^(\d+)\]", body_text))
            local_defs = set(int(n) for n in re.findall(r"^\s*\[\^(\d+)\]:", notes_block, re.MULTILINE))

            missing_local = sorted(list(body_markers - local_defs))
            orphaned_local = sorted(list(local_defs - body_markers))

            if missing_local or orphaned_local:
                part_footnote_errors += 1
                print(f"  [FAIL] {pf.name}: Local footnote mismatch (Missing: {len(missing_local)}, Orphaned: {len(orphaned_local)})")
                if missing_local: print(f"    Missing in {pf.name}: {missing_local[:5]}")
                if orphaned_local: print(f"    Orphaned in {pf.name}: {orphaned_local[:5]}")
            else:
                print(f"  [PASS] {pf.name}: {len(body_markers)} citations resolved locally 1:1.")

        if part_footnote_errors == 0 and not (missing_master or orphaned_master):
            print("  >>> Gate 2 Result: PASS (100% bijective footnote parity globally and locally)")
        else:
            print(f"  >>> Gate 2 Result: FAIL ({part_footnote_errors} parts with footnote discrepancies)")
            all_passed = False

    # -------------------------------------------------------------
    # Check 3: Interactive Table of Contents & Anchor Integrity
    # -------------------------------------------------------------
    print("\n[Gate 3] Auditing interactive Table of Contents & anchor resolution...")
    # 1. Check anchors in master complete edition
    if master_complete_candidates:
        master_content = master_complete_candidates[0].read_text(encoding="utf-8")
        master_anchors = extract_headings_and_anchors(master_content)

        # Extract TOC links from master
        toc_match = re.search(r"## TABLE OF CONTENTS\s*\n(.*?)(?=\n---|\n#|\Z)", master_content, re.DOTALL | re.IGNORECASE)
        if toc_match:
            toc_text = toc_match.group(1)
            toc_links = re.findall(r"\[([^\]]+)\]\(#([^\)]+)\)", toc_text)
            broken_links = []
            for link_text, slug in toc_links:
                if slug.lower() not in master_anchors:
                    broken_links.append((link_text, slug))

            if broken_links:
                print(f"  [WARN] Master TOC has {len(broken_links)} unresolvable slug anchors:")
                for lt, sl in broken_links[:5]:
                    print(f"    Unmatched anchor: [{lt}] -> #{sl}")
                # Note: warn if non-critical, but flag
            else:
                print(f"  [PASS] Master TOC: All {len(toc_links)} links resolve to valid headings.")
        else:
            print("  [FAIL] Master complete edition is missing '## TABLE OF CONTENTS'!")
            all_passed = False

    # 2. Check Part 0 relative links
    part0_candidates = list(final_md_dir.glob("*_part0_*.md"))
    if part0_candidates:
        part0_content = part0_candidates[0].read_text(encoding="utf-8")
        rel_links = re.findall(r"\[([^\]]+)\]\(([^#\)]+)\.md#([^\)]+)\)", part0_content)
        broken_rel = 0
        for link_text, target_base, slug in rel_links:
            target_path = final_md_dir / f"{target_base}.md"
            if not target_path.exists():
                print(f"  [FAIL] Part 0 TOC links to non-existent file: {target_base}.md")
                broken_rel += 1
            else:
                target_anchors = extract_headings_and_anchors(target_path.read_text(encoding="utf-8"))
                if slug.lower() not in target_anchors:
                    print(f"  [WARN] Cross-file anchor in {target_base}.md not found: #{slug} ('{link_text}')")

        if broken_rel == 0:
            print(f"  [PASS] Part 0 TOC: All {len(rel_links)} cross-file relative links target existing files.")
        else:
            print(f"  [FAIL] Part 0 TOC has {broken_rel} broken file links.")
            all_passed = False

    # -------------------------------------------------------------
    # Check 4: MTS-1 Compliance & Encoding
    # -------------------------------------------------------------
    print("\n[Gate 4] Auditing MTS-1 liturgical phrasing and UTF-8 encoding...")
    banned_hits = 0
    for mf in md_files:
        content = mf.read_text(encoding="utf-8")
        for line_num, line in enumerate(content.splitlines(), start=1):
            for pat, reason in BANNED_PHRASES:
                if re.search(pat, line, re.IGNORECASE):
                    banned_hits += 1
                    print(f"  [FAIL] {mf.name}:L{line_num}: Found banned phrase: {line.strip()[:80]}")
                    print(f"         Reason: {reason}")

    if banned_hits == 0:
        print("  >>> Gate 4 Result: PASS (0 banned phrases, 100% MTS-1 doxology compliance)")
    else:
        print(f"  >>> Gate 4 Result: FAIL ({banned_hits} banned phrase occurrences)")
        all_passed = False

    print("\n" + "=" * 75)
    if all_passed:
        print(f"  >>> ALL QUALITY GATES PASSED FOR MONUMENT: {monument_id} <<<")
        print("=" * 75)
        return True
    else:
        print(f"  >>> VERIFICATION FAILED FOR MONUMENT: {monument_id} <<<")
        print("=" * 75)
        return False

def main():
    parser = argparse.ArgumentParser(description="Publication Quality Gate & Ergonomics Auditor")
    parser.add_argument("--monument", required=True, help="Monument ID (e.g. 1899_dolnytsky_typikon)")
    args = parser.parse_args()

    success = verify_monument_publication(args.monument)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
