from pathlib import Path
import re
import sys

def main():
    root = Path(__file__).resolve().parent.parent
    files = [
        root / "Typikons" / "1891 Lviv Synod" / "Source Text" / "1891_lviv_synod_cohort5_source.txt",
        root / "Typikons" / "1891 Lviv Synod" / "Draft" / "1891_lviv_synod_cohort5_raw_draft.md",
        root / "Typikons" / "1891 Lviv Synod" / "Draft" / "1891_lviv_synod_cohort5_footnotes.txt",
        root / "Typikons" / "1891 Lviv Synod" / "Final MD" / "1891_synod_cohort5.md",
        root / "Typikons" / "1891 Lviv Synod" / "Final" / "1891_synod_cohort5.txt",
        root / "Typikons" / "1891 Lviv Synod" / "Final" / "Final_footnotes.txt"
    ]

    all_ok = True
    for f in files:
        if not f.exists():
            print(f"[MISSING] {f.name}")
            all_ok = False
            continue
        content = f.read_text(encoding="utf-8")
        lines = content.splitlines()
        banned = re.findall(r"for ever and ever", content, re.IGNORECASE)
        print(f"{f.name}: {len(lines)} lines, {len(content.encode('utf-8'))} bytes")
        if banned:
            print(f"  [ERROR] Banned phrase 'for ever and ever' found in {f.name} ({len(banned)} times)")
            all_ok = False
        else:
            print(f"  [OK] No banned phrase in {f.name}")

    # Footnote bijectivity verification
    final_md = root / "Typikons" / "1891 Lviv Synod" / "Final MD" / "1891_synod_cohort5.md"
    if final_md.exists():
        md_text = final_md.read_text(encoding="utf-8")
        body_markers = set(re.findall(r"\[\^(\d+)\](?!:)", md_text))
        def_markers = set(re.findall(r"\[\^(\d+)\]:", md_text))
        print("\n--- Footnote Bijectivity Check ---")
        print(f"Body markers: {sorted([int(x) for x in body_markers])}")
        print(f"Definition markers: {sorted([int(x) for x in def_markers])}")
        if body_markers == def_markers:
            print("[OK] Footnotes in 1891_synod_cohort5.md are 100% bijective!")
        else:
            print(f"[ERROR] Footnote mismatch: diff = {body_markers ^ def_markers}")
            all_ok = False

    # Check Deity Trinity pronouns in Profession of Faith
    print("\n--- Deity Pronoun Verification ---")
    trinity_lower = ["he was crucified", "who proceedeth", "whose kingdom", "for without me"]
    lower_found = []
    for f in [root / "Typikons" / "1891 Lviv Synod" / "Final MD" / "1891_synod_cohort5.md"]:
        text = f.read_text(encoding="utf-8")
        for pat in trinity_lower:
            m = re.findall(re.escape(pat), text, re.IGNORECASE)
            # check exact lower case match
            exact_lower = re.findall(pat, text)
            if exact_lower:
                lower_found.append((f.name, pat, len(exact_lower)))
    if lower_found:
        print(f"[WARNING/CHECK] Lowercase patterns found: {lower_found}")
    else:
        print("[OK] Trinity pronouns correctly capitalized!")

    if all_ok:
        print("\n[SUCCESS] All checks PASSED!")
    else:
        print("\n[FAILURE] Some checks FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
