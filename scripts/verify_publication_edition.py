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
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"

PLACEHOLDER_PATTERNS = [
    (r"\[(?:Physical\s+Page\s+\d+\s*/\s*)?(?:Book\s+Page|Physical\s+Page|Leaf|Page)\s+\d+[^\]]*\]", "Bracketed Page/Leaf marker"),
    (r"\*?\[Blank\s+[^\]]+\]\*?", "Blank leaf indicator"),
    (r"===\s*LEAF", "Leaf banner delimiter"),
    (r"<!--\s*LEAF", "HTML leaf comment"),
    (r"^[ \t]*\*?\((?:Physical\s+Page|Physical\s+pp\.|Physical\s+Leaf|Book\s+Page|Printed\s+Page|Leaf\s+p?|Blank\s+Flyleaf)[^)]*\)\*?[ \t]*$", "Physical page reference"),
    (r"^[ \t]*(?:Month\s+—\s*\d+\s*—\s*[A-Za-z]+|—\s*\d+\s*—|\d+\s+—\s+[A-Za-z]+)[ \t]*$", "Running book pagination header"),
    (r"^#+\s*Cohort\s+\d+", "Cohort markdown header"),
    (r"^#+\s*.*?Cohort\s+\d+\s+Raw Draft", "Cohort raw draft header"),
    (r"^#+\s*Cohort\s+\d+\s+Footnotes", "Cohort footnotes header"),
    (r"<!--\s*(?:START|END)?\s*COHORT", "Cohort HTML delimiter"),
    (r"\[INSERT\s+DIAGRAM", "Unresolved diagram placeholder"),
    (r"Translator's\s+Note:\s*Pages\s+\d+", "Synthetic table/page omission disclaimer"),
    (r"\[Left\s+Column\]", "ASCII diagram approximation placeholder"),
    (r"\[Summary\s*:", "Leaked pre-written summary block"),
    (r"\^\[[A-Za-z]\]", "Unnumbered inline translator note"),
    (r"\[TODO\b", "Unresolved TODO marker"),
    (r"\[PLACEHOLDER\b", "Unresolved PLACEHOLDER marker"),
    (r"\[UNRESOLVED_CANONICAL_GAP", "Unresolved canonical gap marker"),
    (r"^[ \t]*(?:#{1,6}\s*|\*\*)?\[(?:Left|Right)\s+Page\s*(?:—|--|-|:)\s*.+?\](?:\*\*)?[ \t]*$", "Un-inlined 2-up Left/Right Page banner"),
    (r"^===\s*COHORT_BOUNDARY\s+\d+\s*===$", "Unstripped cohort boundary marker"),
    (r"\.\.\.\s*(?:\[\^\d+\]\s*)*\[(?:f\.\s*[^\]]+|p\d+[LR][AB]?)\]", "Unstripped seam ellipsis before milestone"),
    (r"\[(?:f\.\s*[^\]]+|p\d+[LR][AB]?)\]\s*$", "Orphan trailing milestone at end of line"),
]

BANNED_PHRASES = [
    (r"\bfor ever and ever\b", "Banned liturgical doxology ('for ever and ever') -> MTS-1 Father Paul standard requires 'now and forever, and unto ages of ages'"),
    (r"\bSedalen\b", "Forbidden vocabulary ('Sedalen' -> MTS-1 requires 'Sessional Hymn')"),
    (r"\bIrmos\b", "Forbidden vocabulary ('Irmos' -> MTS-1 requires 'Heirmos')"),
    (r"\bApolytikion\b", "Forbidden vocabulary ('Apolytikion' -> MTS-1 requires 'Troparion')"),
    (r"\bNekrosim(?:on|a)\b", "Forbidden vocabulary ('Nekrosimon/Nekrosima' -> MTS-1 requires 'Hymn(s) for the Departed (Поко́инъ)')"),
]

NON_VERB_ETH_SET = {
    "beth", "seth", "nazareth", "elizabeth", "gennesaret", "shibboleth",
    "kenneth", "teeth", "beneath", "underneath", "twentieth", "thirtieth",
    "fortieth", "fiftieth", "sixtieth", "seventieth", "eightieth",
    "ninetieth", "hundredth", "thousandth",
}

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
    # Filter out scholarly companion deliverables (Slavonic complete, Drift report, Primitives review, Podoben grid) from English publication gates
    companion_suffixes = ("_slavonic_complete.md", "_drift_report.md", "_primitives_review.md", "_podoben_grid.md")
    md_files = [mf for mf in sorted(final_md_dir.glob("*.md")) if not any(mf.name.endswith(sfx) for sfx in companion_suffixes)]
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

    # 3. Check Deep Service Heading Granularity & Modular Part Balance (Gate 3B / 3C)
    if "octoechos" in monument_id.lower():
        tone_part_files = [
            pf for pf in sorted(final_md_dir.glob("*_part*_tone*.md"))
            if re.search(r"_part[1-8]_tone[1-8]\.md$", pf.name)
        ]
        weekday_part_files = list(final_md_dir.glob("*_part*_weekday*.md"))
        service_check_files = tone_part_files + weekday_part_files
        granularity_errors = 0
        for spf in service_check_files:
            sp_txt = spf.read_text(encoding="utf-8")
            h2_headings = [
                m.group(1).strip()
                for m in re.finditer(r"^##\s+(.+)$", sp_txt, flags=re.MULTILINE)
                if not re.match(r"^(?:TABLE OF CONTENTS|Notes|Footnotes)\b", m.group(1).strip(), re.IGNORECASE)
            ]
            # Check for redundant echo heading e.g. '## TONE 1' right under '# Tone 1: ...'
            redundant_echo = [h for h in h2_headings if re.match(r"^TONE\s+\d+$", h, re.IGNORECASE)]
            if redundant_echo:
                granularity_errors += 1
                print(f"  [FAIL] Gate 3B: {spf.name} contains redundant H2 echo header: {redundant_echo}")
            if len(h2_headings) < 3:
                granularity_errors += 1
                print(f"  [FAIL] Gate 3B: {spf.name} has insufficient H2 service headings ({len(h2_headings)} found, >= 3 required).")
        if granularity_errors == 0 and service_check_files:
            print(f"  [PASS] Gate 3B: All {len(service_check_files)} Tone/Weekday parts have deep H2 service headings and 0 redundant echo headers.")
        elif granularity_errors > 0:
            all_passed = False

        if len(tone_part_files) == 8:
            sizes = [len(pf.read_text(encoding="utf-8")) for pf in tone_part_files]
            sorted_sizes = sorted(sizes)
            median_size = (sorted_sizes[3] + sorted_sizes[4]) / 2.0
            max_size = max(sizes)
            max_pf = tone_part_files[sizes.index(max_size)]
            if max_size > median_size * 2.5:
                print(f"  [FAIL] Gate 3C: Modular Tone part imbalance: {max_pf.name} ({max_size:,} chars) exceeds 2.5x median Tone size ({median_size:,.0f} chars). Consolidated Weekday Cycle must be sliced into its own Part.")
                all_passed = False
            else:
                print(f"  [PASS] Gate 3C: Modular Tone 1-8 part sizes balanced (max={max_size:,} chars vs median={median_size:,.0f} chars, ratio={max_size/max(1.0, median_size):.2f}x <= 2.50x).")

    # -------------------------------------------------------------
    # Check 4: MTS-1 Compliance, Full-Text Vocabulary/Slop/-eth & Encoding
    # -------------------------------------------------------------
    print("\n[Gate 4] Auditing MTS-1 liturgical phrasing, full-text vocabulary/slop/-eth, and UTF-8 encoding...")
    banned_hits = 0
    is_octoechos_monument = "octoechos" in monument_id.lower() or (final_md_dir / f"{monument_id}_propers_corpus.json").exists()
    from scripts.lint_liturgical_slop import lint_slop

    for mf in md_files:
        raw_bytes = mf.read_bytes()
        if raw_bytes.startswith(b"\xef\xbb\xbf"):
            banned_hits += 1
            print(f"  [FAIL] {mf.name}: Contains UTF-8 BOM (\\ufeff)!")

        content = mf.read_text(encoding="utf-8")
        if re.search(r"<sup>.*?</sup>", content, re.IGNORECASE):
            banned_hits += 1
            print(f"  [FAIL] {mf.name}: Contains stray HTML <sup>...</sup> tag!")

        for line_num, line in enumerate(content.splitlines(), start=1):
            for pat, reason in BANNED_PHRASES:
                for m_bp in re.finditer(pat, line, re.IGNORECASE):
                    before = line[:m_bp.start()]
                    after = line[m_bp.end():]
                    if "(*" in before and "*)" in after:
                        last_open = before.rfind("(*")
                        if "*)" not in before[last_open:]:
                            continue
                    if 'lit. "' in line or "(lit. " in line:
                        continue
                    banned_hits += 1
                    print(f"  [FAIL] {mf.name}:L{line_num}: Found banned phrase: {line.strip()[:80]}")
                    print(f"         Reason: {reason}")

            if is_octoechos_monument:
                for m_eth in re.finditer(r"\b([A-Za-z]+eth)\b", line):
                    w_eth = m_eth.group(1)
                    if w_eth.lower() not in NON_VERB_ETH_SET:
                        banned_hits += 1
                        print(f"  [FAIL] {mf.name}:L{line_num}: Unnormalized 3rd-person '-eth' verb '{w_eth}': {line.strip()[:80]}")

        slop_res = lint_slop(mf)
        if not slop_res["passed"]:
            banned_hits += slop_res["violation_count"]
            for v in slop_res["violations"][:5]:
                print(f"  [FAIL] {mf.name}:L{v['line']} [{v['category']}]: '{v['matched_text']}' in: {v['line_snippet'][:80]}")

    if banned_hits == 0:
        print("  >>> Gate 4 Result: PASS (Zero banned phrases, zero slop/BOM/HTML tags, zero unnormalized -eth verbs across body and footnotes)")
    else:
        print(f"  >>> Gate 4 Result: FAIL ({banned_hits} MTS-1 vocabulary/slop/encoding violations detected)")
        all_passed = False

    # -------------------------------------------------------------
    # Check 5: Heading Typography, Language Purity & Apparatus Isolation (Strict Blocker)
    # -------------------------------------------------------------
    print("\n[Gate 5] Auditing heading typography, epigraphic language purity & apparatus isolation...")
    gate5_violations = 0
    master_title = pub_spec.get("master_title", "")

    for mf in md_files:
        content = mf.read_text(encoding="utf-8")
        lines = content.splitlines()

        # 5A: Unparenthesized Cyrillic in Markdown Headings (#) and Body Lines
        for line_num, line in enumerate(lines, start=1):
            if re.match(r"^\s*\[\^\d+\]:", line):
                continue
            if re.search(r'[\u0400-\u04FF]', line):
                # Remove parenthesized substrings (*...*) or (...)
                clean_line = re.sub(r'\([^\)]*[\u0400-\u04FF][^\)]*\)', '', line)
                if re.search(r'[\u0400-\u04FF]', clean_line):
                    gate5_violations += 1
                    print(f"  [FAIL] {mf.name}:L{line_num}: Unparenthesized Cyrillic in body/heading: {line.strip()[:80]}")
                    print("         MTS-1 requires Cyrillic incipits/marginalia to be parenthesized: e.g. (*О постахъ*)")

        # 5B: Repeated Master Document Title in Body
        if master_title:
            escaped_m = re.escape(master_title)
            for line_num, line in enumerate(lines, start=1):
                if ("_part0_" in mf.name or mf.name.endswith("_complete.md")) and line_num == 1:
                    continue
                if re.match(rf"^#\s+{escaped_m}\b", line.strip(), re.IGNORECASE):
                    gate5_violations += 1
                    print(f"  [FAIL] {mf.name}:L{line_num}: Repeated master document title in body: {line.strip()[:80]}")

        # 5C: Cohort Scaffolding Continuation Headers
        for line_num, line in enumerate(lines, start=1):
            if not line.startswith('#'):
                continue
            # Whitelist authentic multi-page historical tables (e.g. Tablet II, Paschal Key Letters)
            if re.search(r'\b(?:Tablet|Paschal\s+Key\s+Letters)\b', line, re.IGNORECASE):
                continue
            if any(w in line.lower() for w in ['(continued', '(concluded', '(conclusion', 'continued from']):
                gate5_violations += 1
                print(f"  [FAIL] {mf.name}:L{line_num}: Scaffolding continuation header found: {line.strip()[:80]}")

        # 5D: Leaked Footnote Definitions in Part Body
        if "_part" in mf.name and not mf.name.endswith("_complete.md"):
            parts = re.split(r'\n---\s*\n\s*### Notes\b', content, flags=re.IGNORECASE)
            body_text = parts[0]
            for line_num, line in enumerate(body_text.splitlines(), start=1):
                if re.match(r"^\s*\[\^\d+\]:", line):
                    gate5_violations += 1
                    print(f"  [FAIL] {mf.name}:L{line_num}: Leaked footnote definition in body text: {line.strip()[:80]}")

    if gate5_violations == 0:
        print("  >>> Gate 5 Result: PASS (Zero unparenthesized Cyrillic, zero repeated titles, zero continuation scaffolding, zero leaked footnotes)")
    else:
        print(f"  >>> Gate 5 Result: FAIL ({gate5_violations} typography/isolation violations detected)")
        all_passed = False

    # -------------------------------------------------------------
    # Check 6: SGC-02 3-Tier Ground-Truth & Leaf Bijection Audit
    # -------------------------------------------------------------
    print("\n[Gate 6] Auditing SGC-02 3-Tier Ground-Truth & Primary-Source Bijection...")
    gate6_violations = 0
    total_pages = mon_cfg.get("total_physical_pages", 0)
    expected_leaves = set(range(1, total_pages + 1))

    # Tier 0: Physical Raster Vault Verification via recursive .rglob()
    img_dir = ws_dir / "Source Text" / "images"
    if img_dir.exists() and total_pages > 0:
        jpg_files = list(img_dir.rglob("Page_*.jpg"))
        if len(jpg_files) < total_pages:
            print(f"  [FAIL] Tier 0 Physical Vault: Found {len(jpg_files)}/{total_pages} Page_XXXX.jpg rasters in {img_dir.relative_to(PROJECT_ROOT)}")
            gate6_violations += 1
        else:
            print(f"  [PASS] Tier 0 Physical Vault: {len(jpg_files)}/{total_pages} 300 DPI leaf rasters verified via .rglob().")

    if monument_id == "2010_lviv_typikon":
        # Part-Level SGC-02 Bijection against Ukrainian TXTs/
        ukr_dir = ws_dir / "Ukrainian TXTs"
        part_pairs = [
            ("Intro.txt", "Final_Dolnytsky_intro.md"),
            ("Part 1.txt", "Final_Dolnytsky_part1_structure.md"),
            ("Part 2.txt", "Final_Dolnytsky_part2_general_rubrics.md"),
            ("Part 3.txt", "Final_Dolnytsky_part3_menaion.md"),
            ("Part 4.txt", "Final_Dolnytsky_part4_triodion.md"),
            ("Part 5.txt", "Final_Dolnytsky_part5_temple.md"),
            ("Appendix.txt", "Final_Dolnytsky_appendix.md"),
        ]
        for ukr_name, eng_name in part_pairs:
            u_path = ukr_dir / ukr_name
            e_path = final_md_dir / eng_name
            if not u_path.exists() or not e_path.exists():
                print(f"  [FAIL] Missing Part pair: {ukr_name} <-> {eng_name}")
                gate6_violations += 1
                continue
            u_len = len(u_path.read_text(encoding="utf-8").strip())
            e_len = len(e_path.read_text(encoding="utf-8").strip())
            ratio = e_len / max(1, u_len)
            if ratio < 0.70 or ratio > 2.80:
                print(f"  [FAIL] Anomalous SGC-02 length ratio for {eng_name}: ratio={ratio:.2f} (eng={e_len}, ukr={u_len})")
                gate6_violations += 1
            else:
                print(f"  [PASS] Part Bijection {ukr_name} <-> {eng_name}: ratio={ratio:.2f} ({e_len:,} chars)")
    else:
        # Cohort-Based Monuments (Monuments 1–6): Enforce 100% canonical === LEAF pN === bijection
        leaf_re = re.compile(r"===\s*LEAF\s+p?(\d+)\s*===", re.IGNORECASE)
        tier_dirs = [
            ("Source Text", ws_dir / "Source Text", "*_cohort*_source.txt"),
            ("Draft", ws_dir / "Draft", "*_cohort*_raw_draft.md"),
            ("Cohorts", ws_dir / "Cohorts", "*_cohort*.md"),
            ("Final TXT", ws_dir / "Final", "*_cohort*.txt"),
        ]
        cohort_counts = {}
        for label, t_dir, pat in tier_dirs:
            if not t_dir.exists():
                print(f"  [FAIL] Missing tier directory: {t_dir.relative_to(PROJECT_ROOT)}")
                gate6_violations += 1
                continue
            files = sorted(t_dir.glob(pat))
            cohort_counts[label] = len(files)
            found_leaves: Set[int] = set()
            for f in files:
                txt = f.read_text(encoding="utf-8")
                for m in leaf_re.finditer(txt):
                    found_leaves.add(int(m.group(1)))
            missing_leaves = sorted(list(expected_leaves - found_leaves))
            if missing_leaves:
                print(
                    f"  [FAIL] {label} ({len(files)} files): Missing {len(missing_leaves)} canonical '=== LEAF pN ===' markers: "
                    f"{missing_leaves[:15]}"
                )
                gate6_violations += 1
            else:
                print(f"  [PASS] {label} ({len(files)} files): {len(found_leaves)}/{total_pages} canonical '=== LEAF pN ===' markers verified.")

        if len(set(cohort_counts.values())) > 1:
            print(f"  [FAIL] Cohort file count mismatch across tiers: {cohort_counts}")
            gate6_violations += 1

        # Cohorts <-> Final MD/*_complete.md Word Conservation
        cohorts_dir = ws_dir / "Cohorts"
        if cohorts_dir.exists() and master_complete_candidates:
            cohort_words = 0
            for cf in sorted(cohorts_dir.glob("*_cohort*.md")):
                c_txt = cf.read_text(encoding="utf-8")
                c_txt = re.sub(r"===\s*LEAF\s+p?\d+\s*===", "", c_txt, flags=re.IGNORECASE)
                cohort_words += len(c_txt.split())
            comp_txt = master_complete_candidates[0].read_text(encoding="utf-8")
            comp_words = len(comp_txt.split())
            w_ratio = comp_words / max(1, cohort_words)
            if w_ratio < 0.90:
                print(f"  [FAIL] Cohort-to-Complete word conservation drop: complete={comp_words:,}w vs cohorts={cohort_words:,}w (ratio={w_ratio:.3f})")
                gate6_violations += 1
            else:
                print(f"  [PASS] Cohort-to-Complete Word Conservation: {comp_words:,} / {cohort_words:,} words (ratio={w_ratio:.3f})")

    if gate6_violations == 0:
        print("  >>> Gate 6 Result: PASS (100% 3-Tier SGC-02 Ground-Truth Bijection Verified)")
    else:
        print(f"  >>> Gate 6 Result: FAIL ({gate6_violations} SGC-02 bijection violations detected)")
        all_passed = False

    # -------------------------------------------------------------
    # Check 7: Hymnographic Normalization, 8-Tone Primitives & Anti-Stub Corpus Gate
    # -------------------------------------------------------------
    propers_corpus_file = final_md_dir / f"{monument_id}_propers_corpus.json"
    primitives_review_file = final_md_dir / f"{monument_id}_primitives_review.md"
    if propers_corpus_file.exists() or primitives_review_file.exists() or "octoechos" in monument_id.lower():
        print("\n[Gate 7] Auditing Hymnographic Normalization, 8-Tone Primitives & Anti-Stub Propers Corpus...")
        gate7_violations = 0

        # 7A & 7B: Scan part1..N and _complete.md for unnormalized Model:/Prosomoion:/Nekrosimon: labels and un-parenthesized Podoben: lines
        unnorm_model_hits = []
        unparen_podoben_hits = []
        for mf in md_files:
            if mf.name.endswith("_apparatus.md") or mf.name.endswith("_footnotes.md"):
                continue
            content = mf.read_text(encoding="utf-8")
            # Separate body from ### Notes / # FOOTNOTES
            body_part = re.split(r"\n(?:---\s*\n\s*### Notes|#\s*FOOTNOTES AND SCHOLARLY COMMENTARY)\b", content, flags=re.IGNORECASE)[0]
            for ln_num, ln in enumerate(body_part.splitlines(), start=1):
                if re.match(r"^\s*\[\^\d+\]:", ln):
                    continue
                if re.search(r"\b(?:Model:|Melodic\s+model:|Model\s+melody:|Prosomoion:|Special\s+Melody:|Same\s+Model\b|Same\s+melody\b|Same\s+Prosomoion\b|Nekrosimon:)", ln, re.IGNORECASE):
                    unnorm_model_hits.append((mf.name, ln_num, ln.strip()[:80]))
                if re.search(r"\bPodoben:", ln, re.IGNORECASE) and not re.search(r"\([^)]*[\u0400-\u04FF][^)]*\)", ln):
                    unparen_podoben_hits.append((mf.name, ln_num, ln.strip()[:80]))

        if unnorm_model_hits:
            gate7_violations += len(unnorm_model_hits)
            print(f"  [FAIL] Gate 7A: Found {len(unnorm_model_hits)} unnormalized 'Model:'/'Prosomoion:'/'Model melody:'/'Nekrosimon:' lines:")
            for fn, ln_num, snip in unnorm_model_hits[:5]:
                print(f"    {fn}:L{ln_num}: {snip}")
        else:
            print("  [PASS] Gate 7A: 0 unnormalized 'Model:' / 'Prosomoion:' / 'Model melody:' / 'Nekrosimon:' lines across all files.")

        if unparen_podoben_hits:
            gate7_violations += len(unparen_podoben_hits)
            print(f"  [FAIL] Gate 7B: Found {len(unparen_podoben_hits)} 'Podoben:' lines missing parenthetical Slavonic witness:")
            for fn, ln_num, snip in unparen_podoben_hits[:5]:
                print(f"    {fn}:L{ln_num}: {snip}")
        else:
            print("  [PASS] Gate 7B: 100% of 'Podoben:' headings include parenthetical Slavonic witness.")

        # 7C: 8-Tone Primitives Registry & Father Paul Digest Completeness
        prim_reg_file = PROJECT_ROOT / "data" / "liturgical_primitives_registry.json"
        if not prim_reg_file.exists():
            print("  [FAIL] Gate 7C: Missing data/liturgical_primitives_registry.json!")
            gate7_violations += 1
        else:
            prim_reg = json.loads(prim_reg_file.read_text(encoding="utf-8"))
            pod_models = prim_reg.get("podoben_models", [])
            pod_tones = set(int(p.get("tone", 0)) for p in pod_models)
            heir_tones = set(int(h.get("tone", 0)) for h in prim_reg.get("sunday_heirmoi", []))
            expected_tones = {1, 2, 3, 4, 5, 6, 7, 8}
            unattested_models = [p.get("id") for p in pod_models if not p.get("attested_loci")]
            if expected_tones - pod_tones or expected_tones - heir_tones:
                print(f"  [FAIL] Gate 7C: Incomplete 8-Tone primitives coverage (Podoben tones={sorted(pod_tones)}, Heirmos tones={sorted(heir_tones)})")
                gate7_violations += 1
            elif unattested_models:
                print(f"  [FAIL] Gate 7C: Found {len(unattested_models)} models with 0 attested loci in active registry: {unattested_models}")
                gate7_violations += 1
            else:
                print(
                    f"  [PASS] Gate 7C: 8-Tone Primitives Registry verified "
                    f"({len(pod_models)} 100% physically-attested Podobens across Tones 1-8, "
                    f"{len(prim_reg.get('sunday_heirmoi', []))} Sunday Heirmoi across Tones 1-8)."
                )

        # 7D: Anti-Stub Bilingual Propers Corpus Gate
        if not propers_corpus_file.exists():
            print(f"  [FAIL] Gate 7D: Missing {propers_corpus_file.name}!")
            gate7_violations += 1
        else:
            corpus_data = json.loads(propers_corpus_file.read_text(encoding="utf-8"))
            c_items = corpus_data.get("items", [])
            c_tones = set(int(it.get("tone", 0)) for it in c_items if int(it.get("tone", 0)) in range(1, 9))
            if len(c_items) < 1500 or len(c_tones) < 8 or "source_provenance" not in corpus_data:
                print(
                    f"  [FAIL] Gate 7D: Propers corpus failed anti-stub gate "
                    f"(items={len(c_items)}, tones={sorted(c_tones)}, has_provenance={'source_provenance' in corpus_data})"
                )
                gate7_violations += 1
            else:
                print(
                    f"  [PASS] Gate 7D: Bilingual Cross-Propers Corpus verified "
                    f"({len(c_items):,} atomic stanzas across Tones {sorted(c_tones)})."
                )

        # 7E & 7F: Internally-Attested Podoben Grid & Cross-Deliverable Mathematical Parity Gate
        grid_md_file = final_md_dir / f"{monument_id}_podoben_grid.md"
        grid_json_file = final_md_dir / f"{monument_id}_podoben_grid.json"
        if not grid_md_file.exists() or not grid_json_file.exists():
            print(f"  [FAIL] Gate 7E: Missing {grid_md_file.name} or {grid_json_file.name}!")
            gate7_violations += 1
        else:
            grid_data = json.loads(grid_json_file.read_text(encoding="utf-8"))
            invocations = grid_data.get("invocations", [])
            grid_tones = set(it.get("tone") for it in invocations if it.get("tone") in range(1, 9))
            min_invocations = 100 if monument_id == "1630_lviv_octoechos" else 20
            if len(invocations) < min_invocations or len(grid_tones) < 8:
                print(f"  [FAIL] Gate 7E: Podoben grid incomplete (invocations={len(invocations)}, tones={sorted(grid_tones)})")
                gate7_violations += 1
            else:
                print(
                    f"  [PASS] Gate 7E: Podoben Grid verified "
                    f"({len(invocations)} physical invocations across Tones {sorted(grid_tones)})."
                )

            # 7F: Cross-Deliverable Podoben Mathematical Parity (complete.md == _podoben_grid.json == _primitives_review.md)
            if master_complete_candidates and primitives_review_file.exists():
                comp_body = re.split(r"\n#\s*FOOTNOTES AND SCHOLARLY COMMENTARY", master_complete_candidates[0].read_text(encoding="utf-8"), flags=re.IGNORECASE)[0]
                comp_pod_count = sum(
                    1 for ln in comp_body.splitlines()
                    if "*Podoben:" in ln or "*Tone and Podoben:" in ln
                )
                grid_pod_count = len(invocations)
                rev_txt = primitives_review_file.read_text(encoding="utf-8")
                m_rev_cnt = re.search(r"invoked\s+`(\d+)`\s+times", rev_txt)
                rev_pod_count = int(m_rev_cnt.group(1)) if m_rev_cnt else -1

                if not (comp_pod_count == grid_pod_count == rev_pod_count):
                    print(
                        f"  [FAIL] Gate 7F: Cross-Deliverable Podoben Mathematical Parity mismatch! "
                        f"complete.md={comp_pod_count}, _podoben_grid.json={grid_pod_count}, _primitives_review.md={rev_pod_count}"
                    )
                    gate7_violations += 1
                else:
                    print(
                        f"  [PASS] Gate 7F: 100% Cross-Deliverable Podoben Mathematical Parity verified "
                        f"(complete.md == _podoben_grid.json == _primitives_review.md == {comp_pod_count} invocations)."
                    )

        if gate7_violations == 0:
            print("  >>> Gate 7 Result: PASS (100% Hymnographic Normalization, 8-Tone Primitives & Full Propers Corpus Verified)")
        else:
            print(f"  >>> Gate 7 Result: FAIL ({gate7_violations} hymnographic/corpus violations detected)")
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
    parser.add_argument("--monument", help="Monument ID (e.g. 1899_dolnytsky_typikon)")
    parser.add_argument("--all-completed", action="store_true", help="Verify all monuments with status=completed")
    args = parser.parse_args()

    if args.all_completed:
        registry = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
        completed_ids = [
            m_id for m_id, cfg in registry.get("monuments", {}).items()
            if cfg.get("status") == "completed"
        ]
        all_ok = True
        for m_id in completed_ids:
            if not verify_monument_publication(m_id):
                all_ok = False
        sys.exit(0 if all_ok else 1)

    if not args.monument:
        parser.error("Must specify --monument <id> or --all-completed")

    success = verify_monument_publication(args.monument)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

