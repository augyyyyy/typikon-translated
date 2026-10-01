#!/usr/bin/env python3
"""
Insert 10 Concelebration & Liturgical Diagrams into Final MD/Final_Dolnytsky_appendix.md
Preserves exact CRLF newlines.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

proj_root = Path(r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation")
app_path = proj_root / "Final MD" / "Final_Dolnytsky_appendix.md"

with open(app_path, "r", encoding="utf-8", newline="") as f:
    content = f.read()

crlf = "\r\n" if "\r\n" in content else "\n"
p_sep = crlf + crlf

DIAGRAMS = [
    # 1. Entrance (Section 51 / point 2)
    (
        f"recites the Prayer of the Entrance himself (see no. 34){p_sep}After the call of the Deacon",
        f"recites the Prayer of the Entrance himself (see no. 34){p_sep}"
        f"[Diagram: At the Entrance]{crlf}"
        f"[Left Column] 6 ... 4 ... 2{crlf}"
        f"[Center] C (Celebrant) | D (Deacon){crlf}"
        f"[Right Column] 5 ... 3 ... 1{p_sep}"
        f"After the call of the Deacon"
    ),
    # 2. Narthex (Section 71 / point 2)
    (
        f"The Deacon or deacons stand near the principal celebrant{p_sep}If only one deacon censes",
        f"The Deacon or deacons stand near the principal celebrant{p_sep}"
        f"[Diagram: At the Narthex]{crlf}"
        f"[Left Column] Candle-bearer ... 6 ... 4 ... 2{crlf}"
        f"[Center] Celebrant ... Deacon{crlf}"
        f"[Right Column] Candle-bearer ... 5 ... 3 ... 1 ... Concelebrants{p_sep}"
        f"If only one deacon censes"
    ),
    # 3. Blessing of Loaves (Section 72 / point 3)
    (
        f"3. At the blessing of loaves, the concelebrants are arranged thus:{p_sep}After the blessing of loaves",
        f"3. At the blessing of loaves, the concelebrants are arranged thus:{p_sep}"
        f"[Diagram: At the Blessing of Loaves]{crlf}"
        f"[Left Column] Candle-bearer ... Concelebrants ... 6 ... 4 ... 2{crlf}"
        f"[Center] TETRAPOD{crlf}"
        f"[Right Column] Candle-bearer ... Concelebrants ... 5 ... 3 ... 1{crlf}"
        f"[Bottom] Celebrant ... Deacon{p_sep}"
        f"After the blessing of loaves"
    ),
    # 4. Magnification (Section 94 / point 1)
    (
        f"and to his right – the Deacon{p_sep}2. Then all sing the Magnification.",
        f"and to his right – the Deacon{p_sep}"
        f"[Diagram: At the Magnification]{crlf}"
        f"[Left Column] Candle-bearer ... 6 ... 4 ... 2 ... Concelebrants{crlf}"
        f"[Center] TETRAPOD{crlf}"
        f"[Right Column] Candle-bearer ... 5 ... 3 ... 1 ... Concelebrants{crlf}"
        f"[Bottom] Celebrant ... Deacon{p_sep}"
        f"2. Then all sing the Magnification."
    ),
    # 5. Paschal Matins Church Doors
    (
        f"In the narthex all stand before the closed church doors.{p_sep}Here the principal celebrant takes the censer",
        f"In the narthex all stand before the closed church doors, as in the diagram below:{p_sep}"
        f"[Diagram: At the Church Doors]{crlf}"
        f"Church doors{crlf}"
        f"___________I_______I___________{crlf}"
        f"Left Kliros ...................................... Right Kliros{crlf}"
        f"A2 ..................................................... A1{crlf}"
        f"C4 ..................................................... C3{crlf}"
        f"C2 ..................................................... C1{crlf}"
        f"D2                     PC                    D1{crlf}"
        f"People{p_sep}"
        f"Here the principal celebrant takes the censer"
    ),
    # 6. Proskomedia Lamb (Section 108 / point 12)
    (
        f'saying: "One of the soldiers."{p_sep}13. The Deacon, having taken wine and water',
        f'saying: "One of the soldiers."{p_sep}'
        f"[Diagram of the Lamb]{crlf}"
        f"/ IC | XC{crlf}"
        f"-----+---{crlf}"
        f"  NI | KA{p_sep}"
        f"13. The Deacon, having taken wine and water"
    ),
    # 7. Little Entrance (Two Deacons, Section 152 / point 6)
    (
        f'the Priest stands in the middle behind them{p_sep}The first Deacon says: "Let us pray to the Lord,"',
        f'the Priest stands in the middle behind them{p_sep}'
        f"[Diagram: At the Little Entrance]{crlf}"
        f"[Left Column] 6 ... 4 ... 2{crlf}"
        f"[Center] D.2 ... D.1 ... Priest{crlf}"
        f"[Right Column] 5 ... 3 ... 1{p_sep}"
        f'The first Deacon says: "Let us pray to the Lord,"'
    ),
    # 8. Before Little Entrance (Concelebration, Section 200 / point 9)
    (
        f'occupy their places near the holy table.{p_sep}10. The concelebrants sit near the High Throne',
        f'occupy their places near the holy table.{p_sep}'
        f"[Diagram: Before the Little Entrance, before the Holy Doors]{crlf}"
        f"[Left Column] Candle-bearer ... 6 ... 4 ... 2 ... Concelebrants{crlf}"
        f"[Right Column] Candle-bearer ... 5 ... 3 ... 1 ... Concelebrants{crlf}"
        f"[Bottom] Celebrant ... Deacon{p_sep}"
        f'10. The concelebrants sit near the High Throne'
    ),
    # 9. High Throne (Concelebration, Section 201 / point 10)
    (
        f'left side – sit to the left{p_sep}11. During the reading of the Gospel all remain in their places',
        f'left side – sit to the left{p_sep}'
        f"[Diagram: At the High Throne]{crlf}"
        f"[Left] 2 ... 4 ... 6{crlf}"
        f"[Center] D (High Place){crlf}"
        f"[Right] 1 ... 3 ... 5{p_sep}"
        f'11. During the reading of the Gospel all remain in their places'
    ),
    # 10. Concelebrants Communion (Section 209 / point 18)
    (
        f'Most Precious Blood from the principal celebrant{p_sep}19. Each, having just communicated',
        f'Most Precious Blood from the principal celebrant{p_sep}'
        f"[Diagram: Communion of the Body / Communion of the Blood]{crlf}"
        f"[Table of Oblation]{crlf}"
        f"4 3 | 4 3{crlf}"
        f"2 1 | 2 1{crlf}"
        f"[Holy Table]{crlf}"
        f"[Principal Celebrant] [Principal Celebrant]{p_sep}"
        f'19. Each, having just communicated'
    )
]

print(f"Initial Final MD/Final_Dolnytsky_appendix.md size: {len(content)} chars")
all_found = True
for idx, (target, repl) in enumerate(DIAGRAMS, 1):
    if target in content:
        print(f"Diagram {idx}: Target found!")
    else:
        print(f"Diagram {idx}: Target NOT found!")
        all_found = False

if all_found:
    for idx, (target, repl) in enumerate(DIAGRAMS, 1):
        content = content.replace(target, repl, 1)
    with open(app_path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print(f"\nAll 10 diagrams successfully inserted into {app_path.name}!")
    print(f"New length: {len(content)} chars")
else:
    print("\nAborting: not all targets were found.")
