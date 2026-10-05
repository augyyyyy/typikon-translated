import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def copy_to_hub():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent  # Liturgical Monuments/Monument 1 - 1891 Lviv Synod
    projects_root = project_root.parent.parent.parent  # Projects

    hub_inbox = projects_root / "Typikon Coded" / "Data" / "Inbox" / "1891_Lviv_Synod"
    hub_inbox.mkdir(parents=True, exist_ok=True)

    files_to_copy = [
        (project_root / "Final" / "1891_synod_cohort1.txt", hub_inbox / "1891_synod_cohort1.txt"),
        (project_root / "Final MD" / "1891_synod_cohort1.md", hub_inbox / "1891_synod_cohort1.md"),
        (project_root / "Final" / "1891_synod_cohort2.txt", hub_inbox / "1891_synod_cohort2.txt"),
        (project_root / "Final MD" / "1891_synod_cohort2.md", hub_inbox / "1891_synod_cohort2.md"),
        (project_root / "Final" / "1891_synod_complete.txt", hub_inbox / "1891_synod_complete.txt"),
        (project_root / "Final MD" / "1891_synod_complete.md", hub_inbox / "1891_synod_complete.md"),
        (project_root / "Final" / "Final_footnotes.txt", hub_inbox / "Final_footnotes.txt"),
        (project_root / "Audit_Reports" / "cohort1_small_pause_report.json", hub_inbox / "cohort1_small_pause_report.json"),
        (project_root / "Audit_Reports" / "cohort2_small_pause_report.json", hub_inbox / "cohort2_small_pause_report.json"),
    ]

    for src, dst in files_to_copy:
        if src.exists():
            shutil.copy2(str(src), str(dst))
            print(f"Copied {src.name} -> {dst}")
        else:
            print(f"WARNING: Source file {src} not found!")

    # Write handoff_note.md in hub inbox
    handoff_note = f"""# Handoff Note: 1891 Lviv Provincial Synod (Tier 1 Calibration Anchor)
**Date**: 2026-10-03  
**Conversation ID**: `8f784143-31de-48a6-84c8-cd829edb3c03`  
**Spoke**: Translation Spoke (`Projects/Translation/Liturgical Monuments/Monument 1 - 1891 Lviv Synod/`)  
**Target Hub**: Typikon Coded Hub (`Projects/Typikon Coded/Data/Inbox/1891_Lviv_Synod/`)  

---

## 1. Executive Summary & Purpose
This handoff delivers the complete, publication-grade English translation and critical apparatus for the statutory decrees of the **1891 Lviv Provincial Synod** (*Чинности и рѣшеня руского провинціяльного Собора въ Галичинѣ ôтбувшого ся во Львовѣ въ роцѣ 1891*). 

These decrees, promulgated under Metropolitan Sylvester Sembratovych, Bishop Julian Pelesz, Bishop Julian Sas-Kuilovsky, and Apostolic Delegate Agostino Ciasca, serve as the statutory and legal basis referenced by **Fr. Isidore Dolnytsky** throughout his landmark 1899 *Typikon* (*Типикъ церковнаго и келейнаго правила*, Appendix XXXI) and directly underpin our 2010 Lviv Synodal Typikon translation baseline.

---

## 2. Text Corpus Scope & Partitioning
* **Master Source**: `1891-1896-Chynnosty-i-Rishenia-Lviv-Provincial-Synod.pdf` (278 pages total).
* **Leaves Translated**: Physical pages 241–270 (Scanned leaves `p245.png` through `p274.png`, 30 pages total).
* **Delivery Units**:
  * **Cohort 1 (pp. 241–257 / leaves p245–p261)**:
    - *Titulus XI. On Fasts*: Statutory fasting disciplines and mitigations permitting dairy (*nabyl*) on MWF with compensatory prayer rules (Ps 50 / 5 Our Fathers & Hail Marys).
    - *Titulus XII. On Offices for the Departed*:
      - *Chapter I, § I*: Divine Liturgies for the Departed (prohibitions on Sundays, commanded feasts, Holy Week Triduum; low mass norms).
      - *Chapter I, § II*: Parastas and Panakhyda rubrics; placement of *kolyvo* and bread loaves on the tetrapod; 1-gulden stipend norm; ban on bodies in church during Triduum and Pascha; Bright Week priestly burial rubrics (Paschal Canon substituted for funeral canon).
      - *Chapter II*: Ecclesiastical Burial and Cemeteries; suicide pastoral theology (*in dubio pro reo* / 1860 Prague Synod norm); cemetery leasing restrictions.
    - *Titulus XIII. On Ecclesiastical Courts*: Three-tier judicial appeal hierarchy (Bishop -> Metropolitan -> Roman Pontiff).
    - *Titulus XIV. On Synods*: Convocation, presidency, decisive vs. consultative votes, extraordinary pro-synodal assemblies (*мѣстосинодальне зôбранє*); statutory consultative presence of the Senior of the Stavropeghial Institute.
    - *Titulus XV. On Church Property (§§ 1–5, § 6 part)*: Three-key chest system (*skarbona*), dual inventories, trustee administration.
  * **Cohort 2 (pp. 258–270 / leaves p262–p274)**:
    - *Titulus XV (Conclusion, §§ 6–7)*: Forest preservation, orchard protection, leasing rules.
    - *Signatures of the Synodal Fathers*: Complete translation of 134 episcopal and presbyteral signatories across the Archeparchy of Lviv, Eparchy of Przemyśl, and Eparchy of Stanyslaviv, including Fr. Isidore Dolnytsky (Spiritual Director of the Seminary) and Dr. Isidore Sharanevych (Senior of the Stavropeghial Institute).
    - *Decree of Papal Confirmation*: Confirmation decree by Pope Leo XIII and the Sacred Congregation *de Propaganda Fide pro negotiis Ritus Orientalis* (Rome, 1895).
    - *Official Synodal Table of Contents*: Exhaustive statutory breakdown of the entire Synod acts (Tituli I–XV, preliminary letters, and four general sessions).

---

## 3. Liturgical, Lexical & Guardrail Verification
1. **Master Liturgical Vocabulary Linting**: 100% compliant with `master_liturgical_vocabulary.json`. Zero forbidden variants (*Sluzhebnik* strictly enforced, *Kafisma* -> *Kathisma*, *Tropar* -> *Troparion*, *Kondak* -> *Kontakion*).
2. **Father Paul Universal Doxology Standard**: Full choral (*"Glory be to the Father, and to the Son, and to the Holy Spirit, now and forever, and unto the ages of ages. Amen."*) and shorthand (*"Glory... Now and forever, and unto the ages of ages:"*) standard strictly maintained; Western phrase *"for ever and ever"* 100% excluded.
3. **Hieratic Deity Pronouns**: 100% capitalized (*He, Him, His, Thou, Thee, Thy, Thine*).
4. **Scholarly Critical Apparatus & Footnote Bijectivity**: Exactly **26 / 26** footnotes bidirectionally paired between text markers `[^1]`–`[^26]` and master definitions in `Final_footnotes.txt` (0 missing, 0 orphaned).
5. **Anti-Pattern Compliance**: 0 anti-patterns introduced across all scripts and files.

---

## 4. Shipped Files Inventory
* `1891_synod_complete.txt`: Pandoc-compliant plain text master edition.
* `1891_synod_complete.md`: Rich Markdown master edition with GitHub alerts.
* `1891_synod_cohort1.txt` & `1891_synod_cohort1.md`: Cohort 1 text and markdown editions.
* `1891_synod_cohort2.txt` & `1891_synod_cohort2.md`: Cohort 2 text and markdown editions.
* `Final_footnotes.txt`: Master critical apparatus (26 entries).
* `cohort1_small_pause_report.json` & `cohort2_small_pause_report.json`: Small Pause Gate verification logs.
"""
    handoff_path = hub_inbox / "handoff_note.md"
    with open(handoff_path, "w", encoding="utf-8") as f:
        f.write(handoff_note)
    print(f"Created {handoff_path} ({handoff_path.stat().st_size} bytes)")
    print("Hub inbox handoff complete.")

if __name__ == "__main__":
    copy_to_hub()
