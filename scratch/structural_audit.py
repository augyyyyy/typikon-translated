import os
import re
import math

UA_DIR = r'e:\Google Antigravity\Projects\Translation\Ukrainian TXTs'
EN_DIR = r'e:\Google Antigravity\Projects\Translation\scratch'
REPORT_DIR = os.path.join(EN_DIR, "reports")

FILE_MAP = {
    'Part 1.txt': 'STITCHED_v3_dolnytsky_part1_structure.txt',
    'Part 2.txt': 'STITCHED_v3_dolnytsky_part2_general_rubrics.txt',
    'Part 3.txt': 'STITCHED_v3_dolnytsky_part3_menaion.txt',
    'Part 4.txt': 'STITCHED_v3_dolnytsky_part4_triodion.txt',
    'Part 5.txt': 'STITCHED_v3_dolnytsky_part5_temple.txt',
    'Appendix.txt': 'STITCHED_v3_dolnytsky_appendix.txt'
}

def get_number_sequences(text):
    """
    Extracts ordered lists from text. E.g., '1.', '2.', '3.' at the start of lines.
    Returns a list of extracted numbers.
    """
    seq = []
    for line in text.splitlines():
        line_clean = line.strip()
        m = re.match(r'^(\d+)\.\s', line_clean)
        if m:
            seq.append(int(m.group(1)))
    return seq

def analyze_sequences(ua_seq, en_seq):
    """
    Looks for missing numbers in the EN sequence compared to the UA sequence.
    """
    missing = []
    en_set = set(en_seq)
    for num in ua_seq:
        if num not in en_set:
            missing.append(num)
    return missing

def get_paragraphs(text):
    """
    Returns non-empty paragraphs.
    """
    return [p.strip() for p in text.split('\n') if p.strip()]

def main():
    print("="*60)
    print("PHASE 2: STRUCTURAL INTEGRITY AUDIT")
    print("="*60)

    for ua_filename, en_filename in FILE_MAP.items():
        ua_path = os.path.join(UA_DIR, ua_filename)
        en_path = os.path.join(EN_DIR, en_filename)

        if not os.path.exists(ua_path) or not os.path.exists(en_path):
            continue

        with open(ua_path, 'r', encoding='utf-8') as f:
            ua_text = f.read()
        with open(en_path, 'r', encoding='utf-8') as f:
            en_text = f.read()

        ua_seq = get_number_sequences(ua_text)
        en_seq = get_number_sequences(en_text)

        ua_paras = get_paragraphs(ua_text)
        en_paras = get_paragraphs(en_text)

        ua_len = len(ua_paras)
        en_len = len(en_paras)
        
        ratio = (en_len / ua_len) * 100 if ua_len > 0 else 100

        print(f"\n--- {ua_filename} ---")
        print(f"Paragraphs: UA = {ua_len}, EN = {en_len} ({ratio:.1f}%)")
        
        if ratio < 80.0:
            print("  WARNING: English translation has significantly fewer paragraphs.")
            
        missing_seq = analyze_sequences(set(ua_seq), set(en_seq))
        if missing_seq:
            print(f"  Missing ordered numbers in EN: {sorted(missing_seq)[:15]}... ({len(missing_seq)} total missing)")
        else:
            print("  Sequence numbers align perfectly.")

if __name__ == '__main__':
    main()
