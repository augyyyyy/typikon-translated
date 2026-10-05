import sys
import re
from pathlib import Path
from extract_all_49_anchors import missing_ids, paras, get_exact_context

sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parent.parent

def get_file_for_fn(fid):
    if fid <= 50:
        return ("Final/Final_Dolnytsky_part1_structure.txt", "Final MD/Final_Dolnytsky_part1_structure.md")
    elif fid <= 240:
        return ("Final/Final_Dolnytsky_part2_general_rubrics.txt", "Final MD/Final_Dolnytsky_part2_general_rubrics.md")
    elif fid <= 468:
        return ("Final/Final_Dolnytsky_part3_menaion.txt", "Final MD/Final_Dolnytsky_part3_menaion.md")
    elif fid <= 662:
        return ("Final/Final_Dolnytsky_part4_triodion.txt", "Final MD/Final_Dolnytsky_part4_triodion.md")
    elif fid <= 752:
        return ("Final/Final_Dolnytsky_part5_temple.txt", "Final MD/Final_Dolnytsky_part5_temple.md")
    else:
        return ("Final/Final_Dolnytsky_appendix.txt", "Final MD/Final_Dolnytsky_appendix.md")

docx_anchors = {}
for fid in missing_ids:
    for p in paras:
        pre, post, full = get_exact_context(p, fid)
        if pre is not None:
            docx_anchors[fid] = (" ".join(pre.split()), " ".join(post.split()), full)
            break

print(f"Total docx anchors found: {len(docx_anchors)} / {len(missing_ids)}\n")

for fid in missing_ids:
    txt_rel, md_rel = get_file_for_fn(fid)
    txt_path = root / txt_rel
    md_path = root / md_rel
    
    txt_content = txt_path.read_text(encoding='utf-8')
    md_content = md_path.read_text(encoding='utf-8')
    
    pre, post, full = docx_anchors[fid]
    
    # Find bounding footnotes in txt
    all_txt_fns = [(int(m.group(1)), m.start()) for m in re.finditer(r'\[\^(\d+)\]', txt_content)]
    prev_fns = [f for f in all_txt_fns if f[0] < fid]
    next_fns = [f for f in all_txt_fns if f[0] > fid]
    
    txt_start = prev_fns[-1][1] if prev_fns else 0
    txt_end = next_fns[0][1] if next_fns else len(txt_content)
    
    txt_window = txt_content[txt_start:txt_end]
    
    # Try searching in txt_window
    # Use key phrases from pre or post
    found_in_txt = False
    for words_count in range(min(6, len(pre.split())), 1, -1):
        phrase = " ".join(pre.split()[-words_count:])
        # flexible regex
        pat = r'\s+'.join(re.escape(w) for w in phrase.split())
        m = list(re.finditer(pat, txt_window, re.IGNORECASE))
        if len(m) == 1:
            found_in_txt = True
            break
        elif len(m) > 1:
            pass
            
    # Same for MD
    all_md_fns = [(int(m.group(1)), m.start()) for m in re.finditer(r'\[\^(\d+)\]', md_content)]
    prev_md_fns = [f for f in all_md_fns if f[0] < fid]
    next_md_fns = [f for f in all_md_fns if f[0] > fid]
    
    md_start = prev_md_fns[-1][1] if prev_md_fns else 0
    md_end = next_md_fns[0][1] if next_md_fns else len(md_content)
    md_window = md_content[md_start:md_end]
    
    found_in_md = False
    for words_count in range(min(6, len(pre.split())), 1, -1):
        phrase = " ".join(pre.split()[-words_count:])
        pat = r'\s+'.join(re.escape(w) for w in phrase.split())
        m = list(re.finditer(pat, md_window, re.IGNORECASE))
        if len(m) == 1:
            found_in_md = True
            break

    prev_id = prev_fns[-1][0] if prev_fns else "START"
    next_id = next_fns[0][0] if next_fns else "END"
    print(f"FN {fid:3d} in [{prev_id}..{next_id}]: TXT={found_in_txt} | MD={found_in_md} | {Path(txt_rel).name}")
    if not (found_in_txt and found_in_md):
        print(f"   PRE: [{pre[-40:]}]")
        print(f"   POST: [{post[:40]}]")
