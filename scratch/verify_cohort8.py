from pathlib import Path
import re

def verify_cohort8():
    project_root = Path(__file__).resolve().parent.parent
    cohort8_txt = project_root / "Liturgical Monuments" / "1891 Lviv Synod" / "Final" / "1891_synod_cohort8.txt"
    cohort8_md = project_root / "Liturgical Monuments" / "1891 Lviv Synod" / "Final MD" / "1891_synod_cohort8.md"
    cohort8_draft = project_root / "Liturgical Monuments" / "1891 Lviv Synod" / "Draft" / "1891_lviv_synod_cohort8_raw_draft.md"
    cohort8_fn = project_root / "Liturgical Monuments" / "1891 Lviv Synod" / "Draft" / "1891_lviv_synod_cohort8_footnotes.txt"
    master_fn = project_root / "Liturgical Monuments" / "1891 Lviv Synod" / "Final" / "Final_footnotes.txt"

    print("=== COHORT 8 VERIFICATION AUDIT ===")

    # 1. Check Final TXT
    with open(cohort8_txt, "r", encoding="utf-8") as f:
        txt_content = f.read()

    txt_markers = set(re.findall(r"\[\^(\d+)\]", txt_content.split("SCHOLARLY CRITICAL APPARATUS")[0]))
    txt_defs = set(re.findall(r"\[\^(\d+)\]:", txt_content.split("SCHOLARLY CRITICAL APPARATUS")[1]))
    print(f"Final TXT Markers in body: {len(txt_markers)} (min: {min(map(int, txt_markers))}, max: {max(map(int, txt_markers))})")
    print(f"Final TXT Definitions in apparatus: {len(txt_defs)} (min: {min(map(int, txt_defs))}, max: {max(map(int, txt_defs))})")
    assert txt_markers == txt_defs, f"Mismatch in Final TXT: {txt_markers ^ txt_defs}"

    # 2. Check Final MD
    with open(cohort8_md, "r", encoding="utf-8") as f:
        md_content = f.read()

    md_markers = set(re.findall(r"\[\^(\d+)\]", md_content.split("## 4. Scholarly Critical Apparatus & Footnotes")[0]))
    md_defs = set(re.findall(r"\[\^(\d+)\]:", md_content.split("## 4. Scholarly Critical Apparatus & Footnotes")[1]))
    print(f"Final MD Markers in body: {len(md_markers)}")
    print(f"Final MD Definitions in apparatus: {len(md_defs)}")
    assert md_markers == md_defs, f"Mismatch in Final MD: {md_markers ^ md_defs}"

    # 3. Check Master Footnotes
    with open(master_fn, "r", encoding="utf-8") as f:
        master_content = f.read()

    master_defs = set(re.findall(r"\[\^(\d+)\]:", master_content))
    expected_cohort8 = set(str(i) for i in range(112, 149))
    missing_in_master = expected_cohort8 - master_defs
    print(f"Master Footnotes total definitions: {len(master_defs)}")
    print(f"Cohort 8 expected definitions [112..148]: {len(expected_cohort8)}")
    assert not missing_in_master, f"Missing in Final_footnotes.txt: {missing_in_master}"

    # 4. Check Banned Phrases (Father Paul Doxology Standard)
    banned = ["for ever and ever", "forever and ever", "unto the ages of ages", "unto the ages of the ages"]
    for b in banned:
        matches_txt = [m.start() for m in re.finditer(re.escape(b), txt_content, re.IGNORECASE)]
        if matches_txt:
            print(f"WARNING: Banned phrase '{b}' found in Final TXT at indices {matches_txt}")
        assert not matches_txt, f"Found banned phrase '{b}' in Final TXT"

        matches_md = [m.start() for m in re.finditer(re.escape(b), md_content, re.IGNORECASE)]
        if matches_md:
            print(f"WARNING: Banned phrase '{b}' found in Final MD at indices {matches_md}")
        assert not matches_md, f"Found banned phrase '{b}' in Final MD"

    print("ALL BANNED PHRASE CHECKS PASSED (Father Paul Doxology Standard 100% compliant)!")

    # 5. Page leaf continuity
    leaves = [f"Leaf p{i}" for i in range(101, 121)]
    for l in leaves:
        assert l in txt_content, f"Missing {l} in Final TXT"
        assert l in md_content, f"Missing {l} in Final MD"
    print("ALL 20 LEAVES (p101..p120 / Book pp. 99..118) VERIFIED IN BOTH EDITIONS!")

    print("COHORT 8 AUDIT COMPLETELY SUCCESSFUL AND PRISTINE!")

if __name__ == "__main__":
    verify_cohort8()
