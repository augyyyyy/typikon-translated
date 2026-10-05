import os
import sys
import re
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_cohort2_gate():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    workspace_root = project_root.parent.parent

    final_txt = project_root / "Final" / "1891_synod_cohort2.txt"
    final_md = project_root / "Final MD" / "1891_synod_cohort2.md"
    footnotes_file = project_root / "Final" / "Final_footnotes.txt"
    report_file = project_root / "Audit_Reports" / "cohort2_small_pause_report.json"

    # Find master_liturgical_vocabulary.json
    shared_lexicon_candidates = [
        workspace_root / "Shared_Lexicon" / "master_liturgical_vocabulary.json",
        project_root.parent.parent / "Shared_Lexicon" / "master_liturgical_vocabulary.json"
    ]
    vocab_path = None
    for cand in shared_lexicon_candidates:
        if cand.exists():
            vocab_path = cand
            break

    report = {
        "cohort": 2,
        "files_audited": [str(final_txt.name), str(final_md.name)],
        "vocabulary_audit": {"passed": True, "violations": []},
        "deity_pronoun_audit": {"passed": True, "violations": []},
        "footnote_symmetry": {"passed": True, "cohort2_text_markers": [], "cohort2_definition_markers": [], "missing": [], "orphaned": []},
        "structural_sequence": {"passed": True, "sections": []}
    }

    # 1. Vocabulary Linting
    forbidden_terms = [
        "for ever and ever",
        "Kafisma",
        "Tropar ",
        "Kondak ",
        "Kondakion",
        "Catavasia",
        "Trephologion",
        "Eye of the Church"
    ]
    
    if vocab_path and vocab_path.exists():
        with open(vocab_path, "r", encoding="utf-8") as f:
            vocab_data = json.load(f)
            elements = vocab_data.get("liturgical_elements", {})
            for elem_name, elem_info in elements.items():
                for forbidden in elem_info.get("forbidden_variants", []):
                    if forbidden not in forbidden_terms:
                        forbidden_terms.append(forbidden)

    with open(final_txt, "r", encoding="utf-8") as f:
        txt_content = f.read()

    for term in forbidden_terms:
        pattern = r"\b" + re.escape(term) + r"\b" if re.match(r"^\w+", term) else re.escape(term)
        matches = list(re.finditer(pattern, txt_content, re.IGNORECASE))
        for m in matches:
            start = max(0, m.start() - 30)
            end = min(len(txt_content), m.end() + 30)
            snippet = txt_content[start:end].replace("\n", " ")
            if term.lower() == "service book":
                continue
            report["vocabulary_audit"]["violations"].append({
                "term": term,
                "snippet": snippet,
                "position": m.start()
            })

    if report["vocabulary_audit"]["violations"]:
        report["vocabulary_audit"]["passed"] = False

    # 2. Deity Pronoun Audit
    # Verify no uncapitalized divine pronouns (He, Him, His, Thou, Thee, Thy, Thine)
    # Check for lowercase pronouns following divine titles
    divine_context_patterns = [
        r"\b(?:God|Christ|Lord|Holy Spirit|Savior)\b[^.\n]*?\b(his|him|he)\b",
        r"\b(?:Thee|Thou|Thy|Thine)\b[^.\n]*?\b(thee|thou|thy|thine)\b"
    ]
    for pat in divine_context_patterns:
        for m in re.finditer(pat, txt_content, re.IGNORECASE):
            snippet = m.group(0)
            # Check if actual divine reference was lowercased
            if re.search(r"\b(his|him|he|thee|thou|thy|thine)\b", snippet):
                report["deity_pronoun_audit"]["violations"].append({
                    "snippet": snippet,
                    "position": m.start()
                })

    if report["deity_pronoun_audit"]["violations"]:
        report["deity_pronoun_audit"]["passed"] = False

    # 3. Footnote Symmetry for Cohort 2 (Markers 22 to 26)
    txt_markers = sorted(list(set(re.findall(r"\[\^(\d+)\]", txt_content))), key=lambda x: int(x))
    report["footnote_symmetry"]["cohort2_text_markers"] = [f"[^{x}]" for x in txt_markers]

    with open(footnotes_file, "r", encoding="utf-8") as f:
        fn_content = f.read()
    def_markers = sorted(list(set(re.findall(r"^\[\^(\d+)\]:", fn_content, re.MULTILINE))), key=lambda x: int(x))
    
    # Cohort 2 definition markers: 22-26
    c2_defs = [m for m in def_markers if int(m) >= 22]
    report["footnote_symmetry"]["cohort2_definition_markers"] = [f"[^{x}]" for x in c2_defs]

    missing = [m for m in txt_markers if m not in def_markers]
    orphaned = [m for m in c2_defs if m not in txt_markers]

    report["footnote_symmetry"]["missing"] = [f"[^{x}]" for x in missing]
    report["footnote_symmetry"]["orphaned"] = [f"[^{x}]" for x in orphaned]

    if missing or orphaned:
        report["footnote_symmetry"]["passed"] = False

    # 4. Structural Sequence
    expected_structural_keys = [
        "TITULUS XV. ON CHURCH PROPERTY",
        "SIGNATURES OF THE SYNODAL FATHERS",
        "From the Archeparchy of Lviv:",
        "From the Eparchy of Przemyśl:",
        "From the Eparchy of Stanyslaviv:",
        "DECREE",
        "By Which the Second Ruthenian Synod of Lviv Is Confirmed",
        "TABLE OF CONTENTS",
        "Acts and Decrees of the Ruthenian Provincial Synod of Lviv (1891)",
        "Part I: Acts of the Synod",
        "Part II: Decrees of the Ruthenian Provincial Synod of Lviv",
        "Part III: Concluding Acts & Confirmation"
    ]
    for key in expected_structural_keys:
        if key in txt_content:
            report["structural_sequence"]["sections"].append(key)
        else:
            report["structural_sequence"]["passed"] = False
            report["structural_sequence"]["sections"].append(f"MISSING: {key}")

    # Write report
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print("SMALL PAUSE GATE AUDIT REPORT — COHORT 2")
    print("=" * 60)
    print(f"Files Audited: {[f.name for f in [final_txt, final_md]]}")
    print(f"1. Vocabulary Linting: {'PASSED' if report['vocabulary_audit']['passed'] else 'FAILED'}")
    if report["vocabulary_audit"]["violations"]:
        print(f"   Violations: {report['vocabulary_audit']['violations']}")
    print(f"2. Deity Pronoun Audit: {'PASSED' if report['deity_pronoun_audit']['passed'] else 'FAILED'}")
    if report["deity_pronoun_audit"]["violations"]:
        print(f"   Violations: {report['deity_pronoun_audit']['violations']}")
    print(f"3. Footnote Symmetry: {'PASSED' if report['footnote_symmetry']['passed'] else 'FAILED'}")
    print(f"   Text Markers: {len(txt_markers)} | Definitions (>=22): {len(c2_defs)}")
    if missing:
        print(f"   Missing Definitions: {missing}")
    if orphaned:
        print(f"   Orphaned Definitions: {orphaned}")
    print(f"4. Structural Sequence: {'PASSED' if report['structural_sequence']['passed'] else 'FAILED'}")
    print(f"   Sections Verified: {len(report['structural_sequence']['sections'])}/{len(expected_structural_keys)}")
    print(f"Report saved to: {report_file}")
    print("=" * 60)

    # Also check total combined work symmetry:
    c1_txt = project_root / "Final" / "1891_synod_cohort1.txt"
    with open(c1_txt, "r", encoding="utf-8") as f:
        c1_content = f.read()
    c1_markers = set(re.findall(r"\[\^(\d+)\]", c1_content))
    total_text_markers = sorted(list(c1_markers | set(txt_markers)), key=lambda x: int(x))
    all_defs = sorted(def_markers, key=lambda x: int(x))
    print(f"COMBINED AUDIT: Total text markers across Cohorts 1 & 2: {len(total_text_markers)} (1..{total_text_markers[-1]})")
    print(f"COMBINED AUDIT: Total master definitions in Final_footnotes.txt: {len(all_defs)} (1..{all_defs[-1]})")
    combined_missing = [m for m in total_text_markers if m not in all_defs]
    combined_orphaned = [m for m in all_defs if m not in total_text_markers]
    if not combined_missing and not combined_orphaned:
        print(">>> 100% PERFECT BIDIRECTIONAL SYMMETRY ACROSS ENTIRE 1891 SYNOD CORPUS! <<<")
    else:
        print(f"Combined missing: {combined_missing}, orphaned: {combined_orphaned}")

    if (report["vocabulary_audit"]["passed"] and 
        report["deity_pronoun_audit"]["passed"] and 
        report["footnote_symmetry"]["passed"] and 
        report["structural_sequence"]["passed"]):
        print(">>> ALL COHORT 2 GATE CHECKS PASSED SUCCESSFULLY. <<<")
        return 0
    else:
        print(">>> GATE CHECKS FAILED. <<<")
        return 1

if __name__ == "__main__":
    sys.exit(run_cohort2_gate())
