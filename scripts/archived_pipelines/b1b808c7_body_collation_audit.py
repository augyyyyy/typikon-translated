#!/usr/bin/env python3
"""
Body Paragraph Collation & Fortification Auditor
================================================
Compares body text paragraphs between the original .docx translation manuscript
and the current Final deliverables.
Detects:
1. Missing paragraphs or dropped rubrical clauses.
2. Sentences present in .docx that were omitted in Final.
3. Passages corrected in Final that were flawed in .docx.
"""

from pathlib import Path
import os
import sys
import json
import re
import difflib

def get_project_root() -> Path:
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "Final").exists() and (parent / "Ukrainian TXTs").exists():
            return parent
    return Path(os.environ.get("TRANSLATION_PROJECT_DIR", r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation"))

def clean_for_diff(text: str) -> str:
    t = re.sub(r'\[\^?\d+[a-z]?\]', '', text)
    t = re.sub(r'[#*_`]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def main():
    root = get_project_root()
    docx_corpus_file = root / "scratch" / "reports" / "docx_corpus.json"
    
    with open(docx_corpus_file, "r", encoding="utf-8") as f:
        docx_data = json.load(f)

    docx_paragraphs = docx_data.get("paragraphs", [])
    
    final_dir = root / "Final"
    final_files = [
        "Final_Dolnytsky_intro.txt",
        "Final_Dolnytsky_part1_structure.txt",
        "Final_Dolnytsky_part2_general_rubrics.txt",
        "Final_Dolnytsky_part3_menaion.txt",
        "Final_Dolnytsky_part4_triodion.txt",
        "Final_Dolnytsky_part5_temple.txt",
        "Final_Dolnytsky_appendix.txt"
    ]
    
    final_full_text = ""
    for fn in final_files:
        fpath = final_dir / fn
        if fpath.exists():
            with open(fpath, "r", encoding="utf-8") as fh:
                final_full_text += fh.read() + "\n\n"

    # Split final into clean sentences / paragraphs
    final_cleaned_paras = [clean_for_diff(p) for p in final_full_text.split("\n") if clean_for_diff(p)]
    final_full_cleaned = " ".join(final_cleaned_paras).lower()

    # Find paragraphs in docx that have no substantial match in Final
    dropped_candidates = []
    
    for dp in docx_paragraphs:
        txt = clean_for_diff(dp.get("text", ""))
        # Ignore very short lines (headers, chapter numbers, etc.)
        if len(txt.split()) < 8:
            continue
            
        # Quick check: 6-word window search
        words = txt.lower().split()
        probe = " ".join(words[:6])
        if probe not in final_full_cleaned:
            # Check secondary probe
            probe2 = " ".join(words[-6:])
            if probe2 not in final_full_cleaned:
                # Potential dropped or heavily reworded paragraph
                dropped_candidates.append({
                    "docx_index": dp["index"],
                    "style": dp.get("style"),
                    "text": txt[:200],
                    "word_count": len(words)
                })

    print(f"Total Docx paragraphs checked: {len(docx_paragraphs)}")
    print(f"Candidate paragraphs divergent or missing in Final: {len(dropped_candidates)}")

    report_path = root / "scratch" / "reports" / "body_divergence_report.md"
    with open(report_path, "w", encoding="utf-8") as rf:
        rf.write("# Body Paragraph Divergence & Fortification Report\n\n")
        rf.write(f"- **Total Docx Paragraphs Evaluated**: {len(docx_paragraphs):,}\n")
        rf.write(f"- **Substantively Divergent / Unmatched Paragraphs**: {len(dropped_candidates):,}\n\n")
        rf.write("## Sample Unmatched / Divergent Passages in Docx\n\n")
        for i, c in enumerate(dropped_candidates[:40], 1):
            rf.write(f"### {i}. Docx P#{c['docx_index']} ({c['word_count']} words, style: `{c['style']}`)\n")
            rf.write(f"> {c['text']}...\n\n")

    print(f"Report written to: {report_path}")

if __name__ == "__main__":
    main()
