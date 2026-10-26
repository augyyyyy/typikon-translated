#!/usr/bin/env python3
"""
Phase 1 v4: Final Marker Placement
====================================
Handles:
1. Part 2: fn 60 (Theotokion context), fn 131 (^[130] or 8)
2. Part 3: fn 339 (Trephologion), fn 346 (Tit. XII)
3. Part 5/Appendix: fn 753-785 (these are in dolnytsky_appendix.txt, NOT part5)
"""

import re
import json
from pathlib import Path

BASE_DIR = Path(r"e:\Google Antigravity\Projects\Translation")
SCRATCH_DIR = BASE_DIR / "scratch"
EN_DIR = BASE_DIR / "English Broken"
REPORT_DIR = SCRATCH_DIR / "reports"

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def fix_part2_final(text):
    """Fix fn 60 and 131."""
    results = []
    
    # Fn 60: appears in "Case 1: Saint without Polyeleos on Sunday"
    # "Sessional Hymn of the saint, Both now: his Theotokion^[60]"
    # BUT: in the EN text, "his theotokion" may be "his Theotokion"
    # AND: the preceding text is "Both now: his Theotokion" which appears MULTIPLE times
    # The FIRST such occurrence in the Canon section for Case 1 is what we need.
    # look for: "After the 3rd Ode" ... "Sessional Hymn" ... "his Theotokion"
    # in the first rubric (Case 1: "Saint without Polyeleos on a Sunday")
    
    # More specific: "3rd Ode" ... "Sessional Hymn" ... "Theotokion" BUT before "After the 6th"
    # Going broader: find the FIRST "Sessional Hymn" + "Theotokion" combo in text
    pattern = r'(After the 3rd Ode[^§]*?Sessional Hymn[^§]*?Both now:\s*(?:his|its)\s+[Tt]heotokion)'
    m = re.search(pattern, text, re.DOTALL)
    if m and '^[60]' not in text:
        pos = m.end()
        # Make sure we're not at a position that already has a footnote
        if not text[pos:pos+3].startswith('^['):
            text = text[:pos] + '^[60]' + text[pos:]
            results.append(('60', True))
        else:
            results.append(('60', False))
    else:
        results.append(('60', False))
    
    # Fn 131: "6 stichera^[130] or 8^[131]"
    # The ^[130] was placed by v2. Search for it.
    idx = text.find('^[130]')
    if idx != -1:
        after_130 = text[idx+6:idx+30]
        # Expect " or 8" or ", or 8" or similar
        match = re.search(r'(\s*(?:,?\s*or\s+8))', after_130)
        if match:
            insert_pos = idx + 6 + match.end()
            if '^[131]' not in text:
                text = text[:insert_pos] + '^[131]' + text[insert_pos:]
                results.append(('131', True))
            else:
                results.append(('131', True))
        else:
            results.append(('131', False))
    else:
        results.append(('131', False))
    
    return text, results


def fix_part3_final(text):
    """Fix fn 339 and 346."""
    results = []
    
    # Fn 339: "Pochaiv Trefologion of 1777" → EN might have "Trephologion"
    # Broader search
    for variant in ['Trephologion of 1777', 'Trefologion of 1777', 'Trofologion of 1777']:
        idx = text.find(variant)
        if idx != -1:
            pos = idx + len(variant)
            if '^[339]' not in text:
                text = text[:pos] + '^[339]' + text[pos:]
            results.append(('339', True))
            break
    else:
        # Try regex
        m = re.search(r'(Tr[eo][fp]h?ologion of 1777)', text, re.IGNORECASE)
        if m:
            pos = m.end()
            if '^[339]' not in text:
                text = text[:pos] + '^[339]' + text[pos:]
            results.append(('339', True))
        else:
            results.append(('339', False))
    
    # Fn 346: "Title XII, part 4, a.c.)" or "Tit. XII" 
    # RAW: "Lviv Synod allows (Title XII, part 4, a.c.)^[346]"
    # Search variants
    for variant in ['a.c.)', 'Tit. XII', 'Title XII']:
        m = re.search(re.escape(variant), text)
        if m:
            # Find end of the parenthetical
            pos = m.end()
            if '^[346]' not in text:
                text = text[:pos] + '^[346]' + text[pos:]
            results.append(('346', True))
            break
    else:
        results.append(('346', False))
    
    return text, results


def create_appendix_stitched():
    """Create a stitched version of the appendix file with markers from RAW Part 5.
    
    The RAW_PART5 includes the appendix content starting around line 1480
    with markers ^[753] through ^[785].
    """
    raw_path = SCRATCH_DIR / "CLEANED_RAW_PART5_TRANSLATION.txt"
    en_path = EN_DIR / "dolnytsky_appendix.txt"
    
    if not raw_path.exists() or not en_path.exists():
        print("  Appendix files not found!")
        return
    
    raw = load_file(raw_path)
    en = load_file(en_path)
    
    # Extract markers from the appendix portion of RAW Part 5
    # These start at ^[753] and go to ^[785]
    markers = {}
    for m in re.finditer(r'\^?\[(\d+)\]', raw):
        fn_num = int(m.group(1))
        if fn_num < 753 or fn_num > 785:
            continue
        if fn_num in markers:
            continue
        
        start = m.start()
        # Get context before
        ctx_before = raw[max(0, start-80):start].strip()
        # Get words before for matching
        words_before = raw[:start].split()
        snippets = {}
        for n in [3, 4, 5, 6]:
            if len(words_before) >= n:
                snippets[n] = ' '.join(words_before[-n:])
        
        markers[fn_num] = {
            'context_before': ctx_before,
            'snippets': snippets,
        }
    
    print(f"  Extracted {len(markers)} appendix markers: [{min(markers.keys())}-{max(markers.keys())}]")
    
    # Normalize quotes in EN text
    def normalize_quotes(text):
        text = text.replace('\u2018', "'").replace('\u2019', "'")
        text = text.replace('\u201C', '"').replace('\u201D', '"')
        text = text.replace('\u2014', '--').replace('\u2013', '-')
        return text
    
    en_norm = normalize_quotes(en.lower())
    en_norm = re.sub(r'\s+', ' ', en_norm)
    
    placed = []
    failed = []
    insertions = []
    
    for fn_num in sorted(markers.keys()):
        info = markers[fn_num]
        marker = f'^[{fn_num}]'
        
        if marker in en:
            placed.append(fn_num)
            continue
        
        found = False
        for n in sorted(info['snippets'].keys(), reverse=True):
            snippet = info['snippets'][n]
            # Normalize snippet
            snippet_norm = normalize_quotes(snippet.lower())
            snippet_norm = re.sub(r'\s+', ' ', snippet_norm)
            # Remove markdown bold markers
            snippet_norm = snippet_norm.replace('**', '')
            
            words = snippet_norm.split()
            if len(words) < 2:
                continue
            
            # Build regex
            pattern = r'[\W_]*'.join(re.escape(w) for w in words)
            try:
                m = re.search(pattern, en_norm)
                if m:
                    # Map to original position
                    # Simple approach: find the same text in original
                    orig_pattern = r'[\W_]*'.join(re.escape(w) for w in words)
                    orig_m = re.search(orig_pattern, en.lower())
                    if orig_m:
                        insertions.append((orig_m.end(), marker, fn_num))
                        placed.append(fn_num)
                        found = True
                        break
            except re.error:
                continue
        
        if not found:
            failed.append(fn_num)
    
    # Sort and apply insertions back-to-front
    insertions.sort(key=lambda x: x[0], reverse=True)
    result = en
    for pos, marker, fn_num in insertions:
        result = result[:pos] + marker + result[pos:]
    
    # Save
    out_path = SCRATCH_DIR / "STITCHED_v3_dolnytsky_appendix.txt"
    save_file(out_path, result)
    
    print(f"  Placed: {len(placed)}")
    print(f"  Failed: {len(failed)} ({failed})")
    
    return placed, failed


def main():
    print("=" * 70)
    print("PHASE 1 v4: FINAL MARKER PLACEMENT")
    print("=" * 70)
    
    total_placed = 0
    total_failed = 0
    
    # Fix Part 2
    print("\n--- Part 2: Final fixes ---")
    p2_path = SCRATCH_DIR / "STITCHED_v3_dolnytsky_part2_general_rubrics.txt"
    p2_text = load_file(p2_path)
    p2_text, p2_results = fix_part2_final(p2_text)
    save_file(p2_path, p2_text)  # Overwrite v3
    p2_placed = sum(1 for _, ok in p2_results if ok)
    p2_failed = sum(1 for _, ok in p2_results if not ok)
    print(f"  Placed: {p2_placed}, Failed: {p2_failed}")
    for name, ok in p2_results:
        print(f"    fn {name}: {'OK' if ok else 'FAIL'}")
    total_placed += p2_placed
    total_failed += p2_failed
    
    # Fix Part 3
    print("\n--- Part 3: Final fixes ---")
    p3_path = SCRATCH_DIR / "STITCHED_v3_dolnytsky_part3_menaion.txt"
    p3_text = load_file(p3_path)
    p3_text, p3_results = fix_part3_final(p3_text)
    save_file(p3_path, p3_text)  # Overwrite v3
    p3_placed = sum(1 for _, ok in p3_results if ok)
    p3_failed = sum(1 for _, ok in p3_results if not ok)
    print(f"  Placed: {p3_placed}, Failed: {p3_failed}")
    for name, ok in p3_results:
        print(f"    fn {name}: {'OK' if ok else 'FAIL'}")
    total_placed += p3_placed
    total_failed += p3_failed
    
    # Fix Appendix (markers from RAW Part 5 that belong to EN appendix)
    print("\n--- Appendix: Markers from RAW Part 5 ---")
    app_placed, app_failed = create_appendix_stitched()
    total_placed += len(app_placed)
    total_failed += len(app_failed)
    
    print(f"\n{'=' * 70}")
    print(f"PHASE 1 v4 COMPLETE")
    print(f"Total newly placed: {total_placed}")
    print(f"Still failed: {total_failed}")
    print(f"{'=' * 70}")
    
    # Count grand total markers across all v3 files
    print(f"\n--- GRAND TOTAL MARKER COUNT ---")
    grand_total = 0
    for fname in [
        "STITCHED_v3_dolnytsky_part1_structure.txt",
        "STITCHED_v3_dolnytsky_part2_general_rubrics.txt",
        "STITCHED_v3_dolnytsky_part3_menaion.txt",
        "STITCHED_v3_dolnytsky_part4_triodion.txt",
        "STITCHED_v3_dolnytsky_part5_temple.txt",
        "STITCHED_v3_dolnytsky_appendix.txt",
    ]:
        fpath = SCRATCH_DIR / fname
        if fpath.exists():
            text = load_file(fpath)
            count = len(re.findall(r'\^\[\d+\]', text))
            print(f"  {fname}: {count} markers")
            grand_total += count
    print(f"  GRAND TOTAL: {grand_total}")


if __name__ == '__main__':
    main()
