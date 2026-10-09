import sys
from pathlib import Path

source_parts = []
for pno in range(651, 661):
    txt = Path(f'scratch/cohort66_extracted/p{pno}.txt').read_text(encoding='utf-8').strip()
    source_parts.append(f"=== LEAF p{pno} ===\n" + txt)

out_text = "\n\n".join(source_parts) + "\n"

target_file = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/1910_skaballanovich_typikon_cohort66_source.txt")
target_file.parent.mkdir(parents=True, exist_ok=True)
target_file.write_text(out_text, encoding="utf-8")
print(f"Wrote {len(out_text)} characters to {target_file}")
