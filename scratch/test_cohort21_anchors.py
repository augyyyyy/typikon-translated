import sys, re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_text = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/cohort21_extracted_pdf_text.txt").read_text(encoding='utf-8')
epub_text = Path("scratch/cohort21_epub_clean.txt").read_text(encoding='utf-8')

# The leaf boundary points:
# p201: starts with "братом чередным"
# p202: starts with "сдержанным вздохом"
# p203: starts with "Египетские киновии по прп. Иоанну Кассиану"
# p204: starts with "Но, как замечено, наиболее выработанную практику"
# p205: starts with "полагали, что надо назначить еще больше того"
# p206: starts with "течения (excessum) нашей молитвы"
# p207: starts with "известными промежутками"
# p208: starts with "центров образованного христианства"
# p209: starts with "как ясное указание на то"
# p210: starts with "Начало новому типу монастырей"
# p211: starts with "имевшая такое же устройство"

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

for p, anchor in anchors:
    pos = epub_text.find(anchor)
    print(f"Leaf p{p}: anchor '{anchor[:30]}' found at pos {pos}")
    if pos == -1:
        print(f"   ERROR: anchor not found for p{p}!")
