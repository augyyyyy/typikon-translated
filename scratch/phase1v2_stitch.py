#!/usr/bin/env python3
"""
Phase 1 v2: Improved Footnote Marker Stitching
================================================
Fixes from v1:
1. Better smart/curly quote normalization
2. Deduplication of extracted markers (keep only unique fn numbers)
3. Wider search window (up to 8 words)
4. Fallback: try matching with punctuation stripped
5. For Part 5: special handling of reformatted Menologion text
6. Reports which markers still fail for AI pass
"""

import re
import json
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(r"e:\Google Antigravity\Projects\Translation")
SCRATCH_DIR = BASE_DIR / "scratch"
EN_DIR = BASE_DIR / "English Broken"
REPORT_DIR = SCRATCH_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Map cleaned RAW files to English Broken counterparts
CLEANED_TO_EN = {
    "CLEANED_RAW_PART1_TRANSLATION.txt": "dolnytsky_part1_structure.txt",
    "CLEANED_RAW_PART2_TRANSLATION.txt": "dolnytsky_part2_general_rubrics.txt",
    "CLEANED_RAW_PART3_TRANSLATION.txt": "dolnytsky_part3_menaion.txt",
    "CLEANED_RAW_PART4_TRANSLATION.txt": "dolnytsky_part4_triodion.txt",
    "CLEANED_RAW_PART5_TRANSLATION.txt": "dolnytsky_part5_temple.txt",
}


# =============================================================================
# QUOTE / PUNCTUATION NORMALIZATION
# =============================================================================

def normalize_quotes(text):
    """Aggressively normalize all quote variants to ASCII equivalents."""
    # Smart/curly single quotes -> straight
    text = text.replace('\u2018', "'")  # '
    text = text.replace('\u2019', "'")  # '
    text = text.replace('\u201A', "'")  # ‚
    text = text.replace('\u2039', "'")  # ‹
    text = text.replace('\u203A', "'")  # ›
    text = text.replace('\u02BC', "'")  # ʼ  (modifier letter apostrophe)
    # Smart/curly double quotes -> straight
    text = text.replace('\u201C', '"')  # "
    text = text.replace('\u201D', '"')  # "
    text = text.replace('\u201E', '"')  # „
    text = text.replace('\u00AB', '"')  # «
    text = text.replace('\u00BB', '"')  # »
    # Dashes
    text = text.replace('\u2014', '--')  # —
    text = text.replace('\u2013', '-')   # –
    return text


def normalize_whitespace(text):
    """Collapse all whitespace to single spaces."""
    return re.sub(r'\s+', ' ', text).strip()


def full_normalize(text):
    """Full normalization for fuzzy matching."""
    text = normalize_quotes(text)
    text = normalize_whitespace(text)
    return text.lower()


def strip_punctuation(text):
    """Remove all punctuation for last-resort matching."""
    return re.sub(r'[^\w\s]', '', text)


# =============================================================================
# MARKER EXTRACTION (improved)
# =============================================================================

def extract_markers_from_raw(raw_text):
    """Extract unique footnote markers with context from cleaned RAW text.
    
    Returns dict: {fn_number: marker_info} (deduplicated, keeping first occurrence)
    """
    markers = {}
    lines = raw_text.split('\n')
    
    for line_num, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip footnote DEFINITION lines (^[N] at start of line)
        if re.match(r'^\^?\[\d+\]', stripped):
            continue
        # Skip lines that are just footnote numbers in brackets at line start  
        if re.match(r'^\[\d+\]', stripped):
            continue
        
        # Find inline markers in body text
        for m in re.finditer(r'\^?\[(\d+)\]', line):
            fn_num = int(m.group(1))
            
            # Skip if we already have this footnote number (dedup!)
            if fn_num in markers:
                continue
            
            start, end = m.start(), m.end()
            
            # Get surrounding context
            ctx_before = line[max(0, start-60):start]
            ctx_after = line[end:min(len(line), end+60)]
            
            # Build multiple snippet sizes for matching
            words_before = line[:start].split()
            snippets = {}
            for n in range(2, 9):
                if len(words_before) >= n:
                    snippets[n] = ' '.join(words_before[-n:])
            
            # Also get a few words AFTER the marker for verification
            words_after = line[end:].split()
            after_snippet = ' '.join(words_after[:4]) if words_after else ''
            
            markers[fn_num] = {
                'number': fn_num,
                'context_before': ctx_before.strip(),
                'context_after': ctx_after.strip(),
                'snippets': snippets,
                'after_snippet': after_snippet,
                'full_line': stripped[:200],
                'line_num': line_num,
            }
    
    return markers


# =============================================================================
# IMPROVED STITCHING
# =============================================================================

def find_insertion_point(en_text_normalized, en_text_original, marker_info):
    """Find where to insert a footnote marker in the English text.
    
    Uses multiple strategies:
    1. Try longest snippet first (8 words down to 3)
    2. Try with full normalization
    3. Try with punctuation stripped as fallback
    4. Verify by checking after-context if possible
    
    Returns: (original_position, confidence, method) or (None, 0, None)
    """
    snippets = marker_info.get('snippets', {})
    if not snippets:
        return None, 0, None
    
    # Strategy 1: Normalized quote matching (longest snippet first)
    for num_words in sorted(snippets.keys(), reverse=True):
        snippet = snippets[num_words]
        norm_snippet = full_normalize(snippet)
        
        if not norm_snippet:
            continue
        
        # Build flexible regex: allow variable whitespace between words
        words = norm_snippet.split()
        if len(words) < 2:
            continue
        
        pattern_parts = [re.escape(w) for w in words]
        pattern = r'\s+'.join(pattern_parts)
        
        try:
            match = re.search(pattern, en_text_normalized)
            if match:
                # Map position back to original text
                orig_pos = map_norm_pos_to_original(en_text_original, en_text_normalized, match.end())
                if orig_pos is not None:
                    confidence = min(1.0, num_words / 6.0)
                    return orig_pos, confidence, f'norm_{num_words}w'
        except re.error:
            continue
    
    # Strategy 2: Punctuation-stripped matching
    en_stripped = strip_punctuation(full_normalize(en_text_original))
    for num_words in sorted(snippets.keys(), reverse=True):
        snippet = snippets[num_words]
        stripped_snippet = strip_punctuation(full_normalize(snippet))
        
        if not stripped_snippet or len(stripped_snippet) < 10:
            continue
        
        words = stripped_snippet.split()
        if len(words) < 3:
            continue
        
        pattern_parts = [re.escape(w) for w in words]
        pattern = r'\s+'.join(pattern_parts)
        
        try:
            match = re.search(pattern, en_stripped)
            if match:
                # Need to find this in the ORIGINAL text 
                # Use the matched words to search in normalized (not stripped) text
                orig_pos = find_approx_position(en_text_original, words)
                if orig_pos is not None:
                    confidence = min(0.9, num_words / 7.0)
                    return orig_pos, confidence, f'stripped_{num_words}w'
        except re.error:
            continue
    
    return None, 0, None


def map_norm_pos_to_original(original, normalized, norm_pos):
    """Map a character position in normalized text back to original text.
    
    Since normalization collapses whitespace and lowercases, we need to
    find the corresponding position in the original.
    """
    # Walk both strings simultaneously
    orig_idx = 0
    norm_idx = 0
    orig_len = len(original)
    norm_len = len(normalized)
    
    while norm_idx < norm_pos and orig_idx < orig_len:
        orig_char = original[orig_idx].lower()
        # Handle quote normalization
        orig_char_normalized = normalize_quotes(original[orig_idx]).lower()
        
        if norm_idx < norm_len:
            norm_char = normalized[norm_idx]
            
            if orig_char_normalized == norm_char:
                orig_idx += 1
                norm_idx += 1
            elif original[orig_idx].isspace():
                # Skip extra whitespace in original
                orig_idx += 1
                # Only advance norm if norm is also at space
                if norm_char == ' ':
                    norm_idx += 1
            else:
                # Character was removed during normalization (quote char etc.)
                orig_idx += 1
        else:
            break
    
    return orig_idx if norm_idx >= norm_pos else None


def find_approx_position(original_text, search_words):
    """Find approximate position of word sequence in original text."""
    if not search_words:
        return None
    
    # Build a pattern from the search words, case-insensitive
    # Allow any non-word chars between words
    pattern_parts = [re.escape(w) for w in search_words]
    pattern = r'[\W_]+'.join(pattern_parts)
    
    try:
        match = re.search(pattern, original_text, re.IGNORECASE)
        if match:
            return match.end()
    except re.error:
        pass
    
    return None


def stitch_all_markers(en_text, markers, part_name):
    """Insert all footnote markers into English text.
    
    Returns: (stitched_text, placed_report, failed_report)
    """
    placed = []
    failed = []
    
    # Pre-compute normalized text once
    en_normalized = full_normalize(en_text)
    
    # Sort by footnote number
    sorted_markers = sorted(markers.values(), key=lambda x: x['number'])
    
    # Collect insertions
    insertions = []
    
    for marker in sorted_markers:
        fn_num = marker['number']
        marker_text = f'^[{fn_num}]'
        
        # Check if already present
        if marker_text in en_text:
            placed.append({
                'number': fn_num,
                'status': 'already_present',
            })
            continue
        
        pos, confidence, method = find_insertion_point(en_normalized, en_text, marker)
        
        if pos is not None and confidence >= 0.4:
            insertions.append((pos, marker_text, fn_num))
            placed.append({
                'number': fn_num,
                'position': pos,
                'confidence': round(confidence, 2),
                'method': method,
                'context': en_text[max(0, pos-30):min(len(en_text), pos+30)],
            })
        else:
            failed.append({
                'number': fn_num,
                'snippets': {k: v for k, v in list(marker['snippets'].items())[:3]},
                'context_before': marker['context_before'][:80],
                'context_after': marker['context_after'][:40],
            })
    
    # Apply insertions back-to-front
    insertions.sort(key=lambda x: x[0], reverse=True)
    result = en_text
    for pos, marker_text, fn_num in insertions:
        result = result[:pos] + marker_text + result[pos:]
    
    return result, placed, failed


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("PHASE 1 v2: IMPROVED FOOTNOTE STITCHING")
    print("=" * 70)
    
    all_results = {}
    total_placed = 0
    total_failed = 0
    all_failed_markers = []
    
    for cleaned_name, en_name in CLEANED_TO_EN.items():
        cleaned_path = SCRATCH_DIR / cleaned_name
        en_path = EN_DIR / en_name
        
        if not cleaned_path.exists():
            print(f"  SKIP: {cleaned_name} not found")
            continue
        if not en_path.exists():
            print(f"  SKIP: {en_name} not found")
            continue
        
        print(f"\n--- Processing {en_name} ---")
        
        # Read files
        with open(cleaned_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        with open(en_path, 'r', encoding='utf-8') as f:
            en_text = f.read()
        
        # Extract markers (deduplicated)
        markers = extract_markers_from_raw(raw_text)
        print(f"  Unique markers extracted: {len(markers)}")
        if markers:
            fn_nums = sorted(markers.keys())
            print(f"  Range: [{min(fn_nums)} - {max(fn_nums)}]")
        
        # Stitch
        stitched_text, placed, failed = stitch_all_markers(en_text, markers, en_name)
        
        placed_count = len([p for p in placed if p.get('status') != 'already_present'])
        already = len([p for p in placed if p.get('status') == 'already_present'])
        
        print(f"  Already present: {already}")
        print(f"  Newly placed: {placed_count}")
        print(f"  Failed: {len(failed)}")
        
        if failed:
            failed_nums = [f['number'] for f in failed]
            print(f"  Failed markers: {failed_nums}")
        
        total_placed += placed_count + already
        total_failed += len(failed)
        
        # Track failed for AI pass
        for f_item in failed:
            f_item['file'] = en_name
            all_failed_markers.append(f_item)
        
        # Save stitched file
        stitched_path = SCRATCH_DIR / f"STITCHED_v2_{en_name}"
        with open(stitched_path, 'w', encoding='utf-8') as f:
            f.write(stitched_text)
        
        all_results[en_name] = {
            'markers_extracted': len(markers),
            'placed': placed_count,
            'already_present': already,
            'failed': len(failed),
            'failed_details': failed,
        }
    
    # Save the failed markers report for AI pass
    failed_report_path = REPORT_DIR / "v2_failed_markers.json"
    with open(failed_report_path, 'w', encoding='utf-8') as f:
        json.dump(all_failed_markers, f, indent=2, ensure_ascii=False)
    
    # Save full report
    full_report_path = REPORT_DIR / "phase1v2_report.json"
    with open(full_report_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 70}")
    print(f"PHASE 1 v2 COMPLETE")
    print(f"Total placed: {total_placed}")
    print(f"Total failed: {total_failed}")
    print(f"Failed markers report: {failed_report_path}")
    print(f"Stitched files: {SCRATCH_DIR}/STITCHED_v2_*")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
