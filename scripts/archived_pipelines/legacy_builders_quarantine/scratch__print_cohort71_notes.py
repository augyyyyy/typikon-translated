from pathlib import Path
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

all_notes_text = ""
for pno in [991, 992, 993]:
    f = Path(f'scratch/cohort71_extracted/notes_p{pno}.txt')
    all_notes_text += f"\n--- PAGE {pno} ---\n" + f.read_text(encoding='utf-8')

# Let's find each note from 469 to 502
for note_num in range(469, 503):
    pattern = rf'(?:^|\n)\s*{note_num}\b'
    m = re.search(pattern, all_notes_text)
    if m:
        start = m.start()
        # next note pattern
        next_num = note_num + 1
        m_next = re.search(rf'(?:^|\n)\s*{next_num}\b', all_notes_text[start:])
        if m_next:
            end = start + m_next.start()
        else:
            end = start + 500
        print(f"[{note_num}] -> global [^{note_num - 469 + 2303}]")
        print(all_notes_text[start:end].strip())
        print("="*60)
    else:
        print(f"[{note_num}] NOT FOUND!")
