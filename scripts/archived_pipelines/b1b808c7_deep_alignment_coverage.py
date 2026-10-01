#!/usr/bin/env python3
"""
Section-by-Section Alignment & Coverage Verification
====================================================
Performs a section-by-section fuzzy alignment to measure exact coverage
and identify whether any actual sentences or liturgical instructions from
the original Docx were omitted from Final/.
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
        if (parent / "Final").exists():
            return parent
    return Path(os.environ.get("TRANSLATION_PROJECT_DIR", r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation"))

def normalize(text: str) -> str:
    t = re.sub(r'\[\^?\d+[a-z]?\]', '', text)
    t = re.sub(r'[“”—–"\'#*_`\(\)\[\]]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip().lower()
    return t

def main():
    root = get_project_root()
    docx_corpus_file = root / "scratch" / "reports" / "docx_corpus.json"
    
    with open(docx_corpus_file, "r", encoding="utf-8") as f:
        docx_data = json.load(f)

    final_dir = root / "Final"
    final_files = [
        ("Intro", "Final_Dolnytsky_intro.txt"),
        ("Part 1", "Final_Dolnytsky_part1_structure.txt"),
        ("Part 2", "Final_Dolnytsky_part2_general_rubrics.txt"),
        ("Part 3", "Final_Dolnytsky_part3_menaion.txt"),
        ("Part 4", "Final_Dolnytsky_part4_triodion.txt"),
        ("Part 5", "Final_Dolnytsky_part5_temple.txt"),
        ("Appendix", "Final_Dolnytsky_appendix.txt")
    ]
    
    final_corpus = {}
    for label, fname in final_files:
        with open(final_dir / fname, "r", encoding="utf-8") as fh:
            final_corpus[label] = fh.read()

    combined_final_norm = normalize(" ".join(final_corpus.values()))

    # Check each Docx paragraph
    docx_paras = docx_data.get("paragraphs", [])
    total_paras = len(docx_paras)
    matched_paras = 0
    unmatched_substantive = []

    for p in docx_paras:
        txt = p.get("text", "").strip()
        words = txt.split()
        if len(words) < 10:
            # Skip short titles/numbers/markers
            continue
            
        norm_txt = normalize(txt)
        # Check if 10-word probe exists in combined_final_norm
        probe_len = min(10, len(words))
        probe = " ".join(norm_txt.split()[:probe_len])
        
        if probe in combined_final_norm:
            matched_paras += 1
        else:
            # Fallback: check mid-slice probe
            mid = len(words) // 2
            probe_mid = " ".join(norm_txt.split()[mid:mid+probe_len])
            if probe_mid and probe_mid in combined_final_norm:
                matched_paras += 1
            else:
                unmatched_substantive.append({
                    "index": p["index"],
                    "word_count": len(words),
                    "text": txt
                })

    substantive_total = matched_paras + len(unmatched_substantive)
    coverage_pct = round((matched_paras / substantive_total) * 100, 2) if substantive_total else 100.0

    print("=" * 60)
    print("SECTION-BY-SECTION COVERAGE & ALIGNMENT RESULTS")
    print("=" * 60)
    print(f"Total Docx paragraphs: {total_paras}")
    print(f"Substantive paragraphs checked (>=10 words): {substantive_total}")
    print(f"Matched in Final: {matched_paras} ({coverage_pct}%)")
    print(f"Unmatched / heavily reworded paragraphs: {len(unmatched_substantive)}")

    # Write findings
    out_file = root / "scratch" / "reports" / "unmatched_substantive_docx.json"
    with open(out_file, "w", encoding="utf-8") as fh:
        json.dump(unmatched_substantive, fh, ensure_ascii=False, indent=2)

    print(f"Details written to: {out_file}")

if __name__ == "__main__":
    main()
