import sys
import re
from pathlib import Path
from extract_all_49_anchors import missing_ids, paras, get_exact_context

sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parent.parent
deliverable_pairs = [
    ("Final/Final_Dolnytsky_intro.txt", "Final MD/Final_Dolnytsky_intro.md"),
    ("Final/Final_Dolnytsky_part1_structure.txt", "Final MD/Final_Dolnytsky_part1_structure.md"),
    ("Final/Final_Dolnytsky_part2_general_rubrics.txt", "Final MD/Final_Dolnytsky_part2_general_rubrics.md"),
    ("Final/Final_Dolnytsky_part3_menaion.txt", "Final MD/Final_Dolnytsky_part3_menaion.md"),
    ("Final/Final_Dolnytsky_part4_triodion.txt", "Final MD/Final_Dolnytsky_part4_triodion.md"),
    ("Final/Final_Dolnytsky_part5_temple.txt", "Final MD/Final_Dolnytsky_part5_temple.md"),
    ("Final/Final_Dolnytsky_appendix.txt", "Final MD/Final_Dolnytsky_appendix.md")
]

file_texts = {}
for txt_path_str, md_path_str in deliverable_pairs:
    txt_p = root / txt_path_str
    md_p = root / md_path_str
    if txt_p.exists() and md_p.exists():
        file_texts[txt_p] = txt_p.read_text(encoding='utf-8')
        file_texts[md_p] = md_p.read_text(encoding='utf-8')

def find_target_in_corpus(fid, pre, post):
    # Find matching locations in files
    # Normalize spaces
    pre_words = pre.split()
    post_words = post.split()
    
    matches_found = []
    for fpath, content in file_texts.items():
        # search with subsets of words
        for pre_len in range(min(5, len(pre_words)), 1, -1):
            pre_sub = " ".join(pre_words[-pre_len:])
            # escape for regex, allowing flexible whitespace
            pre_pattern = r'\s+'.join(re.escape(w) for w in pre_words[-pre_len:])
            for m in re.finditer(pre_pattern, content, re.IGNORECASE):
                pos = m.end()
                surrounding = content[max(0, m.start()-20):min(len(content), pos+40)]
                matches_found.append((fpath, m.start(), pos, surrounding))
            if matches_found:
                break
    return matches_found

print("Mapping missing footnotes to deliverable files:")
for fid in missing_ids:
    for p in paras:
        pre, post, full = get_exact_context(p, fid)
        if pre is not None:
            pre_clean = " ".join(pre.split())
            post_clean = " ".join(post.split())
            matches = find_target_in_corpus(fid, pre_clean, post_clean)
            txt_matches = [m for m in matches if m[0].suffix == '.txt']
            md_matches = [m for m in matches if m[0].suffix == '.md']
            print(f"FN {fid:3d}: txt_matches={len(txt_matches)}, md_matches={len(md_matches)} | {[m[0].name for m in txt_matches]}")
            break
