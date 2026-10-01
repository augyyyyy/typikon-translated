#!/usr/bin/env python3
"""
Restore Liturgical Concelebration Diagrams in Appendix
======================================================
Restores the 10 liturgical concelebration diagrams recovered from the original
manuscript into their exact structural locations in Final_Dolnytsky_appendix.txt.
"""

from pathlib import Path
import re
import sys

def get_project_root() -> Path:
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "Final").exists():
            return parent
    return Path(__file__).resolve().parent.parent

DIAGRAMS = [
    # 1. Entrance (Section 51)
    (
        r'(51\. For the Entrance, all go out.*?behind all, and recites the Prayer of the Entrance himself \(see no\. 34\)\.)\n\n(After the call of the Deacon)',
        r'\1\n\n[Diagram: At the Entrance]\n[Left Column] 6 ... 4 ... 2\n[Center] C (Celebrant) | D (Deacon)\n[Right Column] 5 ... 3 ... 1\n\n\2'
    ),
    # 2. Narthex (Section 71)
    (
        r'(71\. Then, during the procession at the Litiya.*?The Deacon or deacons stand near the principal celebrant\.)\n\n(If only one deacon censes)',
        r'\1\n\n[Diagram: At the Narthex]\n[Left Column] Candle-bearer ... 6 ... 4 ... 2\n[Center] Celebrant ... Deacon\n[Right Column] Candle-bearer ... 5 ... 3 ... 1 ... Concelebrants\n\n\2'
    ),
    # 3. Blessing of Loaves (Section 72)
    (
        r'(72\. At the blessing of loaves, the concelebrants are arranged thus:)\n\n(After the blessing of loaves, all go in a double row)',
        r'\1\n\n[Diagram: At the Blessing of Loaves]\n[Left Column] Candle-bearer ... Concelebrants ... 6 ... 4 ... 2\n[Center] TETRAPOD\n[Right Column] Candle-bearer ... Concelebrants ... 5 ... 3 ... 1\n[Bottom] Celebrant ... Deacon\n\n\2'
    ),
    # 4. Magnification (Section 94)
    (
        r'(all stand on the sides of the tetrapod in two rows, facing one another, the principal celebrant stands in the middle before the tetrapod, and to his right - the deacon\.)\n\n(95\. Then all sing the Magnification\.)',
        r'\1\n\n[Diagram: At the Magnification]\n[Left Column] Candle-bearer ... 6 ... 4 ... 2 ... Concelebrants\n[Center] TETRAPOD\n[Right Column] Candle-bearer ... 5 ... 3 ... 1 ... Concelebrants\n[Bottom] Celebrant ... Deacon\n\n\2'
    ),
    # 5. Paschal Matins: Church doors
    (
        r'(In the narthex all stand before the closed church doors, as in the diagram below:)\n\n(Here the principal celebrant takes the censer)',
        r'\1\n\n[Diagram: At the Church Doors]\nChurch doors\n___________I_______I__________\nLeft Kliros ...................................... Right Kliros\nA2 ..................................................... A1\nC4 ..................................................... C3\nC2 ..................................................... C1\nD2                     PC                    D1\nPeople\n\n\2'
    ),
    # 6. Proskomedia Lamb (Section 108)
    (
        r'(saying: "One of the soldiers\."\s*)\n\n(109\. The deacon, having taken wine and water)',
        r'\1\n\n[Diagram of the Lamb]\nIC | XC\n---+---\nNI | KA\n\n\2'
    ),
    # 7. Little Entrance (Section 194)
    (
        r'(194\. On the Little Entrance all go out, having lowered their hands.*?in front - the younger ones\.)\n\n(Before the holy doors all stand)',
        r'\1\n\n[Diagram: At the Little Entrance]\n[Left Column] 6 ... 4 ... 2\n[Center] D.2 ... D.1 ... Priest\n[Right Column] 5 ... 3 ... 1\n\n\2'
    ),
    # 8. Before Little Entrance (Section 194/195)
    (
        r'(All stand in two rows, in front - the younger ones, facing the people\.)\n\n(195\. At "Wisdom, arise" all enter)',
        r'\1\n\n[Diagram: Before the Little Entrance, before the Holy Doors]\n[Left Column] Candle-bearer ... 6 ... 4 ... 2 ... Concelebrants\n[Right Column] Candle-bearer ... 5 ... 3 ... 1 ... Concelebrants\n[Bottom] Celebrant ... Deacon\n\n\2'
    ),
    # 9. High Throne (Section 197)
    (
        r'(It befits him to sit on the southern side\.)\n\n(198\. The other concelebrants sit)',
        r'\1\n\n[Diagram: At the High Throne]\n[Left] 2 ... 4 ... 6\n[Center] D (High Place)\n[Right] 1 ... 3 ... 5\n\n\2'
    ),
    # 10. Communion of Body and Blood (Section 207)
    (
        r'(approach and in the same manner commune of the Holy Blood\.)\n\n(208\. The principal celebrant, having said)',
        r'\1\n\n[Diagram: Communion of the Body / Communion of the Blood]\n[Table of Oblation]\n4  3  |  4  3\n2  1  |  2  1\n[Holy Table]\n[Principal Celebrant]\n\n\2'
    )
]

def main():
    root = get_project_root()
    app_path = root / "Final" / "Final_Dolnytsky_appendix.txt"
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()

    inserted_count = 0
    for i, (pat_str, rep_str) in enumerate(DIAGRAMS, 1):
        pat = re.compile(pat_str, re.DOTALL)
        if pat.search(content):
            content = pat.sub(rep_str, content)
            inserted_count += 1
            print(f"  Diagram {i}: Successfully inserted.")
        else:
            print(f"  Diagram {i}: Match not found (already inserted or pattern mismatch).")

    with open(app_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nTotal diagrams inserted: {inserted_count} / {len(DIAGRAMS)}")

if __name__ == "__main__":
    main()
