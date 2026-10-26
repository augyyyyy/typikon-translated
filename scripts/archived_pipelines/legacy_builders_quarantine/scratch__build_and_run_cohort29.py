# -*- coding: utf-8 -*-
"""
Master Cohort 29 Assembler and Gate Runner
Monument: Typik of Fr. Isidore Dolnytsky (Lviv Stauropegion, 1899)
Leaves: p561 to p580
"""

import sys
import subprocess
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT_ROOT / "Liturgical Monuments" / "1899 Dolnytsky Typikon"

SOURCE_OUT = WORKSPACE / "Source Text" / "1899_dolnytsky_typikon_cohort29_source.txt"
DRAFT_OUT = WORKSPACE / "Draft" / "1899_dolnytsky_typikon_cohort29_raw_draft.md"
FOOTNOTES_OUT = WORKSPACE / "Draft" / "1899_dolnytsky_typikon_cohort29_footnotes.txt"

# Import helper functions from generate_cohort29_full
from generate_cohort29_full import (
    FOOTNOTES_CONTENT,
    make_table1_cs, make_table1_en,
    make_table2_page_cs, make_table2_page_en,
    make_pascha_diff_cs, make_pascha_diff_en,
    make_table3_p576_cs, make_table3_p576_en,
    make_table3_p577_cs, make_table3_p577_en,
    make_table3_p578_cs, make_table3_p578_en,
)

# -------------------------------------------------------------
# Source Text Construction
# -------------------------------------------------------------
def build_source_text():
    parts = []

    # p561
    parts.append("""=== LEAF p561 ===
Оу҆ка́зъ Слꙋ́жбъ Подви́жныхъ.
ТРЇѠ́ДИ ПО́СТНЫЯ.

Недѣ́ля Мытаря̀ и҆ Фарісе́я.
Въ шестѝ дне́хъ ѿ Понедѣ́льника, да́же до Сꙋббѡ́ты Блꙋ́днагw, Трїѡ́дь не и҆́мать ничесѡ́же, но то́кмо Ѻ҆ктѡ́ихъ и҆ Минє́а. — Зага́льница.

Недѣ́ля Блꙋ́днагw.
1. Въ пятѝ дне́хъ ѿ Понедѣ́льника до Пятка̀ Мясопꙋ́ст. Трїѡ́дь не и҆́мать ничесѡ́же, но то́кмо Ѻ҆ктѡ́ихъ и҆ Минє́а.
2. Сꙋббѡ́та Мясопꙋ́стна: Задꙋ́шна, безъ Минє́и.

Недѣ́ля Мясопꙋ́стна
Ѡ҆ стра́шномъ Сꙋдѣ̀.
1. Слꙋ́жба Седми́ци Сыропꙋ́ст. є҆́сть Покая́нна, я҆́ки Предпра́зденственна вели́цѣй м҃-ци.
2. Въ Понедѣ́льникъ, Вто́рникъ и҆ Четверто́къ, Трїѡ́дь ма́ло что̀ и҆́мать, про́чее же держи́тъ Ѻ҆ктѡ́ихъ и҆ Минє́а.
3. Въ Сре́дꙋ и҆ Пято́къ Трїѡ́ди и҆́мать Слꙋ́жбꙋ По́стнꙋ полнѣ́йшꙋ.
(: 4. Сꙋббѡ́та Сыропꙋ́ст. Ст҃ы̑мъ По́стникѡмъ.

Недѣ́ля Сыропꙋ́стна.
А҆да́мово и҆згна́нїе.
1. Въ патодне́вїи ѿ Понедѣ́льника до Пятка̀ а҃-ыя Седми́ци Постѡ́въ, Слꙋ́жба По́стна. — Съ Понедѣ́лникомъ Нача́ло вели́кїя м҃-ци.
2. Сꙋббѡ́та а҃-я Постѡ́въ. ВМ. Ѳеѡ́дѡръ Тѵ́ронъ.""")

    # p562
    parts.append("""=== LEAF p562 ===
560       Оу҆ка́зъ Слꙋ́жбъ Подви́жныхъ.

Недѣ́ля а҃-я Постѡ́въ.
Правосла́вїе: проти́вꙋ І҆конобо́рцевъ.
1. Въ Пятодне́вїи ѿ Понедѣ́льника до Пятка̀ в҃-ыя Седми́ци Постѡ́въ, Слꙋ́жба По́стна.
2. Ѿ Понедѣ́льника, и҆ ни́жае пое́мъ на Повече́рїихъ Канѡ́нъ Ст҃ы́хъ Минє́и, хотя́щихъ слꙋчи́тися ѿ Сꙋбб. Ла́заревыя да́же до Недѣ́ли Ѳѡмины̀, ѻ҆бою́дꙋ вклю́чнѡ.
3. Сꙋббѡ́та в҃-я Постѡ́въ: Слꙋ́жба Мꙋ́ченикѡмъ, Ст҃и́телемъ и҆ всѣ̑мъ Ст҃ы̑мъ, та́же Оу҆со́пшимъ, по Оу҆ста́вꙋ Сꙋббѡ́тъ А҆ллилꙋ́евыхъ, со Слꙋ́жбою Ст҃а́гw ряд. Минє́и. Си́це быва́етъ и҆ въ г҃-ю и҆ д҃-ю Сꙋббѡ́тꙋ Поста̀.

Недѣ́ля в҃-я Постѡ́въ.
Бези́менна, Покая́нна.
1. Въ Пятодне́вїи ѿ Понедѣ́льника до Пятка̀ г҃-їя Седми́ци Постѡ́въ, Слꙋ́жба По́стна.
2. Сꙋббѡ́та г҃-я Постѡ́въ: Слꙋ́жба Сꙋббѡ́ты А҆ллилꙋ́евыя, я҃кwже в҃-ыя.

Недѣ́ля г҃-я Постѡ́въ.
Крестопокло́нна.
1. Въ Пятодне́вїи ѿ Понедѣ́льника до Пятка̀ Седми́ци д҃-я Постѡ́въ, Слꙋ́жба Крестопокло́нна.
2. Сꙋббѡ́та д҃-я Постѡ́въ: Слꙋ́жба я҃кwже и҆ в҃-ыя и҆ г҃-їя Постѡ́въ.

Недѣ́ля д҃-я Постѡ́въ.
Бези́менна Покая́нна.
По Произволе́нїю, и҆ Слꙋ́жба Ст҃о́мꙋ І҆ѡа́ннꙋ Лѣ́ствичникꙋ.
1. Въ Понедѣ́лникъ Вто́рникъ, Сре́дꙋ и҆ Пято́къ є҃-ыя Седми́ци Постѡ́въ, Слꙋ́жба По́стна.""")

    # p563
    parts.append("""=== LEAF p563 ===
Оу҆ка́зъ Слꙋ́жбъ Подви́жныхъ.       561

2. Къ Четверто́къ є҃-ыя Седми́ци Постѡ́въ: Слꙋ́жба Покая́нна вел. Канѡ́на, съ Поклѡ́ны.
3. Сꙋббѡ́та є҃-я Постѡ́въ: А҆ка́ѳїстова.

Недѣ́ля є҃-я Постѡ́въ.
Бези́менна Покая́нна.
По произволе́нїю и҆ Слꙋ́жба Преп. Марíи Є҆гѵ́петскїя.
Въ Пятодне́вїи ѿ Понедѣ́льника до Пятка̀ ѕ҃-ыя Седми́ци Постѡ́въ, Слꙋ́жба По́стна.

ТРЇѠ́ДИ ЦВѢ́ТНЫЯ.
Сꙋббѡ́та ѕ҃-я Постѡ́въ: Ла́зарева.
Канѡ́ни Ст҃ы́хъ и҆́же на рядꙋ̀ Минє́и ѿ сея̀ Сꙋббѡ́ты да́же до Недѣ́ли Ѳѡмины̀, предпѣ́шася на Повече́рїихъ ѿ Понедѣ́лн. в҃-ыя Седми́ци Постѡ́въ и҆ ни́жае.

⊕ Недѣ́ля ѕ҃-я Постѡ́въ: Ва́їй.
Пра́здникъ є҆динодне́вный, съ Бдѣ́нїемъ.
1. Въ вел. Понедѣ́лникъ, Вто́рникъ и҆ Сре́дꙋ: Слꙋ́жба Страстно-Покая́нна, я҃́ки Предпра́зденственна Страсте́мъ Хрⷭ҇то́вымъ.¹)
2. Къ вел. Четверто́къ: Та́йна Ве́чера, и҆ нача́ло Стра́сти Хрⷭ҇то́выя.
3. Въ вел. Пято́къ: Стра́сть Хрⷭ҇то́ва.
4. Въ вел. Сꙋббѡ́тꙋ: Низложе́нїе Хрⷭ҇та̀ во Гро́бъ

⊕⊕ Недѣ́ля Па́схи: ВОСКРЕСЕ́НЇЕ ХРТО́ВО.
Пра́здникъ Тридесятьдевятодне́вный.
1. Ѿ Понедѣ́лника да́же до Сꙋббѡ́ты Свѣ́тлыя вклю́чнѡ пое́мъ всю̀ Слꙋ́жбꙋ Па́сцѣ.

----------------
¹) Зрѝ ¹) на стр. 427.""")

    # p564
    parts.append("""=== LEAF p564 ===
562       Оу҆ка́зъ Слꙋ́жбъ Подви́жныхъ.

2. Въ Понедѣ́лникъ и҆ Вто́рникъ возде́ржꙋемся ѿ рабо́тъ, и҆ пресꙋ́тствꙋемъ Бг҃ослꙋже́нїю; во всю́ же Седми́цꙋ разрѣша́емся на мясоя́стїе.

⊕⊕ Недѣ́ля в҃-я ѿ Па́схи: А҆нтіпа́схи: Ѳѡмина̀.
Пра́здникъ Седмодне́вный, съ Бдѣ́нїемъ.
Понедѣ́льникъ, Вто́рникъ, Среда̀, Четверто́къ, Пят. и҆ Сꙋббѡ́та: Внꙋ́трь Пра́здника Недѣ́ли Ѳѡмины̀, со Минє́ю.

Недѣ́ля г҃-я ѿ Па́схи: Мѷроно́сицъ.
Пра́здникъ Седмодне́вный.
Понедѣ́льникъ, Вто́рникъ, Среда̀, Четверто́къ, Пят. и҆ Сꙋббѡ́та: Внꙋ́трь Пра́здника Мѷроно́сицъ, со Минє́ю.

Недѣ́ля д҃-я ѿ Па́схи: Разсла́бленнагw.
Пра́здникъ Тридне́вный.
1. Понедѣ́лникъ и҆ Вто́рникъ: Внꙋ́трь Пра́здника Разсла́бленнагw, со Минє́ю.
2. Среда̀ Преполове́нїя н҃-ци. Пра́здникъ ѻ҆смодне́вный, безъ Бдѣ́нїя, и҆ безъ Полѷеле́я.

Недѣ́ля є҃-я ѿ Па́схи: Самаряни́ны.
Пра́здникъ четверодне́вный.
1. Понедѣ́лникъ и҆ Вто́рникъ: Внꙋ́трь Пра́здника Преполове́нїя; Слꙋ́жба же Самаряни́ны запина́ется до́ндеже ѿда́стся Пра́здникъ Преполове́нїя.
(: 2. Среда̀: Ѿда́нїе Преполове́нїя.
3. Четверт. Пят. и҆ Сꙋббѡ́та: Внꙋ́трь Пра́здника Самаряни́ны.""")

    # p565
    parts.append("""=== LEAF p565 ===
Оу҆ка́зъ Слꙋ́жбъ Подви́жныхъ.       563

Недѣ́ля ѕ҃-я ѿ Па́схи: Слѣпа́гw.
Пра́здникъ четверодне́вный.
1. Понедѣ́лникъ, Вто́рникъ и҆ Среда̀: Внꙋ́трь Пра́здника Слѣпа́гw; въ Сре́дꙋ же є҆щѐ и҆ ⊕ Ѿда́нїе Па́схи, и҆ Предпра́зденство Вознесе́нїя.
⊕⊕ 2. Четверто́къ: ВОЗНЕСЕ́НЇЕ. Пра́здникъ девятодне́вный, съ Бдѣ́нїемъ.

Недѣ́ля з҃-я ѿ Па́схи. Ст҃ы́хъ Ѻ҆те́цъ.
1. Понедѣ́лникъ, Вто́рникъ, Среда̀ и҆ Четверто́къ: внꙋ́трь Пра́здника Вознесе́нїя.
(: 2. Пято́къ: Ѿда́нїе Вознесе́нїя.
3. Сꙋббѡ́та Задꙋ́шна, по Оу҆ста́вꙋ Мясопꙋ́ст. здѣ̀ на стр. 363.

⊕⊕ Недѣ́ля н҃-ци. СОШЕ́СТВЇЕ С. ДХ҃А.
Пра́здникъ седмодне́вный, съ Бдѣ́нїемъ.
1. Понедѣ́лникъ С. Дх҃а. (и҆ Пра́зд. Ст҃ы́я Тро́йци, по произвол). Воздержа́нїе ѿ рабо́тъ, съ присꙋ́тствїемъ Бг҃ослꙋже́нїю.
2. Разрѣше́нїе на мя́со во все́й Седми́ци.
(: 3. Сꙋббѡ́та: Ѿда́нїе Соше́ствїя С. Дх҃а.

Недѣ́ля а҃-я по Соше́ств. Всѣ́хъ Ст҃ы́хъ.
Здѣ̀ коне́цъ Трїѡ́ди дре́внїя.
1. Съ се́ю Недѣ́лею начина́ется ря́дъ Є҆ѵл҃їй Воскре́сныхъ Оу҆́треннихъ, и҆ Лїтꙋргíйныхъ Дневны́хъ.
2. Въ Понедѣ́лникъ, Вто́рникъ и҆ Сре́дꙋ Трїѡ́дь не и҆́мать ничесѡ́же.
⊕⊕ 3. Четверто́къ: ЕVХАРЇ́СТЇИ. Пра́здникъ Ѻ҆смодне́вный. Бдѣ́нїе прено́симъ на Недѣ́лю.""")

    # p566
    parts.append("""=== LEAF p566 ===
564       Оу҆ка́зъ Слꙋ́жбъ Подви́жныхъ.

Недѣ́ля в҃-я по Соше́ств. Бдѣ́нїе Єv҆харі́ст.
1. Съ се́ю Недѣ́лею начина́ется ря́дъ Гласо́въ.
(: 2. Въ Четверто́къ: Ѿда́нїе Пра́здника Єv҆харі́стїи.
+ 3. Въ Пято́къ: Сострада́нїе П. Бц҃и. Пра́здникъ є҆динодне́вный, Полѷеле́йный; и҆ съ си́мъ коне́цъ Трїѡ́ди но́выя.

О К Т Ѡ И Х Я.
Въ Недѣ́лю     Слꙋ́жба Воскре́сна.
” Понед.      ” Покая́нна, и҆ А҆́нгелѡмъ.
” Вто́рн.      ” Покая́нна, и҆ Предте́чи.
” Сре́д. и҆ Пят. ” Крестꙋ̀, и҆ Бг҃оро́дици.
” Четверт.    ” А҆пⷭ҇лѡмъ, и҆ С. Нїкола́ю.
” Сꙋббѡ́тꙋ    ” Всѣ̑мъ Ст҃ы̑мъ и҆ Оу҆со́п.""")

    # p567: Skrizhal I
    parts.append(f"""=== LEAF p567 ===
СКРИЖА́ЛЬ I.
Врꙋцѣлѣ́та и҆ Ключѝ Грани́ч.
на послѣ́дная 40 лѣ̑та І҆ндіктїѡ́на,
си́рѣчь Крꙋ́га 532 лѣ̑тъ,
14-гw ѿ нача́ла мíра.

{make_table1_cs()}""")

    # p568 to p574: Skrizhal II
    parts.append(f"""=== LEAF p568 ===
СКРИЖА́ЛЬ II.
Врꙋцѣлѣ́та и҆ Ключѝ Грани́ч.
на всю́ 532 лѣ́та І҆ндіктїѡ́на 15-гw ѿ нача́ла мíра.

{make_table2_page_cs(1941, 20)}""")

    parts.append(f"""=== LEAF p569 ===
{make_table2_page_cs(2001, 28)}""")

    parts.append(f"""=== LEAF p570 ===
{make_table2_page_cs(2085, 28)}""")

    parts.append(f"""=== LEAF p571 ===
{make_table2_page_cs(2169, 28)}""")

    parts.append(f"""=== LEAF p572 ===
{make_table2_page_cs(2253, 28)}""")

    parts.append(f"""=== LEAF p573 ===
{make_table2_page_cs(2337, 28)}""")

    parts.append(f"""=== LEAF p574 ===
{make_table2_page_cs(2421, 18, col3_rows=16)}""")

    # p575: Paschal Differences
    parts.append(f"""=== LEAF p575 ===
ПА́СХИ РИ́МСКЇЯ И҆ ГРЕ́ЧЕСКЇЯ
Разли́чїе
на послѣ́дная 40 лѣ̑та І҆ндіктїѡ́на 14-гw¹).
А҆.-А҆прі́л. — М.-Ма́рт. — 0-ра́внw.

{make_pascha_diff_cs()}

----------------
¹) Разли́чїе ѿкрыва́ется ѿ приложе́нїя къ Па́сцѣ Гре́честкѣй дні́й 13.""")

    # p576: Table III upper
    parts.append(f"""=== LEAF p576 ===
III. СКРИЖА́ЛЬ ВСЕГДА́ШНАЯ
содержа́ща 35 столпѡ́въ Недѣ́ль всегẁ лѣ́та съ оу҆каза́нїемъ Є҆ѵл҃їй и҆ Гласо́въ рядовы́хъ.

{make_table3_p576_cs()}""")

    # p577: Table III middle
    parts.append(f"""=== LEAF p577 ===
III. СКРИЖА́ЛЬ ВСЕГДА́ШНАЯ (Продолже́нїе)
Недѣ́ли 12–29 по Соше́ствїи Ст҃а́гw Дꙋ́ха.

{make_table3_p577_cs()}""")

    # p578: Table III lower
    parts.append(f"""=== LEAF p578 ===
III. СКРИЖА́ЛЬ ВСЕГДА́ШНАЯ (Оконча́нїе)
Недѣ́ли 30–32, Предпо́стныя Недѣ́ли, Февра́ль и҆ Оу҆каза́нїе Є҆ѵа́ггелїй.

{make_table3_p578_cs()}

Є҆V́ЛЇА НЕДѢ́ЛЬ Ѻ҆СО́БЕННЫХЪ МИНЕ́И.
стѣка́ющася ся Є҆ѵ́лїами Недѣ́ль рядовы́хъ.

a) Нед. Ст҃ы́хъ Ѻ҆те́цъ пе́рвыхъ 6 Собо́рѡвъ: ѕ҃і. І҆́ꙋл.
b) ” предъ Воздви́ж.
c) ” по Воздви́ж.
d) ” Ст҃ы́хъ Ѻ҆те́цъ в҃-гw Собо́ра Нїке́йск.: а҃і. Ѻ҆кт.
e) ” рядова́я стѣка́ющася съ Нед. Пра́отецъ.

f) Нед. Ст҃ы́хъ Пра́отецъ.
g) ” Ст҃ы́хъ Ѻ҆те́цъ.
h) ” по Рождествѣ̀.
i) ” предъ Просвѣ́щ.
l) ” по Просвѣ́щ.""")

    # p579: Vrazumlenie Skrizhali
    parts.append("""=== LEAF p579 ===
ВРАЗꙋМЛЕ́НЇЕ СКРИЖА́ЛИ.

1. Скрижа́ль содержи́тъ 35 Столпѡ́въ Недѣ́ль всегẁ лѣ́та по числꙋ̀ 35 Ключе́въ Грани́чныхъ, и҆ ѿвѣща́ющихъ и҆̀мъ 35 дне́й Пасха́льныхъ.

2. На челѣ̀ Скрижа́ли, си́рѣчь въ 1-мъ рядꙋ̀ є҆я̀ непре́чномъ, стоя́тъ всѝ 35 Ключѝ Грани́чнїи, подъ ко́емждо же ключе́мъ простира́ется ря́дъ, и҆лѝ Сто́лпъ, Недѣ́ль всегẁ лѣ́та, съ оу҆каза́нїемъ днѐ мѣ́сяца, въ є҆гѡ́же грани́цахъ сїя̑ Недѣ́ли слꙋча́ются, и҆ числа̀ и҆лѝ загла́вїя и҆́хъ. И҆ мѣ́сяци оу҆́бо пи́сани сꙋ́ть внѣ̀ столпа̀, ѡ҆шꙋ́ю, предѣ́лени є҆ди́нъ ѿ дрꙋга́гw че́ртами пре́чными, чермны́ми, степенѐви́дными; де́нь мѣ́сяца пи́саный внꙋ́трь Столпа̀, число́ же, и҆лѝ загла́вїе Недѣ́кли, пи́сано внѣ̀ Столпа̀, ѡ҆деснꙋ́ю Скрижа́ли.

3. Въ рядꙋ̀ 7-мъ стоя́тъ всѝ 35 дні́е, въ ни́хже слꙋчи́тися мо́жетъ Недѣ́ля Мытаре́ва, съ не́юже начина́ется Трїѡ́дь.

4. Въ рядꙋ̀ 8-мъ стоя́тъ всѝ 35 дні́е Пасха́льнїи чермнопи́сани, ѿвѣщава́ющїи 35 Ключе́мъ Грани́чнымъ.

5. Въ 5 рядѣ́хъ, и҆́же содержа́тся междꙋ̀ Мытаре́мъ и҆ Ключѝ Грани́чными, стоя́тъ вся̑ 5 Недѣ́ли, я҃же слꙋчи́тися могꙋ́тъ междꙋ̀ Бг҃оявле́нїемъ и҆ Мытаре́мъ, си́рѣчь, Недѣ́ля по Просвѣще́нїи, и҆ 4 послѣ́днїя рядовы́я (кѳ҃, л҃, ла҃, лв҃). Ѻ҆ба́че, поне́же не вся̑ сїя̑ Недѣ́ли всегда̀ и҆мѣ́ютъ мѣ́сто, я҃кwже и҆зъяви́хомъ на стр. 159. (и҆́бо сїѐ зави́ситъ ѿ прискоре́нїя, и҆лѝ замедле́нїя Па́схи), сегẁ ра́ди въ си́хъ 5 рядѣ́хъ нѣ́каа мѣ̑ста ѡ҆брѣта́ются пра́здна, є҆́же зна́менꙋетъ, я҃ко тогда̀ Недѣ́ли, ѿвѣщава́ющїя и҆̀мъ ѡ҆деснꙋ́ю скрижа́ли, не и҆мѣ́ютъ мѣ́ста. Н. пр. подъ ключе́мъ Грани́чнымъ А҆, вся̑ мѣ́ста пра́здна сꙋ́ть; зна́менꙋетъ оу҆́бо, я҃кw ѿ""")

    # p580
    parts.append("""=== LEAF p580 ===
Вразꙋмлє́нїе Скрижа́ли.       581

си́хъ 5 Недѣ́ль ни є҆ди́на тогда̀ во́змется, но а҆́бїе по Бг҃оявле́нїи Трїѡ́дь

6. Ѿ Недѣ́ль Трїѡ́дныхъ положи́хомъ то́кмо трѝ, си́рѣчь средото́чнꙋю, я҃же є҆́сть Па́схи, и҆ двѣ̀ кра́йныя, си́рѣчь Мытаре́вꙋ, и҆ Всѣ́хъ Ст҃ы́хъ; прѡ́чїя же посре́дныя ѡ҆ста́вихомъ, зане́же оу҆до́бь задержа́ти я҃ въ па́мяти и҆ безъ Скрижа́ли, и҆мѣ́ютъ бо ѡ҆бы́чнѡ загла́вїя ѡ҆со́бенная, и҆ Слꙋ́жбы сво́йственныя ѿвѣща́ющїя загла́вїемъ.

7. Въ Недѣ́ляхъ предваря́ющихъ Мытаре́вꙋ не положи́хомъ ни Гла́са, ни Є҆ѵл҃їа воскре́снагw, и҆́бо сїя̑ зави́сятъ ѿ Па́схи мимоше́дшїя, и҆ сегẁ ра́ди подоба́етъ и҆ска́ти я҃ при концѝ Скрижа́ли въ предѣ́лѣхъ І҆анꙋа́рїа и҆ Феврꙋа́рїа подъ Ключе́мъ Грани́ч. Па́схи мимоше́дшїя.

8. При нѣ́кїихъ Недѣ́ляхъ положе́ни сꙋ́ть бꙋ́квы лати́нскїя чермны́я. Е҆́же зна́менꙋетъ я҃ко тогда̀ съ Є҆ѵл҃їемъ ѻ҆́ныя Недѣ́кли рядовы́я и҆́мать лꙋчи́тися є҆щѐ и҆ дрꙋго́е Недѣ́ли нѣ́коея ѿ 10 ѡ҆со́бенныхъ Минє́и, я҃же положи́хомъ при концѝ Скрижа́ли, съ ѿноси́тельными бꙋ́квами лати́нскими.¹)

9. По си́хъ, а҆́ще хо́щеши оу҆вѣ́дѣти, кі́я Недѣ́ли въ нѣ́коемъ го́дѣ подоба́етъ воспрїя́ти междꙋ̀ Бг҃оявле́нїемъ и҆ Мытаре́мъ, и҆щѝ пре́жде всѣ́хъ Клю́чь Грани́чный Па́схи грядꙋ́щїя, по Оу҆ка́зꙋ Скрижа́ли I-я, и҆лѝ II-я, и҆ подъ ни́мъ въ Скрижа́ли III-й ѡ҆бря́щеши ты́я Недѣ́ли; то́чїю, а҆́ще го́дъ престꙋ́пный, держи́ся Столпа̀ безпосре́днѡ слѣ́дꙋющагw. А҆́ще же хо́щеши оу҆вѣ́дѣти, ка́я Недѣ́ля, и҆ Гла́съ и҆ Є҆ѵл҃їе воскр. и҆́мать воспрїя́тися къ нѣ́кой ѿ Недѣ́ль по Соше́ствїи С. Дꙋ́ха, то оу҆вѣ-

----------------
¹) То́кмо Є҆ѵл҃їе Недѣ́ли к҃и-ыя, а҆́ще слꙋчи́тся пре́жде и҆лѝ послѣ́де Пра́отецъ, ѡ҆ставля́емъ на Недѣ́лю Пра́отецъ, а҆ въ к҃и-ю чте́мъ рядово́е Пра́отецъ є҆ди́но.""")

    return "\n\n".join(parts) + "\n"

# -------------------------------------------------------------
# Draft Markdown Translation Construction
# -------------------------------------------------------------
def build_draft_text():
    parts = []

    # Title header
    parts.append("# Typik of Fr. Isidore Dolnytsky (1899) — Cohort 29\n")

    # p561
    parts.append("""[Leaf p561 / Page 559]

## Directory of Movable Services

### Of the Lenten Triodion

#### Sunday of the Publican and the Pharisee
In the six days from Monday until the Saturday of the Prodigal Son, the Triodion has nothing, but only the Octoechos and the Menaion. — Fast-free week.

#### Sunday of the Prodigal Son
**1.** In the five days from Monday until Meatfare Friday, the Triodion has nothing, but only the Octoechos and the Menaion.  
**2.** Meatfare Saturday: For the Dead (All Souls), without the Menaion.

#### Sunday of Meatfare
##### Of the Dread Judgment
**1.** The Service of Cheesefare Week is Penitential, as a Forefeast of the Great Forty Days.  
**2.** On Monday, Tuesday, and Thursday, the Triodion has little, and the Octoechos and the Menaion hold the rest.  
**3.** On Wednesday and Friday, the Triodion has the fuller Fasting Service.  
**4.** **(:** Cheesefare Saturday: To the Holy Ascetics.

#### Sunday of Cheesefare
##### Adam’s Expulsion from Paradise
**1.** In the five days from Monday until Friday of the 1st Week of the Fast, the Service is Fasting. — With Monday begins the Great Forty Days.  
**2.** 1st Saturday of the Fast: Great Martyr Theodore the Recruit (Tyro).""")

    # p562
    parts.append("""[Leaf p562 / Page 560]

#### 1st Sunday of the Fast
##### Orthodoxy: Against the Iconoclasts
**1.** In the five days from Monday until Friday of the 2nd Week of the Fast, the Service is Fasting.  
**2.** From Monday and downward, we sing at Compline the Canons of the Saints of the Menaion that will occur from Lazarus Saturday until Thomas Sunday, both inclusive.  
**3.** 2nd Saturday of the Fast: Service to the Martyrs, Hierarchs, and all Saints, likewise for the Deceased, according to the Typikon of Alleluia Saturdays, with the Service of the ordinary Saint of the Menaion. Thus it takes place also on the 3rd and 4th Saturdays of the Fast.

#### 2nd Sunday of the Fast
##### Nameless, Penitential
**1.** In the five days from Monday until Friday of the 3rd Week of the Fast, the Service is Fasting.  
**2.** 3rd Saturday of the Fast: Service of an Alleluia Saturday, as that of the 2nd.

#### 3rd Sunday of the Fast
##### Veneration of the Precious Cross
**1.** In the five days from Monday until Friday of the 4th Week of the Fast, the Service is of the Cross-Veneration.  
**2.** 4th Saturday of the Fast: Service as on the 2nd and 3rd of the Fast.

#### 4th Sunday of the Fast
##### Nameless, Penitential
At discretion, also the Service to Saint John of the Ladder (Climacus).  
**1.** On Monday, Tuesday, Wednesday, and Friday of the 5th Week of the Fast, the Service is Fasting.""")

    # p563
    parts.append("""[Leaf p563 / Page 561]

**2.** On Thursday of the 5th Week of the Fast: Penitential Service of the Great Canon, with prostrations.  
**3.** 5th Saturday of the Fast: Of the Akathist.

#### 5th Sunday of the Fast
##### Nameless, Penitential
At discretion, also the Service of Venerable Mary of Egypt.  
In the five days from Monday until Friday of the 6th Week of the Fast, the Service is Fasting.

### Of the Flowery Triodion (Pentecostarion)

#### 6th Saturday of the Fast: Of Lazarus
The Canons of the Saints that occur in the ordinary course of the Menaion from this Saturday until Thomas Sunday have been pre-sung at Compline from Monday of the 2nd Week of the Fast downward.

#### ⊕ 6th Sunday of the Fast: Palm Sunday (Flowery)
Feast of one day, with a Vigil.  
**1.** On Great Monday, Tuesday, and Wednesday: Passion-Penitential Service, as a Forefeast of Christ's Sufferings.[^741]  
**2.** On Great Thursday: The Mystical Supper, and the beginning of Christ's Passion.  
**3.** On Great Friday: The Passion of Christ.  
**4.** On Great Saturday: The Laying of Christ in the Tomb.

#### ⊕⊕ Sunday of Pascha: THE RESURRECTION OF CHRIST
Feast of thirty-nine days.  
**1.** From Monday until Bright Saturday inclusive, we sing the entire Service to Pascha.""")

    # p564
    parts.append("""[Leaf p564 / Page 562]

**2.** On Monday and Tuesday we abstain from labor and are present at divine services; and during the entire week we are permitted meat (fast-free).

#### ⊕⊕ 2nd Sunday after Pascha: Antipascha: Of Thomas
Feast of seven days, with a Vigil.  
Monday, Tuesday, Wednesday, Thursday, Friday, and Saturday: Within the Feast of Thomas Sunday, with the Menaion.

#### 3rd Sunday after Pascha: Of the Myrrh-Bearers
Feast of seven days.  
Monday, Tuesday, Wednesday, Thursday, Friday, and Saturday: Within the Feast of the Myrrh-Bearers, with the Menaion.

#### 4th Sunday after Pascha: Of the Paralytic
Feast of three days.  
**1.** Monday and Tuesday: Within the Feast of the Paralytic, with the Menaion.  
**2.** Wednesday of Mid-Pentecost: Feast of eight days, without a Vigil, and without a Polyeleos.

#### 5th Sunday after Pascha: Of the Samaritan Woman
Feast of four days.  
**1.** Monday and Tuesday: Within the Feast of Mid-Pentecost; but the Service of the Samaritan Woman is deferred until the Feast of Mid-Pentecost is concluded (Apodosis).  
**2.** **(:** Wednesday: Apodosis of Mid-Pentecost.  
**3.** Thursday, Friday, and Saturday: Within the Feast of the Samaritan Woman.""")

    # p565
    parts.append("""[Leaf p565 / Page 563]

#### 6th Sunday after Pascha: Of the Blind Man
Feast of four days.  
**1.** Monday, Tuesday, and Wednesday: Within the Feast of the Blind Man; and on Wednesday also the ⊕ Apodosis of Pascha, and the Forefeast of the Ascension.  
**2.** **⊕⊕** Thursday: ASCENSION. Feast of nine days, with a Vigil.

#### 7th Sunday after Pascha: Of the Holy Fathers
**1.** Monday, Tuesday, Wednesday, and Thursday: Within the Feast of the Ascension.  
**2.** **(:** Friday: Apodosis of the Ascension.  
**3.** Saturday for the Dead (All Souls), according to the Meatfare Typikon, here on page 363.

#### ⊕⊕ Sunday of Pentecost: DESCENT OF THE HOLY SPIRIT
Feast of seven days, with a Vigil.  
**1.** Monday of the Holy Spirit (and the Feast of the Holy Trinity, at discretion): Abstinence from labor, with attendance at divine services.  
**2.** Dispensation for meat (fast-free) throughout the entire week.  
**3.** **(:** Saturday: Apodosis of the Descent of the Holy Spirit.

#### 1st Sunday after Pentecost: All Saints
Here is the end of the ancient Triodion.  
**1.** With this Sunday begins the series of Sunday Matins Gospels and daily Liturgy Gospels.  
**2.** On Monday, Tuesday, and Wednesday, the Triodion has nothing.  
**3.** **⊕⊕** Thursday: OF THE EUCHARIST (Corpus Christi). Feast of eight days. The Vigil is transferred to Sunday.""")

    # p566
    parts.append("""[Leaf p566 / Page 564]

#### 2nd Sunday after Pentecost: Vigil of the Eucharist
**1.** With this Sunday begins the cycle of the Tones.  
**2.** **(:** On Thursday: Apodosis of the Feast of the Eucharist.  
**3.** **+** On Friday: Compassion of the Most Holy Theotokos. Feast of one day, with a Polyeleos; and with this is the end of the new Triodion.

### Of the Octoechos

| Day | Service | Dedication |
| :--- | :--- | :--- |
| On Sunday | Service | Resurrectional |
| On Monday | ” | Penitential, and to the Angels |
| On Tuesday | ” | Penitential, and to the Forerunner |
| On Wednesday and Friday | ” | To the Cross, and to the Mother of God |
| On Thursday | ” | To the Apostles, and to St. Nicholas |
| On Saturday | ” | To All Saints, and for the Deceased |""")

    # p567: Tablet I
    parts.append(f"""[Leaf p567 / Page 565]

### Tablet I
#### Dominical Letters and Boundary Keys
For the last 40 years of the Indiction, that is, of the Cycle of 532 years, the 14th from the creation of the world.

{make_table1_en()}""")

    # p568 to p574: Tablet II
    parts.append(f"""[Leaf p568 / Page 566]

### Tablet II
#### Dominical Letters and Boundary Keys
For all 532 years of the 15th Indiction from the creation of the world (Years 1941 to 2000).

{make_table2_page_en(1941, 20)}""")

    parts.append(f"""[Leaf p569 / Page 567]

### Tablet II (Continued: Years 2001 to 2084)

{make_table2_page_en(2001, 28)}""")

    parts.append(f"""[Leaf p570 / Page 568]

### Tablet II (Continued: Years 2085 to 2168)

{make_table2_page_en(2085, 28)}""")

    parts.append(f"""[Leaf p571 / Page 569]

### Tablet II (Continued: Years 2169 to 2252)

{make_table2_page_en(2169, 28)}""")

    parts.append(f"""[Leaf p572 / Page 570]

### Tablet II (Continued: Years 2253 to 2336)

{make_table2_page_en(2253, 28)}""")

    parts.append(f"""[Leaf p573 / Page 571]

### Tablet II (Continued: Years 2337 to 2420)

{make_table2_page_en(2337, 28)}""")

    parts.append(f"""[Leaf p574 / Page 572]

### Tablet II (Concluded: Years 2421 to 2472)

{make_table2_page_en(2421, 18, col3_rows=16)}""")

    # p575: Paschal Differences
    parts.append(f"""[Leaf p575 / Page 573]

### Roman and Greek Paschas
#### Difference
For the last 40 years of the 14th Indiction.[^742]  
Apr. = April. — Mar. = March. — 0 = equal (same day).

{make_pascha_diff_en()}""")

    # p576: Table III upper
    parts.append(f"""[Leaf p576 / Pages 574–575]

### Tablet III: Perpetual Table
Containing 35 Columns of the Sundays of the Entire Year, with Indication of the Regular Gospels and Tones.

{make_table3_p576_en()}""")

    # p577: Table III middle
    parts.append(f"""[Leaf p577 / Pages 576–577]

### Tablet III: Perpetual Table (Continued)
#### Sundays 12 to 29 after Pentecost

{make_table3_p577_en()}""")

    # p578: Table III lower
    parts.append(f"""[Leaf p578 / Pages 578–579]

### Tablet III: Perpetual Table (Concluded)
#### Sundays 30 to 32 after Pentecost, Pre-Lenten Cycle, and Legend of Concurring Gospels

{make_table3_p578_en()}

#### Gospels of Special Sundays of the Menaion
Concurring with the Gospels of the Ordinary Sundays.

- **a)** Sunday of the Holy Fathers of the First Six Ecumenical Councils: July 16.
- **b)** Sunday before the Exaltation.
- **c)** Sunday after the Exaltation.
- **d)** Sunday of the Holy Fathers of the Seventh Ecumenical Council (Second of Nicaea): October 11.
- **e)** Ordinary Sunday concurring with the Sunday of the Forefathers.
- **f)** Sunday of the Holy Forefathers.
- **g)** Sunday of the Holy Fathers.
- **h)** Sunday after the Nativity of Christ.
- **i)** Sunday before the Enlightenment (Theophany).
- **l)** Sunday after the Enlightenment (Theophany).""")

    # p579: Vrazumlenie Skrizhali
    parts.append("""[Leaf p579 / Page 580]

### Explanation of the Tablet

**1.** The Tablet contains 35 Columns of the Sundays of the entire year according to the number of the 35 Boundary Keys, and the 35 Paschal days corresponding to them.

**2.** At the head of the Tablet, that is, in its 1st horizontal row, stand all 35 Boundary Keys; and beneath each key extends a row, or Column, of the Sundays of the entire year, with an indication of the day of the month within whose boundaries these Sundays occur, and their numbers or titles. And the months are written outside the column, on the left, separated from one another by horizontal, red, step-like lines; the day of the month is written inside the Column, while the number or title of the Sunday is written outside the Column, on the right of the Tablet.

**3.** In the 7th row stand all 35 days on which the Sunday of the Publican may occur, with which the Triodion begins.

**4.** In the 8th row stand all 35 Paschal days written in cinnabar (red), corresponding to the 35 Boundary Keys.

**5.** In the 5 rows contained between the Publican and the Boundary Keys, stand all 5 Sundays that can occur between Theophany and the Publican, namely, the Sunday after Enlightenment (Theophany), and the 4 last ordinary Sundays (29th, 30th, 31st, 32nd). However, since not all these Sundays always take place, as we explained on page 159 (for this depends on the earliness or lateness of Pascha), on this account in these 5 rows certain spaces are found blank, which signifies that then the Sundays corresponding to them on the right of the tablet have no place. For example, under the Boundary Key 1 (A), all spaces are blank; it signifies, therefore, that of""")

    # p580: Vrazumlenie Skrizhali (concluded)
    parts.append("""[Leaf p580 / Page 581]

these 5 Sundays not a single one is then taken, but immediately after Theophany the Triodion begins.

**6.** Of the Triodion Sundays we have set down only three, that is, the central one, which is Pascha, and the two extreme ones, namely, that of the Publican, and that of All Saints; but the other intervening ones we have omitted, since it is easy to keep them in memory even without the Tablet, for they usually have special titles, and proper Services corresponding to the titles.

**7.** On the Sundays preceding that of the Publican we have set down neither the Tone nor the Sunday Gospel, for these depend on the preceding Pascha, and on this account one must seek them at the end of the Tablet in the boundaries of January and February under the Boundary Key of the preceding Pascha.

**8.** Beside certain Sundays, red Latin letters are placed. This signifies that then, together with the Gospel of that ordinary Sunday, another Gospel of a certain Sunday of the 10 special ones of the Menaion is also to occur, which we have set down at the end of the Tablet with corresponding Latin letters.[^743]

**9.** After this, if one desires to know which Sundays in a given year ought to be taken between Theophany and the Publican, let one seek first of all the Boundary Key of the coming Pascha, according to the Directory of Tablet I or II, and under it in Tablet III one will find those Sundays; only, if it is a leap year, adhere to the Column immediately following. And if one desires to know which Sunday, Tone, and Sunday Gospel is to be taken on any of the Sundays after the Descent of the Holy Spirit, then know—""")

    return "\n\n---\n\n".join(parts) + "\n"

# -------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------
def main():
    print("Building Source Text...")
    source_text = build_source_text()
    SOURCE_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(SOURCE_OUT, "w", encoding="utf-8") as f:
        f.write(source_text)
    print(f"  Wrote {SOURCE_OUT} ({len(source_text)} chars)")

    print("Building Draft Markdown Translation...")
    draft_text = build_draft_text()
    DRAFT_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(DRAFT_OUT, "w", encoding="utf-8") as f:
        f.write(draft_text)
    print(f"  Wrote {DRAFT_OUT} ({len(draft_text)} chars)")

    print("Building Footnotes File...")
    FOOTNOTES_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(FOOTNOTES_OUT, "w", encoding="utf-8") as f:
        f.write(FOOTNOTES_CONTENT)
    print(f"  Wrote {FOOTNOTES_OUT} ({len(FOOTNOTES_CONTENT)} chars)")

    print("\nExecuting Small Pause Gatekeeper Suite...")
    cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "run_small_pause_gate.py"), "--monument", "1899_dolnytsky_typikon", "--cohort", "29"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.stderr:
        print("STDERR:\n", res.stderr)

    return res.returncode

if __name__ == "__main__":
    sys.exit(main())
