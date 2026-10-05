from pathlib import Path

for path in [Path('Final/Final_Dolnytsky_part3_menaion.txt'), Path('Final MD/Final_Dolnytsky_part3_menaion.md')]:
    text = path.read_text(encoding='utf-8')
    text = text.replace('general rule of a Saint with All-Night Vigil[^277];', 'general rule of a Saint with All-Night Vigil;')
    text = text.replace('general rule of a Saint with All-Night Vigil[^277] on Sunday, only if', 'general rule of a Saint with All-Night Vigil on Sunday, only if')
    path.write_text(text, encoding='utf-8')
    c = text.count("[^277]")
    print(f"Cleaned {path.name}, count of [^277] is now: {c}")
