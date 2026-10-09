import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

draft_path = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort17_raw_draft.md")
content = draft_path.read_text(encoding="utf-8")

# Replace the three violations:
content = content.replace(
    'There standeth the deacon, the common minister, crying aloud and saying: \'Let us attend\'; and this frequently... after him the lector beginneth: \'The prophecy of Isaiah\'; then',
    'There stands the deacon, the common minister, crying aloud and saying: \'Let us attend\'; and this frequently... after him the lector begins: \'The prophecy of Isaiah\'; then'
)

content = content.replace(
    'that the bishop ariseth not during the reading of the Gospel',
    'that the bishop does not rise during the reading of the Gospel'
)

content = content.replace(
    'Concerning the reading of the *Shepherd* in the churches Eusebius likewise maketh mention',
    'Concerning the reading of the *Shepherd* in the churches Eusebius likewise makes mention'
)

draft_path.write_text(content, encoding="utf-8")
print(f"Updated {draft_path}")
