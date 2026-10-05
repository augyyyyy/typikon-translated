import sys
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def assemble():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    c1_md_path = project_root / "Final MD" / "1891_synod_cohort1.md"
    c2_md_path = project_root / "Final MD" / "1891_synod_cohort2.md"
    footnotes_path = project_root / "Final" / "Final_footnotes.txt"

    with open(c1_md_path, "r", encoding="utf-8") as f:
        c1_md = f.read()

    with open(c2_md_path, "r", encoding="utf-8") as f:
        c2_md = f.read()

    with open(footnotes_path, "r", encoding="utf-8") as f:
        fn_text = f.read()

    # In c1_md, extract body from Titulus XI up to the start of Titulus XV § 6
    # In c1_md, Titulus XV ends with: "**6.** If any change should have to be made with respect to church property, let administrators, in order to undertake that..."
    # In c2_md, Titulus XV concludes with: "**6.** *(Concluded)* ...that they have recourse to their Ordinaries..."
    # We stitch Titulus XV cleanly!
    
    # Extract c1 body from "## Titulus XI. On Fasts" up to before "**6.** If any change"
    c1_split = c1_md.split("**6.** If any change should have to be made with respect to church property, let administrators, in order to undertake that...")[0]
    
    # In c2, extract from "**6.** *(Concluded)* ...that they have recourse" up to before "## Scholarly Critical Apparatus & Footnotes"
    c2_body_split = c2_md.split("## Titulus XV. On Church Property *(Conclusion)*\n*(Continued from p. 257 / Leaf p262)*\n\n**6.** *(Concluded)* ...that they have recourse")
    c2_body = "**6.** If any change should have to be made with respect to church property, let administrators, in order to undertake that, have recourse" + c2_body_split[1].split("## Scholarly Critical Apparatus & Footnotes")[0]

    # Clean up c1 body to start at Titulus XI
    c1_body = "## Titulus XI. On Fasts" + c1_split.split("## Titulus XI. On Fasts")[1]

    complete_md = f"""# Acts and Decrees of the Ruthenian Provincial Synod of Lviv (1891)
## Complete Tier 1 Text: Physical Pages 241–270 (Leaves p245–p274)

> [!NOTE]
> **Historical & Statutory Context**  
> The 1891 Lviv Provincial Synod (*Чинности и рѣшеня руского провинціяльного Собора въ Галичинѣ ôтбувшого ся во Львовѣ въ роцѣ 1891*, published 1896; with Appendices published 1897) forms the legal, canonical, and liturgical bedrock for Fr. Isidore Dolnytsky’s 1899 Typikon and the contemporary 2010 UGCC Synodal Typikon. This complete translation edition encompasses the statutory decrees on Fasting disciplines (*Titulus XI*), the complete statutory ordo for Memorial Services and Divine Liturgies for the Departed (*Titulus XII*), Ecclesiastical Courts (*Titulus XIII*), Synodal Governance (*Titulus XIV*), the Administration of Church Property (*Titulus XV*), the historic Signatures of the Synodal Fathers, the Decree of Papal Confirmation, the Official Synodal Table of Contents, and the 26-entry Scholarly Critical Apparatus.

---

## Comprehensive Table of Contents
1. [Titulus XI. On Fasts](#titulus-xi-on-fasts)
2. [Titulus XII. On Offices for the Departed](#titulus-xii-on-offices-for-the-departed)
   - [Chapter I. On Divine Liturgies and Other Offices for the Departed](#chapter-i-on-divine-liturgies-and-other-offices-for-the-departed)
   - [§ I. On the Divine Liturgy for the Departed](#-i-on-the-divine-liturgy-for-the-departed)
   - [§ II. On the Office for the Departed](#-ii-on-the-office-for-the-departed)
   - [Chapter II. On Ecclesiastical Burial and Cemeteries](#chapter-ii-on-ecclesiastical-burial-and-cemeteries)
3. [Titulus XIII. On Ecclesiastical Courts](#titulus-xiii-on-ecclesiastical-courts)
4. [Titulus XIV. On Synods](#titulus-xiv-on-synods)
   - [I. Regarding Those Who Are to Be Summoned to the Synod](#i-regarding-those-who-are-to-be-summoned-to-the-synod)
   - [II. Regarding the Time of Holding Provincial and Diocesan Synods](#ii-regarding-the-time-of-holding-provincial-and-diocesan-synods)
5. [Titulus XV. On Church Property](#titulus-xv-on-church-property)
6. [Signatures of the Synodal Fathers](#signatures-of-the-synodal-fathers)
   - [The Synodal Hierarchy & Presidency](#the-synodal-hierarchy--presidency)
   - [From the Archeparchy of Lviv](#from-the-archeparchy-of-lviv)
   - [From the Eparchy of Przemyśl](#from-the-eparchy-of-przemyśl)
   - [From the Eparchy of Stanyslaviv](#from-the-eparchy-of-stanyslaviv)
7. [Decree of Papal Confirmation](#decree-of-papal-confirmation)
8. [Official Synodal Table of Contents](#official-synodal-table-of-contents)
9. [Scholarly Critical Apparatus & Footnotes](#scholarly-critical-apparatus--footnotes)

---

{c1_body.strip()}

{c2_body.strip()}

---

## Scholarly Critical Apparatus & Footnotes

{chr(10).join([line for line in fn_text.splitlines() if line.startswith('[^')])}
"""

    out_complete_md = project_root / "Final MD" / "1891_synod_complete.md"
    with open(out_complete_md, "w", encoding="utf-8") as f:
        f.write(complete_md)
    print(f"Created {out_complete_md} ({out_complete_md.stat().st_size} bytes)")

    # Plain text version
    c1_txt_path = project_root / "Final" / "1891_synod_cohort1.txt"
    c2_txt_path = project_root / "Final" / "1891_synod_cohort2.txt"
    with open(c1_txt_path, "r", encoding="utf-8") as f:
        c1_txt = f.read()
    with open(c2_txt_path, "r", encoding="utf-8") as f:
        c2_txt = f.read()

    # Split c1_txt before "6. If any change should have to be made with respect to church property, let administrators, in order to undertake that..."
    c1_txt_split = c1_txt.split("6. If any change should have to be made with respect to church property, let administrators, in order to undertake that...")[0]
    
    # Split c2_txt
    c2_txt_split = c2_txt.split("6. (Concluded) ...that they have recourse")
    c2_txt_body = "6. If any change should have to be made with respect to church property, let administrators, in order to undertake that, have recourse" + c2_txt_split[1].split("================================================================================\nCRITICAL APPARATUS FOOTNOTES")[0]

    complete_txt = f"""ACTS AND DECREES OF THE RUTHENIAN PROVINCIAL SYNOD OF LVIV (1891)
Complete Tier 1 Edition: Physical Pages 241–270 (Leaves p245–p274)

{c1_txt_split.strip()}

{c2_txt_body.strip()}

================================================================================
CRITICAL APPARATUS FOOTNOTES
================================================================================

{chr(10).join([line for line in fn_text.splitlines() if line.startswith('[^')])}
"""
    out_complete_txt = project_root / "Final" / "1891_synod_complete.txt"
    with open(out_complete_txt, "w", encoding="utf-8") as f:
        f.write(complete_txt)
    print(f"Created {out_complete_txt} ({out_complete_txt.stat().st_size} bytes)")

if __name__ == "__main__":
    assemble()
