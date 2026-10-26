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

def main():
    api_key = get_deepseek_key()
    if not api_key:
        print("Error: DEEPSEEK_API_KEY not found.")
        return

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = """
Write a python script `scratch/search_anti_patterns.py` that walks a target directory (default: current directory '.') and scans all `.py` and `.md` files for code anti-patterns.
The script should identify:
1. Bare except blocks: `except:` or `except Exception:` followed immediately by `pass` or empty block.
2. Hardcoded absolute paths: Strings containing `C:\\Users`, `E:\\`, `OneDrive\\Documents`, or similar absolute paths.
3. Missing `encoding` parameter in `open(...)` calls: Files opened without explicitly specifying `encoding='utf-8'` (or similar).
4. Subprocess or git calls in python that do not disable pagers (e.g. running 'git diff' or 'git log' without PAGER env variable set to 'cat' or '--no-pager').
5. Fragile regex for structural headers: Any regex pattern looking for 'Ode \d+' or similar heading splits instead of startswith/procedural checks.

The script must print a clean, clear markdown report showing the filename, line number, anti-pattern type, and the matching line of code. Write the python code directly, without markdown wrapper blocks (no ```python and ```), so it can be written straight to disk.
"""

    payload = {
        "model": "deepseek-v4-pro",
        "messages": [
            {"role": "system", "content": "You are a senior python developer. Write clean, robust, runnable python code directly without any markdown formatting wrappers or explanation."},
            {"role": "user", "content": prompt}
        ],
        "thinking": {"type": "enabled"}
    }

    print("Calling DeepSeek V4 Pro to build the searcher...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        res_json = response.json()
        content = res_json['choices'][0]['message']['content'].strip()
        
        # Strip markdown code blocks if any got returned despite system instructions
        if content.startswith("```python"):
            content = content[9:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        output_path = r"scratch\search_anti_patterns.py"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully generated and wrote searcher script to {output_path}")
    except Exception as e:
        print(f"Error calling DeepSeek: {e}")

if __name__ == "__main__":
    main()
