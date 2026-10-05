from pathlib import Path

for path in [Path('Final/Final_Dolnytsky_part2_general_rubrics.txt'), Path('Final MD/Final_Dolnytsky_part2_general_rubrics.md')]:
    text = path.read_text(encoding='utf-8')
    
    # 1. Remove premature [^112] from Chapter 2 Vespers Troparia
    text = text.replace('troparion and day of the week[^112].', 'troparion and day of the week.')
    text = text.replace('troparion and of the day of the week[^112].\n\n   * *If two saints', 'troparion and of the day of the week.\n\n   * *If two saints')
    text = text.replace('troparion and of the day of the week[^112].\n   * *If two saints', 'troparion and of the day of the week.\n   * *If two saints')
    
    # 2. Remove premature [^196] from Chapter 2 Compline
    text = text.replace('first of the day[^196], then of the Temple', 'first of the day, then of the Temple')
    
    # 3. Remove premature [^115] from Chapter 2 Liturgy
    text = text.replace('Theotokion/Kontakion of the Temple[^115].', 'Theotokion/Kontakion of the Temple.')
    text = text.replace('Theotokion of the Temple[^115].', 'Theotokion of the Temple.')

    path.write_text(text, encoding='utf-8')
    print(f"Cleaned {path.name}")
