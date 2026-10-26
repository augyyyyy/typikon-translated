from pathlib import Path
import re

def verify_cohort9():
    project_root = Path(__file__).resolve().parent.parent
    cohort9_src = project_root / "Liturgical Monuments" / "1891 Lviv Synod" / "Source Text" / "1891_lviv_synod_cohort9_source.txt"
    cohort9_txt = project_root / "Liturgical Monuments" / "1891 Lviv Synod" / "Final" / "1891_synod_cohort9.txt"
    cohort9_md = project_root / "Liturgical Monuments" / "1891 Lviv Synod" / "Final MD" / "1891_synod_cohort9.md"
    cohort9_draft = project_root / "Liturgical Monuments" / "1891 Lviv Synod" / "Draft" / "1891_lviv_synod_cohort9_raw_draft.md"
    cohort9_fn = project_root / "Liturgical Monuments" / "1891 Lviv Synod" / "Draft" / "1891_lviv_synod_cohort9_footnotes.txt"
    master_fn = project_root / "Liturgical Monuments" / "1891 Lviv Synod" / "Final" / "Final_footnotes.txt"

    print("=== COHORT 9 VERIFICATION AUDIT ===")

    # 0. Check file existence, sizes, and line counts
    files = [
        ("Source Text", cohort9_src),
        ("Draft MD", cohort9_draft),
        ("Cohort Footnotes", cohort9_fn),
        ("Final MD", cohort9_md),
        ("Final TXT", cohort9_txt),
        ("Master Footnotes", master_fn)
    ]
    for name, p in files:
        assert p.exists(), f"File missing: {p}"
        lines = len(p.read_text(encoding="utf-8").splitlines())
        size = p.stat().st_size
        print(f"[{name}] {p.name}: {size:,} bytes, {lines:,} lines")

    # 1. Check Final TXT Footnotes
    txt_content = cohort9_txt.read_text(encoding="utf-8")
    txt_parts = txt_content.split("SCHOLARLY CRITICAL APPARATUS & FOOTNOTES")
    txt_markers = set(re.findall(r"\[\^(\d+)\]", txt_parts[0]))
    txt_defs = set(re.findall(r"\[\^(\d+)\]:", txt_parts[1]))
    print(f"\nFinal TXT Markers in body: {len(txt_markers)} (range: {min(map(int, txt_markers))}..{max(map(int, txt_markers))})")
    print(f"Final TXT Definitions in apparatus: {len(txt_defs)} (range: {min(map(int, txt_defs))}..{max(map(int, txt_defs))})")
    assert txt_markers == txt_defs, f"Mismatch in Final TXT: {txt_markers ^ txt_defs}"

    # 2. Check Final MD Footnotes
    md_content = cohort9_md.read_text(encoding="utf-8")
    md_parts = md_content.split("## 2. Scholarly Critical Apparatus & Footnotes")
    md_markers = set(re.findall(r"\[\^(\d+)\]", md_parts[0]))
    md_defs = set(re.findall(r"\[\^(\d+)\]:", md_parts[1]))
    print(f"Final MD Markers in body: {len(md_markers)} (range: {min(map(int, md_markers))}..{max(map(int, md_markers))})")
    print(f"Final MD Definitions in apparatus: {len(md_defs)} (range: {min(map(int, md_defs))}..{max(map(int, md_defs))})")
    assert md_markers == md_defs, f"Mismatch in Final MD: {md_markers ^ md_defs}"

    # 3. Check Cohort Footnotes File
    fn_content = cohort9_fn.read_text(encoding="utf-8")
    cohort_fn_defs = set(re.findall(r"\[\^(\d+)\]:", fn_content))
    expected_cohort9 = set(str(i) for i in range(149, 167))
    print(f"Cohort Footnotes file definitions: {len(cohort_fn_defs)}")
    assert cohort_fn_defs == expected_cohort9, f"Cohort Footnotes mismatch: {cohort_fn_defs ^ expected_cohort9}"

    # 4. Check Master Footnotes File
    master_content = master_fn.read_text(encoding="utf-8")
    master_defs = set(re.findall(r"\[\^(\d+)\]:", master_content))
    missing_in_master = expected_cohort9 - master_defs
    print(f"Master Footnotes total definitions: {len(master_defs)}")
    print(f"Cohort 9 expected definitions [149..166]: {len(expected_cohort9)}")
    assert not missing_in_master, f"Missing in Final_footnotes.txt: {missing_in_master}"

    # 5. Check Banned Phrases (Father Paul Doxology Standard)
    banned = ["for ever and ever", "forever and ever"]
    for b in banned:
        matches_txt = [m.start() for m in re.finditer(re.escape(b), txt_content, re.IGNORECASE)]
        assert not matches_txt, f"Found banned phrase '{b}' in Final TXT"
        matches_md = [m.start() for m in re.finditer(re.escape(b), md_content, re.IGNORECASE)]
        assert not matches_md, f"Found banned phrase '{b}' in Final MD"

    print("Father Paul Doxology Standard: 100% compliant (Zero occurrences of 'for ever and ever').")

    # 6. Check Canonical Realia
    realia = ["Tetrapod", "Plashchanytsia", "Melchizedek"]
    for term in realia:
        assert term in md_content, f"Missing canonical term {term} in Final MD"
        assert term in txt_content, f"Missing canonical term {term} in Final TXT"
    print("Canonical Realia verification: PASSED (Tetrapod, Plashchanytsia, Melchizedek present).")

    # 7. Check Leaf Markers in Source Text
    src_content = cohort9_src.read_text(encoding="utf-8")
    expected_leaves = [f"=== LEAF p{p} ===" for p in range(121, 141)]
    for leaf in expected_leaves:
        assert leaf in src_content, f"Missing leaf marker {leaf} in source text"
    print(f"Source Text Leaf Markers: All 20 leaves (p121..p140) verified.")

    print("\n>>> ALL COHORT 9 VERIFICATION AUDITS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    verify_cohort9()
