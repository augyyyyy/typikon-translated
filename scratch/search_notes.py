import fitz
import re

doc = fitz.open(r'E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf')

with open("scratch/search_notes_829_832.txt", "w", encoding="utf-8") as out:
    for p in range(828, 835):
        text = doc[p-1].get_text()
        out.write(f"=== PAGE {p} ===\n")
        # Find footnote markers like numbers in brackets or superscripts
        # In this PDF, note numbers often appear as [123] or just numbers
        for m in re.finditer(r'\[?(\d{3})\]?', text):
            num = int(m.group(1))
            if 695 <= num <= 745:
                # get context
                start = max(0, m.start() - 40)
                end = min(len(text), m.end() + 40)
                ctx = text[start:end].replace('\n', ' ')
                out.write(f"  Note {num} at pos {m.start()}: ...{ctx}...\n")
        out.write("\n")
