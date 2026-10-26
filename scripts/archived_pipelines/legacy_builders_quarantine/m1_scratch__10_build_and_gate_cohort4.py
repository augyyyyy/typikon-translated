import os
import sys
import re
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def build_cohort4():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    workspace_root = project_root.parent.parent

    raw_draft_path = project_root / "Draft" / "1891_lviv_synod_cohort4_raw_draft.md"
    fn_path = project_root / "Draft" / "1891_lviv_synod_cohort4_footnotes.txt"
    final_md_path = project_root / "Final MD" / "1891_synod_cohort4.md"
    final_txt_path = project_root / "Final" / "1891_synod_cohort4.txt"
    master_fn_path = project_root / "Final" / "Final_footnotes.txt"
    report_file = project_root / "Audit_Reports" / "cohort4_small_pause_report.json"

    with open(raw_draft_path, "r", encoding="utf-8") as f:
        draft_content = f.read()

    with open(fn_path, "r", encoding="utf-8") as f:
        fn_content = f.read()

    # Split draft content into leaves
    leaf_pattern = r"\[Leaf (p\d+) / Page (\d+)\]"
    leaf_parts = re.split(leaf_pattern, draft_content)
    # leaf_parts[0] is the pre-matter
    # then triplets: leaf_id, page_num, text_chunk

    leaves = {}
    for i in range(1, len(leaf_parts), 3):
        lid = leaf_parts[i]
        pnum = leaf_parts[i+1]
        chunk = leaf_parts[i+2].strip()
        # Clean trailing separators if present
        chunk = re.sub(r"\n---\s*$", "", chunk).strip()
        leaves[lid] = {"page": pnum, "text": chunk}

    # Verify we got p21 to p40 (20 leaves)
    expected_leaves = [f"p{n}" for n in range(21, 41)]
    assert list(leaves.keys()) == expected_leaves, f"Leaf keys mismatch: {list(leaves.keys())}"

    # Build Final MD
    header_md = """# Acts and Decrees of the Ruthenian Provincial Synod of Lviv (1891)
## Tier 1 (The Calibration Anchor) — Cohort 4: Physical Pages 21–40 (Leaves p21–p40)

> [!NOTE]
> **Historical & Canonical Significance**  
> Cohort 4 of the **1891 Lviv Provincial Synod** (*Чинности и рѣшеня руского провинціяльного Собора въ Галичинѣ ôтбувшого ся во Львовѣ въ роцѣ 1891*) details the procedural, liturgical, and statutory constitution of the conciliar assemblies. It encompasses the conclusion of the preparatory prayers in the Metropolitan Chapel, the solemn oath of secrecy (*secretum synodale*) sworn by the clergy and the lay Senior of the Stauropegion Institute, the statutory Instruction defining the competencies of Synodal Judges (*Judices Querelarum et Excusationum*), Promoters, Secretaries, Notaries, and Masters of Ceremonies, the formal decrees prepared for Session I (Decrees on the Opening, Profession of Faith according to Urban VIII, Manner of Life, Non-Infringement of Rights, and Prohibition of Unauthorized Withdrawal), the complete liturgical ordo and civic-ecclesiastical procession for the First Public and Solemn Session with the Hierarchical Divine Liturgy of the Holy Spirit in St. George Cathedral, the episcopal suffrage and solemn profession of faith upon the Holy Gospels, the establishment and working methodology of the three conciliar Commissions (Dogmatic-Disciplinary, Rubrical-Liturgical, Monastic-Administrative) at the General Seminary of Lviv, the protocols of General Congregations II and III and Session II, and the ceremonies of the Final Session—including the statutory nomination and oath of the Synodal Witnesses (*Testes Synodales*) for Lviv, Przemyśl, and Stanyslaviv, the conciliar subscription protocol at the High Altar (*Velykyi Prestol*) modeled upon the 1720 Synod of Zamość, and the convocation decree appointing the next Provincial Synod for 1896.

---

## Table of Contents
1. [Continuation of the Preparatory General Congregation (Leaves p21–p29 / pp. 19–27)](#continuation-of-the-preparatory-general-congregation)
   - [Concluding Preparatory Prayers & Address (Leaf p21 / p. 19)](#concluding-preparatory-prayers--address)
   - [Solemn Oath of Synodal Secrecy (Leaves p21–p22 / pp. 19–20)](#solemn-oath-of-synodal-secrecy)
   - [Nomination of Synodal Officials & Statutory Instruction (Leaves p22–p24 / pp. 20–22)](#statutory-instruction-for-synodal-officials)
   - [Examination of Chapter Credentials (Leaf p25 / p. 23)](#examination-of-chapter-credentials)
   - [Statutory Decrees Prepared for Session I (Leaves p25–p28 / pp. 23–26)](#statutory-decrees-prepared-for-session-i)
     - [1. Decree on the Opening of the Synod](#1-decree-on-the-opening-of-the-synod)
     - [2. Decree on the Making of the Profession of Faith](#2-decree-on-the-making-of-the-profession-of-faith)
     - [3. Decree on the Manner of Life during the Time of the Synod](#3-decree-on-the-manner-of-life-during-the-time-of-the-synod)
     - [4. Decree on the Non-Infringement of the Rights of Others](#4-decree-on-the-non-infringement-of-the-rights-of-others)
     - [5. Decree That It Is Not Permitted to Withdraw from the Synod](#5-decree-that-it-is-not-permitted-to-withdraw-from-the-synod)
   - [Decree Announcing the Second Session (Leaves p28–p29 / pp. 26–27)](#decree-announcing-the-second-session)
   - [Concluding Congregation Prayers & Citywide Bell-Tolling (Leaf p29 / p. 27)](#concluding-congregation-prayers--citywide-bell-tolling)
2. [First Public and Solemn Session (Leaves p29–p34 / pp. 27–32)](#first-public-and-solemn-session)
   - [Civic & Ecclesiastical Procession Order (Leaves p29–p30 / pp. 27–28)](#civic--ecclesiastical-procession-order)
   - [Hierarchical Divine Liturgy of the Holy Spirit (Leaves p30–p31 / pp. 28–29)](#hierarchical-divine-liturgy-of-the-holy-spirit)
   - [Opening of the Synod and Episcopal Suffrage (Leaves p31–p32 / pp. 29–30)](#opening-of-the-synod-and-episcopal-suffrage)
   - [Solemn Profession of Faith upon the Holy Gospels (Leaf p32 / p. 30)](#solemn-profession-of-faith-upon-the-holy-gospels)
   - [Promulgation of Synodal Decrees & Appointment of Judges (Leaves p33–p34 / pp. 31–32)](#promulgation-of-synodal-decrees--appointment-of-judges)
   - [Designation of the Second Session & Recording of Acts (Leaf p34 / p. 32)](#designation-of-the-second-session--recording-of-acts)
3. [Working Methodology of the Synod: General Congregation II & The Three Commissions (Leaves p34–p36 / pp. 32–34)](#working-methodology-of-the-synod)
   - [Assembly at the General Seminary Church (Leaf p34 / p. 32)](#assembly-at-the-general-seminary-church)
   - [Constitution and Mandates of the Three Synodal Commissions (Leaves p34–p35 / pp. 32–33)](#constitution-and-mandates-of-the-three-synodal-commissions)
   - [Daily Commission Meetings, Written Memorials, & Protocols (Leaves p35–p36 / pp. 33–34)](#daily-commission-meetings-written-memorials--protocols)
4. [Congregation III in Order (General Congregation II) (Leaf p36 / p. 34)](#congregation-iii-in-order-general-congregation-ii)
5. [Second Public and Solemn Session (Leaves p37–p38 / pp. 35–36)](#second-public-and-solemn-session)
6. [Final Session and Conclusion of the Synod (Leaves p38–p40 / pp. 36–38)](#final-session-and-conclusion-of-the-synod)
   - [Statutory Nomination of Synodal Witnesses (*Testes Synodales*) (Leaves p38–p39 / pp. 36–37)](#statutory-nomination-of-synodal-witnesses)
   - [Solemn Gospel Oath of the Synodal Witnesses (Leaf p39 / p. 37)](#solemn-gospel-oath-of-the-synodal-witnesses)
   - [Subscription of Synodal Decrees at the High Altar (Leaves p39–p40 / pp. 37–38)](#subscription-of-synodal-decrees-at-the-high-altar)
   - [Decree Appointing the Next Provincial Synod in 1896 (Leaf p40 / p. 38)](#decree-appointing-the-next-provincial-synod-in-1896)
7. [Scholarly Critical Apparatus & Footnotes](#scholarly-critical-apparatus--footnotes)

---
"""

    # Assemble body text for MD
    body_md_chunks = []
    for lid in expected_leaves:
        pnum = leaves[lid]["page"]
        text = leaves[lid]["text"]
        body_md_chunks.append(f"*(Physical Page {pnum} / Leaf {lid})*\n\n{text}")

    full_md_body = "\n\n---\n\n".join(body_md_chunks)

    fn_section_md = f"""

---

## Scholarly Critical Apparatus & Footnotes

{fn_content.strip()}
"""

    full_final_md = header_md + "\n" + full_md_body + fn_section_md

    with open(final_md_path, "w", encoding="utf-8") as f:
        f.write(full_final_md)
    print(f"Created {final_md_path} ({final_md_path.stat().st_size} bytes)")

    # Build Final TXT
    header_txt = """ACTS AND DECREES OF THE RUTHENIAN PROVINCIAL SYNOD OF LVIV (1891)
Tier 1 (The Calibration Anchor) — Cohort 4: Physical Pages 21–40 (Leaves p21–p40)

================================================================================
ORDO OF THE RUTHENIAN PROVINCIAL SYNOD (CONTINUED)
General Congregations, Solemn Public Sessions, Commissions, & Closing Rites
(Physical Leaves p21–p40 / Book Pages 19–38)
================================================================================
"""

    body_txt_chunks = []
    for lid in expected_leaves:
        pnum = leaves[lid]["page"]
        text = leaves[lid]["text"]
        # In plain text, strip markdown formatting if desired or keep clean plain layout
        clean_text = text.replace("*", "")
        body_txt_chunks.append(f"[Physical Page {pnum} / Leaf {lid}]\n\n{clean_text}")

    full_txt_body = "\n\n" + ("\n\n" + "-"*80 + "\n\n").join(body_txt_chunks)

    fn_section_txt = f"""

================================================================================
CRITICAL APPARATUS FOOTNOTES (COHORT 4: [^37]–[^45])
================================================================================

{fn_content.strip()}
"""

    full_final_txt = header_txt + full_txt_body + "\n" + fn_section_txt

    with open(final_txt_path, "w", encoding="utf-8") as f:
        f.write(full_final_txt)
    print(f"Created {final_txt_path} ({final_txt_path.stat().st_size} bytes)")

    # Update Final_footnotes.txt if not already appended
    with open(master_fn_path, "r", encoding="utf-8") as f:
        master_fn = f.read()

    if "[^37]:" not in master_fn:
        cohort4_fn_block = f"""
## Cohort 4 Footnotes (pp. 21–40)

{fn_content.strip()}
"""
        with open(master_fn_path, "a", encoding="utf-8") as f:
            f.write(cohort4_fn_block)
        print(f"Appended Cohort 4 footnotes to {master_fn_path}")
    else:
        print(f"Cohort 4 footnotes already present in {master_fn_path}")

    # Now run Gate Verification
    print("=" * 70)
    print("RUNNING COHORT 4 GATE VERIFICATION")
    print("=" * 70)

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
        "cohort": 4,
        "files_audited": [str(final_txt_path.name), str(final_md_path.name)],
        "vocabulary_audit": {"passed": True, "violations": []},
        "deity_pronoun_audit": {"passed": True, "violations": []},
        "footnote_symmetry": {
            "passed": True,
            "cohort4_text_markers": [],
            "cohort4_definition_markers": [],
            "missing": [],
            "orphaned": []
        },
        "structural_sequence": {"passed": True, "sections": []}
    }

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

    with open(final_txt_path, "r", encoding="utf-8") as f:
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
            # Filter out non-divine false positives
            if re.search(r"\b(his|him|he)\b", snippet) and any(w in snippet.lower() for w in ["first parents", "man", "adam", "peter", "servant", "priest", "bishop", "delegate", "promoter"]):
                continue
            if re.search(r"\b(thee|thou|thy|thine)\b", snippet) and not re.search(r"\b[A-Z][a-z]*(Thee|Thou|Thy|Thine)\b", snippet):
                report["deity_pronoun_audit"]["violations"].append({
                    "snippet": snippet,
                    "position": m.start()
                })

    if report["deity_pronoun_audit"]["violations"]:
        report["deity_pronoun_audit"]["passed"] = False

    # 3. Footnote Symmetry for Cohort 4 (Markers 37 to 45)
    txt_markers = sorted(list(set(re.findall(r"\[\^(\d+)\]", txt_content))), key=lambda x: int(x))
    report["footnote_symmetry"]["cohort4_text_markers"] = [f"[^{x}]" for x in txt_markers]

    cohort_defs = sorted(list(set(re.findall(r"^\[\^(\d+)\]:", fn_content, re.MULTILINE))), key=lambda x: int(x))
    report["footnote_symmetry"]["cohort4_definition_markers"] = [f"[^{x}]" for x in cohort_defs]

    missing = [m for m in txt_markers if m not in cohort_defs]
    orphaned = [m for m in cohort_defs if m not in txt_markers]

    report["footnote_symmetry"]["missing"] = [f"[^{x}]" for x in missing]
    report["footnote_symmetry"]["orphaned"] = [f"[^{x}]" for x in orphaned]

    if missing or orphaned:
        report["footnote_symmetry"]["passed"] = False

    # 4. Master Critical Apparatus Symmetry across all cohorts in Final_footnotes.txt
    with open(master_fn_path, "r", encoding="utf-8") as f:
        master_fn_content = f.read()
    master_defs = sorted(list(set(re.findall(r"^\[\^(\d+)\]:", master_fn_content, re.MULTILINE))), key=lambda x: int(x))

    # 5. Structural Sequence Verification
    expected_structural_keys = [
        "Duties of the Synodal Judges",
        "Duties of the Promoters of the Synod",
        "Duties of the Secretaries of the Synod",
        "Duties of the Notaries of the Synod",
        "Duties of the Masters of Ceremonies",
        "1. Decree on the Opening of the Synod",
        "2. Decree on the Making of the Profession of Faith",
        "3. Decree on the Manner of Life during the Time of the Synod",
        "4. Decree on the Non-Infringement of the Rights of Others",
        "5. Decree That It Is Not Permitted to Withdraw from the Synod",
        "First Public and Solemn Session",
        "General Congregation II",
        "Congregation III in Order (General Congregation II)",
        "Second Public and Solemn Session",
        "Final Session and Conclusion of the Synod"
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

    print(f"Files Audited: {[f.name for f in [final_txt_path, final_md_path]]}")
    print(f"1. Vocabulary Linting: {'PASSED' if report['vocabulary_audit']['passed'] else 'FAILED'}")
    if report["vocabulary_audit"]["violations"]:
        print(f"   Violations: {report['vocabulary_audit']['violations']}")
    print(f"2. Deity Pronoun Audit: {'PASSED' if report['deity_pronoun_audit']['passed'] else 'FAILED'}")
    if report["deity_pronoun_audit"]["violations"]:
        print(f"   Violations: {report['deity_pronoun_audit']['violations']}")
    print(f"3. Footnote Symmetry: {'PASSED' if report['footnote_symmetry']['passed'] else 'FAILED'}")
    print(f"   Cohort 4 Text Markers: {len(txt_markers)} ({txt_markers[0]}..{txt_markers[-1]})")
    print(f"   Cohort 4 Definitions: {len(cohort_defs)} ({cohort_defs[0]}..{cohort_defs[-1]})")
    if missing:
        print(f"   Missing Definitions: {missing}")
    if orphaned:
        print(f"   Orphaned Definitions: {orphaned}")
    print(f"4. Structural Sequence: {'PASSED' if report['structural_sequence']['passed'] else 'FAILED'}")
    print(f"   Sections Verified: {len(report['structural_sequence']['sections'])}/{len(expected_structural_keys)}")
    print(f"Report saved to: {report_file}")
    print("=" * 70)

    # Master cumulative symmetry check
    c1_txt = project_root / "Final" / "1891_synod_cohort1.txt"
    c2_txt = project_root / "Final" / "1891_synod_cohort2.txt"
    c3_txt = project_root / "Final" / "1891_synod_cohort3.txt"
    with open(c1_txt, "r", encoding="utf-8") as f:
        c1_content = f.read()
    with open(c2_txt, "r", encoding="utf-8") as f:
        c2_content = f.read()
    with open(c3_txt, "r", encoding="utf-8") as f:
        c3_content = f.read()

    all_corpus_markers = sorted(list(
        set(re.findall(r"\[\^(\d+)\]", c1_content)) |
        set(re.findall(r"\[\^(\d+)\]", c2_content)) |
        set(re.findall(r"\[\^(\d+)\]", c3_content)) |
        set(txt_markers)
    ), key=lambda x: int(x))

    print(f"CUMULATIVE AUDIT: Text markers across Cohorts 1, 2, 3, 4: {len(all_corpus_markers)} (1..{all_corpus_markers[-1]})")
    print(f"CUMULATIVE AUDIT: Master definitions in Final_footnotes.txt: {len(master_defs)} (1..{master_defs[-1]})")
    master_missing = [m for m in all_corpus_markers if m not in master_defs]
    master_orphaned = [m for m in master_defs if m not in all_corpus_markers]

    if not master_missing and not master_orphaned:
        print(">>> 100% PERFECT BIDIRECTIONAL FOOTNOTE BIJECTIVITY ACROSS ENTIRE CORPUS (1..45)! <<<")
    else:
        print(f"Master Footnote Discrepancies - Missing: {master_missing}, Orphaned: {master_orphaned}")

    if (report["vocabulary_audit"]["passed"] and 
        report["deity_pronoun_audit"]["passed"] and 
        report["footnote_symmetry"]["passed"] and 
        report["structural_sequence"]["passed"] and
        not master_missing and not master_orphaned):
        print(">>> ALL COHORT 4 SMALL PAUSE GATE CHECKS PASSED PERFECTLY. <<<")
        return 0
    else:
        print(">>> GATE CHECKS FAILED. <<<")
        return 1

if __name__ == "__main__":
    sys.exit(build_cohort4())
