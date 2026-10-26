from pathlib import Path
import re

def main():
    p = Path('scratch/cohort80_extracted')
    for pno in range(791, 801):
        txt_file = p / f"p{pno}.txt"
        if txt_file.exists():
            content = txt_file.read_text(encoding='utf-8')
            page_markers = re.findall(r'\{[сc]\.?\s*(\d+)\}', content)
            fn_markers = re.findall(r'\[(\d+)\]', content)
            print(f"p{pno}: chars={len(content)}, orig_pages={page_markers}, footnotes={fn_markers}")

if __name__ == '__main__':
    main()
