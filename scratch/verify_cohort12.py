"""Cohort 12 Verification Suite
Validates file sizes, banned phrases, footnote bijectivity, and leaf continuity
in compliance with MTS-1 and AGENTS.md standards.
"""
from pathlib import Path
import re
import sys

def main() -> int:
    base_dir = Path("Typikons/1891 Lviv Synod")
    errors = []

    files_to_check = {
        "Source Text": base_dir / "Source Text" / "1891_lviv_synod_cohort12_source.txt",
        "Raw Draft MD": base_dir / "Draft" / "1891_lviv_synod_cohort12_raw_draft.md",
        "Draft Footnotes": base_dir / "Draft" / "1891_lviv_synod_cohort12_footnotes.txt",
        "Final MD": base_dir / "Final MD" / "1891_synod_cohort12.md",
        "Final TXT": base_dir / "Final" / "1891_synod_cohort12.txt",
        "Master Footnotes": base_dir / "Final" / "Final_footnotes.txt",
    }

    print("=== 1. FILE EXISTENCE & METRICS ===")
    for label, path in files_to_check.items():
        if not path.exists():
            errors.append(f"Missing file: {label} at {path}")
            print(f"[-] {label}: MISSING ({path})")
        else:
            size = path.stat().st_size
            lines = len(path.read_text(encoding="utf-8").splitlines())
            if size == 0:
                errors.append(f"Empty file: {label} ({path})")
                print(f"[-] {label}: EMPTY ({path})")
            else:
                print(f"[+] {label}: {size:,} bytes, {lines:,} lines ({path.name})")

    if errors:
        print("\nAborting further checks due to missing files.")
        return 1

    print("\n=== 2. BANNED PHRASES CHECK (MTS-1) ===")
    banned_regex = re.compile(r"for\s+ever\s+and\s+ever", re.IGNORECASE)
    for label in ["Raw Draft MD", "Final MD", "Final TXT", "Master Footnotes"]:
        path = files_to_check[label]
        content = path.read_text(encoding="utf-8")
        matches = banned_regex.findall(content)
        if matches:
            errors.append(f"Banned phrase 'for ever and ever' found in {label}: {len(matches)} instance(s)")
            print(f"[-] {label}: FOUND {len(matches)} instance(s) of banned phrase")
        else:
            print(f"[+] {label}: Clean (0 instances of banned phrase)")

    print("\n=== 3. FOOTNOTE BIJECTIVITY CHECK ([^186] - [^209]) ===")
    expected_fns = set(range(186, 210))
    final_md_text = files_to_check["Final MD"].read_text(encoding="utf-8")
    final_txt_text = files_to_check["Final TXT"].read_text(encoding="utf-8")
    master_fn_text = files_to_check["Master Footnotes"].read_text(encoding="utf-8")

    # In-text calls: [^N] not preceded by newline (which would be definition)
    md_calls = set(int(m) for m in re.findall(r"(?<!\n)\[\^(\d+)\]", final_md_text))
    txt_calls = set(int(m) for m in re.findall(r"(?<!\n)\[\^(\d+)\]", final_txt_text))
    defs = set(int(m) for m in re.findall(r"(?m)^\[\^(\d+)\]:", master_fn_text))

    cohort_md_calls = md_calls.intersection(expected_fns)
    cohort_txt_calls = txt_calls.intersection(expected_fns)
    cohort_defs = defs.intersection(expected_fns)

    print(f"Expected footnote range: 186 to 209 (Total: {len(expected_fns)})")
    print(f"Calls in Final MD: {len(cohort_md_calls)} / {len(expected_fns)}")
    print(f"Calls in Final TXT: {len(cohort_txt_calls)} / {len(expected_fns)}")
    print(f"Definitions in Master Footnotes: {len(cohort_defs)} / {len(expected_fns)}")

    missing_md = expected_fns - cohort_md_calls
    if missing_md:
        errors.append(f"Missing footnote calls in Final MD: {sorted(missing_md)}")
        print(f"[-] Missing in Final MD: {sorted(missing_md)}")
    else:
        print("[+] Final MD calls: 100% matched")

    missing_txt = expected_fns - cohort_txt_calls
    if missing_txt:
        errors.append(f"Missing footnote calls in Final TXT: {sorted(missing_txt)}")
        print(f"[-] Missing in Final TXT: {sorted(missing_txt)}")
    else:
        print("[+] Final TXT calls: 100% matched")

    missing_defs = expected_fns - cohort_defs
    if missing_defs:
        errors.append(f"Missing footnote definitions in Master Footnotes: {sorted(missing_defs)}")
        print(f"[-] Missing in Master Footnotes: {sorted(missing_defs)}")
    else:
        print("[+] Master Footnotes definitions: 100% matched")

    print("\n=== 4. LEAF MARKER SEQUENCE & CONTINUITY ===")
    expected_leaves = [f"p{i}" for i in range(181, 201)]
    for label in ["Source Text", "Raw Draft MD", "Final MD"]:
        path = files_to_check[label]
        content = path.read_text(encoding="utf-8")
        found_leaves = re.findall(r"===\s*LEAF\s*(p\d+)\s*===", content)
        if found_leaves == expected_leaves:
            print(f"[+] {label}: All 20 leaves (p181-p200) present in exact sequence")
        else:
            errors.append(f"{label} leaf sequence mismatch. Found: {found_leaves[:3]}...{found_leaves[-3:]}")
            print(f"[-] {label}: Leaf sequence mismatch! Found {len(found_leaves)} leaves")

    # Final TXT uses ASCII boxed header format
    txt_content = files_to_check["Final TXT"].read_text(encoding="utf-8")
    found_txt_leaves = re.findall(r"\[Physical Page \d+ / Leaf (p\d+) / Book Page \d+\]", txt_content)
    if found_txt_leaves == expected_leaves:
        print(f"[+] Final TXT: All 20 leaves (p181-p200) present in exact sequence")
    else:
        errors.append(f"Final TXT leaf sequence mismatch. Found: {found_txt_leaves[:3]}...{found_txt_leaves[-3:]}")
        print(f"[-] Final TXT: Leaf sequence mismatch! Found {len(found_txt_leaves)} leaves")

    print("\n=== 5. BOOK PAGE CONTINUITY (177 - 196) ===")
    expected_pages = list(range(177, 197))
    source_content = files_to_check["Source Text"].read_text(encoding="utf-8")
    found_pages = [int(p) for p in re.findall(r"\[Стр\.\s*(\d+)\]", source_content)]
    if found_pages == expected_pages:
        print(f"[+] Source Text: All 20 book pages (177-196) present in exact sequence")
    else:
        errors.append(f"Source book page mismatch. Found: {found_pages}")
        print(f"[-] Source Text: Book page mismatch! Found {found_pages}")

    print("\n=== 6. LITURGICAL TERMINOLOGY & REALIA AUDIT ===")
    realia_terms = [
        "Tetrapod",
        "Krylosy",
        "Kovcheh",
        "Melchizedek",
        "Iliton",
        "Sakkos",
        "Dikirion",
    ]
    for term in realia_terms:
        count_md = len(re.findall(rf"\b{term}\b", final_md_text, re.IGNORECASE))
        if count_md > 0:
            print(f"[+] Realia '{term}': {count_md} occurrence(s) in Final MD")
        else:
            errors.append(f"Realia '{term}' not found in Final MD")
            print(f"[-] Realia '{term}': NOT FOUND")

    print("\n==========================================")
    if errors:
        print(f"FAILED: {len(errors)} error(s) detected:")
        for err in errors:
            print(f"  - {err}")
        return 1
    else:
        print("SUCCESS: All verification checks passed with 100% compliance!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
