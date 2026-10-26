from pathlib import Path
import re

def main():
    txt = Path('scratch/notes_p968_p974.txt').read_text(encoding='utf-8')
    m117 = re.search(r'\n117\.\s*', txt)
    if m117:
        print(f"117 found at {m117.start()}")
        sub = txt[m117.start():]
        # Look for numbers starting lines like \n118. or next section title like ВЕЧЕРНЯ or similar
        m_next = re.search(r'\n([0-9]+)\.\s*', sub[10:])
        if m_next:
            print("Next note number:", m_next.group(1), "at", m_next.start())
            print("Full text of 117:\n", sub[:m_next.start()+10])
        else:
            print("No next numbered note. Look for heading:")
            for line in sub[:2500].splitlines()[:50]:
                if line.isupper() or "---" in line or "===" in line:
                    print("Heading/Page:", line)

if __name__ == '__main__':
    main()
