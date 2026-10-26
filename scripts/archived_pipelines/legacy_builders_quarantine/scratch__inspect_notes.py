from pathlib import Path
import re

def main():
    notes_dir = Path('scratch/cohort57_extracted')
    all_notes_text = ""
    for pno in range(966, 971):
        f = notes_dir / f"notes_p{pno}.txt"
        if f.exists():
            all_notes_text += f"\n--- NOTES PAGE p{pno} ---\n" + f.read_text(encoding='utf-8')
    
    Path('scratch/all_notes_raw.txt').write_text(all_notes_text, encoding='utf-8')
    print("Combined notes raw length:", len(all_notes_text))
    
    # Check for notes 81 through 117
    found = {}
    for n in range(80, 120):
        m = re.search(rf"(?:^|\n)\s*{n}\.\s*", all_notes_text)
        if m:
            found[n] = m.start()
            print(f"Found Note {n} at pos {m.start()}")
        else:
            print(f"Note {n} NOT found with standard pattern")

if __name__ == '__main__':
    main()
