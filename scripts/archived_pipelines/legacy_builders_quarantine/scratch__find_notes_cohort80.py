from pathlib import Path
import re

def main():
    p = Path('scratch/cohort80_extracted')
    full_notes_text = ""
    for pno in range(1000, 1004):
        txt_file = p / f"notes_p{pno}.txt"
        if txt_file.exists():
            full_notes_text += f"\n--- NOTES PAGE {pno} ---\n" + txt_file.read_text(encoding='utf-8')
    
    # Save combined notes
    out_file = Path('scratch/cohort80_notes_extracted.txt')
    out_file.write_text(full_notes_text, encoding='utf-8')
    print(f"Wrote {len(full_notes_text)} chars to {out_file}")

    # Find footnotes 629 to 657
    for num in range(629, 658):
        pos = full_notes_text.find(f"[{num}]")
        if pos != -1:
            snippet = full_notes_text[pos:pos+150].replace('\n', ' ')
            # Print without cyrillic issue
            print(f"Found [{num}] at {pos}: {snippet.encode('ascii', errors='backslashreplace').decode('ascii')[:100]}")
        else:
            print(f"NOT FOUND: [{num}]")

if __name__ == '__main__':
    main()
