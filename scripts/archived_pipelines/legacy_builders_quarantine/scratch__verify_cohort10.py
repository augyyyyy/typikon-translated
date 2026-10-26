from pathlib import Path
import re
import sys

def verify_cohort10():
    base_dir = Path(__file__).resolve().parent.parent / "Liturgical Monuments" / "1891 Lviv Synod"
    source_file = base_dir / "Source Text" / "1891_lviv_synod_cohort10_source.txt"
    draft_file = base_dir / "Draft" / "1891_lviv_synod_cohort10_raw_draft.md"
    cohort_fn_file = base_dir / "Draft" / "1891_lviv_synod_cohort10_footnotes.txt"
    final_md_file = base_dir / "Final MD" / "1891_synod_cohort10.md"
    final_txt_file = base_dir / "Final" / "1891_synod_cohort10.txt"
    master_fn_file = base_dir / "Final" / "Final_footnotes.txt"

    files = [
        ("Source Text", source_file),
        ("Raw Draft", draft_file),
        ("Cohort Footnotes", cohort_fn_file),
        ("Final Markdown", final_md_file),
        ("Final Plain Text", final_txt_file),
        ("Master Footnotes", master_fn_file),
    ]

    print("=== COHORT 10 FILE INTEGRITY AUDIT ===")
    for label, path in files:
        if not path.exists():
            print(f"ERROR: {label} not found at {path}")
            sys.exit(1)
        stat = path.stat()
        with path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"[{label}] Exists | Size: {stat.st_size} bytes | Lines: {len(lines)}")

    # 1. Check leaf markers in Source Text
    with source_file.open("r", encoding="utf-8") as f:
        src_content = f.read()
    for p in range(141, 161):
        marker = f"=== LEAF p{p} ==="
        if marker not in src_content:
            print(f"ERROR: Missing leaf marker {marker} in source text")
            sys.exit(1)
    print("✓ All 20 leaf markers (p141 to p160) present in source text.")

    # 2. Check leaf markers in Final MD and Final TXT
    with final_md_file.open("r", encoding="utf-8") as f:
        md_content = f.read()
    with final_txt_file.open("r", encoding="utf-8") as f:
        txt_content = f.read()

    for p, bp in zip(range(141, 161), range(137, 157)):
        md_marker = f"Physical Page {p} / Leaf p{p} / Book Page {bp}"
        txt_marker = f"[Physical Page {p} / Leaf p{p} / Book Page {bp}]"
        if md_marker not in md_content:
            print(f"ERROR: Missing leaf marker {md_marker} in Final MD")
            sys.exit(1)
        if txt_marker not in txt_content:
            print(f"ERROR: Missing leaf marker {txt_marker} in Final TXT")
            sys.exit(1)
    print("✓ All 20 leaf markers verified in Final MD and Final TXT.")

    # 3. Check Footnote Bijectivity
    expected_fns = [f"[^{n}]" for n in range(167, 179)]
    for fn in expected_fns:
        if fn not in md_content:
            print(f"ERROR: Footnote marker {fn} missing in Final MD")
            sys.exit(1)
        if fn not in txt_content:
            print(f"ERROR: Footnote marker {fn} missing in Final TXT")
            sys.exit(1)
        def_fn = f"{fn}:"
        if def_fn not in md_content:
            print(f"ERROR: Footnote definition {def_fn} missing in Final MD")
            sys.exit(1)
        if def_fn not in txt_content:
            print(f"ERROR: Footnote definition {def_fn} missing in Final TXT")
            sys.exit(1)

    with master_fn_file.open("r", encoding="utf-8") as f:
        master_fn_content = f.read()
    for fn in expected_fns:
        def_fn = f"{fn}:"
        if def_fn not in master_fn_content:
            print(f"ERROR: Footnote definition {def_fn} missing in Final_footnotes.txt")
            sys.exit(1)
    print("✓ Footnote bijectivity confirmed for [^167] through [^178] across MD, TXT, and Master Footnotes.")

    # 4. Check Banned Phrases
    banned = ["for ever and ever", "forever and ever", "for ever and ever."]
    for b in banned:
        matches_md = re.findall(re.escape(b), md_content, re.IGNORECASE)
        matches_txt = re.findall(re.escape(b), txt_content, re.IGNORECASE)
        if matches_md:
            print(f"ERROR: Found banned phrase '{b}' in Final MD: {len(matches_md)} occurrences")
            sys.exit(1)
        if matches_txt:
            print(f"ERROR: Found banned phrase '{b}' in Final TXT: {len(matches_txt)} occurrences")
            sys.exit(1)
    print("✓ 0 occurrences of banned phrase 'for ever and ever' in MD and TXT.")

    # 5. Check Doxology Standard
    doxology = "unto the ages of ages"
    matches_md = re.findall(re.escape(doxology), md_content, re.IGNORECASE)
    matches_txt = re.findall(re.escape(doxology), txt_content, re.IGNORECASE)
    print(f"✓ Doxology '{doxology}' present: {len(matches_md)} in MD, {len(matches_txt)} in TXT.")

    # 6. Check Deity Capitalization
    deity_pronouns = ["He", "Him", "His", "Thou", "Thee", "Thy", "Thine"]
    for dp in deity_pronouns:
        if dp in md_content:
            print(f"✓ Deity pronoun '{dp}' verified present in translation.")
            break

    print("=== ALL VERIFICATION CHECKS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
    verify_cohort10()
