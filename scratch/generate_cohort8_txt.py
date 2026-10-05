from pathlib import Path
import re

def build_cohort8_txt():
    project_root = Path(__file__).resolve().parent.parent
    md_file = project_root / "Typikons" / "1891 Lviv Synod" / "Final MD" / "1891_synod_cohort8.md"
    fn_file = project_root / "Typikons" / "1891 Lviv Synod" / "Draft" / "1891_lviv_synod_cohort8_footnotes.txt"
    target_txt = project_root / "Typikons" / "1891 Lviv Synod" / "Final" / "1891_synod_cohort8.txt"

    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    with open(fn_file, "r", encoding="utf-8") as f:
        fn_content = f.read()

    # We want the text body from section 1 to before section 4 (footnotes)
    # In 1891_synod_cohort8.md:
    # "## 1. Decrees of the Ruthenian Provincial Synod: Titulus II. On the Mysteries and Their Administration (Continued)"
    # down to "## 4. Scholarly Critical Apparatus & Footnotes"
    body_match = re.search(
        r"## 1\. Decrees of the Ruthenian Provincial Synod: Titulus II.*?\n\n(.*?)\n\n## 4\. Scholarly Critical Apparatus & Footnotes",
        md_content,
        re.DOTALL
    )
    if not body_match:
        raise ValueError("Could not find body section in 1891_synod_cohort8.md")

    raw_body = body_match.group(1)

    # Let's inspect pages in raw_body:
    # Pages are formatted as:
    # *(Physical Page XX / Leaf pYY)*
    # Let's convert to:
    # [Physical Page XX / Leaf pYY]
    # And dividers:
    # "---" -> "--------------------------------------------------------------------------------"
    
    lines = raw_body.splitlines()
    cleaned_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check page marker
        m_page = re.match(r"^\*\((Physical Page \d+ / Leaf p\d+)\)\*$", line.strip())
        if m_page:
            cleaned_lines.append(f"[{m_page.group(1)}]")
            i += 1
            continue

        # Check horizontal rule
        if line.strip() == "---":
            cleaned_lines.append("--------------------------------------------------------------------------------")
            i += 1
            continue

        # Check headers:
        # ### CHAPTER V. On the Mystery of Anointing (Holy Unction)
        # or ## 2. Decrees of the Ruthenian Provincial Synod: Titulus III...
        # or #### Section 1: On Exorcisms
        m_h2 = re.match(r"^## \d+\. Decrees of the Ruthenian Provincial Synod:\s*(.*)$", line.strip())
        if m_h2:
            title = m_h2.group(1).upper()
            cleaned_lines.append(f"\n{'='*80}\n{title}\n{'='*80}")
            i += 1
            continue

        m_h3 = re.match(r"^### (CHAPTER [IVXLCDM]+\.?)\s*(.*)$", line.strip(), re.IGNORECASE)
        if m_h3:
            chap_num = m_h3.group(1).upper()
            chap_title = m_h3.group(2).upper()
            cleaned_lines.append(f"{chap_num}\n{chap_title}")
            i += 1
            continue

        m_h4 = re.match(r"^#### (Section \d+:?\s*.*)$", line.strip(), re.IGNORECASE)
        if m_h4:
            sec_title = m_h4.group(1).upper()
            cleaned_lines.append(f"[{sec_title}]")
            i += 1
            continue

        m_h3_other = re.match(r"^### (.*)$", line.strip())
        if m_h3_other:
            other_title = m_h3_other.group(1).upper()
            cleaned_lines.append(f"[{other_title}]")
            i += 1
            continue

        # Clean italics and bold from normal text:
        # *italic* -> italic
        # **bold** -> bold
        # Also clean markdown formatting from quotes
        clean_text = line
        # Remove bold
        clean_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", clean_text)
        # Remove italics
        clean_text = re.sub(r"\*([^*]+)\*", r"\1", clean_text)
        
        cleaned_lines.append(clean_text)
        i += 1

    body_text = "\n".join(cleaned_lines)
    # Normalize multiple blank lines to double newlines
    body_text = re.sub(r"\n{3,}", "\n\n", body_text)

    # Footnotes:
    # Strip italics from footnotes for clean plain text apparatus
    fn_clean_lines = []
    for fn_l in fn_content.splitlines():
        cl = re.sub(r"\*\*([^*]+)\*\*", r"\1", fn_l)
        cl = re.sub(r"\*([^*]+)\*", r"\1", cl)
        fn_clean_lines.append(cl)
    fn_clean = "\n".join(fn_clean_lines)

    header = """ACTS AND DECREES OF THE RUTHENIAN PROVINCIAL SYNOD OF LVIV (1891)
Tier 1 (The Calibration Anchor) — Cohort 8: Physical Pages 99–118 (Leaves p101–p120)

================================================================================
TITULUS II ON THE SACRAMENTS (CONCLUDED), TITULUS III ON SACRAMENTALS,
AND TITULUS IV ON THE PUBLIC WORSHIP OF GOD
(Physical Leaves p101–p120 / Book Pages 99–118)
================================================================================
"""

    footer_banner = """
================================================================================
SCHOLARLY CRITICAL APPARATUS & FOOTNOTES
================================================================================
"""

    final_txt = header + "\n" + body_text.strip() + "\n" + footer_banner + "\n" + fn_clean.strip() + "\n"

    with open(target_txt, "w", encoding="utf-8") as f:
        f.write(final_txt)

    print(f"Generated {target_txt}: {len(final_txt)} bytes, {len(final_txt.splitlines())} lines.")

if __name__ == "__main__":
    build_cohort8_txt()
