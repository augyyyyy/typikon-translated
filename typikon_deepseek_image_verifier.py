import os
import sys
import json
import time
import requests
import argparse
import re

# Robust DeepSeek key loader
def get_deepseek_key():
    # 1. Check direct environment variable
    key = os.getenv("DEEPSEEK_API_KEY")
    if key and key != "your_deepseek_api_key_here":
        return key

    # 2. Check global .env file path
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

    # 3. Check local .env
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

BASE_DIR = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation"
FINAL_DIR = os.path.join(BASE_DIR, "Final")
OUT_DIR = os.path.join(BASE_DIR, "Audit_Reports")
LOG_PATH = os.path.join(BASE_DIR, "visual_audit_log.md")
FOOTNOTES_PATH = os.path.join(FINAL_DIR, "Final_footnotes.txt")

os.makedirs(OUT_DIR, exist_ok=True)

def get_lines_for_image(img_num):
    if not os.path.exists(LOG_PATH):
        return None, None
        
    try:
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading audit log: {e}")
        return None, None
        
    sections = content.split("### ")
    for sec in sections:
        if f"Image {img_num:03d}" in sec or f"Image {img_num}\b" in sec:
            # Target File
            file_match = re.search(r"\*\*Target File\*\*:\s*`([^`]+)`", sec)
            if not file_match:
                file_match = re.search(r"\*\*Target Files\*\*:\s*`([^`]+)`", sec)
            target_file = file_match.group(1).strip() if file_match else None
            
            # Lines Audited
            lines_match = re.search(r"\*\*Lines Audited\*\*:\s*([^\r\n]+)", sec)
            lines_str = lines_match.group(1).replace("`", "").strip() if lines_match else ""
            
            return target_file, lines_str
            
    return None, None

def get_file_for_image_fallback(img_num):
    if 1 <= img_num <= 5:
        return "Final_Dolnytsky_intro.txt"
    elif 6 <= img_num <= 22:
        return "Final_Dolnytsky_part1_structure.txt"
    elif 23 <= img_num <= 53:
        return "Final_Dolnytsky_part2_general_rubrics.txt"
    elif 54 <= img_num <= 146:
        return "Final_Dolnytsky_part3_menaion.txt"
    elif 147 <= img_num <= 210:
        return "Final_Dolnytsky_part4_triodion.txt"
    elif 211 <= img_num <= 247:
        return "Final_Dolnytsky_part5_temple.txt"
    elif 248 <= img_num <= 287:
        return "Final_Dolnytsky_appendix.txt"
    return None

def call_deepseek_text_audit(key, img_num, eng_filename, lines_msg, eng_segment, footnotes_content, model_name="deepseek-v4-pro"):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    
    prompt = f"""You are an expert Byzantine Liturgical Auditor. Your task is to perform a strict semantic and formatting audit of an English translation of the Ukrainian Greek-Catholic Church (UHKC) Typikon.

We are auditing the text of Page {img_num} (associated with lines: {lines_msg}).

Below is the corresponding English translation segment, and the Master Footnotes file.

---
ENGLISH TRANSLATION SEGMENT ({eng_filename}):
{eng_segment}
---
MASTER FOOTNOTES FILE (Final_footnotes.txt):
{footnotes_content}
---

Your task:
1. Analyze the English translation segment.
2. Verify the following:
   - Footnote markers (e.g. `[^N]`) are correctly formatted and positioned.
   - The terminology complies with standard Byzantine liturgical English (e.g., "Sessional Hymn" instead of "Kathisma" for Сідален, "Compline" instead of "Povechiria", "Temple" instead of "Church/Khram", etc.).
   - Hieratic pronouns (He, Him, His, Who referring to God) are properly capitalized, while pronouns referring to the Theotokos (Virgin Mary), saints, angels, or humans remain lowercase.
   - Bolding, italics, list structures, and heading levels are clean and consistent.
   - Identify any typos, awkward phrasing, or formatting errors.

Output your report for this page in the following format:
### Page {img_num} ({lines_msg})
- **Footnotes present**: [List footnote numbers present in this segment]
- **Discrepancies / Issues found**:
  - [List any glossary violations, capitalization errors, formatting problems, or awkward phrasing. If none, state "None"]
- **Remediation Action**: [Specify the exact correction needed. If none, state "None"]
"""

    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "You are an elite Canonical Auditor for the Ruthenian Byzantine Catholic Church. You map English translations strictly against liturgical rules and glossary matrices."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    # Configure thinking mode if using reasoning models
    is_reasoning = "reasoner" in model_name or "pro" in model_name or "chat" not in model_name
    if is_reasoning:
        # Pass thinking mode at root level for direct HTTP payload
        data["thinking"] = {"type": "enabled"}
    else:
        data["temperature"] = 0.1

    max_retries = 5
    backoff = 2
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            if response.status_code == 429:
                sleep_time = backoff ** attempt + 2
                print(f"     [Rate Limit] HTTP 429 on page {img_num}. Retrying in {sleep_time}s (attempt {attempt+1}/{max_retries})...")
                time.sleep(sleep_time)
                continue
            response.raise_for_status()
            res_json = response.json()
            
            choice = res_json['choices'][0]['message']
            content = choice.get('content', '')
            reasoning = choice.get('reasoning_content', '')
            
            if reasoning:
                return f"{content}\n\n<details>\n<summary>DeepSeek V4 Auditing Reasoning Chain</summary>\n\n{reasoning}\n</details>"
            return content
        except Exception as e:
            if attempt == max_retries - 1:
                return f"Error calling DeepSeek API for page {img_num} after {max_retries} attempts: {e}"
            sleep_time = backoff ** attempt + 2
            print(f"     [Error] {e} on page {img_num}. Retrying in {sleep_time}s (attempt {attempt+1}/{max_retries})...")
            time.sleep(sleep_time)
            
    return f"Error: Failed to get response for page {img_num} due to rate limits or transient errors."

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    parser = argparse.ArgumentParser(description="Dolnytsky Typikon Text Auditor (DeepSeek V4)")
    parser.add_argument("--start-img", type=int, default=125, help="Start image number (1-287)")
    parser.add_argument("--end-img", type=int, default=130, help="End image number (1-287)")
    parser.add_argument("--output", type=str, default="Visual_Image_Audit_Report.md", help="Output report filename")
    parser.add_argument("--model", type=str, default="deepseek-v4-pro", help="DeepSeek model name")
    
    args = parser.parse_args()
    
    print("Initializing Typikon DeepSeek Translation Text Auditor...")
    key = get_deepseek_key()
    if not key:
        print("Error: DeepSeek API key not found in .env files.")
        sys.exit(1)
        
    print(f"Auditing pages from {args.start_img} to {args.end_img} using model {args.model}...")
    
    # Load footnotes content
    footnotes_content = ""
    if os.path.exists(FOOTNOTES_PATH):
        with open(FOOTNOTES_PATH, "r", encoding="utf-8") as f:
            footnotes_content = f.read()
    else:
        print(f"Warning: Footnotes file not found at {FOOTNOTES_PATH}")
        
    out_file = os.path.join(OUT_DIR, args.output)
    
    # Write report header if starting new audit
    if args.start_img == 125 or not os.path.exists(out_file):
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"# Typikon Translation Audit Report (DeepSeek V4)\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: {args.model}\n")
            f.write(f"Auditing Pages: {args.start_img} to {args.end_img}\n")
            f.write(f"---\n\n")
            
    # Cache loaded English files
    eng_cache = {}
    
    for img_num in range(args.start_img, args.end_img + 1):
        eng_file, lines_str = get_lines_for_image(img_num)
        
        if not eng_file:
            # Fallback mapping
            eng_file = get_file_for_image_fallback(img_num)
            lines_str = "full file (fallback)"
            
        if not eng_file:
            print(f"Skipping page {img_num} - could not map to English file.")
            continue
            
        print(f"  -> Auditing page {img_num} ({lines_str}) against {eng_file}...")
        
        if eng_file not in eng_cache:
            eng_path = os.path.join(FINAL_DIR, eng_file)
            if os.path.exists(eng_path):
                with open(eng_path, "r", encoding="utf-8") as f:
                    eng_cache[eng_file] = f.read()
            else:
                print(f"Error: English file not found at {eng_path}")
                continue
                
        eng_content = eng_cache[eng_file]
        
        # Segment the text if range is known
        eng_segment = eng_content
        lines_msg = "full file"
        if lines_str and "-" in lines_str:
            lines_msg = f"lines {lines_str}"
            m = re.findall(r"\d+", lines_str)
            if len(m) >= 2:
                start_line = int(m[0])
                end_line = int(m[1])
                lines_list = eng_content.splitlines()
                eng_segment = "\n".join(lines_list[start_line - 1 : min(end_line, len(lines_list))])
        
        report = call_deepseek_text_audit(key, img_num, eng_file, lines_msg, eng_segment, footnotes_content, args.model)
        
        print(f"     Done. Writing report details...")
        with open(out_file, "a", encoding="utf-8") as f:
            f.write(report + "\n\n---\n\n")
            
        # Respect rate limits
        time.sleep(2)
        
    print(f"\nSaved translation audit report to {out_file}\n")

if __name__ == "__main__":
    main()
