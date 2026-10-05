import os
import requests
import json

def get_deepseek_key():
    global_env = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\.env"
    if os.path.exists(global_env):
        try:
            with open(global_env, "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k_clean = k.strip().replace("[", "").replace("]", "")
                        if k_clean in ("deepseek-v4-pro", "DEEPSEEK_API_KEY"):
                            return v.strip()
        except Exception as e:
            print(f"Error reading global .env: {e}")
    return os.getenv("DEEPSEEK_API_KEY")

def perfect_file(filepath, tag_to_add="[MODEL: DEEPSEEK-PERFECTED]"):
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return False

    api_key = get_deepseek_key()
    if not api_key:
        print("Error: DEEPSEEK_API_KEY not found.")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = f"""
You are an expert systems architect and lead editor for a translation project.
Your task is to "perfect" the following planning document (implementation plan or task list).
Review it for:
1. Technical completeness: Ensure all steps, scripts, and target paths are correct.
2. Anti-pattern compliance: Ensure the proposed changes do not violate zero-tolerance rules (like bare except blocks, hardcoded absolute paths, missing encoding flags, etc.).
3. UGCC translation standard: Ensure terminology and guidelines adhere to UGCC standard names (e.g. Tserkovne Oko, Sluzhebnik, proper pronouns).
4. Edge cases: Highlight any potential gaps or risks during execution.

Modify the document to be as detailed, precise, and perfect as possible.
You MUST add the tag `{tag_to_add}` on the very first line of the document.
Return ONLY the perfected markdown content. Do not include markdown code block wrappers (like ```markdown or ```).

Here is the document to perfect:
---
{content}
"""

    payload = {
        "model": "deepseek-v4-pro",
        "messages": [
            {"role": "system", "content": "You are a professional systems auditor. Output the perfected document directly as markdown without wrappers or conversation."},
            {"role": "user", "content": prompt}
        ],
        "thinking": {"type": "enabled"}
    }

    print(f"Calling DeepSeek V4 Pro to perfect {os.path.basename(filepath)}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        res_json = response.json()
        perfected_content = res_json['choices'][0]['message']['content'].strip()
        
        # Clean any accidental wrappers
        if perfected_content.startswith("```markdown"):
            perfected_content = perfected_content[11:]
        elif perfected_content.startswith("```"):
            perfected_content = perfected_content[3:]
        if perfected_content.endswith("```"):
            perfected_content = perfected_content[:-3]
        perfected_content = perfected_content.strip()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(perfected_content + "\n")
        print(f"Successfully perfected and saved to {filepath}")
        return True
    except Exception as e:
        print(f"Error during perfection pipeline for {filepath}: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python perfect_plan.py <path_to_markdown_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    perfect_file(filepath)
