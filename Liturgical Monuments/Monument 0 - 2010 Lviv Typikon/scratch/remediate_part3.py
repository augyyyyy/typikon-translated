import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parent.parent

txt_path = root / 'Final/Final_Dolnytsky_part3_menaion.txt'
md_path = root / 'Final MD/Final_Dolnytsky_part3_menaion.md'

txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

print("Applying Part 3 remediations...")

# 1. FN 300
old_txt_300 = 'on the 3rd and 9th - of the Forefeast.\n'
new_txt_300 = 'on the 3rd and 9th - of the Forefeast[^300].\n'
assert old_txt_300 in txt
txt = txt.replace(old_txt_300, new_txt_300, 1)

old_md_300 = 'on the 3rd and 9th – of the Forefeast.\n'
new_md_300 = 'on the 3rd and 9th – of the Forefeast[^300].\n'
assert old_md_300 in md
md = md.replace(old_md_300, new_md_300, 1)

# 2. FN 320 (in TXT)
assert 'up to "O come, let us worship" inclusive. Deacons,' in txt
txt = txt.replace('up to "O come, let us worship" inclusive. Deacons,',
                  'up to "O come, let us worship" inclusive[^320]. Deacons,', 1)

# 3. FN 338
old_txt_338 = '14.\tCommunion Hymn "Praise the Lord" and of the Feast.\n'
new_txt_338 = '14.\tCommunion Hymn "Praise the Lord" and of the Feast[^338].\n'
assert old_txt_338 in txt
txt = txt.replace(old_txt_338, new_txt_338, 1)

old_md_338 = '3. Communion Hymn "Praise the Lord" and of the Feast\n\n---\n\n## 3.5 January'
new_md_338 = '3. Communion Hymn "Praise the Lord" and of the Feast[^338]\n\n---\n\n## 3.5 January'
assert old_md_338 in md
md = md.replace(old_md_338, new_md_338, 1)

# 4. FN 339
assert 'already given in the Pochaiv Anthologion of 1777. We will present' in txt
txt = txt.replace('already given in the Pochaiv Anthologion of 1777. We will present',
                  'already given in the Pochaiv Anthologion of 1777[^339]. We will present', 1)

assert 'already given in the Pochaiv *Anthologion* of 1777. We will present' in md
md = md.replace('already given in the Pochaiv *Anthologion* of 1777. We will present',
                'already given in the Pochaiv *Anthologion* of 1777[^339]. We will present', 1)

# 5. FN 345
old_txt_345 = '3.\tCommunion Hymn "Praise the Lord" and of the Saint.\n'
new_txt_345 = '3.\tCommunion Hymn "Praise the Lord" and of the Saint[^345].\n'
assert old_txt_345 in txt
txt = txt.replace(old_txt_345, new_txt_345, 1)

old_md_345 = '3. Communion Hymn "Praise the Lord" and of the Saint\n'
new_md_345 = '3. Communion Hymn "Praise the Lord" and of the Saint[^345]\n'
assert old_md_345 in md
md = md.replace(old_md_345, new_md_345, 1)

# 6. FN 359
old_txt_359 = '3.\tCommunion Hymn "Praise the Lord" and of the Feast.\n'
new_txt_359 = '3.\tCommunion Hymn "Praise the Lord" and of the Feast[^359].\n'
assert old_txt_359 in txt
txt = txt.replace(old_txt_359, new_txt_359, 1)

old_md_359 = 'Communion Hymn "Praise the Lord" and of the Feast\n\n### 3.5.8 January: Our Venerable Father Theodosius'
new_md_359 = 'Communion Hymn "Praise the Lord" and of the Feast[^359]\n\n### 3.5.8 January: Our Venerable Father Theodosius'
assert old_md_359 in md
md = md.replace(old_md_359, new_md_359, 1)

# 7. FN 360 (in MD)
old_md_360 = 'at the decision of the Ecclesiarch.\n'
new_md_360 = 'at the decision of the Ecclesiarch[^360].\n'
assert old_md_360 in md
md = md.replace(old_md_360, new_md_360, 1)

# 8. FN 362
old_txt_362 = 'according to the general rule of a Saint with All-Night Vigil; it departs from the general rule'
new_txt_362 = 'according to the general rule of a Saint with All-Night Vigil[^362]; it departs from the general rule'
assert old_txt_362 in txt
txt = txt.replace(old_txt_362, new_txt_362, 1)

old_md_362 = 'according to the general rule of a Saint with All-Night Vigil; it departs from the general rule'
new_md_362 = 'according to the general rule of a Saint with All-Night Vigil[^362]; it departs from the general rule'
assert old_md_362 in md
md = md.replace(old_md_362, new_md_362, 1)

# 9. FN 370
old_txt_370 = '1.\tKathisma is sequential.\n'
new_txt_370 = '1.\tKathisma is sequential[^370].\n'
assert old_txt_370 in txt
txt = txt.replace(old_txt_370, new_txt_370, 1)

old_md_370 = '1. **Kathisma:** "is sequential\n'
new_md_370 = '1. **Kathisma:** Kathisma is sequential[^370].\n'
assert old_md_370 in md
md = md.replace(old_md_370, new_md_370, 1)

# 10. FN 379
old_txt_379 = 'Communion Hymn "Praise the Lord" and of the Feast \n'
new_txt_379 = 'Communion Hymn "Praise the Lord" and of the Feast[^379].\n'
assert old_txt_379 in txt
txt = txt.replace(old_txt_379, new_txt_379, 1)

old_md_379 = 'Communion Hymn "Praise the Lord" and of the Feast\n\n#### II. APODOSIS OF THE MEETING'
new_md_379 = 'Communion Hymn "Praise the Lord" and of the Feast[^379].\n\n#### II. APODOSIS OF THE MEETING'
assert old_md_379 in md
md = md.replace(old_md_379, new_md_379, 1)

# 11. FN 388 (in MD)
old_md_388 = '*“It is truly meet”* and Dismissal\n'
new_md_388 = '*“It is truly meet”* and Dismissal[^388].\n'
assert old_md_388 in md
md = md.replace(old_md_388, new_md_388, 1)

# 12. FN 392 (in MD)
old_md_392 = '### 3.7.2 March: Forefeast of the Annunciation\n'
new_md_392 = '### 3.7.2 March: Forefeast of the Annunciation[^392]\n'
assert old_md_392 in md
md = md.replace(old_md_392, new_md_392, 1)

# 13. FN 393 (in MD)
old_md_393 = 'RULES FOR THE ABOVE-MENTIONED CASES\n\nFOREFEAST OF THE ANNUNCIATION'
new_md_393 = 'RULES FOR THE ABOVE-MENTIONED CASES[^393]\n\nFOREFEAST OF THE ANNUNCIATION'
assert old_md_393 in md
md = md.replace(old_md_393, new_md_393, 1)

# 14. FN 406 (Restoring Case 4 from DOCX)
old_txt_406 = '''4. ANNUNCIATION ON WEDNESDAY OF THE VENERATION OF THE CROSS
This service has been removed since, in our rite, with the permission of the Apostolic See of the 9 Fridays before Easter, all daily services in the Lenten period have been abolished, with the exception of the service on the 1st week.'''

new_txt_406 = '''4. ANNUNCIATION ON WEDNESDAY OF THE VENERATION OF THE CROSS
The Service of the Archangel is sung on another day or at Compline. The service of the Wednesday of the Veneration of the Cross and of the Feast we sing according to the general Lenten rule, only:
AT VESPERS WITH THE SERVICE OF CHRYSOSTOM
On Tuesday evening
At "Lord, I have cried" - 10 stichera: 6 of the Triodion and 4 of the Feast, Glory: of the Triodion, Both now: of the Feast.
After the Entrance - 2 readings of the Triodion with their prokeimena and 2 first of the 5 of the Feast, which are given at yesterday's Vespers, and also the Small Litany with the exclamation of the Trisagion, and from here the Service of Chrysostom.
AT COMPLINE: According to the rule given here on p. 254 [→REF:p254].
AT MATINS
Canons 2 making 10: of the Feast on 6 and of the Cross on 4, and where there is a three-ode canon, there will be 4 canons on 14, that is of the Feast on 4, of the Cross on 2 and 2 three-ode canons on 8; also Katavasia - heirmos of the three-ode canon[^406]. After the 3rd ode - Kontakion-Ikos of the Feast and Sessional hymn of the Cross, Glory, and now: of the Feast; after the 6th - Kontakion-Ikos of the Cross; at the 9th - "More honorable"; after the 9th - Triadikon Exaposteilarion.
At "The Praises" and at the Aposticha: stichera of the Triodion, only at "The Praises" - Glory, and now: of the Feast.'''

assert old_txt_406 in txt
txt = txt.replace(old_txt_406, new_txt_406, 1)

old_md_406 = '''4. ANNUNCIATION ON WEDNESDAY OF THE VENERATION OF THE CROSS

This service has been removed since, in our rite, with the permission of the Apostolic See of the 9 Fridays before Easter, all daily services in the Lenten period have been abolished, with the exception of the service on the 1st week.'''

new_md_406 = '''4. ANNUNCIATION ON WEDNESDAY OF THE VENERATION OF THE CROSS

The Service of the Archangel is sung on another day or at Compline. The service of the Wednesday of the Veneration of the Cross and of the Feast we sing according to the general Lenten rule, only:

##### At Vespers with the Service of Chrysostom

On Tuesday evening

1. **On *"Lord, I have cried"*:* 10 stichera: 6 of the *Triodion* and 4 of the Feast, Glory: of the *Triodion*, Both now: of the Feast.
2. After the Entrance – 2 readings of the *Triodion* with their prokeimena and 2 first of the 5 of the Feast, which are given at yesterday's Vespers, and also the Small Litany with the exclamation of the Trisagion, and from here the Service of Chrysostom.

##### At Compline

According to the rule given here on p. 254 [→REF:p254].

##### At Matins

1. **Canons:** Canons 2 making 10: of the Feast on 6 and of the Cross on 4, and where there is a three-ode canon, there will be 4 canons on 14, that is of the Feast on 4, of the Cross on 2 and 2 three-ode canons on 8; also Katavasia – heirmos of the three-ode canon[^406]. After the 3rd ode – Kontakion-Ikos of the Feast and Sessional hymn of the Cross, Glory, and now: of the Feast; after the 6th – Kontakion-Ikos of the Cross; at the 9th – "More honorable"; after the 9th – Triadikon Exaposteilarion.
2. **Praises & Aposticha:** At "The Praises" and at the Aposticha: stichera of the *Triodion*, only at "The Praises" – Glory, and now: of the Feast.'''

assert old_md_406 in md
md = md.replace(old_md_406, new_md_406, 1)

# 15. FN 438
old_txt_438 = '1.\tResurrectional Troparion, of the Fathers and of the Apostle; Kontakion of the Fathers, Glory: of the Apostle, Both now: of the Ascension.\n'
new_txt_438 = '1.\tResurrectional Troparion, of the Fathers and of the Apostle; Kontakion of the Fathers, Glory: of the Apostle, Both now: of the Ascension[^438].\n'
assert old_txt_438 in txt
txt = txt.replace(old_txt_438, new_txt_438, 1)

old_md_438 = '1. Resurrectional Troparion, of the Fathers and of the Apostle; Kontakion of the Fathers, Glory: of the Apostle, Both now: of the Ascension\n'
new_md_438 = '1. Resurrectional Troparion, of the Fathers and of the Apostle; Kontakion of the Fathers, Glory: of the Apostle, Both now: of the Ascension[^438].\n'
assert old_md_438 in md
md = md.replace(old_md_438, new_md_438, 1)

# 16. FN 444
old_txt_444 = 'ON THE CO-SUFFERING OF THE MOST HOLY THEOTOKOS \n'
new_txt_444 = 'ON THE CO-SUFFERING OF THE MOST HOLY THEOTOKOS[^444]\n'
assert old_txt_444 in txt
txt = txt.replace(old_txt_444, new_txt_444, 1)

old_md_444 = 'ON THE CO-SUFFERING OF THE MOST HOLY THEOTOKOS\n'
new_md_444 = 'ON THE CO-SUFFERING OF THE MOST HOLY THEOTOKOS[^444]\n'
assert old_md_444 in md
md = md.replace(old_md_444, new_md_444, 1)

# 17. FN 450 (in MD)
old_md_450 = '### 3.11.5 July: Forefeast of the Procession of the Precious Cross\n'
new_md_450 = '### 3.11.5 July: Forefeast of the Procession of the Precious Cross[^450]\n'
assert old_md_450 in md
md = md.replace(old_md_450, new_md_450, 1)

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully written Part 3 remediations!")
