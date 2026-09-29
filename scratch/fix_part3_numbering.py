import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def fix_part3_md_numbering():
    md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
    md = md_path.read_text(encoding='utf-8')

    # 1. Fix Renovation on Sunday (L249-255)
    target1 = """3.\t3 readings to the Renovation.

3. At the Aposticha – Resurrectional stichera; Glory: to the Renovation, Both now: of the Forefeast

4. After the Trisagion – Resurrectional Troparion, Glory: to the Renovation, Both now: of the Forefeast

5. **Dismissal:** Great Dismissal with Resurrectional commemoration"""

    replacement1 = """3. **Readings:** 3 readings to the Renovation.

4. **Aposticha:** At the Aposticha – Resurrectional stichera; Glory: to the Renovation, Both now: of the Forefeast

5. **Troparia:** After the Trisagion – Resurrectional Troparion, Glory: to the Renovation, Both now: of the Forefeast

6. **Dismissal:** Great Dismissal with Resurrectional commemoration"""

    assert target1 in md, "Target 1 not found in MD"
    md = md.replace(target1, replacement1)

    # 2. Fix Nativity/Theophany Eve Vespers (L1150-1165)
    target2 = """The Priest, having put on an epitrachelion and having gone out before the Holy Doors, bows low and begins the usual: "Blessed is our God". Choirs: "Amen", also "Glory to Thee, our God, glory to Thee", "O Heavenly King" and the rest with the Trisagion and "Our Father" up to "O come, let us worship" inclusive. Deacons, if there be [any], go out with the Priest before the Holy Doors and the right one of them exclaims: "Bless, Master", and the Priest: "Blessed is our God"[^323]

During the introductory Psalm the Priest, standing before the Holy Doors, says the evening prayers, as usual, and the deacons stand beside him and, at the end of the Psalm, one of them (the right) sings the Great Litany, and the Priest – its exclamation, and then, all bow low and withdraw to the sanctuary. If there be no deacons, then the Priest himself sings the litany

3.	*“Blessed is the man”* and the Small Litany, for which the second deacon goes out before the Holy Doors, and the Priest – the exclamation from his place. If there be no deacon, then the Priest himself, according to local custom, reads the litany quietly, sitting in his place, and the Choir sings its responses.

4. **On *"Lord, I have cried"*:* usual censing, which the Priest or deacons, if there be [any], perform; stichera on 8, "Glory, Both now" from the Heirmologion or according to the tone of the idiomesa

At "Glory, Both now" – Entrance with the Gospel, which the first deacon carries, if there be one, and the second precedes him with the censer; the Priest says the usual Prayer of the Entrance, as at Vespers, and blesses the Entrance, as at the Liturgy

At the end of the stichera the Deacon exclaims, if there be one, if – not, then the Priest himself: "Wisdom, attend", lifting up the Gospel, and while "O Gladsome Light" is sung, the Priest or deacon carrying the Gospel goes out, and behind them the Priest, through the middle doors to the sanctuary and, having placed the Gospel on the Holy Table, censes everything as usual and stands before the steps of the Holy Table

After the singing of "O Gladsome Light" the Priest exclaims with the deacons, if there be [any]: "Let us attend! Peace be unto all!", "Wisdom", "Let us attend" and, while the Prokimenon of the day is sung, the Priest withdraws behind the Holy Table, and the deacons remain near the Holy Doors, exclaiming "Wisdom" and "Let us attend" to all the readings, of which on the Nativity of Christ there will be 8, and on Theophany – 11, with a separate troparion and its verses after the first three and after the second three readings

At the end of the readings the Priest returns before the steps of the Holy Table or the first deacon, if there be one, enters before the Holy Doors, where he sings the Small Litany; the Priest – the exclamation of the Trisagion, but the Trisagion is not sung, but immediately after the exclamation there will be "Let us attend! Peace be unto all!", "Wisdom", "Let us attend" and the Prokimenon of the Feast is sung; after "Wisdom" and "Let us attend" – Apostle to the Galatians, refrain 201 "I speak after the manner of men"; Gospel according to Matthew, refrain 83 "The kingdom of heaven is like to a grain of mustard seed"[^324]  (on Theophany: to the Corinthians, refrain 143 from the half "Brethren, I would not have you ignorant"; Gospel according to Luke, refrain 9 "Now in the fifteenth year"). The Gospel is read by the Priest himself[^325]  from the Holy Doors, and the first of the deacons, if there be [any], exclaims: "Wisdom, attend! Let us hear the Holy Gospel"; priest: "The reading from the Holy Gospel according to (Name)"; and the second: "Let us attend"

After the singing of the Gospel the Priest, having kissed the beginning of the Gospel reading and having given [it] to the first deacon to kiss, also to the second, approaches the Holy Table, on which he places the Holy Gospel, which remains there. The deacons, having bowed low before the steps of the Holy Table, go out, each through his doors, before the Holy Doors and, having bowed low, first the second Deacon exclaims "Let us all say", and also the first after "Vouchsafe" – the litany "Let us complete". If there be no deacons, then the Priest himself sings the litanies from the Holy Table and immediately after the second exclamation of the litany "Let us complete" gives the Great Dismissal of the Feast itself. (On Theophany there is no dismissal here, but it will be after the Blessing of Water).

After the Dismissal both choirs gather together in the middle of the church and sing the Troparion, Glory, Both now: Kontakion of the Feast, and at the end the sacred ministers close the Holy Doors and, having bowed low, withdraw to the sacristy."""

    replacement2 = """1. The Priest, having put on an epitrachelion and having gone out before the Holy Doors, bows low and begins the usual: "Blessed is our God". Choirs: "Amen", also "Glory to Thee, our God, glory to Thee", "O Heavenly King" and the rest with the Trisagion and "Our Father" up to "O come, let us worship" inclusive. Deacons, if there be [any], go out with the Priest before the Holy Doors and the right one of them exclaims: "Bless, Master", and the Priest: "Blessed is our God"[^323]

2. During the introductory Psalm the Priest, standing before the Holy Doors, says the evening prayers, as usual, and the deacons stand beside him and, at the end of the Psalm, one of them (the right) sings the Great Litany, and the Priest – its exclamation, and then, all bow low and withdraw to the sanctuary. If there be no deacons, then the Priest himself sings the litany

3. *“Blessed is the man”* and the Small Litany, for which the second deacon goes out before the Holy Doors, and the Priest – the exclamation from his place. If there be no deacon, then the Priest himself, according to local custom, reads the litany quietly, sitting in his place, and the Choir sings its responses.

4. **On *"Lord, I have cried"*:* usual censing, which the Priest or deacons, if there be [any], perform; stichera on 8, "Glory, Both now" from the Heirmologion or according to the tone of the idiomesa

5. **Entrance:** At "Glory, Both now" – Entrance with the Gospel, which the first deacon carries, if there be one, and the second precedes him with the censer; the Priest says the usual Prayer of the Entrance, as at Vespers, and blesses the Entrance, as at the Liturgy

6. At the end of the stichera the Deacon exclaims, if there be one, if – not, then the Priest himself: "Wisdom, attend", lifting up the Gospel, and while "O Gladsome Light" is sung, the Priest or deacon carrying the Gospel goes out, and behind them the Priest, through the middle doors to the sanctuary and, having placed the Gospel on the Holy Table, censes everything as usual and stands before the steps of the Holy Table

7. After the singing of "O Gladsome Light" the Priest exclaims with the deacons, if there be [any]: "Let us attend! Peace be unto all!", "Wisdom", "Let us attend" and, while the Prokimenon of the day is sung, the Priest withdraws behind the Holy Table, and the deacons remain near the Holy Doors, exclaiming "Wisdom" and "Let us attend" to all the readings, of which on the Nativity of Christ there will be 8, and on Theophany – 11, with a separate troparion and its verses after the first three and after the second three readings

8. At the end of the readings the Priest returns before the steps of the Holy Table or the first deacon, if there be one, enters before the Holy Doors, where he sings the Small Litany; the Priest – the exclamation of the Trisagion, but the Trisagion is not sung, but immediately after the exclamation there will be "Let us attend! Peace be unto all!", "Wisdom", "Let us attend" and the Prokimenon of the Feast is sung; after "Wisdom" and "Let us attend" – Apostle to the Galatians, refrain 201 "I speak after the manner of men"; Gospel according to Matthew, refrain 83 "The kingdom of heaven is like to a grain of mustard seed"[^324]  (on Theophany: to the Corinthians, refrain 143 from the half "Brethren, I would not have you ignorant"; Gospel according to Luke, refrain 9 "Now in the fifteenth year"). The Gospel is read by the Priest himself[^325]  from the Holy Doors, and the first of the deacons, if there be [any], exclaims: "Wisdom, attend! Let us hear the Holy Gospel"; priest: "The reading from the Holy Gospel according to (Name)"; and the second: "Let us attend"

9. After the singing of the Gospel the Priest, having kissed the beginning of the Gospel reading and having given [it] to the first deacon to kiss, also to the second, approaches the Holy Table, on which he places the Holy Gospel, which remains there. The deacons, having bowed low before the steps of the Holy Table, go out, each through his doors, before the Holy Doors and, having bowed low, first the second Deacon exclaims "Let us all say", and also the first after "Vouchsafe" – the litany "Let us complete". If there be no deacons, then the Priest himself sings the litanies from the Holy Table and immediately after the second exclamation of the litany "Let us complete" gives the Great Dismissal of the Feast itself. (On Theophany there is no dismissal here, but it will be after the Blessing of Water).

10. After the Dismissal both choirs gather together in the middle of the church and sing the Troparion, Glory, Both now: Kontakion of the Feast, and at the end the sacred ministers close the Holy Doors and, having bowed low, withdraw to the sacristy."""

    assert target2 in md, "Target 2 not found in MD"
    md = md.replace(target2, replacement2)

    # 3. Fix Synaxis of the Forerunner on Sunday (L1800-1806)
    target3 = """1.\t*“Blessed is the man”*, as usual.

3. **On *"Lord, I have cried"*:* 10 stichera: 3 Resurrectional, 4 of the Feast and 3 of the Forerunner, Glory: to the Forerunner, Both now: Dogmatikon of the sequential tone

4. **Aposticha:** Aposticha Resurrectional, Glory: to the Forerunner, Both now: of the Feast

At the end: Resurrectional Troparion, Glory: to the Forerunner, Both now: of the Feast"""

    replacement3 = """1. **Kathisma:** *“Blessed is the man”*, as usual.

2. **On *"Lord, I have cried"*:* 10 stichera: 3 Resurrectional, 4 of the Feast and 3 of the Forerunner, Glory: to the Forerunner, Both now: Dogmatikon of the sequential tone

3. **Aposticha:** Aposticha Resurrectional, Glory: to the Forerunner, Both now: of the Feast

4. **Troparia:** At the end: Resurrectional Troparion, Glory: to the Forerunner, Both now: of the Feast"""

    assert target3 in md, "Target 3 not found in MD"
    md = md.replace(target3, replacement3)

    # 4. Fix Cheesefare Saturday Finding of Head (L2668-2680)
    target4 = """1.\t*“Blessed is the man”* (according to the rule – 1st antiphon).

1. **On *"Lord, I have cried"*:* 6 stichera: 3 to the Forerunner and 3 to the Fathers, Glory: to the Forerunner, Both now: 1st Theotokion of the tone that is being given up

2. **Entrance:** Prokimenon of the day and Paremia of the *Triodion*, Prokimenon of the *Triodion* and 3 readings to the Forerunner; and immediately after the readings the Priest having taken off the phelonion and having closed the Holy Doors: "Vouchsafe, O Lord"

3. **Aposticha:** Aposticha of the *Triodion* and one stichera to the Forerunner with his refrain; Glory: to the Fathers, Both now: their Theotokion

4. **Troparia:** Troparion to the Forerunner, Glory: to the Fathers, Both now: Resurrectional Theotokion according to the tone of the Doxastikon

5. Litany "Have mercy on us, O God" and three great prostrations

7.\t"O All-Holy Trinity", "Blessed be the name of the Lord", "Blessed be the Lord", *“It is truly meet”* and dismissal (from "Glory to Thee, O Christ God")."""

    replacement4 = """1. **Kathisma:** *“Blessed is the man”* (according to the rule – 1st antiphon).

2. **On *"Lord, I have cried"*:* 6 stichera: 3 to the Forerunner and 3 to the Fathers, Glory: to the Forerunner, Both now: 1st Theotokion of the tone that is being given up

3. **Entrance:** Prokimenon of the day and Paremia of the *Triodion*, Prokimenon of the *Triodion* and 3 readings to the Forerunner; and immediately after the readings the Priest having taken off the phelonion and having closed the Holy Doors: "Vouchsafe, O Lord"

4. **Aposticha:** Aposticha of the *Triodion* and one stichera to the Forerunner with his refrain; Glory: to the Fathers, Both now: their Theotokion

5. **Troparia:** Troparion to the Forerunner, Glory: to the Fathers, Both now: Resurrectional Theotokion according to the tone of the Doxastikon

6. Litany "Have mercy on us, O God" and three great prostrations

7. "O All-Holy Trinity", "Blessed be the name of the Lord", "Blessed be the Lord", *“It is truly meet”* and dismissal (from "Glory to Thee, O Christ God")."""

    assert target4 in md, "Target 4 not found in MD"
    md = md.replace(target4, replacement4)

    # 5. Fix Finding of Head on Monday (L2806-2816)
    target5 = """1.\t*“Blessed is the man”* (according to the rule – 1st antiphon).

4. **On *"Lord, I have cried"*:* 10 stichera: 4 of the *Triodion* and 6 to the Forerunner, Glory: to the Forerunner, Both now: 1st Theotokion according to the tone of the Doxastikon

5. **Entrance:** Entrance, Great Prokimenon of the *Triodion*, 3 readings to the Forerunner and immediately "Vouchsafe, O Lord"

6. **Aposticha:** Aposticha of the *Triodion*, Glory: to the Forerunner, Both now: Theotokion from the Sunday Aposticha according to the tone of the Doxastikon

7. After "Now lettest Thou" – Troparion to the Forerunner, Glory, and now: Resurrectional Theotokion according to the tone of the troparion

8. Litany "Have mercy on us, O God", three great prostrations without prayer and Great Dismissal"""

    replacement5 = """1. **Kathisma:** *“Blessed is the man”* (according to the rule – 1st antiphon).

2. **On *"Lord, I have cried"*:* 10 stichera: 4 of the *Triodion* and 6 to the Forerunner, Glory: to the Forerunner, Both now: 1st Theotokion according to the tone of the Doxastikon

3. **Entrance:** Entrance, Great Prokimenon of the *Triodion*, 3 readings to the Forerunner and immediately "Vouchsafe, O Lord"

4. **Aposticha:** Aposticha of the *Triodion*, Glory: to the Forerunner, Both now: Theotokion from the Sunday Aposticha according to the tone of the Doxastikon

5. **Troparia:** After "Now lettest Thou" – Troparion to the Forerunner, Glory, and now: Resurrectional Theotokion according to the tone of the troparion

6. Litany "Have mercy on us, O God", three great prostrations without prayer and Great Dismissal"""

    assert target5 in md, "Target 5 not found in MD"
    md = md.replace(target5, replacement5)

    md_path.write_text(md, encoding='utf-8')
    print("Successfully repaired all Part 3 list numbering defects!")

if __name__ == '__main__':
    fix_part3_md_numbering()
