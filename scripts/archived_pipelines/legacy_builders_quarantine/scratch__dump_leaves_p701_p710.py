from pathlib import Path

out = []
for pno in range(701, 711):
    f = Path(f'scratch/cohort71_extracted/p{pno}.txt')
    out.append(f"==================== LEAF p{pno} ====================\n")
    out.append(f.read_text(encoding='utf-8'))
    out.append("\n\n")

Path('scratch/cohort71_raw_text.txt').write_text("".join(out), encoding='utf-8')
print("Successfully written cohort71_raw_text.txt in UTF-8")
