import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def clean_paragraph(p_text):
    # normalize spaces and line breaks inside paragraph
    lines = [l.strip() for l in p_text.splitlines() if l.strip()]
    return " ".join(lines)

def process_leaf(raw_text):
    raw_text = raw_text.replace('\xa0', ' ')
    # Split by double newline or empty lines
    # Notice that headings are short lines followed by text, or paragraphs
    lines = raw_text.splitlines()
    paragraphs = []
    current = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append(" ".join(current))
                current = []
        else:
            # Check if line looks like an independent heading or page marker
            if stripped.startswith('{с.') or stripped.startswith('{c.'):
                if current:
                    paragraphs.append(" ".join(current))
                    current = []
                paragraphs.append(stripped)
            elif stripped in [
                "Величина перикоп", "Праздничные чтения", "Лекционарии",
                "Церемониальная сторона чтений", "Читавшие лица",
                "Возглас «Мир всем»", "Призывы к вниманию и тишине", "Вонмем",
                "Обряды чтения", "Чтение неканонических книг",
                "Проповедь", "Время проповеди", "Проповедовавшие лица."
            ]:
                if current:
                    paragraphs.append(" ".join(current))
                    current = []
                paragraphs.append(stripped)
            else:
                current.append(stripped)
    if current:
        paragraphs.append(" ".join(current))
    
    # Return formatted leaf text
    return "\n\n".join(paragraphs)

output_parts = []
for p in range(161, 171):
    raw = Path(f"scratch/leaf_texts/p{p}.txt").read_text(encoding="utf-8")
    leaf_body = process_leaf(raw)
    output_parts.append(f"=== LEAF p{p} ===\n{leaf_body}")

full_source = "\n\n".join(output_parts) + "\n"
target = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/1910_skaballanovich_typikon_cohort17_source.txt")
target.write_text(full_source, encoding="utf-8")
print(f"Wrote {len(full_source)} chars to {target}")
