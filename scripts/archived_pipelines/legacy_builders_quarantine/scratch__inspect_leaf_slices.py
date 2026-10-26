import sys, re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

epub_text = Path("scratch/cohort21_epub_clean.txt").read_text(encoding='utf-8')

anchors = [
    (201, "братом чередным"),
    (202, "сдержанным вздохом"),
    (203, "Египетские киновии по прп. Иоанну Кассиану"),
    (204, "Но, как замечено, наиболее выработанную практику"),
    (205, "полагали, что надо назначить еще больше того"),
    (206, "течения (excessum) нашей молитвы"),
    (207, "известными промежутками"),
    (208, "центров образованного христианства"),
    (209, "как ясное указание на то"),
    (210, "Начало новому типу монастырей"),
]

positions = [epub_text.find(a[1]) for a in anchors]
positions.append(len(epub_text))

for i in range(len(anchors)):
    p = anchors[i][0]
    start = positions[i]
    end = positions[i+1]
    leaf_slice = epub_text[start:end].strip()
    fns = re.findall(r'\[(\d+)\]', leaf_slice)
    orig_pages = re.findall(r'\{с\.\s*\d+\}', leaf_slice)
    print(f"=== LEAF p{p} === (len: {len(leaf_slice)}, fns: {fns}, orig_pages: {orig_pages})")
    lines = leaf_slice.splitlines()
    print("   FIRST 200 chars:", leaf_slice[:200].replace('\n', ' '))
    print("   LAST 200 chars: ", leaf_slice[-200:].replace('\n', ' '))
