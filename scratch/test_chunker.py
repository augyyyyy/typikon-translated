import os
import re

BASE_DIR = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation"
UKR_DIR = os.path.join(BASE_DIR, "Ukrainian TXTs")
ENG_DIR = os.path.join(BASE_DIR, "Final")

PAIRS = [
    ("Intro.txt", "Final_Dolnytsky_intro.txt"),
    ("Part 1.txt", "Final_Dolnytsky_part1_structure.txt"),
    ("Part 2.txt", "Final_Dolnytsky_part2_general_rubrics.txt"),
    ("Part 3.txt", "Final_Dolnytsky_part3_menaion.txt"),
    ("Part 4.txt", "Final_Dolnytsky_part4_triodion.txt"),
    ("Part 5.txt", "Final_Dolnytsky_part5_temple.txt"),
    ("Appendix.txt", "Final_Dolnytsky_appendix.txt"),
    ("Footnotes.txt", "Final_footnotes.txt")
]

# Patterns that indicate a logical header boundary
HEADER_PATTERNS = [
    re.compile(r'^ЧАСТИНА\s+[IVXLCDM]+', re.IGNORECASE),
    re.compile(r'^PART\s+[IVXLCDM]+', re.IGNORECASE),
    re.compile(r'^(ВЕЧІРНЯ|VESPERS|ПОВЕЧІР’Я|COMPLINE|ПІВНІЧНА|MIDNIGHT OFFICE|УТРЕНЯ|MATINS|ЛІТУРГІЯ|LITURGY)$', re.IGNORECASE),
    re.compile(r'^ЧИН\s+', re.IGNORECASE),
    re.compile(r'^ORDER\s+OF\s+', re.IGNORECASE),
    re.compile(r'^\d+\.\s+[A-ZА-Я]', re.UNICODE), # e.g. "1. Vesting" or "1. Одягання"
    re.compile(r'^###\s+'),
    re.compile(r'^##\s+'),
    re.compile(r'^#\s+'),
    re.compile(r'^Від видавництва', re.IGNORECASE),
    re.compile(r'^Publisher\'s\s+Note', re.IGNORECASE),
    re.compile(r'^СКЛАДОВІ\s+ЧАСТИНИ', re.IGNORECASE),
    re.compile(r'^CONSTITUENT\s+PARTS', re.IGNORECASE),
    re.compile(r'^Примітка', re.IGNORECASE),
    re.compile(r'^Note', re.IGNORECASE),
    re.compile(r'^\[\^?\d+\]'), # Footnote marker at start of line
]

LANDMARK_REGEXES = [
    re.compile(r'^\s*(PART|ЧАСТИНА)\s+[IVXLCDM]+', re.IGNORECASE),
    re.compile(r'^\s*(VESPERS|ВЕЧІРНЯ|COMPLINE|ПОВЕЧІР’Я|MIDNIGHT\s+OFFICE|ПІВНІЧНА|MATINS|УТРЕНЯ|LITURGY|ЛІТУРГІЯ)($|\s)', re.IGNORECASE),
    re.compile(r'^\s*(ORDER\s+OF|ЧИН\s+)', re.IGNORECASE),
    re.compile(r'^\s*(\d+)\.\s+\w+', re.UNICODE),
    re.compile(r'^\s*(Beginning|Початок|Notes|Примітки|Note|Примітка|Main\s+Part|Головна\s+частина|Conclusion|Закінчення|Rubrics|Чинності|Text|Текст|Publisher\'s\s+Note|Від\s+видавництва|CONSTITUENT\s+PARTS|СКЛАДОВІ\s+ЧАСТИНИ)($|\s)', re.IGNORECASE),
]

def get_anchor_key(p):
    p_clean = p.strip()
    
    # 1. PART/ЧАСТИНА
    m = re.match(r'^(PART|ЧАСТИНА)\s+([IVXLCDM]+)', p_clean, re.IGNORECASE)
    if m:
        return f"PART_{m.group(2).upper()}"
        
    # 2. Match dates (e.g. 1 September / 1 вересня / September 1)
    months_ukr = ["вересня", "жовтня", "листопада", "грудня", "січня", "лютого", "березня", "квітня", "травня", "червня", "липня", "серпня"]
    months_eng = ["september", "october", "november", "december", "january", "february", "march", "april", "may", "june", "july", "august"]
    
    # Check Ukrainian format: "1 вересня"
    m = re.match(r'^(\d+)(?:–\d+|-до)?\s+([а-яяєїіґ]+)', p_clean, re.IGNORECASE)
    if m:
        day = m.group(1)
        month_str = m.group(2).lower()
        if month_str in months_ukr:
            month_idx = months_ukr.index(month_str) + 9 # September is 9th
            if month_idx > 12:
                month_idx -= 12
            return f"DATE_{month_idx}_{day}"
            
    # Check English format: "1 September" or "September 1"
    m = re.match(r'^(\d+)(?:st|nd|rd|th)?\s+(?:of\s+)?([a-z]+)', p_clean, re.IGNORECASE)
    if m:
        day = m.group(1)
        month_str = m.group(2).lower()
        if month_str in months_eng:
            month_idx = months_eng.index(month_str) + 9
            if month_idx > 12:
                month_idx -= 12
            return f"DATE_{month_idx}_{day}"
            
    m = re.match(r'^([a-z]+)\s+(\d+)', p_clean, re.IGNORECASE)
    if m:
        month_str = m.group(1).lower()
        day = m.group(2)
        if month_str in months_eng:
            month_idx = months_eng.index(month_str) + 9
            if month_idx > 12:
                month_idx -= 12
            return f"DATE_{month_idx}_{day}"
            
    # 3. Numbered headings (e.g. 1. Vesting)
    m = re.match(r'^(\d+)\.', p_clean)
    if m:
        return f"NUM_{m.group(1)}"
        
    # 4. Major headings
    for key in ["VESPERS", "ВЕЧІРНЯ", "COMPLINE", "ПОВЕЧІР’Я", "MATINS", "УТРЕНЯ", "LITURGY", "ЛІТУРГІЯ"]:
        if key.lower() in p_clean[:20].lower():
            return f"HEAD_{key.upper()}"
            
    return None

def align_and_chunk(ukr_text, eng_text, max_chars=12000):
    ukr_lines = [line.strip() for line in ukr_text.split('\n')]
    eng_lines = [line.strip() for line in eng_text.split('\n')]
    
    # Filter out empty lines but keep their index mapping
    ukr_nonempty = [(idx, line) for idx, line in enumerate(ukr_lines) if line]
    eng_nonempty = [(idx, line) for idx, line in enumerate(eng_lines) if line]
    
    ukr_anchors = []
    for idx, line in ukr_nonempty:
        key = get_anchor_key(line)
        if key:
            ukr_anchors.append((key, idx, line))
            
    eng_anchors = []
    for idx, line in eng_nonempty:
        key = get_anchor_key(line)
        if key:
            eng_anchors.append((key, idx, line))
            
    aligned_pairs = []
    u_ptr = 0
    e_ptr = 0
    
    while u_ptr < len(ukr_anchors) and e_ptr < len(eng_anchors):
        u_key, u_idx, u_line = ukr_anchors[u_ptr]
        e_key, e_idx, e_line = eng_anchors[e_ptr]
        
        if u_key == e_key:
            aligned_pairs.append((u_idx, e_idx))
            u_ptr += 1
            e_ptr += 1
        else:
            matched = False
            for look_ahead in range(1, 6):
                if u_ptr + look_ahead < len(ukr_anchors):
                    if ukr_anchors[u_ptr + look_ahead][0] == e_key:
                        u_ptr += look_ahead
                        matched = True
                        break
                if e_ptr + look_ahead < len(eng_anchors):
                    if eng_anchors[e_ptr + look_ahead][0] == u_key:
                        e_ptr += look_ahead
                        matched = True
                        break
            if not matched:
                u_ptr += 1
                e_ptr += 1
                
    chunks = []
    last_u_idx = 0
    last_e_idx = 0
    
    for u_idx, e_idx in aligned_pairs:
        u_chunk_text = "\n".join(ukr_lines[last_u_idx:u_idx])
        e_chunk_text = "\n".join(eng_lines[last_e_idx:e_idx])
        
        if u_chunk_text.strip() or e_chunk_text.strip():
            chunks.append((u_chunk_text, e_chunk_text))
            
        last_u_idx = u_idx
        last_e_idx = e_idx
        
    u_chunk_text = "\n".join(ukr_lines[last_u_idx:])
    e_chunk_text = "\n".join(eng_lines[last_e_idx:])
    if u_chunk_text.strip() or e_chunk_text.strip():
        chunks.append((u_chunk_text, e_chunk_text))
        
    # Optional proportional subdivision if a chunk is too large
    final_chunks = []
    for u_c, e_c in chunks:
        if len(u_c) > max_chars or len(e_c) > max_chars:
            u_l = u_c.split('\n')
            e_l = e_c.split('\n')
            u_mid = len(u_l) // 2
            e_mid = len(e_l) // 2
            
            u_c1 = "\n".join(u_l[:u_mid])
            u_c2 = "\n".join(u_l[u_mid:])
            e_c1 = "\n".join(e_l[:e_mid])
            e_c2 = "\n".join(e_l[e_mid:])
            
            final_chunks.append((u_c1, e_c1))
            final_chunks.append((u_c2, e_c2))
        else:
            final_chunks.append((u_c, e_c))
            
    return final_chunks


def main():
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    for ukr_file, eng_file in PAIRS:
        ukr_path = os.path.join(UKR_DIR, ukr_file)
        eng_path = os.path.join(ENG_DIR, eng_file)
        
        if not os.path.exists(ukr_path) or not os.path.exists(eng_path):
            continue
            
        with open(ukr_path, 'r', encoding='utf-8') as f:
            ukr_text = f.read()
        with open(eng_path, 'r', encoding='utf-8') as f:
            eng_text = f.read()
            
        chunks = align_and_chunk(ukr_text, eng_text)
        
        print(f"=== {ukr_file} vs {eng_file} ===")
        print(f"  Generated {len(chunks)} aligned chunks.")
        # Print sample from first few chunks
        for i in range(min(4, len(chunks))):
            u_c, e_c = chunks[i]
            u_sample = u_c.split('\n')[0][:50] if u_c else "[Empty]"
            e_sample = e_c.split('\n')[0][:50] if e_c else "[Empty]"
            print(f"    Chunk {i+1}:")
            print(f"      UKR: {u_sample}")
            print(f"      ENG: {e_sample}")
        print()




if __name__ == "__main__":
    main()
