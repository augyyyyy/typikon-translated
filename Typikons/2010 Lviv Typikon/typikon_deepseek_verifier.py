import os
import re
import time
import requests
from dotenv import load_dotenv

# Robust DeepSeek key loader to handle different execution directories and formats
def get_deepseek_key():
    # 1. Try direct environment variable
    key = os.getenv("DEEPSEEK_API_KEY")
    if key and key != "your_deepseek_api_key_here":
        return key

    # 2. Try global .env file path
    global_env = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\.env"
    if os.path.exists(global_env):
        try:
            with open(global_env, "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k_clean = k.strip().replace("[", "").replace("]", "")
                        if k_clean in ("deepseek-v4-pro", "DEEPSEEK_API_KEY"):
                            val = v.strip()
                            if val:
                                return val
        except Exception as e:
            print(f"Warning: Error reading global .env: {e}")

    # 3. Try local .env
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k_clean = k.strip().replace("[", "").replace("]", "")
                        if k_clean in ("deepseek-v4-pro", "DEEPSEEK_API_KEY"):
                            val = v.strip()
                            if val and val != "your_deepseek_api_key_here":
                                return val
        except Exception as e:
            print(f"Warning: Error reading local .env: {e}")

    return None

load_dotenv()

DEEPSEEK_API_KEY = get_deepseek_key()
# Transition legacy model names to the current DeepSeek V4 API
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")
API_URL = "https://api.deepseek.com/chat/completions"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UKR_DIR = os.path.join(BASE_DIR, "Ukrainian TXTs")
ENG_DIR = os.path.join(BASE_DIR, "Final")
OUT_DIR = os.path.join(BASE_DIR, "Audit_Reports")
SYSTEM_INSTRUCTIONS_PATH = os.path.join(BASE_DIR, "_brain", "SYSTEM_INSTRUCTIONS.md")

os.makedirs(OUT_DIR, exist_ok=True)

# Define pairs: (Ukrainian filename, English filename)
PAIRS = [
    # Already audited successfully before the server restart:
    # ("Intro.txt", "Final_Dolnytsky_intro.txt"),
    # ("Part 1.txt", "Final_Dolnytsky_part1_structure.txt"),
    # ("Part 2.txt", "Final_Dolnytsky_part2_general_rubrics.txt"),
    # ("Part 3.txt", "Final_Dolnytsky_part3_menaion.txt"),
    ("Part 4.txt", "Final_Dolnytsky_part4_triodion.txt"),
    ("Part 5.txt", "Final_Dolnytsky_part5_temple.txt"),
    ("Appendix.txt", "Final_Dolnytsky_appendix.txt"),
    ("Footnotes.txt", "Final_footnotes.txt")
]

# Read system instructions to serve as cached prefix context
def load_system_instructions():
    if os.path.exists(SYSTEM_INSTRUCTIONS_PATH):
        try:
            with open(SYSTEM_INSTRUCTIONS_PATH, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Warning: Could not read SYSTEM_INSTRUCTIONS.md: {e}")
    return "No system instructions file found."

SYSTEM_INSTRUCTIONS_CONTENT = load_system_instructions()

# DeepSeek Caching Optimization: Prepend static instructions/glossary at the absolute start of prompt
SYSTEM_PROMPT = f"""You are an expert liturgical translator and auditor.
Below are the canonical system instructions, style rules, and Master Terminology Glossary for the Dolnytsky Typikon translation project.
You must use these rules to evaluate and audit the translation.

---
SYSTEM INSTRUCTIONS & MASTER GLOSSARY:
{SYSTEM_INSTRUCTIONS_CONTENT}
---

CRITICAL AUDIT TASK:
Perform a strict 1:1 comparison and audit between the original Ukrainian source text and its corresponding English translation.
Identify:
1. Missing sentences or dropped concepts.
2. Semantic inaccuracies or mistranslations.
3. Violations of liturgical terminology rules (e.g., using forbidden variants instead of canonical English terms from the glossary).
4. Pronoun and deity capitalization rule violations.

Output your findings as a concise markdown list of errors or warnings. If the translation is perfect, state 'No issues found.'"""

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
        
    # 4. Footnote anchors
    m = re.match(r'^\[\^?(\d+)\]', p_clean)
    if m:
        return f"FOOT_{m.group(1)}"
        
    # 5. Major headings
    for key in ["VESPERS", "ВЕЧІРНЯ", "COMPLINE", "ПОВЕЧІР’Я", "MATINS", "УТРЕНЯ", "LITURGY", "ЛІТУРГІЯ"]:
        if key.lower() in p_clean[:20].lower():
            return f"HEAD_{key.upper()}"
            
    return None

def align_and_chunk(ukr_text, eng_text, max_chars=12000):
    """
    Symmetrically chunks Ukrainian and English files using line-based structural anchors
    and look-ahead sequential resynchronization.
    """
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
        
    # Group small chunks to stay efficient, but keep under max_chars
    grouped_chunks = []
    curr_u, curr_e = [], []
    curr_len = 0
    
    for u_c, e_c in chunks:
        if curr_len + len(u_c) + len(e_c) > max_chars and curr_u:
            grouped_chunks.append(("\n".join(curr_u), "\n".join(curr_e)))
            curr_u, curr_e = [u_c], [e_c]
            curr_len = len(u_c) + len(e_c)
        else:
            curr_u.append(u_c)
            curr_e.append(e_c)
            curr_len += len(u_c) + len(e_c)
            
    if curr_u:
        grouped_chunks.append(("\n".join(curr_u), "\n".join(curr_e)))
        
    # Proportional subdivision for any chunk that is still too large
    final_chunks = []
    for u_c, e_c in grouped_chunks:
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

def call_deepseek(ukr_chunk, eng_chunk):
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_deepseek_api_key_here":
        return "[DRY RUN / NO API KEY] Would call DeepSeek here to compare.", ""
        
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # U-Shaped Attention Wrap: Critical reminders repeated at the absolute end of user prompt
    user_content = f"""### Ukrainian Source Segment:
{ukr_chunk}

### English Translation Segment:
{eng_chunk}

---
REMINDER OF CRITICAL RULES:
1. Verify if any sentence, footnote marker, or instruction from the Ukrainian source is missing or dropped in the English translation.
2. Verify if the liturgical terms comply with the master glossary (e.g., "Sessional Hymn" instead of "Kathisma" for Сідален, "Prokimenon" instead of "Prokeimenon", etc.).
3. Point out any semantic discrepancies or inaccuracies.
4. Output your findings as a concise markdown list of issues, or state "No issues found." if it is fully compliant."""

    # Automatically configure thinking mode: enable thinking for V4-Pro/Reasoner, disable for Flash/Chat
    is_reasoning = "reasoner" in DEEPSEEK_MODEL or "pro" in DEEPSEEK_MODEL
    thinking_type = "enabled" if is_reasoning else "disabled"

    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ],
        "thinking": {"type": thinking_type}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        res_json = response.json()
        
        choice = res_json['choices'][0]['message']
        content = choice.get('content', '')
        reasoning = choice.get('reasoning_content', '')
        
        return content, reasoning
    except Exception as e:
        return f"Error calling API: {e}", ""

def main():
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print(f"Initializing Typikon DeepSeek Verifier...")
    print(f"Model configured: {DEEPSEEK_MODEL}")
    if not DEEPSEEK_API_KEY:
        print("⚠️ Warning: DEEPSEEK_API_KEY is not set. Script will run in DRY RUN mode.")
        
    for ukr_file, eng_file in PAIRS:
        ukr_path = os.path.join(UKR_DIR, ukr_file)
        eng_path = os.path.join(ENG_DIR, eng_file)
        
        if not os.path.exists(ukr_path) or not os.path.exists(eng_path):
            print(f"Skipping pair {ukr_file} / {eng_file} - File not found.")
            continue
            
        print(f"Auditing {ukr_file} vs {eng_file}...")
        
        with open(ukr_path, 'r', encoding='utf-8') as f:
            ukr_text = f.read()
        with open(eng_path, 'r', encoding='utf-8') as f:
            eng_text = f.read()
            
        chunks = align_and_chunk(ukr_text, eng_text)
        print(f"  -> Generated {len(chunks)} aligned semantic chunks.")
        
        report_lines = [
            f"# Audit Report: {ukr_file} vs {eng_file}",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Model: {DEEPSEEK_MODEL}",
            "---\n"
        ]
        
        for i, (u_chunk, e_chunk) in enumerate(chunks):
            print(f"  -> Processing Chunk {i+1}/{len(chunks)}")
            report_lines.append(f"## Chunk {i+1}")
            
            # Print sample snippet of the chunk headers
            u_sample = u_chunk.split('\n')[0][:50] if u_chunk else "[Empty]"
            e_sample = e_chunk.split('\n')[0][:50] if e_chunk else "[Empty]"
            print(f"     UKR: {u_sample}")
            print(f"     ENG: {e_sample}")
            
            content, reasoning = call_deepseek(u_chunk, e_chunk)
            
            if reasoning:
                report_lines.append("<details>")
                report_lines.append("<summary>DeepSeek R1 Chain-of-Thought Reasoning</summary>\n")
                report_lines.append(reasoning)
                report_lines.append("\n</details>\n")
                
            report_lines.append("### Audit Findings")
            report_lines.append(content + "\n")
            
            # Rate limit protection (polite pause, only if calling real API)
            if DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "your_deepseek_api_key_here":
                time.sleep(1)
            
        out_file = os.path.join(OUT_DIR, f"Audit_{ukr_file.replace('.txt', '.md')}")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
        
        print(f"Saved report to {out_file}\n")

if __name__ == "__main__":
    main()
