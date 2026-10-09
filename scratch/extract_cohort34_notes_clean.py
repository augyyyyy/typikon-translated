import sys
from pathlib import Path
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open("E:/Google Drive/Liturgical Library/3. Modern Service Books and Typikons/Typikon/Historical Typikons/1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf")

# Get text from pages 505 to 507
raw_text = doc[504].get_text() + "\n" + doc[505].get_text() + "\n" + doc[506].get_text()

# We know the positions or we can split precisely
# Let's inspect where note 17 begins and note 35 begins
start_17 = raw_text.find("17. По рассказу")
if start_17 == -1:
    start_17 = raw_text.find("17. По рассказу")
end_34 = raw_text.find("35. Родом придворный")
if end_34 == -1:
    end_34 = raw_text.find("35. Родом придворный")

section = raw_text[start_17:end_34]

# Let's define the anchors for notes 17 to 34
note_heads = [
    (17, "17. По рассказу"),
    (18, "18. Дмитриевский Τυπικὰ"),
    (19, "19. Путеш. арх. Антония"),
    (20, "20. Симеон Сол. О бож. мол."),
    (21, "21. Goar, Εὐχολόγ."),
    (22, "22. Патм. ркп. № 266"),
    (23, "23. Дрезден. ркп. № 140"),
    (24, "24. Дрезден. ркп. № 140,"),
    (25, "25. Дмитриевский, Богосл."),
    (26, "26. На что впервые"),
    (27, "27. Патм. ркп. № 266,"),
    (28, "28. Дрезд. ркп. № 140,"),
    (29, "29. Правило митр. Георгия"),
    (30, "30. Дмитриевский, Богосл."),
    (31, "31. Дрезд. ркп. № 140,"),
    (32, "32. Дмитриевский, Εὐχ."),
    (33, "33. Евх. Париж. Национ. б."),
    (34, "34. Сохранился в рукописи"),
]

parsed_notes = {}
for i in range(len(note_heads)):
    num, head = note_heads[i]
    # find head
    idx = raw_text.find(head)
    if idx == -1:
        # try without non-breaking space
        head_alt = head.replace("\u00a0", " ")
        idx = raw_text.find(head_alt)
    if idx == -1:
        print(f"Error finding note {num} with head '{head}'")
        continue
    
    if i + 1 < len(note_heads):
        next_num, next_head = note_heads[i+1]
        next_idx = raw_text.find(next_head)
        if next_idx == -1:
            next_idx = raw_text.find(next_head.replace("\u00a0", " "))
        note_body = raw_text[idx:next_idx].strip()
    else:
        note_body = raw_text[idx:end_34].strip()
    
    # Clean up whitespace
    lines = [l.strip() for l in note_body.splitlines() if l.strip()]
    cleaned = " ".join(lines)
    parsed_notes[num] = cleaned
    print(f"=== NOTE {num} ===")
    print(cleaned)
    print()

out_file = Path("scratch/cohort34_russian_notes_clean.txt")
with open(out_file, "w", encoding="utf-8") as f:
    for num in sorted(parsed_notes.keys()):
        f.write(f"[{num}] {parsed_notes[num]}\n\n")
