import sys
from pathlib import Path

# Set project root relative to this script
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Output files
source_file = PROJECT_ROOT / "Typikons" / "1899 Dolnytsky Typikon" / "Source Text" / "1899_dolnytsky_typikon_cohort29_source.txt"
draft_file = PROJECT_ROOT / "Typikons" / "1899 Dolnytsky Typikon" / "Draft" / "1899_dolnytsky_typikon_cohort29_raw_draft.md"
footnotes_file = PROJECT_ROOT / "Typikons" / "1899 Dolnytsky Typikon" / "Draft" / "1899_dolnytsky_typikon_cohort29_footnotes.txt"

print("Paths configured.")
