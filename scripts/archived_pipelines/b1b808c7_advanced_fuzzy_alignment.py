#!/usr/bin/env python3
"""
Advanced Fuzzy Alignment & Omission Detector
=============================================
Normalizes vocabulary variations (Prokeimenon -> Prokimenon, leavetaking -> apodosis, etc.)
and tests semantic paragraph matching using difflib to detect whether any true liturgical
rubrics were omitted in Final.
"""

from pathlib import Path
import os
import sys
import json
import re
import difflib

VOCAB_MAP = {
    r'\bprokeimenon\b': 'prokimenon',
    r'\bprokeimena\b': 'prokimena',
    r'\bleavetaking\b': 'apodosis',
    r'\bleave-taking\b': 'apodosis',
    r'\boko tserkovne\b': 'tserkovne oko',
    r'\beye of the church\b': 'tserkovne oko',
    r'\btrephologion\b': 'anthologion',
    r'\bsedalen\b': 'sessional hymn',
    r'\bsidalen\b': 'sessional hymn',
    r'\bkondak\b': 'kontakion',
    r'\birmos\b': 'heirmos',
    r'\birmoi\b': 'heirmoi',
    r'\bpochayiv\b': 'pochaiv',
    r'\bpochaev\b': 'pochaiv',
    r'\bmegalynaria\b': 'magnification',
    r'\bvelychannye\b': 'magnification',
    r'\bvsenichne\b': 'all-night vigil',
    r'\bpovechiria\b': 'compline',
    r'\bpivnichna\b': 'midnight office',
    r'\bobidnytsia\b': 'typika',
    r'\bsamohlasen\b': 'idiomelon',
    r'\bpodiben\b': 'prosomoion',
}

def clean_and_normalize(text: str) -> str:
    t = text.lower()
    for pat, rep in VOCAB_MAP.items():
        t = re.sub(pat, rep, t)
    # Remove all punctuation, quotes, footnote markers
    t = re.sub(r'\[\^?\d+[a-z]?\]:?', '', t)
    t = re.sub(r'[^a-z0-9\s]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def main():
    root = Path(__file__).resolve().parent.parent
    if "brain" in str(root):
        root = Path(r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation")

    with open(root / "scratch" / "reports" / "unmatched_substantive_docx.json", "r", encoding="utf-8") as fh:
        unmatched = json.load(fh)

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
    
    final_paragraphs = []
    for fn in final_files:
        with open(final_dir / fn, "r", encoding="utf-8") as fh:
            for p in fh:
                cl = clean_and_normalize(p)
                if len(cl.split()) >= 6:
                    final_paragraphs.append(cl)

    # Join full normalized final text for sliding substring matches
    final_full_joined = " ".join(final_paragraphs)

    truly_missing = []
    reworded_or_split = []

    for item in unmatched:
        txt = clean_and_normalize(item["text"])
        words = txt.split()
        if len(words) < 10:
            continue

        # Check sub-phrases of 6 words across start, mid, end
        p_start = " ".join(words[:6])
        p_mid = " ".join(words[len(words)//2 : len(words)//2 + 6])
        p_end = " ".join(words[-6:])

        if p_start in final_full_joined or p_mid in final_full_joined or p_end in final_full_joined:
            reworded_or_split.append(item)
        else:
            # Fuzzy match check against closest paragraph
            best_ratio = 0.0
            for fp in final_paragraphs:
                # Fast length filter
                if abs(len(fp) - len(txt)) > len(txt) * 0.5:
                    continue
                r = difflib.SequenceMatcher(None, txt[:100], fp[:100]).ratio()
                if r > best_ratio:
                    best_ratio = r
                    if best_ratio > 0.65:
                        break
            
            if best_ratio > 0.65:
                reworded_or_split.append(item)
            else:
                truly_missing.append({
                    "index": item["index"],
                    "words": len(words),
                    "best_ratio": round(best_ratio, 2),
                    "text": item["text"]
                })

    print("=" * 60)
    print("ADVANCED FUZZY ALIGNMENT ANALYSIS")
    print("=" * 60)
    print(f"Total candidate unmatched evaluated: {len(unmatched)}")
    print(f"Accounted for by vocabulary mapping or paragraph split: {len(reworded_or_split)}")
    print(f"Truly divergent / missing candidates: {len(truly_missing)}")

    out_file = root / "scratch" / "reports" / "truly_divergent_passages.json"
    with open(out_file, "w", encoding="utf-8") as fh:
        json.dump(truly_missing, fh, ensure_ascii=False, indent=2)

    print(f"Report written to: {out_file}")

if __name__ == "__main__":
    main()
