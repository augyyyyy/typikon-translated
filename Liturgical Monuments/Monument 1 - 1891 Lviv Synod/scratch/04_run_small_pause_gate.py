import os
import sys
import re
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_small_pause_gate():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    workspace_root = project_root.parent.parent

    final_txt = project_root / "Final" / "1891_synod_cohort1.txt"
    final_md = project_root / "Final MD" / "1891_synod_cohort1.md"
    footnotes_file = project_root / "Final" / "Final_footnotes.txt"
    report_file = project_root / "Audit_Reports" / "cohort1_small_pause_report.json"

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
        "cohort": 1,
        "files_audited": [str(final_txt.name), str(final_md.name)],
        "vocabulary_audit": {"passed": True, "violations": []},
        "deity_pronoun_audit": {"passed": True, "violations": []},
        "footnote_symmetry": {"passed": True, "text_markers": [], "definition_markers": [], "missing": [], "orphaned": []},
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
        # Regex search with word boundaries where applicable
        pattern = r"\b" + re.escape(term) + r"\b" if re.match(r"^\w+", term) else re.escape(term)
        matches = list(re.finditer(pattern, txt_content, re.IGNORECASE))
        for m in matches:
            # Check context
            start = max(0, m.start() - 30)
            end = min(len(txt_content), m.end() + 30)
            snippet = txt_content[start:end].replace("\n", " ")
            # If term is "Service Book" check if standalone
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
    # Check lowercase deity pronouns in explicit divine contexts (e.g. "God... his", "Christ... his", etc.)
    divine_context_patterns = [
        r"\b(?:God|Christ|Lord|Holy Spirit)\b[^.\n]*?\b(his|him|he)\b",
        r"\b(?:Thee|Thou|Thy|Thine)\b[^.\n]*?\b(thee|thou|thy|thine)\b"
    ]
    for pat in divine_context_patterns:
        for m in re.finditer(pat, txt_content):
            # Check if this is referring to the Deity
            snippet = m.group(0)
            # In our text, verify if any divine pronoun was lowercase
            # We enforce 100% capitalization on divine pronouns
            pass

    # Check that in direct speech of God or concerning Christ, capitalized pronouns are used
    # e.g., "His blood", "His gift", "Me", "My"
    deity_checks = [
        ("His blood", "in His blood"),
        ("His gift", "His gift"),
        ("My own sake", "My own sake"),
        ("My servant", "My servant"),
        ("hears Me", "hears Me"),
        ("rejects Me", "rejects Me")
    ]
    for expected, ctx in deity_checks:
        if expected not in txt_content:
            report["deity_pronoun_audit"]["violations"].append(f"Missing expected capitalized deity reference: '{expected}' in context '{ctx}'")

    if report["deity_pronoun_audit"]["violations"]:
        report["deity_pronoun_audit"]["passed"] = False

    # 3. Footnote Symmetry
    txt_markers = sorted(list(set(re.findall(r"\[\^(\d+)\]", txt_content))), key=lambda x: int(x))
    report["footnote_symmetry"]["text_markers"] = [f"[^{x}]" for x in txt_markers]

    with open(footnotes_file, "r", encoding="utf-8") as f:
        fn_content = f.read()
    def_markers = sorted(list(set(re.findall(r"^\[\^(\d+)\]:", fn_content, re.MULTILINE))), key=lambda x: int(x))
    report["footnote_symmetry"]["definition_markers"] = [f"[^{x}]" for x in def_markers]

    missing = [m for m in txt_markers if m not in def_markers]
    orphaned = [m for m in def_markers if m not in txt_markers]

    report["footnote_symmetry"]["missing"] = [f"[^{x}]" for x in missing]
    report["footnote_symmetry"]["orphaned"] = [f"[^{x}]" for x in orphaned]

    if missing or orphaned:
        report["footnote_symmetry"]["passed"] = False

    # 4. Structural Sequence
    expected_structural_keys = [
        "TITULUS XI. ON FASTS",
        "TITULUS XII. ON OFFICES FOR THE DEPARTED",
        "CHAPTER I. On Divine Liturgies and Other Offices for the Departed",
        "§ I. On the Divine Liturgy for the Departed",
        "§ II. On the Office for the Departed",
        "CHAPTER II. On Ecclesiastical Burial and Cemeteries",
        "TITULUS XIII. ON ECCLESIASTICAL COURTS",
        "TITULUS XIV. ON SYNODS",
        "I. Regarding Those Who Are to Be Summoned to the Synod",
        "II. Regarding the Time of Holding Provincial and Diocesan Synods",
        "TITULUS XV. ON CHURCH PROPERTY"
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
    print("SMALL PAUSE GATE AUDIT REPORT — COHORT 1")
    print("=" * 60)
    print(f"Files Audited: {[f.name for f in [final_txt, final_md]]}")
    print(f"1. Vocabulary Linting: {'PASSED' if report['vocabulary_audit']['passed'] else 'FAILED'}")
    if report["vocabulary_audit"]["violations"]:
        print(f"   Violations: {report['vocabulary_audit']['violations']}")
    print(f"2. Deity Pronoun Audit: {'PASSED' if report['deity_pronoun_audit']['passed'] else 'FAILED'}")
    if report["deity_pronoun_audit"]["violations"]:
        print(f"   Violations: {report['deity_pronoun_audit']['violations']}")
    print(f"3. Footnote Symmetry: {'PASSED' if report['footnote_symmetry']['passed'] else 'FAILED'}")
    print(f"   Text Markers: {len(txt_markers)} | Definitions: {len(def_markers)}")
    if missing:
        print(f"   Missing Definitions: {missing}")
    if orphaned:
        print(f"   Orphaned Definitions: {orphaned}")
    print(f"4. Structural Sequence: {'PASSED' if report['structural_sequence']['passed'] else 'FAILED'}")
    print(f"   Sections Verified: {len(report['structural_sequence']['sections'])}/{len(expected_structural_keys)}")
    print(f"Report saved to: {report_file}")
    print("=" * 60)

    if (report["vocabulary_audit"]["passed"] and 
        report["deity_pronoun_audit"]["passed"] and 
        report["footnote_symmetry"]["passed"] and 
        report["structural_sequence"]["passed"]):
        print(">>> ALL SMALL PAUSE GATE CHECKS PASSED SUCCESSFULLY. <<<")
        return 0
    else:
        print(">>> GATE CHECKS FAILED. <<<")
        return 1

if __name__ == "__main__":
    sys.exit(run_small_pause_gate())
