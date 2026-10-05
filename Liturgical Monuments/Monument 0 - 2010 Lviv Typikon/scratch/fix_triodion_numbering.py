import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

md_path = Path('Final MD/Final_Dolnytsky_part4_triodion.md')
lines = md_path.read_text(encoding='utf-8').splitlines()

# 1. Line 93: Fix Meatfare Saturday Vespers
for i, l in enumerate(lines):
    if l.startswith('5. At the end: Troparion for the dead'):
        print(f"Fixing Meatfare Saturday Vespers at line {i+1}")
        lines[i] = "6. At the end: Troparion for the dead (\"By the depth of wisdom\"), Glory, Both now: Theotokion"
        lines[i+2] = "7. \"Have mercy on us, O God\", dismissal for the dead and \"In blessed falling asleep\"."
        break

# 2. Line 262: Fix 1st Hour Lenten
for i, l in enumerate(lines):
    if l.startswith('5.\t"Lord, have mercy" (40)'):
        print(f"Fixing 1st Hour Lenten at line {i+1}")
        lines[i] = "5. \"Lord, have mercy\" (40), \"Thou Who at all times\" and the rest with the prostrations."
        lines[i+2] = "6. Trisagion with \"Our Father\", \"For Thine is the Kingdom\" and \"Lord, have mercy\" (12)"
        lines[i+4] = "7. Final prayer: at the 1st Hour – \"O Christ, the True Light\", and at the others – their proper ones"
        lines[i+6] = "8. \"Glory to Thee, O Christ God\" and the rest and dismissal."
        break

# 3. Line 346: Fix Praises of Fathers
for i, l in enumerate(lines):
    if l.startswith('4.\t4 Stichera of the Praises of the Fathers'):
        print(f"Fixing Praises of Fathers at line {i+1}")
        lines[i] = "4. 4 Stichera of the Praises of the Fathers, Glory: of the Fathers, Both now: Theotokion"
        lines[i+2] = "5. **After the Great Doxology:** Troparion to the Fathers, Glory, Both now: Theotokion from the Sunday ones in the tone of the [Troparion of] the Fathers"
        lines[i+4] = "6. **Dismissal:** Great Dismissal with commemoration of the Fathers"
        break

# 4. Line 492: Fix 6th Hour Lenten
for i, l in enumerate(lines):
    if l.startswith('6.\t"Lord, have mercy" (40)'):
        print(f"Fixing 6th Hour Lenten at line {i+1}")
        lines[i] = "6. \"Lord, have mercy\" (40), \"Thou Who at all times\" and the rest with the prostrations."
        lines[i+2] = "7. Trisagion with 3 prostrations, and after \"Our Father\" – the exclamation \"For Thine is the Kingdom\" and \"Lord, have mercy\" (12)"
        lines[i+4] = "8. Final prayer of the Hour and \"Glory to Thee, O Christ God\", dismissal of the 1st Hour (or of the other Hours – their proper ones)"
        break

# 5. Line 568: Fix Typika Lenten conclusion
for i, l in enumerate(lines):
    if l.startswith('Trisagion with prostrations and, after "Our Father"'):
        print(f"Fixing Typika Lenten conclusion at line {i+1}")
        lines[i] = "10. Trisagion with prostrations and, after \"Our Father\", – \"Lord, have mercy\" (12) and prayer \"All-Holy Trinity\"."
        lines[i+2] = "11. \"O All-holy Trinity\" and \"Blessed be the name of the Lord\" (3) with prostrations."
        lines[i+4] = "12. Glory, Both now: Psalm \"I will bless the Lord\""
        lines[i+6] = "13. *“It is truly meet”* and a prostration; Glory, Both now: \"Lord, have mercy\" (2), \"Lord, bless\"."
        break

# 6. Line 758: Fix 17th Kathisma & Canons
for i, l in enumerate(lines):
    if l.startswith('4.\t17th Kathisma ("The Blameless")'):
        print(f"Fixing 17th Kathisma at line {i+1}")
        lines[i] = "4. 17th Kathisma (\"The Blameless\"), in two stations, with refrains and troparia"
        lines[i+2] = "5. **Canons:** *Distribution:* Canons 3 on 14: of the Temple of the Lord or Theotokos with heirmos on 6, of the Saint of the *Menaion* on 4 and of the *Triodion* on 4"
        break

# 7. Line 1232: Fix Praises & It is a good thing
for i, l in enumerate(lines):
    if "5. **Praises (Lauds):** 4 and, after the Small Doxology" in l:
        print(f"Fixing Praises and It is a good thing at line {i+1}")
        lines[i] = "6. **Praises (Lauds):** Stichera of the Praises – 4 and, after the Small Doxology, – \"Let us complete\"."
        lines[i+2] = "7. \"It is a good thing\" once, Trisagion with \"Our Father\" and Troparion \"When the glorious disciples\", without Theotokion."
        lines[i+4] = "8. Priest: \"Wisdom\"; Choir: \"Bless\""
        break

# 8. Line 1324: Fix Passion Gospels Aposticha
for i, l in enumerate(lines):
    if l.startswith('10.\t"To Thee belongs glory"'):
        print(f"Fixing Passion Gospels at line {i+1}")
        lines[i] = "10. \"To Thee belongs glory\"[^595], \"Glory to Thee Who Hast shown us the light\"."
        lines[i+2] = "11. Litany \"Let us complete\" and, after the exclamation \"For Thou Art a merciful [God]\"[^596], immediately – the eleventh Gospel"
        lines[i+4] = "12. **Aposticha:** Aposticha and the twelfth Gospel"
        lines[i+6] = "13. \"It is a good thing\", Trisagion, \"Our Father\", Troparion of Friday \"Thou Hast redeemed\"."
        break

# 9. Line 1378: Fix Shroud procession
for i, l in enumerate(lines):
    if l.startswith('4.\t"Let us all say", "Vouchsafe", "Let us complete"'):
        print(f"Fixing Shroud procession at line {i+1}")
        lines[i] = "4. \"Let us all say\", \"Vouchsafe\", \"Let us complete\" and Aposticha of the *Triodion*."
        lines[i+2] = "5. At the last sticheron of the Aposticha, that is at \"Thee, Who Art clothed with light\", takes place the procession with the Shroud and the placing of it on the Tomb"
        break

# 10. Line 1592: Fix Bright Saturday Vespers
for i, l in enumerate(lines):
    if l.startswith('3.\t*“Lord, I have cried”* – in Tone 2'):
        print(f"Fixing Bright Saturday Vespers at line {i+1}")
        lines[i] = "3. *“Lord, I have cried”* – in Tone 2, with the usual censing. Stichera – Resurrectional 3 and of the *Triodion* 4; Glory: of the *Triodion*, Both now: 1st Theotokion of the current Tone 2 (Dogmatikon)."
        lines[i+2] = "4. **Entrance:** Entrance with the Gospel and usual censing at \"O Gladsome Light\"; and, after the Great Prokimenon, the Deacon, and if there is none, the Priest exclaims: \"Wisdom!\", and the reading from Genesis begins, and other readings"
        lines[i+4] = "5. \"Let us all say\", \"Vouchsafe\" and \"Let us complete\"."
        lines[i+6] = "6. At the Aposticha: one Resurrection Sticheron of the *Octoechos*, given in the Pentecostarion, and then the Paschal Stichera: \"Let God arise\" with their refrains"
        break

md_path.write_text('\n'.join(lines), encoding='utf-8')
print("Successfully fixed all Triodion list numbering defects!")
