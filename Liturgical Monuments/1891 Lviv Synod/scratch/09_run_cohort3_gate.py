import os
import sys
import re
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_cohort3_gate():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    workspace_root = project_root.parent.parent

    final_txt = project_root / "Final" / "1891_synod_cohort3.txt"
    final_md = project_root / "Final MD" / "1891_synod_cohort3.md"
    cohort_fn_file = project_root / "Draft" / "1891_lviv_synod_cohort3_footnotes.txt"
    master_footnotes_file = project_root / "Final" / "Final_footnotes.txt"
    report_file = project_root / "Audit_Reports" / "cohort3_small_pause_report.json"

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
        "cohort": 3,
        "files_audited": [str(final_txt.name), str(final_md.name)],
        "vocabulary_audit": {"passed": True, "violations": []},
        "deity_pronoun_audit": {"passed": True, "violations": []},
        "footnote_symmetry": {
            "passed": True,
            "cohort3_text_markers": [],
            "cohort3_definition_markers": [],
            "missing": [],
            "orphaned": []
        },
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
    divine_context_patterns = [
        r"\b(?:God|Christ|Lord|Holy Spirit|Savior)\b[^.\n]*?\b(his|him|he)\b",
        r"\b(?:Thee|Thou|Thy|Thine)\b[^.\n]*?\b(thee|thou|thy|thine)\b"
    ]
    for pat in divine_context_patterns:
        for m in re.finditer(pat, txt_content, re.IGNORECASE):
            snippet = m.group(0)
            # Filter out non-divine false positives (e.g. human persons in relative proximity)
            # Check specifically if lowercase pronoun was applied directly to God/Christ/Spirit
            if re.search(r"\b(his|him|he)\b", snippet) and any(w in snippet.lower() for w in ["first parents", "man", "adam", "peter", "servant", "priest"]):
                continue
            if re.search(r"\b(thee|thou|thy|thine)\b", snippet) and not re.search(r"\b[A-Z][a-z]*(Thee|Thou|Thy|Thine)\b", snippet):
                report["deity_pronoun_audit"]["violations"].append({
                    "snippet": snippet,
                    "position": m.start()
                })

    if report["deity_pronoun_audit"]["violations"]:
        report["deity_pronoun_audit"]["passed"] = False

    # 3. Footnote Symmetry for Cohort 3 (Markers 27 to 36)
    txt_markers = sorted(list(set(re.findall(r"\[\^(\d+)\]", txt_content))), key=lambda x: int(x))
    report["footnote_symmetry"]["cohort3_text_markers"] = [f"[^{x}]" for x in txt_markers]

    with open(cohort_fn_file, "r", encoding="utf-8") as f:
        fn_content = f.read()
    cohort_defs = sorted(list(set(re.findall(r"^\[\^(\d+)\]:", fn_content, re.MULTILINE))), key=lambda x: int(x))
    report["footnote_symmetry"]["cohort3_definition_markers"] = [f"[^{x}]" for x in cohort_defs]

    missing = [m for m in txt_markers if m not in cohort_defs]
    orphaned = [m for m in cohort_defs if m not in txt_markers]

    report["footnote_symmetry"]["missing"] = [f"[^{x}]" for x in missing]
    report["footnote_symmetry"]["orphaned"] = [f"[^{x}]" for x in orphaned]

    if missing or orphaned:
        report["footnote_symmetry"]["passed"] = False

    # 4. Master Critical Apparatus Symmetry across all cohorts in Final_footnotes.txt
    with open(master_footnotes_file, "r", encoding="utf-8") as f:
        master_fn_content = f.read()
    master_defs = sorted(list(set(re.findall(r"^\[\^(\d+)\]:", master_fn_content, re.MULTILINE))), key=lambda x: int(x))

    # 5. Structural Sequence Verification
    expected_structural_keys = [
        "OFFICIAL FRONT MATTER & PROVENANCE",
        "DOCUMENT I. LETTER OF THE RUTHENIAN METROPOLITAN PROVINCE OF HALYCH",
        "DOCUMENT II. LETTER OF THE METROPOLITAN OF THE RUTHENIAN PROVINCE OF HALYCH",
        "DOCUMENT III. LETTER OF CARDINAL GIOVANNI SIMEONI",
        "DOCUMENT IV. ANNOUNCEMENT OF THE CONVOCATION OF THE RUTHENIAN PROVINCIAL SYNOD",
        "DOCUMENT V. ORDO TO BE OBSERVED IN THE CONVOCATION AND CELEBRATION",
        "Preparatory General Congregation",
        "Blessed is our God always, now and forever, and unto the ages of ages.",
        "O Heavenly King, the Comforter, Spirit of truth"
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

    print("=" * 70)
    print("SMALL PAUSE GATE AUDIT REPORT — COHORT 3")
    print("=" * 70)
    print(f"Files Audited: {[f.name for f in [final_txt, final_md]]}")
    print(f"1. Vocabulary Linting: {'PASSED' if report['vocabulary_audit']['passed'] else 'FAILED'}")
    if report["vocabulary_audit"]["violations"]:
        print(f"   Violations: {report['vocabulary_audit']['violations']}")
    print(f"2. Deity Pronoun Audit: {'PASSED' if report['deity_pronoun_audit']['passed'] else 'FAILED'}")
    if report["deity_pronoun_audit"]["violations"]:
        print(f"   Violations: {report['deity_pronoun_audit']['violations']}")
    print(f"3. Footnote Symmetry: {'PASSED' if report['footnote_symmetry']['passed'] else 'FAILED'}")
    print(f"   Cohort 3 Text Markers: {len(txt_markers)} ({txt_markers[0]}..{txt_markers[-1]})")
    print(f"   Cohort 3 Definitions: {len(cohort_defs)} ({cohort_defs[0]}..{cohort_defs[-1]})")
    if missing:
        print(f"   Missing Definitions: {missing}")
    if orphaned:
        print(f"   Orphaned Definitions: {orphaned}")
    print(f"4. Structural Sequence: {'PASSED' if report['structural_sequence']['passed'] else 'FAILED'}")
    print(f"   Sections Verified: {len(report['structural_sequence']['sections'])}/{len(expected_structural_keys)}")
    print(f"Report saved to: {report_file}")
    print("=" * 70)

    # Master corpus symmetry check
    c1_txt = project_root / "Final" / "1891_synod_cohort1.txt"
    c2_txt = project_root / "Final" / "1891_synod_cohort2.txt"
    with open(c1_txt, "r", encoding="utf-8") as f:
        c1_content = f.read()
    with open(c2_txt, "r", encoding="utf-8") as f:
        c2_content = f.read()

    all_corpus_markers = sorted(list(
        set(re.findall(r"\[\^(\d+)\]", c1_content)) |
        set(re.findall(r"\[\^(\d+)\]", c2_content)) |
        set(txt_markers)
    ), key=lambda x: int(x))

    print(f"CUMULATIVE AUDIT: Text markers across Cohorts 1, 2, and 3: {len(all_corpus_markers)} (1..{all_corpus_markers[-1]})")
    print(f"CUMULATIVE AUDIT: Master definitions in Final_footnotes.txt: {len(master_defs)} (1..{master_defs[-1]})")
    master_missing = [m for m in all_corpus_markers if m not in master_defs]
    master_orphaned = [m for m in master_defs if m not in all_corpus_markers]

    if not master_missing and not master_orphaned:
        print(">>> 100% PERFECT BIDIRECTIONAL FOOTNOTE BIJECTIVITY ACROSS ENTIRE CORPUS! <<<")
    else:
        print(f"Master Footnote Discrepancies - Missing: {master_missing}, Orphaned: {master_orphaned}")

    if (report["vocabulary_audit"]["passed"] and 
        report["deity_pronoun_audit"]["passed"] and 
        report["footnote_symmetry"]["passed"] and 
        report["structural_sequence"]["passed"] and
        not master_missing and not master_orphaned):
        print(">>> ALL COHORT 3 SMALL PAUSE GATE CHECKS PASSED PERFECTLY. <<<")
        return 0
    else:
        print(">>> GATE CHECKS FAILED. <<<")
        return 1

if __name__ == "__main__":
    sys.exit(run_cohort3_gate())
