from pathlib import Path
import re

def main():
    txt = Path('scratch/notes_p968_p974.txt').read_text(encoding='utf-8')
    m117 = re.search(r'\n117\.\s*', txt)
    sub = txt[m117.start():]
    m118 = re.search(r'\n118\.\s*', sub[10:])
    note117_full = sub[:m118.start()+10]
    Path('scratch/note117_complete.txt').write_text(note117_full, encoding='utf-8')
    print("Note 117 complete length:", len(note117_full))

if __name__ == '__main__':
    main()
