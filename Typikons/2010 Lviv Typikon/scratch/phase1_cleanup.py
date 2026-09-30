#!/usr/bin/env python3
"""
Phase 1: Typikon Translation — Programmatic Cleanup
=====================================================
This script performs all mechanical cleanup tasks:

1. CLEAN RAW FILES: Strip AI commentary, chunk headers, and deduplicate chunks
2. EXTRACT FOOTNOTE MARKERS: Build a map of {footnote_number: context_snippet} from cleaned RAW
3. STITCH MARKERS: Re-insert ^[n] markers into English Broken body text
4. FIX GLOSSARY ARTIFACTS: Remove doubled terms like "Gradual (Gradual)"
5. VERIFY FOOTNOTE ALIGNMENT: Cross-check English footnotes.txt against Ukrainian Footnotes.txt
6. GENERATE REPORTS: Diff logs of all changes
"""

import re
import os
import json
from pathlib import Path
from difflib import SequenceMatcher, unified_diff

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(r"e:\Google Antigravity\Projects\Translation")
RAW_DIR = BASE_DIR / "RAW"
EN_DIR = BASE_DIR / "English Broken"
UA_DIR = BASE_DIR / "Ukrainian TXTs"
SCRATCH_DIR = BASE_DIR / "scratch"
REPORT_DIR = SCRATCH_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Map of RAW files to their English Broken counterparts
RAW_TO_EN = {
    "RAW_PART1_TRANSLATION.txt": "dolnytsky_part1_structure.txt",
    "RAW_PART2_TRANSLATION.txt": "dolnytsky_part2_general_rubrics.txt",
    "RAW_PART3_TRANSLATION.txt": "dolnytsky_part3_menaion.txt",
    "RAW_PART4_TRANSLATION.txt": "dolnytsky_part4_triodion.txt",
    "RAW_PART5_TRANSLATION.txt": "dolnytsky_part5_temple.txt",
}

# =============================================================================
# STEP 1: CLEAN RAW FILES
# =============================================================================

# Patterns to strip from RAW files
AI_COMMENTARY_PATTERNS = [
    # AI conversational lines
    r'^I apologize.*$',
    r'^I have reviewed.*$',
    r'^I have conducted.*$',
    r'^Here is the corrected.*$',
    r'^The "extra part".*$',
    r'^You are correct\..*$',
    r'^You are absolutely right\..*$',
    r'^I contradicted myself.*$',
    r'^I acknowledge the Master Chunk List.*$',
    r'^I am ready to begin\..*$',
    r'^Please provide the source text.*$',
    r'^Now we shall present the order.*$',  # AI transition
    r'^Acknowledge the chunks.*$',
    # Chunk list preamble (the bulleted acknowledgment)
    r'^\*\s+\*\*Chunk \d+:\*\*.*$',
    # Section headers like "OUTSIDE A FEAST" in the preamble
    r'^MASTER CHUNK LIST:.*$',
    r'^Based on the Table of Contents.*$',
]

# Chunk headers to strip
CHUNK_HEADER_PATTERN = re.compile(r'^\*\*Chunk \d+.*?\*\*\s*$', re.MULTILINE)

# Pre-compile AI patterns
AI_PATTERNS_COMPILED = [re.compile(p, re.MULTILINE) for p in AI_COMMENTARY_PATTERNS]


def find_preamble_end(lines):
    """Find where the actual translation content begins in a RAW file.
    
    The preamble consists of:
    - File identifier (RAW_PART_X)
    - AI acknowledgment of chunk list
    - Bulleted chunk list repeat
    - "I am ready to begin" type messages
    
    Returns the index of the first line of actual content.
    """
    # Look for the first chunk header after any preamble
    for i, line in enumerate(lines):
        stripped = line.strip()
        # The actual content starts with a chunk header like "**Chunk N: ..."
        # OR with actual body text (introductory paragraphs)
        if re.match(r'^\*\*Chunk \d+', stripped):
            return i
        # Or if we find the first real content paragraph after preamble markers
        if i > 5 and stripped and not any(p.match(stripped) for p in AI_PATTERNS_COMPILED):
            # Check if previous lines were preamble
            prev_lines = [lines[j].strip() for j in range(max(0, i-3), i)]
            if any('ready to begin' in pl.lower() or 'acknowledge' in pl.lower() for pl in prev_lines):
                return i
    return 0


def detect_duplicate_chunks(lines):
    """Detect if any chunk appears more than once in the file.
    
    Returns a dict of {chunk_number: [line_numbers_of_appearances]}.
    """
    chunk_positions = {}
    for i, line in enumerate(lines):
        m = re.match(r'^\*\*Chunk (\d+)', line.strip())
        if m:
            num = int(m.group(1))
            if num not in chunk_positions:
                chunk_positions[num] = []
            chunk_positions[num].append(i)
    
    duplicates = {k: v for k, v in chunk_positions.items() if len(v) > 1}
    return chunk_positions, duplicates


def clean_raw_file(raw_path):
    """Clean a single RAW file.
    
    Returns:
        cleaned_text: The cleaned text
        report: Dict of changes made
    """
    with open(raw_path, 'r', encoding='utf-8') as f:
        original_text = f.read()
    
    lines = original_text.split('\n')
    report = {
        'file': raw_path.name,
        'original_lines': len(lines),
        'stripped_commentary': [],
        'stripped_headers': [],
        'duplicate_chunks': {},
        'preamble_lines_removed': 0,
    }
    
    # Step 1a: Find and remove preamble
    preamble_end = find_preamble_end(lines)
    if preamble_end > 0:
        report['preamble_lines_removed'] = preamble_end
        lines = lines[preamble_end:]
    
    # Step 1b: Detect duplicate chunks
    chunk_positions, duplicates = detect_duplicate_chunks(lines)
    report['duplicate_chunks'] = {k: [str(v) for v in vals] for k, vals in duplicates.items()}
    
    # For duplicates, keep only the last occurrence (which is typically the corrected version)
    if duplicates:
        lines_to_remove = set()
        for chunk_num, positions in duplicates.items():
            # Keep the last occurrence, remove all earlier ones
            for pos in positions[:-1]:
                # Find the range of this chunk: from its header to the next chunk header or end
                next_chunks = [p for p in chunk_positions.get(chunk_num + 1, []) if p > pos]
                # Find the next chunk header of ANY number after this position
                end = len(lines)
                for other_pos_list in chunk_positions.values():
                    for other_pos in other_pos_list:
                        if other_pos > pos and other_pos < end and other_pos != pos:
                            end = other_pos
                for j in range(pos, end):
                    lines_to_remove.add(j)
        
        lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]
    
    # Step 1c: Strip AI commentary lines
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        is_commentary = False
        for pattern in AI_PATTERNS_COMPILED:
            if pattern.match(stripped):
                report['stripped_commentary'].append(stripped[:80])
                is_commentary = True
                break
        if not is_commentary:
            cleaned_lines.append(line)
    
    # Step 1d: Strip chunk headers (but keep the content)
    final_lines = []
    for line in cleaned_lines:
        if CHUNK_HEADER_PATTERN.match(line.strip()):
            report['stripped_headers'].append(line.strip()[:80])
            # Don't add this line
            continue
        final_lines.append(line)
    
    # Step 1e: Remove excessive blank lines (more than 2 consecutive)
    result_lines = []
    blank_count = 0
    for line in final_lines:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 2:
                result_lines.append(line)
        else:
            blank_count = 0
            result_lines.append(line)
    
    report['final_lines'] = len(result_lines)
    return '\n'.join(result_lines), report


# =============================================================================
# STEP 2: EXTRACT FOOTNOTE MARKERS FROM RAW TEXT
# =============================================================================

def extract_markers_from_raw(raw_text):
    """Extract all footnote markers and their surrounding context from RAW text.
    
    Returns a list of dicts: [{number, context_before, context_after, full_line}]
    """
    markers = []
    # Match ^[N] or [N] in body text (not in footnote definition lines)
    # Footnote definitions start with ^[N] at the beginning of a line
    lines = raw_text.split('\n')
    
    for line_num, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip footnote definition lines (start with ^[N] or [N] at line start)
        if re.match(r'^\^?\[\d+\]', stripped):
            continue
        
        # Find inline markers in body text
        for m in re.finditer(r'\^?\[(\d+)\]', line):
            fn_num = int(m.group(1))
            start, end = m.start(), m.end()
            
            # Get context: 40 chars before and after the marker
            ctx_before = line[max(0, start-40):start].strip()
            ctx_after = line[end:min(len(line), end+40)].strip()
            
            # Get 4-word snippet before the marker for matching
            words_before = line[:start].split()
            snippet_4w = ' '.join(words_before[-4:]) if len(words_before) >= 4 else ' '.join(words_before)
            
            markers.append({
                'number': fn_num,
                'context_before': ctx_before,
                'context_after': ctx_after,
                'snippet_4w': snippet_4w,
                'full_line': stripped,
                'line_num': line_num,
                'position_in_line': start,
            })
    
    return markers


# =============================================================================
# STEP 3: STITCH MARKERS INTO ENGLISH BROKEN TEXT
# =============================================================================

def normalize_text(text):
    """Normalize text for fuzzy matching."""
    # Remove extra whitespace, normalize quotes, etc.
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('"', '"').replace('"', '"').replace("'", "'").replace("'", "'")
    text = text.replace('—', '--').replace('–', '-')
    return text.strip().lower()


def find_best_insertion_point(en_text, marker_info, window_size=6):
    """Find the best place in the English text to insert a footnote marker.
    
    Uses fuzzy matching of the context surrounding the marker in the RAW text.
    
    Args:
        en_text: The full English Broken text
        marker_info: Dict with context_before, snippet_4w, etc.
        window_size: Number of words to match (tries from window_size down to 3)
    
    Returns:
        (position, confidence) or (None, 0) if no match found
    """
    snippet = marker_info['snippet_4w']
    if not snippet:
        return None, 0
    
    # Try progressively shorter snippets
    words = snippet.split()
    for num_words in range(min(window_size, len(words)), 2, -1):
        search_snippet = ' '.join(words[-num_words:])
        normalized_snippet = normalize_text(search_snippet)
        
        if not normalized_snippet:
            continue
        
        # Search in normalized English text
        en_normalized = normalize_text(en_text)
        
        # Find all occurrences
        pos = en_normalized.find(normalized_snippet)
        if pos >= 0:
            # Map back to original text position
            # Find the end of this snippet in original text
            original_pos = find_original_position(en_text, normalized_snippet, pos)
            if original_pos is not None:
                confidence = num_words / window_size
                return original_pos, confidence
    
    return None, 0


def find_original_position(original_text, normalized_target, norm_pos):
    """Map a position in normalized text back to the original text.
    
    This is a simplified approach: we search for approximate matches.
    """
    # Try to find the snippet in the original text using a fuzzy approach
    target_words = normalized_target.split()
    if not target_words:
        return None
    
    # Build a regex pattern that allows flexible whitespace
    pattern_parts = [re.escape(w) for w in target_words]
    pattern = r'\s+'.join(pattern_parts)
    
    try:
        m = re.search(pattern, original_text, re.IGNORECASE)
        if m:
            return m.end()  # Insert after the matched text
    except re.error:
        pass
    
    return None


def stitch_markers_into_text(en_text, markers, part_name):
    """Insert footnote markers into English text.
    
    Returns:
        stitched_text, report
    """
    report = {
        'part': part_name,
        'total_markers': len(markers),
        'placed': [],
        'failed': [],
    }
    
    # Sort markers by their expected position (by footnote number)
    markers_sorted = sorted(markers, key=lambda x: x['number'])
    
    # Track insertions (offset grows as we insert markers)
    insertions = []  # [(position, marker_text)]
    
    for marker in markers_sorted:
        fn_num = marker['number']
        marker_text = f'^[{fn_num}]'
        
        # Check if marker already exists in text
        if marker_text in en_text:
            report['placed'].append({
                'number': fn_num,
                'status': 'already_present',
            })
            continue
        
        pos, confidence = find_best_insertion_point(en_text, marker)
        
        if pos is not None and confidence >= 0.5:
            insertions.append((pos, marker_text))
            report['placed'].append({
                'number': fn_num,
                'position': pos,
                'confidence': round(confidence, 2),
                'context': en_text[max(0, pos-30):pos+30],
            })
        else:
            report['failed'].append({
                'number': fn_num,
                'snippet': marker['snippet_4w'],
                'context_before': marker['context_before'],
            })
    
    # Apply insertions from back to front (so positions stay valid)
    insertions.sort(key=lambda x: x[0], reverse=True)
    result = en_text
    for pos, marker_text in insertions:
        result = result[:pos] + marker_text + result[pos:]
    
    return result, report


# =============================================================================
# STEP 4: FIX GLOSSARY ARTIFACTS
# =============================================================================

# Patterns of doubled terms to fix
DOUBLED_TERMS = [
    (r'the Gradual \(Gradual\)', 'the Gradual'),
    (r'the Praises \(Praises\)', 'the Praises'),
    (r'the Praises \(Lauds\) \(Praises\)', 'the Praises (Lauds)'),
    (r'Gradual \(Stepenna\) \(Gradual\)', 'Gradual (Stepenna)'),
    (r'Praises \(Lauds\) stichera \(Praises\)', 'Praises (Lauds) stichera'),
    # Add more as discovered
]


def fix_glossary_artifacts(text):
    """Fix doubled glossary terms and other formatting artifacts."""
    changes = []
    for pattern, replacement in DOUBLED_TERMS:
        count = len(re.findall(pattern, text, re.IGNORECASE))
        if count > 0:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
            changes.append(f'Fixed "{pattern}" -> "{replacement}" ({count} occurrences)')
    
    return text, changes


# =============================================================================
# STEP 5: VERIFY FOOTNOTE ALIGNMENT
# =============================================================================

def parse_footnotes(text, label="file"):
    """Parse a footnotes file into a dict of {number: content}.
    
    Handles various formats:
    - ^[N] text
    - [N] text  
    - ¹ text (superscript)
    """
    footnotes = {}
    current_num = None
    current_text = []
    
    for line in text.split('\n'):
        stripped = line.strip()
        
        # Match footnote start patterns
        m = re.match(r'^\^?\[(\d+)\]\s*(.*)', stripped)
        if not m:
            m = re.match(r'^(\d+)\.\s*(.*)', stripped)  # Fallback: "N. text"
        
        if m:
            # Save previous footnote
            if current_num is not None:
                footnotes[current_num] = ' '.join(current_text).strip()
            
            current_num = int(m.group(1))
            current_text = [m.group(2)] if m.group(2) else []
        elif current_num is not None and stripped:
            # Continuation of current footnote
            current_text.append(stripped)
    
    # Save last footnote
    if current_num is not None:
        footnotes[current_num] = ' '.join(current_text).strip()
    
    return footnotes


def verify_footnote_alignment(en_footnotes_path, ua_footnotes_path):
    """Compare English and Ukrainian footnote files for alignment.
    
    Returns a report of mismatches.
    """
    with open(en_footnotes_path, 'r', encoding='utf-8') as f:
        en_text = f.read()
    with open(ua_footnotes_path, 'r', encoding='utf-8') as f:
        ua_text = f.read()
    
    en_fns = parse_footnotes(en_text, "English")
    ua_fns = parse_footnotes(ua_text, "Ukrainian")
    
    report = {
        'en_count': len(en_fns),
        'ua_count': len(ua_fns),
        'missing_in_en': [],
        'missing_in_ua': [],
        'present_in_both': [],
        'numbering_issues': [],
    }
    
    all_nums = sorted(set(list(en_fns.keys()) + list(ua_fns.keys())))
    
    for num in all_nums:
        if num in en_fns and num in ua_fns:
            report['present_in_both'].append(num)
        elif num in en_fns and num not in ua_fns:
            report['missing_in_ua'].append(num)
        elif num not in en_fns and num in ua_fns:
            report['missing_in_en'].append(num)
    
    # Check for numbering gaps
    if all_nums:
        expected = list(range(min(all_nums), max(all_nums) + 1))
        for num in expected:
            if num not in all_nums:
                report['numbering_issues'].append(f'Gap at footnote {num}')
    
    return report


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("=" * 70)
    print("PHASE 1: TYPIKON TRANSLATION CLEANUP")
    print("=" * 70)
    
    all_reports = {}
    
    # -------------------------------------------------------------------------
    # STEP 1: Clean RAW files
    # -------------------------------------------------------------------------
    print("\n--- STEP 1: Cleaning RAW files ---")
    raw_reports = {}
    cleaned_raws = {}
    
    for raw_name in RAW_TO_EN:
        raw_path = RAW_DIR / raw_name
        if not raw_path.exists():
            print(f"  SKIP: {raw_name} not found")
            continue
        
        print(f"  Cleaning {raw_name}...")
        cleaned_text, report = clean_raw_file(raw_path)
        cleaned_raws[raw_name] = cleaned_text
        raw_reports[raw_name] = report
        
        # Save cleaned version
        cleaned_path = SCRATCH_DIR / f"CLEANED_{raw_name}"
        with open(cleaned_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        
        print(f"    Original: {report['original_lines']} lines")
        print(f"    Preamble removed: {report['preamble_lines_removed']} lines")
        print(f"    Commentary stripped: {len(report['stripped_commentary'])} lines")
        print(f"    Headers stripped: {len(report['stripped_headers'])} headers")
        print(f"    Duplicate chunks: {list(report['duplicate_chunks'].keys()) or 'none'}")
        print(f"    Final: {report['final_lines']} lines")
    
    all_reports['raw_cleanup'] = raw_reports
    
    # -------------------------------------------------------------------------
    # STEP 2: Extract footnote markers from cleaned RAW
    # -------------------------------------------------------------------------
    print("\n--- STEP 2: Extracting footnote markers from RAW ---")
    all_markers = {}
    
    for raw_name, cleaned_text in cleaned_raws.items():
        markers = extract_markers_from_raw(cleaned_text)
        all_markers[raw_name] = markers
        
        fn_numbers = sorted(set(m['number'] for m in markers))
        print(f"  {raw_name}: {len(markers)} markers found")
        if fn_numbers:
            print(f"    Range: [{min(fn_numbers)} - {max(fn_numbers)}]")
    
    # -------------------------------------------------------------------------
    # STEP 3: Stitch markers into English Broken text
    # -------------------------------------------------------------------------
    print("\n--- STEP 3: Stitching markers into English text ---")
    stitch_reports = {}
    
    for raw_name, en_name in RAW_TO_EN.items():
        en_path = EN_DIR / en_name
        if not en_path.exists():
            print(f"  SKIP: {en_name} not found")
            continue
        
        markers = all_markers.get(raw_name, [])
        if not markers:
            print(f"  SKIP: No markers for {raw_name}")
            continue
        
        with open(en_path, 'r', encoding='utf-8') as f:
            en_text = f.read()
        
        print(f"  Stitching into {en_name} ({len(markers)} markers)...")
        stitched_text, report = stitch_markers_into_text(en_text, markers, en_name)
        stitch_reports[en_name] = report
        
        print(f"    Placed: {len(report['placed'])} markers")
        print(f"    Failed: {len(report['failed'])} markers")
        
        if report['failed']:
            print(f"    Failed markers: {[f['number'] for f in report['failed']]}")
        
        # Save stitched version
        stitched_path = SCRATCH_DIR / f"STITCHED_{en_name}"
        with open(stitched_path, 'w', encoding='utf-8') as f:
            f.write(stitched_text)
    
    all_reports['stitching'] = stitch_reports
    
    # -------------------------------------------------------------------------
    # STEP 4: Fix glossary artifacts in stitched files
    # -------------------------------------------------------------------------
    print("\n--- STEP 4: Fixing glossary artifacts ---")
    glossary_reports = {}
    
    for en_name in RAW_TO_EN.values():
        stitched_path = SCRATCH_DIR / f"STITCHED_{en_name}"
        if not stitched_path.exists():
            continue
        
        with open(stitched_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        fixed_text, changes = fix_glossary_artifacts(text)
        glossary_reports[en_name] = changes
        
        if changes:
            print(f"  {en_name}:")
            for change in changes:
                print(f"    {change}")
            
            with open(stitched_path, 'w', encoding='utf-8') as f:
                f.write(fixed_text)
        else:
            print(f"  {en_name}: No artifacts found")
    
    all_reports['glossary_fixes'] = glossary_reports
    
    # -------------------------------------------------------------------------
    # STEP 5: Verify footnote alignment
    # -------------------------------------------------------------------------
    print("\n--- STEP 5: Verifying footnote alignment ---")
    en_fn_path = EN_DIR / "footnotes.txt"
    ua_fn_path = UA_DIR / "Footnotes.txt"
    
    if en_fn_path.exists() and ua_fn_path.exists():
        fn_report = verify_footnote_alignment(en_fn_path, ua_fn_path)
        all_reports['footnote_alignment'] = fn_report
        
        print(f"  English footnotes: {fn_report['en_count']}")
        print(f"  Ukrainian footnotes: {fn_report['ua_count']}")
        print(f"  Present in both: {len(fn_report['present_in_both'])}")
        print(f"  Missing in EN: {fn_report['missing_in_en'][:10]}{'...' if len(fn_report['missing_in_en']) > 10 else ''}")
        print(f"  Missing in UA: {fn_report['missing_in_ua'][:10]}{'...' if len(fn_report['missing_in_ua']) > 10 else ''}")
        print(f"  Numbering issues: {fn_report['numbering_issues'][:5]}{'...' if len(fn_report['numbering_issues']) > 5 else ''}")
    else:
        print(f"  EN footnotes exists: {en_fn_path.exists()}")
        print(f"  UA footnotes exists: {ua_fn_path.exists()}")
    
    # -------------------------------------------------------------------------
    # SAVE MASTER REPORT
    # -------------------------------------------------------------------------
    report_path = REPORT_DIR / "phase1_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(all_reports, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n{'=' * 70}")
    print(f"PHASE 1 COMPLETE")
    print(f"Reports saved to: {REPORT_DIR}")
    print(f"Cleaned RAW files saved to: {SCRATCH_DIR}/CLEANED_*")
    print(f"Stitched EN files saved to: {SCRATCH_DIR}/STITCHED_*")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
