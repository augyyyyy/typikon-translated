import sys
from pathlib import Path
import re

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

p = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort9_raw_draft.md")
txt = p.read_text(encoding="utf-8")

# Let's perform replacements for the archaic rubrical verbs
replacements = [
    (r"\bthe reader readeth\b", "the reader reads"),
    (r"\bthe deacon readeth\b", "the deacon reads"),
    (r"\bthe deacon maketh\b", "the deacon makes"),
    (r"\bthe deacon dismisseth\b", "the deacon dismisses"),
    (r"\bThe priest readeth\b", "The priest reads"),
    (r"\breadeth\b", "reads"),
    (r"\bbeginneth\b", "begins"),
    (r"\bmaketh\b", "makes"),
    (r"\bstandeth\b", "stands"),
    (r"\btaketh\b", "takes"),
    (r"\binstructeth\b", "instructs"),
    (r"\bFirst he shall utter thanksgiving\b", "First he offers thanksgiving"),
    (r"\bhe shall have a reward\b", "he receives a reward"),
]

new_txt = txt
for pat, rep in replacements:
    new_txt = re.sub(pat, rep, new_txt)

p.write_text(new_txt, encoding="utf-8")
print("Replacements complete.")
