from pathlib import Path
import re

def main():
    text = Path('scratch/cohort80_notes_extracted.txt').read_text(encoding='utf-8')
    
    # Let's find each footnote from 629 to 657
    notes = {}
    for num in range(629, 658):
        # Match pattern like: num.\s or num.\xa0
        m = re.search(rf"(?:^|\n)\s*{num}\.[\s\xa0]+", text)
        if m:
            start_pos = m.end()
            # Find next footnote
            m_next = re.search(rf"(?:^|\n)\s*{num+1}\.[\s\xa0]+", text[start_pos:])
            if m_next:
                end_pos = start_pos + m_next.start()
                fn_content = text[start_pos:end_pos].strip()
            else:
                fn_content = text[start_pos:].strip()
            notes[num] = fn_content
        else:
            print(f"FAILED TO FIND NOTE {num}")

    print(f"Total notes found: {len(notes)}")
    out_lines = []
    for num, content in sorted(notes.items()):
        clean_content = " ".join(content.split())
        out_lines.append(f"[{num}]: {clean_content}")
        
    Path('scratch/cohort80_notes_raw.txt').write_text("\n\n".join(out_lines), encoding='utf-8')
    print("Wrote scratch/cohort80_notes_raw.txt successfully!")

if __name__ == '__main__':
    main()
