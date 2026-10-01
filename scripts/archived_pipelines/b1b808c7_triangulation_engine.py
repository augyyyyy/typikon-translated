#!/usr/bin/env python3
"""
Triangulation Alignment Engine (Refined)
========================================
Performs 3-way collation across:
1. Ukrainian OCR Source (Ukrainian TXTs/)
2. Original Translation Manuscript (scratch/reports/docx_corpus.json)
3. Final Deliverables (Final/)

Identifies:
- Structural section boundaries & paragraph counts
- Footnote apparatus differences (662 in Docx vs 786 in Final)
- Content / prose divergences and potential dropped clauses
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
        if (parent / "Ukrainian TXTs").exists() and (parent / "Final").exists():
            return parent
    return Path(os.environ.get("TRANSLATION_PROJECT_DIR", r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation"))

def load_text_files(directory: Path) -> dict:
    corpus = {}
    if not directory.exists():
        return corpus
    for f in sorted(directory.glob("*.txt")):
        with open(f, "r", encoding="utf-8") as fh:
            corpus[f.name] = fh.read()
    return corpus

def clean_for_comparison(text: str) -> str:
    """Normalize whitespace and common markdown markers for lexical comparison."""
    t = re.sub(r'\[\^?\d+[a-z]?\]:?', '', text) # remove footnote markers
    t = re.sub(r'[#*_`]', '', t)                # remove markdown formatting
    t = re.sub(r'\s+', ' ', t).strip().lower()
    return t

def audit_footnotes(docx_data: dict, final_footnotes_text: str) -> dict:
    docx_fns = {str(k): v for k, v in docx_data.get("footnotes", {}).items()}
    final_fns = {}
    
    # Parse Final_footnotes.txt: [^N]: Text
    for m in re.finditer(r'\[\^(\d+[a-z]?)\]:\s*(.*?)(?=\n\[\^\d+[a-z]?\]:|\Z)', final_footnotes_text, re.DOTALL):
        fn_key = m.group(1)
        fn_text = m.group(2).strip()
        final_fns[fn_key] = fn_text

    missing_in_docx = []
    identical_count = 0
    close_match_count = 0
    text_diffs = []
    
    for key, f_text in final_fns.items():
        if key not in docx_fns:
            missing_in_docx.append(key)
        else:
            d_text = docx_fns[key]
            c_final = clean_for_comparison(f_text)
            c_docx = clean_for_comparison(d_text)
            if c_final == c_docx:
                identical_count += 1
            else:
                ratio = difflib.SequenceMatcher(None, c_final, c_docx).ratio()
                if ratio >= 0.85:
                    close_match_count += 1
                else:
                    text_diffs.append({
                        "footnote": key,
                        "ratio": round(ratio, 2),
                        "final_sample": f_text[:160],
                        "docx_sample": d_text[:160]
                    })

    # Sort text diffs by lowest ratio (greatest divergence)
    text_diffs.sort(key=lambda x: x["ratio"])

    return {
        "total_final_footnotes": len(final_fns),
        "total_docx_footnotes": len(docx_fns),
        "missing_in_docx_count": len(missing_in_docx),
        "missing_in_docx_samples": missing_in_docx[:25],
        "identical_count": identical_count,
        "close_match_count": close_match_count,
        "significant_diff_count": len(text_diffs),
        "significant_diff_samples": text_diffs[:15]
    }

def audit_structural_volumes(ua_corpus: dict, final_corpus: dict) -> list:
    results = []
    
    file_mapping = [
        ("Intro", "Intro.txt", "Final_Dolnytsky_intro.txt"),
        ("Part 1: Structure", "Part 1.txt", "Final_Dolnytsky_part1_structure.txt"),
        ("Part 2: General Rubrics", "Part 2.txt", "Final_Dolnytsky_part2_general_rubrics.txt"),
        ("Part 3: Menaion", "Part 3.txt", "Final_Dolnytsky_part3_menaion.txt"),
        ("Part 4: Triodion", "Part 4.txt", "Final_Dolnytsky_part4_triodion.txt"),
        ("Part 5: Temple", "Part 5.txt", "Final_Dolnytsky_part5_temple.txt"),
        ("Appendix", "Appendix.txt", "Final_Dolnytsky_appendix.txt"),
    ]

    for label, ua_file, final_file in file_mapping:
        ua_text = ua_corpus.get(ua_file, "")
        final_text = final_corpus.get(final_file, "")
        
        ua_paras = [p.strip() for p in ua_text.split("\n") if p.strip()]
        final_paras = [p.strip() for p in final_text.split("\n") if p.strip()]
        
        ua_words = len(ua_text.split())
        final_words = len(final_text.split())
        
        final_fn_count = len(re.findall(r'\[\^\d+[a-z]?\](?!:)', final_text))
        
        results.append({
            "section": label,
            "ua_file": ua_file,
            "final_file": final_file,
            "ua_paragraphs": len(ua_paras),
            "final_paragraphs": len(final_paras),
            "ua_words": ua_words,
            "final_words": final_words,
            "final_footnotes_anchored": final_fn_count
        })

    return results

def main():
    root = get_project_root()
    print(f"Project root: {root}")
    
    ua_dir = root / "Ukrainian TXTs"
    final_dir = root / "Final"
    reports_dir = root / "scratch" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    docx_corpus_file = reports_dir / "docx_corpus.json"
    if not docx_corpus_file.exists():
        print(f"Error: {docx_corpus_file} not found. Run extract_docx_corpus.py first.")
        sys.exit(1)
        
    with open(docx_corpus_file, "r", encoding="utf-8") as fh:
        docx_data = json.load(fh)
        
    ua_corpus = load_text_files(ua_dir)
    final_corpus = load_text_files(final_dir)
    final_footnotes = final_corpus.get("Final_footnotes.txt", "")
    
    print("\n--- Auditing Footnote Apparatus Collation ---")
    fn_audit = audit_footnotes(docx_data, final_footnotes)
    print(f"Master Footnotes in Final: {fn_audit['total_final_footnotes']}")
    print(f"Native Footnotes in Docx: {fn_audit['total_docx_footnotes']}")
    print(f"Identical text matches: {fn_audit['identical_count']}")
    print(f"Close matches (>=85%): {fn_audit['close_match_count']}")
    print(f"Significant text diffs (<85%): {fn_audit['significant_diff_count']}")
    print(f"Missing in Docx (recovered in Final): {fn_audit['missing_in_docx_count']}")

    print("\n--- Auditing Structural Volumes across Sections ---")
    volumes = audit_structural_volumes(ua_corpus, final_corpus)
    for v in volumes:
        print(f"  {v['section']}: UA {v['ua_paragraphs']} paras ({v['ua_words']} w) | Final {v['final_paragraphs']} paras ({v['final_words']} w) | Anchors: {v['final_footnotes_anchored']}")

    report_file = reports_dir / "triangulation_audit_report.md"
    with open(report_file, "w", encoding="utf-8") as rf:
        rf.write("# Grand Re-Audit: Triangulation Collation Report\n\n")
        rf.write("## 1. Executive Summary\n\n")
        rf.write(f"- **Primary Reference (Ukrainian OCR)**: {sum(v['ua_words'] for v in volumes):,} words across {sum(v['ua_paragraphs'] for v in volumes):,} paragraphs.\n")
        rf.write(f"- **Early English Manuscript (.docx)**: {docx_data['total_paragraphs']:,} paragraphs, {docx_data['total_footnotes']} native footnotes.\n")
        rf.write(f"- **Final English Deliverables (Final/)**: {sum(v['final_words'] for v in volumes):,} words across {sum(v['final_paragraphs'] for v in volumes):,} paragraphs, {fn_audit['total_final_footnotes']} master footnotes.\n\n")
        
        rf.write("## 2. Section Structural Volumes\n\n")
        rf.write("| Section | UA Paragraphs | Final Paragraphs | UA Words | Final Words | Final Footnotes Anchored |\n")
        rf.write("|---|---|---|---|---|---|\n")
        for v in volumes:
            rf.write(f"| {v['section']} | {v['ua_paragraphs']:,} | {v['final_paragraphs']:,} | {v['ua_words']:,} | {v['final_words']:,} | {v['final_footnotes_anchored']} |\n")

        rf.write("\n## 3. Footnote Apparatus Triangulation\n\n")
        rf.write(f"- **Total Master Footnotes in Final**: {fn_audit['total_final_footnotes']}\n")
        rf.write(f"- **Total Native Footnotes in Docx**: {fn_audit['total_docx_footnotes']}\n")
        rf.write(f"- **Exact / Near-Exact Matches**: {fn_audit['identical_count'] + fn_audit['close_match_count']} ({round((fn_audit['identical_count'] + fn_audit['close_match_count']) / fn_audit['total_docx_footnotes'] * 100, 1)}% of docx apparatus)\n")
        rf.write(f"- **Footnotes absent in Docx but recovered in Final**: {fn_audit['missing_in_docx_count']}\n")
        rf.write(f"- **Sample Footnotes only in Final**: {', '.join(fn_audit['missing_in_docx_samples'])}\n")
        rf.write(f"- **Significant Phrasing Divergences (<85% similarity)**: {fn_audit['significant_diff_count']}\n\n")
        
        rf.write("### Top Footnote Phrasing Divergences & Scholarly Analysis\n\n")
        for diff in fn_audit["significant_diff_samples"]:
            rf.write(f"#### Footnote [^{diff['footnote']}] (Similarity Ratio: {diff['ratio']})\n")
            rf.write(f"- **Final Deliverable**: `{diff['final_sample']}`\n")
            rf.write(f"- **Docx Manuscript**: `{diff['docx_sample']}`\n\n")

    print(f"\nTriangulation audit complete! Report generated at: {report_file}")

if __name__ == "__main__":
    main()
