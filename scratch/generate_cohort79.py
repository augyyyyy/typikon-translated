# -*- coding: utf-8 -*-
"""
Cohort 79 Generator Script
Generates:
1. Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/1910_skaballanovich_typikon_cohort79_source.txt
2. Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort79_footnotes.txt
3. Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort79_raw_draft.md
"""

from pathlib import Path

# Paths
base_dir = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon")
source_file = base_dir / "Source Text" / "1910_skaballanovich_typikon_cohort79_source.txt"
footnotes_file = base_dir / "Draft" / "1910_skaballanovich_typikon_cohort79_footnotes.txt"
draft_file = base_dir / "Draft" / "1910_skaballanovich_typikon_cohort79_raw_draft.md"

source_content = """=== LEAF p781 ===
чувстве любви к виновнику торжества, а также приличествует памяти святого, как годичному дню его кончины. В нынешней практике держание свеч народом за бдением сохранилось только для двух дней Страстной седмицы и связанных с нею Вербного воскресенья и пасхальной утрени; на полиелеях же бдений оно сохранилось для священников; впрочем, оно заменяется горением паникадила, о возжжении которого Типикон нигде ничего не говорит. По раздаянии свеч настоятель, «емуже предходит диакон со свещею горящею, кадит Перее на аналогии икону окрест», как средоточную в {с. 647} этот момент святыню,

«и идет во олтарь, и тамо св. трапезу и олтарь весь кадит и во храме святыя местныя иконы вся, таже священнопредстоятелей по обоим странам, и правый лик певцев и левый; посем кадит преходя стоящий народ весь и паки св. двери, и две точию иконы — Христову и Богородицыну, и на аналогии. В тоже время (во время этого каждения) поют величание, со избранными стихи от псалмов Давидовых (в воскресенье затем — тропари Ангельский собор, см. 3 гл. и 8 сентября, аще в неделю). По сем обычном пении ектения от диакона малая глаголется, и седальны поются (ранее их — ипакои воскресный), и входят вси священнослужители (с началом чтения) во святый олтарь, и изоблачаются священных одежд, точию держай чреду иерей остает во облачении, к прочитанию Евангелия».

Обычно каждение начинается после пения в 1-й раз священнослужителями величания.

Ангельский собор

После Непорочных или полиелея поются стоящие в тесной связи с Непорочными тропари «Ангельский собор». Они поются с самым характерным стихом 118 псалма, выражающим его главную мысль, именно 12-м стихом: «Благословен еси, Господи, научи мя оправданием Твоим». Этим заменяется присоединение тропаря к каждому стиху псалма. Составляя, таким образом, одно с этою кафизмою, настоящие тропари и оканчиваются обычным заключением кафизмы: «Слава и ныне», что присоединяется к двум последним тропарям, «аллилуиа 3, слава Тебе Боже, — 3». Поются тропари на тот же 5-й глас, на который положено петь эту (17-ю) кафизму. (Помещаются тропари в приложениях к Октоиху,

=== LEAF p782 ===
Часослову и в Ирмологии). Они, — точнее 4 из всех 6, основные, — изображают чувства, переживавшиеся «собором» (δήμος) Ангелов и мироносицами во время смерти и воскресения Спасителя; 5-й прославляет Св. Троицу, а 6-й — Богоматерь.

История тропарей «Ангельский собор»

Тропари «Ангельский собор» — иерусалимского происхождения. В известном иерусалимском «Последовании» Страстной и Пасхальной седм. IX в. по ркп. 1122 г. в службе Ваий есть из них 2–6, а к 1-му близок начальный («Ангельский собор удивися, зря Тебе на жребя возшедша»); соответствующие 3 тропаря Великой субботы здесь начинаются каждый «Ангельский собор», и 3-й очень близок к нынешнему первому («… вменившася; Адам же ликуя со Евою взываше: погибшее овча аз есмь, воззови мя, Спасе, и спаси мя») [615]. Но Студийским и Евергетид. уставам эти тропари, по-видимому, незнакомы.

Груз. ркп. Иер. уст. в чине воскр. бдения о них: «на Непорочных 3 воскр. стихиры 5 гл.»; греч. ркп. и печ.: «по (άπό) Непорочных (№ 381: говорится: Благословен еси Господи и поются) тропари воскр. гл. 5 Ангельский собор и прочие»; слав. ркп.: «по третией же статии (Непорочных) не рекше Слава и ныне глаголетьс. треп. гл. 5 Ангельский собор». Греч. текст {с. 648} следующие варианты со слав.: 2 — «с милостивыми» — συμπαθώς, «вещаше мироносицам»; 4 — «Спасе, слышаху (ένηχοΰντο) Ангела (Иерус. посл. + ясно) вещающа» [616].

Малая ектения на полиелее

После того потока хвалы и радости, какой представляют собою Непорочны с их тропарями, и особенно полиелей, является потребность в просительной молитве, освежающей и внимание, так долго занятое хвалебными песнями. Малая ектения по полиелее или Непорочных и отвечает этой цели. То или другое и в качестве кафизмы должно иметь ее после себя. Возглас этой ектении: «Яко благословися имя Твое и прославися Царство Твое, Отца…» (почти тождественный с заключительным славословием 8-й утр. мол.) указывает первыми словами своими на содержание 118 пс. и обращает ум молящихся на отрадную мысль о Царстве славы в соответствие (под тон) настоящему ликованию. От этого возгласа так и веет радостью, и он так приноровлен к данному случаю, что более нигде на службах не употребляется, за исключением пасхальной утрени, на которой он положен по 8

=== LEAF p783 ===
песни канона, и в распространенном виде — на великосубботней утрене по 1 статье Непорочных. Об этой ектении говорит только Служебник.

Возглас полиелейной ектении в древности

В старых греч. Евх. возглас: «Яко благословися и прославися пречестное и великолепое имя Твое»; в ркп. слав. Тип. до XV в.: «Яко Бог милости…»; в слав. Служебн., Венеция, 1544 г.: "по 3 кафисме возглас «Яко благословися и прославися», по 4 кафисме: «Яко святися и прославися»", в Служ. Петра Могилы 1-й по Непорочных и по 3-й кафизме, «егда чтется», 2-й «аще случится в неделю полиелей» (следовательно, бывал полиелей и при Непорочных с ектенией по том и другом); в Служебн. Моск. 1602 г. (старообр.) и 1647 г.: «по Непор.: Яко благословися и прославися, аще же есть святому полиелеос, по многомилостивом: Яко Ты еси освящение наше». С Моск. 1658 г. и позднейш. греч., как ныне [617].

Ипакои

Теперь по общему чину кафизм, одной из которых является полиелей или Непорочны, следовало бы петься седальну. Но на воскресной утрене седален по столь великой кафизме, какова эта, заменяется более торжественною песнью — ипакои (υπακοή). Происходя от глагола υπακούω, прислушиваться, иногда — отвечать, откликаться, это слово (кроме литургического языка употребляется только в Новом Завете в значении «послушание») в качестве литургического термина имеет значение «припев». По идее ипакои, следовательно, должен быть припевом (народа) к стихам Непорочных, {с. 649} и, заступая место седальна после них (или после полиелея), отличается от него и тем, что, подобно «кафизме», к которой присоединяется, не имеет разрешения на выслушивание его сидя. По всему этому он и короче седальна. Кроме воскресной утрени, он употребляется лишь в самые великие из двунадесятых праздников и им подобных дней (Рождество Христово, Крещение, Неделя ваий, Пасха, Успение, 29 июня, Неделя Фомина, Неделя праотец и отец), но уже по 3 песни канона. Напев — близкий к седальнам.

История его

=== LEAF p784 ===
В IV в. подпевание к каждому стиху псалма какого-либо стиха называлось ΰπηχεΐν, ΰπακούειν, а этот подпеваемый стих назывался υπακοή. Афанасий Великий говорит о псалмах, имеющих υπακοή аллилуиа; св. Иоанн Златоуст указывает в качестве ύпакоαί к некоторым псалмам их стихи, например к пс. 117 стих «Сей день». Блж. Августин такое подпевание называет respondere [618]. Следовательно, ипакои первоначально соответствовал лат. респонсорию, стиху псалма, сопровождавшему чтение (Св. Писания или отцев); и нынешний ипакои всегда предшествует чтению и довольно краток. К песнопениям небиблейским название ипакои не прилагалось еще в VII в.: он не упоминается в известном описании синайской утрени. В иерус. «Последовании» IX–X в. есть нынешние ипакои Недели ваий и Пасхи с этим названием [619]. По Студийско-Алексиевскому уставу ипакои («упакои») в исключительных, впрочем, случаях (но здесь след, должно быть, древней общей практики) пелся так: первый раз певцом, затем народом, певец — псалмический стих к нему, народ опять ипакои, певец — конец его [620].

Воскресные ипакои

Большинство воскресных ипакоев, именно 1–5 и 8 гл., воспевают посещение живоносного гроба мироносицами, — соответственно Непорочным тропарям, к которым они так непосредственно примыкают, и тому часу ночи, когда они поются (потому, кроме утрени, они поются и на полунощнице). Остальные рисуют плоды воскресения. Каждый следующий продолжает описание предыдущего. С краткостью здесь соединена сила выражения (например, начало 1-го: «Разбойничо покаяние рай окраде»).

По древним уставам

Автор воскресных ипакоев неизвестен. Древнейшее упоминание о них — в Студийско-Алексиевском и Евергетидском уставах: в обоих они пелись по кафизмах; в первом то по 1, то по 2-й кафизме; в последнем — по 2-й [621]. Груз. и греч. ркп. Иерус. уст.: «и ипакои», древнейшие слав.: «и поется {с. 650} ипакои»; поздн. (ркп. Моск. Син. б. № 678 XV в.) опускают «поется». В Киево-Печерской лавре читается.

Полиелейное чтение

=== LEAF p785 ===
Ипакои, как и седален, составляет, собственно, песненное введение к следующему за ним святоотеческому чтению, которое в воскресенье, как и по кафизмах, должно иметь предметом изъяснение литургийного Евангелия или Апостола. В воскресенья, с которыми соединяются особые воспоминания, взамен этого бывает «чтение праздника». Здешнее чтение, будучи необходимым для отдыха певцов и слушателей перерывом в том потоке песней, который, начинаясь с полиелея, простирается до Евангелия, составляет обычное для псалтирного пения заключение.

=== LEAF p786 ===
СТЕПЕННЫ

Псалтирное пение теперь сменяется подражательным ему христианским, и заканчивающее такое пение чтение здесь бывает величайшим. Разумеем степенны и Евангелие. Степенны (αναβαθμοί), в просторечии называемые за способ пения их антифонами, как показывает название, составляют подражание псалмам 119–133, надписанным «песни степеней». Такое надписание псалмов (с евр. «восхождений», Вульгата: graduum) объясняют ныне так, что эти псалмы пелись праздничными паломниками в Иерусалиме при подъеме на его возвышенность, или партиями возвращавшихся из плена (прежде объясняли название так, что эти псалмы пелись на ступенях лестницы из храмового двора женщин во двор израильтян, — на том основании, что раввины сравнивали эти псалмы с 15 ступенями той лестницы). Под впечатлением недавних бедствий избранного народа, псалмы эти часто говорят о ценности для последнего Иерусалима и храма и внушают чувство крепкой надежды на Бога, способной усладить горесть всяких бедствий. Эти-то псалмы и легли в основу степенных антифонов. Для каждого гласа -3 степенна, по 3 антифона в каждом, только для 8 гл. 4 степенна. Каждый антифон поется дважды, по разу правым и левым хорами. Степенны 5–8 гл. параллельны (как и гласы) степенным 1–4 гл. и подражают в 1 и 5 гл. пс. 119–121, 2 и 6 гл. — 122–124, 3 и 7 гл. — 125–127, 4 и 8 гл. — 128–132. Они содержат молитву об исправлении и очищении души и выражают надежду на это исправление; так как оно достигается благодатью Духа Святого, то каждый 3-й стих (антифон) посвящен Его прославлению. Частнее — степенны то заключают молитву к Богу, чтобы он просветил «меня» добродетелью, спас от страстей, греховного огня, от диавола, то стараются сообщить надежде на Бога непоколебимость и любви к Нему крепость, описывают благодать Церкви, сладость пустынного жития и молитвы во храме (которая в воскресный день сменяла для древнего монаха келейную молитву — «о рекших мне во дворы внидем Господни»).

Таким образом, степен{с. 651}ны имеют общеназидательное (не специально воскресное), аскетическое содержание, как вообще в воскресную службу введено много общеназидательного элемента, ввиду того, что на воскресенье Церковь смотрит не только как на день для прославления этого события, но и как на день, в который христианин, занятый целую неделю житейскими заботами, может подумать и о душе. Но и при таком содержании степенны вяжутся с воспоминанием воскресения, напоминая о

=== LEAF p787 ===
спогребении Христу для совоскресения с Ним (ср. Апостол Великой субботы). Напев антифонов сложнее тропарного и седального; в нем звучит торжество победы над страстями. Особую красоту их пению сообщает повторение каждого стиха обоими ликами без припевов, исключая последний стих (в честь Духа Святого), который, как заключительный, имеет припев Слава и ныне, благодаря чему прославление Святого Духа предваряется прославлением Св. Троицы. Число 9 для антифонов каждого гласа могло быть выбрано на основании видения св. Игнатия, что 9 чинов Ангельских попеременно воспевали Св. Троицу.

История степенн

Степенны по слогу настолько отличаются от Дамаскиновых песнопений Октоиха, что уже Никифор Каллист, а вслед за ним Никодим Святогорец, считали автором их св. Феодора Студита [622], и помечены его именем, по-видимому, в ркп. Бодлеевой библ. И по содержанию они соответствуют всему направлению литературной деятельности св. Феодора (все же новейшие византологи не помещают их в числе его творений). Они упоминаются Ипотипосисом на нынешнем месте воскресной утрени [623]. По Ал. — Студиевскому уставу на праздничной утрене, не имевшей ни Непорочных, ни полиелея, это была самая торжественная часть. По этому уставу степенны пелись со стихами степенных псалмов: в каждом степенне 1 ант. без стихов впереди, затем 4 стиха псалма, причем 1-й с аллилуиа и нененайками, ант. 2-й, 4 других стиха псалма с такими же прибавками к 1-му ст. и ант. 3-й (Святому Духу) [624].

Звон к Евангелию

Степенны своим аскетическим содержанием очищают, «возвышают» душу и этим подготовляют молящихся к слушанию Евангелия. О предстоящем чтении последнего возвещается во время пения степени звоном «в кампаны», т. е. трезвоном. Этот звон указывает на то, что «во всю землю изыде вещание» Евангелия. Евангелие только воскресной и праздничной утрени имеет пред собою звон, а литургийное — нет, потому что последнее часто не {с. 652} имеет отношения к воспоминаемому событию и потому что на литургии звоном отмечается более священный момент. Практика переносит звон к утреннему Евангелию на начало полиелея [625]. «Иерей же и диакон, вшедше во святилище, облачатся по обычаю», — если не было полиелея, к

=== LEAF p788 ===
которому нужно было облачиться, или если облачение снималось на чтение.

По старым уставам

Груз. ркп.: «кандиловжигатель звонит в железное; священник и диакон облачаются»; греч.: «отходит кандилаптис и знаменает (в) железное»; древн. слав.: «кандилаптис шед знаменает в железное, иерей же в алтари облачится (в священныя ризы)»; поздн. (с XV в.): «параекклисиарх шед ударяет в един кампан…»; старообр.: «+ или в железное било» (нет о облачении) [626].

=== LEAF p789 ===
ПРОКИМЕН УТРЕНИ

Более непосредственным, чем степенны, подготовлением к утреннему Евангелию служит прокимен. Прокимен утрени всегда содержит прославление празднуемого события, тогда как вечерний не имеет отношения к нему (за немногими исключениями). Это, следовательно, всегда праздничный прокимен. Он имеет не такой напев, как вечерний и литургийный (почему обычно поется речитативом), но являясь не самостоятельною песнью, как вечерний, а служа лишь подготовлением к Евангелию, он никогда не поется с такою торжественностью, как некоторые вечерние прокимны, т. е. всегда поется только 2 1/2 (а не 4 1/2) раза. И возгласы пред ним менее сложны. «И глаголет (диакон): Вонмем, премудрость. Канонарх же сказует: Прокимен, псалом Давидов, гласа», т. е. канонарх произносит: «Прокимен, псалом Давидов, глас N». Таким образом, здесь пред прокимном нет преподания мира и второго вонмем, потому что то и другое будет пред Евангелием. Непонятно, почему на утрене только указывается называть, откуда взят прокимен («Псалом Давидов»); впрочем, то же, по-видимому, указывается делать и для прокимнов великопостных вечерен, и для литургийных, если они берутся не из Псалтири; так, пред прокимном «Величит душа Моя» прибавляется «песнь Богородицы», пред прокимном «Благословен еси, Господи Боже отец наших» — «песнь отцев». В Киево-Печерской лавре не возглашается «псалом Давидов».

{с. 653}

По древним уставам

В греч. Тип. о прокимне глухо (груз. и не упоминает); слав. XIV в.: «диак.: вонмем, иерей: мир всем, мы: и дух. тв., диак.: премудр., певец глаголеть псалом Давидов, диак.: вонмем; поет певец прок. наст. гласа и мы поем тожь, таже певец поет стих и мы прок., и паки певец прок., мы же поем близ конца прок., таже певец поет конец». В поздн. глухо.

В Служебн. Моск. 1602 и 1647 г., старообр. Служебнике и уставе + мир всем и 2-е вонмем; в остальных слав. и греч. — глухо [627]. Так как прокимен — остаток ветхозаветного чтения, которое в древности всегда предшествовало новозаветным, так как он был как бы песненным чтением Псалтири (Вступ. гл., 162), а пред чтением всегда объявлялось,

=== LEAF p790 ===
откуда оно, то, должно быть, то же делалось ранее всегда и пред прокимном.

При Арсении Суханове на Востоке утр. прокимен пелся хорами трижды (целый) без всяких возгласов и стихов [628].

Воскресные прокимны утрени

И прокимен воскресной вечерни посвящен событию воскресения Христова, но он так прямо не относится к этому событию и не говорит о нем с такою ясностью, как утренний прокимен, в котором большей частью есть и самое понятие «воскресение». Это потому, что он готовит к Евангелию о воскресении. Кроме того, от вечернего прокимна утренний отличается тем, что он не один и тот же для каждого воскресенья, а изменяется по гласам. Таким образом, воскресных утренних прокимнов 8. Для них выбраны из псалмов преимущественно те стихи, где говорится о том особом, непосредственном действии Промысла, которое древний еврей образно называл поднятием, «возстанием», евр. cum, Господа как бы от ложа обычного покоя Его, — слово, передаваемое у LXX чрез άνίστημι, которое означает, кроме поднятия с ложа, и воскресение. Именно, воскресные утренние прокимны и их стихи взяты из следующих псалмов:

1. гл. «Ныне воскресну, глаголет Господь» — из Пс. 11:6, 7.
2. гл. «Возстани, Господи Боже мой, повелением» — Пс. 7:8, 2.
3. гл. «Рцыте во языцех, яко Господь воцарися» — Пс. 95:10, 1.
4. гл. «Воскресни, Господи, помози нам» — Пс. 43:27, 2.
5. гл. «Воскресни, Господи Боже мой… яко Ты царствуеши» — Пс. 9:33, 2.
6. гл. «Господи, воздвигни силу Твою (т. е. Христа)» — Пс. 79:3, 2.
7. гл. «Воскресни, Господи Боже мой… не забуди» — Пс. 9:33, 2.
8. гл. «Воцарится Господь во век» — Пс. 145:10, 1.

Тема прокимнов 3 и 8 гл. совпадает с вечерним прокимном. В 8 гл., как заключительном, наиболее уместно «во век», как и вообще ряд прокимнов дает некоторое развитие мысли (1 гл. — только обещание {с. 654} воскресения и вообще спасения, о котором Господь говорит открыто, «не обинюся», παρρησιάсоμαι). Стихами к прокимнам, как и вообще делается, берутся начальные стихи тех псалмов, из которых прокимны (остаток практики, когда с подпеванием прокимна пелся целый псалом); исключение — прокимен 1 гл., где стих выбран более подходящий к прокимну: «Словеса Господня — словеса чиста» —
"""

source_file.parent.mkdir(parents=True, exist_ok=True)
with open(source_file, "w", encoding="utf-8") as f:
    f.write(source_content.strip() + "\n")
print(f"Wrote source file: {source_file}")

footnotes_content = """[^2449]: Papadopoulos-Kerameus, A., *Analekta hierosolymitikēs stachyologias* [Gr. Ἀνάλεκτα ἱεροσολυμιτικῆς σταχυολογίας], II, 163 [printed 6, 163].
[^2450]: *Horologion* [Gr. Ὡρολόγιον], 98.
[^2451]: *Euchologion* [Gr. Εὐχολόγιον], Venice, 1622, fol. 4v; *Sluzhebnik* of Peter Mohyla, 84–85; Moscow, 1602, fols. 38–39; 1647, fol. 39; 1658, fol. 127; MS of the Moscow Synodal Library No. 328/383, fol. 7.
[^2452]: St. Athanasius the Great, *Letter to Marcellinus* [*Epistula ad Marcellinum*]; St. John Chrysostom, *Homilies on Psalms 117, 111, 144*; St. Augustine, *Expositions on Psalm 41*.
[^2453]: Papadopoulos-Kerameus, A., *Analekta hierosolymitikēs stachyologias* [Gr. Ἀνάλεκτα ἱεροσολυμιτικῆς σταχυολογίας], II [printed 8], 192.
[^2454]: MS of the Moscow Synodal Library No. 330/380, fol. 107v.
[^2455]: Ibid., and fol. 4; Dmitrievsky, A., *Typika* [Gr. Τυπικά], 608.
[^2456]: Nikephoros Kallistos, *Exposition of the Degrees* [*Iz'yasnenie stepeney*]; Nicodemus the Hagiorite, *Nea Klimax* [Gr. Νέα κλῖμαξ], 1844, 13, according unto Archbishop Modest (*On the Church Octoechos*, Vilna, 1865, pp. 22ff.), who proves that the 'chief shepherd' mentioned in the antiphons is the brother of St. Theodore, St. Joseph, Archbishop of Thessalonica (for which reason the antiphons with such a mention are sung today in the East by the hierarch).
[^2457]: Dmitrievsky, A., *Typika* [Gr. Τυπικά], 229.
[^2458]: MS of the Moscow Typography Library No. 285/342/1206, fols. 90v–99v, where the Anabathmoi of Tone 1 are set to musical notation.
[^2459]: If for this one might still find some justification, then for the fact that this ringing in certain places is made upon a single bell—none whatever.
[^2460]: Kekelidze, K., Archpriest, *Liturgicheskie gruzinskie pamyatniki* [Georgian Liturgical Monuments], 318; MSS of the Moscow Rumyantsev Museum, Sevastyanov Coll. No. 491/35, fol. 5; Synodal Library, Greek No. 381, fol. 5v; Slavic Typikon No. 328/383, fol. 7; No. 329/384, fol. 18; No. 678/386, fol. 8v; Kyiv Theological Academy Museum Aa 194, p. 30; Old Believer Typikon, (8) fol. 15v.
[^2461]: For citations, see p. 652, note 2; p. 648, note 2 [of the original Russian edition].
[^2462]: *Proskynitarion*, ch. 46, p. 239.
"""

footnotes_file.parent.mkdir(parents=True, exist_ok=True)
with open(footnotes_file, "w", encoding="utf-8") as f:
    f.write(footnotes_content.strip() + "\n")
print(f"Wrote footnotes file: {footnotes_file}")

draft_content = """=== LEAF p781 ===
...the feeling of love toward the Author of the triumph, and likewise befits the memory of the saint, as the annual anniversary of his repose. In present practice, the holding of candles by the people during the Vigil has been preserved only for two days of Passion Week and the Palm Sunday and Paschal Matins connected therewith; at the Polyeleos of Vigils, however, it has been preserved for the priests; moreover, it is replaced by the burning of the chandelier (*panikadilo*), concerning the kindling of which the Typikon nowhere says anything. After the distribution of candles the superior, "preceded by the deacon with a burning candle, censes first round about the icon upon the analogion," as the focal *(Orig. p. 647)* sanctuary at this moment,

"and goes into the altar, and there censes the Holy Table and the entire altar, and all the holy local icons in the temple, and then the presiding clergy on both sides, and the right choir of chanters and the left; thereafter he censes passing through all the standing people, and again the Holy Doors, and only two icons—of Christ and of the Mother of God, and that upon the analogion. At the same time (during this censing) they sing the Magnification (*velichanie*), with selected verses from the Psalms of David (on Sunday thereafter—the troparia **"The assembly of the Angels,"** see Chapter 3 and September 8, if on a Sunday). After this customary singing, the Little Ektenia is said by the deacon, and the sessional hymns are sung (prior unto them—the Sunday Hypakoe), and all the clergy enter (with the beginning of the reading) into the holy altar and divest themselves of the sacred vestments, only the priest holding the weekly turn remaining in vestments for the reading of the Gospel."

Customarily the censing begins after the singing of the Magnification for the first time by the clergy.

### "The Assembly of the Angels" (*Angel'skiy sobor*)

After the Blameless or the Polyeleos there are sung the troparia **"The assembly of the Angels"** (*Angel'skiy sobor*), which stand in close connection with the Blameless. They are sung with the most characteristic verse of Psalm 118 [LXX; Masoretic 119], expressing its main thought, namely verse 12: **"Blessed art Thou, O Lord, teach me Thy statutes"** (*Blagosloven esi, Gospodi, nauchi mya opravdaniem Tvoim*). By this is replaced the appending of a troparion unto every verse of the psalm. Constituting thus one whole with this kathisma, these present troparia likewise conclude with the customary conclusion of a kathisma: **"Glory... Both now..."** subjoined unto the final two troparia, and **"Alleluia, alleluia, alleluia, glory to Thee, O God"** (thrice). The troparia are sung in the same Tone 5 in which this (17th) Kathisma is appointed to be sung. (The troparia are located in the appendices unto the Octoechos,

=== LEAF p782 ===
...the Horologion, and in the Heirmologion). They—more precisely, four of all six, the primary ones—depict the feelings experienced by the 'assembly' (*dēmos*, Gr. δῆμος) of the Angels and by the Myrrh-bearers at the time of the death and Resurrection of the Savior; the 5th glorifies the Holy Trinity, and the 6th—the Mother of God.

### History of the Troparia "The Assembly of the Angels" (*Istoriya troparey "Angel'skiy sobor"*)

The troparia **"The assembly of the Angels"** are of Jerusalem origin. In the well-known Jerusalem *Order of Passion and Paschal Week* of the 9th century according unto MS 1122, in the service of Palm Sunday there are troparia 2–6 of them, while unto the 1st the opening one is close (**"The assembly of the Angels was astonished, beholding Thee mounted upon a colt"**); the corresponding three troparia of Holy Saturday here each begin with **"The assembly of the Angels,"** and the 3rd is very close unto the present first (**"...being numbered; while Adam exulting with Eve cried aloud: I am the lost sheep, call me back, O Savior, and save me"**) [^2449]. Yet unto the Studite and Evergetis typika these troparia, apparently, are unfamiliar.

The Georgian MS of the Jerusalem Typikon in the order of the Sunday Vigil says concerning them: 'at the Blameless, three Sunday stichera of Tone 5'; the Greek MSS and printed editions: 'after (*apo*, Gr. ἀπό) the Blameless (No. 381: is said: **Blessed art Thou, O Lord**, and are sung) the Sunday troparia of Tone 5, **The assembly of the Angels**, and the rest'; the Slavic MSS: 'after the third stasis (of the Blameless), not having said **Glory... Both now...**, are said the troparia of Tone 5, **The assembly of the Angels**.' The Greek text *(Orig. p. 648)* [gives] the following variants with the Slavonic: 2—'with merciful tears'—*sympathōs* (Gr. συμπαθῶς), 'spoke unto the myrrh-bearers'; 4—'O Savior, heard (*enēchounto*, Gr. ἐνηχοῦντο) the Angel (Jerusalem Order + clearly) speaking' [^2450].

### The Little Ektenia at the Polyeleos (*Malaya ekteniya na polielee*)

After that torrent of praise and joy which the Blameless with their troparia, and especially the Polyeleos, represent, there arises the need for a prayer of supplication, refreshing likewise the attention that has been so long occupied with songs of praise. The Little Ektenia after the Polyeleos or the Blameless answers precisely this purpose. Either of these, moreover, as a kathisma must have it thereafter. The exclamation of this ektenia: **"For blessed is Thy Name, and glorified is Thy kingdom, of the Father, and of the Son, and of the Holy Spirit..."** (almost identical with the concluding doxology of the 8th Matins Prayer) indicates by its opening words the content of Psalm 118 [LXX; Masoretic 119] and directs the mind of the worshippers unto the consoling thought of the Kingdom of glory in harmony with (setting the tone for) the present rejoicing. From this exclamation joy fairly breathes forth, and it is so adapted unto this occasion that it is nowhere else used in the services, with the exception of Paschal Matins, at which it is appointed after Ode 8

=== LEAF p783 ===
...of the Canon, and in an extended form—at Holy Saturday Matins after the 1st Stasis of the Blameless. Concerning this ektenia speaks only the Sluzhebnik.

### The Exclamation of the Polyeleos Ektenia in Antiquity (*Vozglas polieleynoy ektenii v drevnosti*)

In old Greek Euchologia the exclamation is: **"For blessed and glorified is Thy most honorable and majestic Name"**; in MSS of the Slavic Typikon prior unto the 15th century: **"For Thou art a God of mercy..."**; in the Slavic Sluzhebnik, Venice, 1544: 'after the 3rd Kathisma the exclamation: **"For blessed and glorified,"** after the 4th Kathisma: **"For holy and glorified art Thou"**'; in the Sluzhebnik of Peter Mohyla: the 1st after the Blameless and after the 3rd Kathisma, 'when it is read,' the 2nd 'if a Polyeleos happens on a Sunday' (consequently, a Polyeleos occurred even along with the Blameless, with an ektenia after both the one and the other); in the Moscow Sluzhebnik of 1602 (Old Believer) and 1647: 'after the Blameless: **"For blessed and glorified,"** but if there is a Polyeleos unto a saint, after the Many-Merciful: **"For Thou art our sanctification"**.' From the Moscow 1658 edition and later Greek editions, it is as today [^2451].

### The Hypakoe (*Ipakoi*)

Now, according unto the general order of kathismata, of which the Polyeleos or the Blameless is one, a sessional hymn ought to be sung. But at Sunday Matins the sessional hymn after so great a kathisma as this is replaced by a more solemn hymn—the Hypakoe (*hypakoē*, Gr. ὑπακοή). Derived from the verb *hypakouō* (Gr. ὑπακούω), to listen attentively, at times to answer, to respond, this word (which outside liturgical language is used only in the New Testament in the meaning of 'obedience') in the capacity of a liturgical term has the meaning of 'refrain.' According unto the idea of the Hypakoe, therefore, it ought to be a refrain (of the people) unto the verses of the Blameless, *(Orig. p. 649)* and, taking the place of the sessional hymn after them (or after the Polyeleos), differs from it also in that, like the 'kathisma' unto which it is subjoined, it has no permission for listening unto it sitting. On account of all this, it is also shorter than a sessional hymn. Besides Sunday Matins, it is used only on the greatest of the Twelve Great Feasts and days similar unto them (the Nativity of Christ, Theophany, Palm Sunday, Pascha, the Dormition, June 29 [Ss. Peter and Paul], Thomas Sunday, the Sunday of the Forefathers and of the Fathers), but then already after Ode 3 of the Canon. Its melody is close unto that of the sessional hymns.

### Its History (*Istoriya ego*)

=== LEAF p784 ===
In the 4th century, the chanting in response unto each verse of a psalm of any verse was called *hypēchein* (Gr. ὑπηχεῖν), *hypakouein* (Gr. ὑπακούειν), and this responsive verse was called *hypakoē* (Gr. ὑπακοή). St. Athanasius the Great speaks of psalms having as their *hypakoē* 'Alleluia'; St. John Chrysostom indicates as *hypakoai* (Gr. ὑπακοαί) unto certain psalms their verses, for example unto Psalm 117 [LXX; Masoretic 118] the verse **"This is the day."** Blessed Augustine calls such responsive singing *respondere* [^2452]. Consequently, the Hypakoe originally corresponded unto the Latin responsory, the psalm verse that accompanied a reading (from Holy Scripture or the Fathers); and the present Hypakoe always precedes a reading and is quite brief. Unto non-biblical hymns the designation 'Hypakoe' was not yet applied in the 7th century: it is not mentioned in the well-known description of the Sinaitic Matins. In the Jerusalem *Order* of the 9th–10th centuries there are our present Hypakoai of Palm Sunday and Pascha under this title [^2453]. According unto the Studite-Alexis Typikon, the Hypakoe (*upakoi*) in exceptional cases, however (though here is a trace, presumably, of an ancient general practice), was sung thus: the first time by the chanter, then by the people; the chanter chanted the psalm verse unto it, the people again the Hypakoe, and the chanter—its conclusion [^2454].

### Sunday Hypakoai (*Voskresnye ipakoi*)

The majority of the Sunday Hypakoai, namely of Tones 1–5 and 8, celebrate the visit of the life-bearing tomb by the Myrrh-bearing women—correspondingly unto the Troparia of the Blameless, unto which they so directly adjoin, and unto that hour of the night when they are sung (for which reason, besides Matins, they are sung also at the Midnight Office). The remaining ones depict the fruits of the Resurrection. Each subsequent one continues the description of the preceding. With brevity there is united here power of expression (for example, the beginning of that of Tone 1: **"The repentance of the thief plundered Paradise"**).

### According to Ancient Typika (*Po drevnim ustavam*)

The author of the Sunday Hypakoai is unknown. The earliest mention of them is in the Studite-Alexis and Evergetis typika: in both they were sung after the kathismata; in the former at times after the 1st, at times after the 2nd Kathisma; in the latter—after the 2nd [^2455]. The Georgian and Greek MSS of the Jerusalem Typikon: 'and the Hypakoe'; the earliest Slavic MSS: 'and there is sung *(Orig. p. 650)* the Hypakoe'; later ones (MS of the Moscow Synodal Library No. 678 of the 15th century) omit 'is sung.' In the Kyiv-Pechersk Lavra it is read.

### The Polyeleos Reading (*Polieleynoe chtenie*)

=== LEAF p785 ===
The Hypakoe, like the sessional hymn, constitutes, properly speaking, a hymnographic introduction unto the patristic reading that follows after it, which on Sunday, as also after the kathismata, ought to have as its subject the exposition of the Gospel or Epistle of the Divine Liturgy. On Sundays with which special commemorations are joined, in place of this there is the 'reading of the feast.' The reading here, being a pause necessary for the rest of the singers and hearers in that stream of hymns which, beginning with the Polyeleos, extends unto the Gospel, constitutes the conclusion customary for psalmody.

=== LEAF p786 ===
# THE ANABATHMOI (*Stepenny*)

Psalm singing is now replaced by Christian singing imitative thereof, and the reading that concludes such singing is the greatest here. We mean the Anabathmoi (*Hymns of Degrees*) and the Gospel. The Anabathmoi (*anabathmoi*, Gr. ἀναβαθμοί), in popular parlance called antiphons on account of their manner of singing, as the title shows, constitute an imitation of Psalms 119–133 [LXX; Masoretic 120–134], inscribed **"Songs of Degrees"** (*pesni stepeney*). Such an inscription of the psalms (from the Hebrew 'ascents' [*ma'aloth*], Vulgate: *graduum*) is explained today in that these psalms were sung by festal pilgrims in Jerusalem upon ascending its heights, or by bands of those returning from the captivity (formerly the title was explained in that these psalms were sung upon the steps of the stairway from the temple Court of the Women into the Court of the Israelites—on the ground that the rabbis compared these psalms unto the 15 steps of that stairway). Under the impression of the recent calamities of the chosen people, these psalms frequently speak of the value unto the latter of Jerusalem and the temple, and inspire a feeling of steadfast hope in God, capable of sweetening the bitterness of all afflictions. It is these psalms that formed the foundation of the gradual antiphons (*stepennye antifony*). For each tone there are 3 gradual hymns (*stepenna*), with 3 antiphons in each, only for Tone 8 are there 4 gradual hymns. Each antiphon is sung twice, once by the right and once by the left choir. The Anabathmoi of Tones 5–8 are parallel (as are the tones) unto the Anabathmoi of Tones 1–4, and imitate in Tones 1 and 5 Psalms 119–121 [LXX; Masoretic 120–122], in Tones 2 and 6—122–124 [LXX; Masoretic 123–125], in Tones 3 and 7—125–127 [LXX; Masoretic 126–128], in Tones 4 and 8—128–132 [LXX; Masoretic 129–133]. They contain a prayer for the correction and purification of the soul, and express hope for this correction; since this is attained through the grace of the Holy Spirit, every 3rd verse (antiphon) is dedicated unto His glorification. More particularly, the Anabathmoi either contain a prayer unto God that He enlighten 'me' with virtue, save from passions, from the fire of sin, from the devil, or they strive to impart unto hope in God steadfastness and unto love for Him strength, describing the grace of the Church, the sweetness of the eremitic life and of prayer in the temple (which on Sunday replaced for the ancient monk the prayer of the cell—**"Concerning them that said unto me: We will go into the courts of the Lord"**).

Thus the Anabathmoi *(Orig. p. 651)* have a generally edifying (not specifically Sunday), ascetic content, just as in general into the Sunday service much generally edifying material has been introduced, in view of the fact that the Church looks upon Sunday not only as a day for the glorification of this event, but also as a day wherein the Christian, occupied the entire week with worldly cares, can reflect upon his soul. Yet even with such a content, the Anabathmoi are knit together with the commemoration of the Resurrection, reminding us of

=== LEAF p787 ===
...being buried together with Christ in order to be co-resurrected with Him (cf. the Epistle of Holy Saturday [Rom. 6:3–11]). The melody of the antiphons is more complex than the troparic and sessional melodies; in it sounds forth the triumph of victory over the passions. A special beauty is imparted unto their singing by the repetition of each verse by both choirs without refrains, excepting the final verse (in honor of the Holy Spirit), which, as concluding, has the refrain **"Glory... Both now..."**, by virtue of which the glorification of the Holy Spirit is preceded by the glorification of the Holy Trinity. The number 9 for the antiphons of each tone could have been chosen on the basis of the vision of St. Ignatius, that 9 ranks of Angels alternately chanted praise unto the Holy Trinity.

### History of the Anabathmoi (*Istoriya stepenn*)

The Anabathmoi in their style differ so much from the Damascene hymns of the Octoechos that already Nikephoros Kallistos, and following him Nicodemus the Hagiorite, considered St. Theodore the Studite to be their author [^2456], and they are inscribed with his name, apparently, in a MS of the Bodleian Library. And in content they correspond unto the entire direction of the literary activity of St. Theodore (nevertheless modern Byzantinists do not place them among his works). They are mentioned by the *Hypotyposis* at the present place of Sunday Matins [^2457]. According unto the Alexis-Studite Typikon, at festal Matins, which had neither the Blameless nor the Polyeleos, this was the most solemn part. According unto this Typikon, the Anabathmoi were sung with the verses of the Gradual Psalms: in each gradual hymn 1 antiphon without verses beforehand, then 4 verses of the psalm, with the 1st accompanied by 'Alleluia' and *nenenaika* [melismatic syllables], antiphon 2, four other verses of the psalm with the same additions unto the 1st verse, and antiphon 3 (unto the Holy Spirit) [^2458].

### The Peal for the Gospel (*Zvon k Evangeliyu*)

The Anabathmoi by their ascetic content purify and 'elevate' the soul, and thereby prepare the worshippers for the hearing of the Gospel. Concerning the impending reading of the latter, announcement is made during the singing of the Gradual Antiphons by the ringing 'on the bells' (*v kampany*), that is, a festive peal (*trezvon*). This ringing indicates that 'their sound has gone forth into all the earth'—the proclamation of the Gospel. Only the Gospel of Sunday and festal Matins has a bell-ringing before it, whereas that of the Divine Liturgy has none, because the latter often has no *(Orig. p. 652)* connection with the commemorated event and because at the Divine Liturgy a more sacred moment is marked by ringing. Practice transfers the ringing for the Matins Gospel unto the beginning of the Polyeleos [^2459]. 'And the priest and the deacon, having entered into the sanctuary, vest according unto custom'—if there were no Polyeleos, for

=== LEAF p788 ===
...which it was necessary to vest, or if the vestments were removed for the reading.

### According to Old Typika (*Po starym ustavam*)

The Georgian MS: 'the lamp-lighter rings upon the iron; the priest and the deacon vest'; the Greek: 'the lamp-lighter (*kandilaptēs*, Gr. κανδηλάπτης) departs and gives the signal upon the iron'; the ancient Slavic: 'the lamp-lighter having gone forth gives the signal upon the iron, while the priest in the altar vests (in sacred robes)'; later ones (from the 15th century): 'the paraecclesiarch having gone forth strikes upon a single bell...'; the Old Believer: '+ or upon the iron semantron' (it says nothing concerning vesting) [^2460].

=== LEAF p789 ===
# THE MATINS PROKEIMENON (*Prokimen utreni*)

A more direct preparation for the Matins Gospel than the Anabathmoi is served by the Prokeimenon. The Matins Prokeimenon always contains a glorification of the commemorated event, whereas the Vesperal Prokeimenon has no relation unto it (with a few exceptions). This, consequently, is always a festal prokeimenon. It has not such a melody as the Vesperal and Liturgical prokeimena (for which reason it is usually sung in recitative), yet being not an independent chant like the Vesperal one, but serving merely as a preparation for the Gospel, it is never sung with such solemnity as certain Vesperal prokeimena, that is, it is always sung only 2 1/2 (and not 4 1/2) times. And the exclamations before it are less complex. 'And the deacon says: **"Let us attend. Wisdom."** The canonarch then announces: **"The Prokeimenon, a Psalm of David, of Tone..."**,' that is, the canonarch pronounces: **"The Prokeimenon, a Psalm of David, Tone N."** Thus here before the prokeimenon there is no imparting of peace and no second **"Let us attend,"** because both the one and the other will take place before the Gospel. It is incomprehensible why at Matins alone it is directed to name whence the prokeimenon is taken (**"A Psalm of David"**); however, the same, apparently, is directed to be done both for the prokeimena of Lenten Vespers and for the Liturgical ones if they are taken not from the Psalter; thus, before the prokeimenon **"My soul doth magnify the Lord"** there is added 'the Canticle of the Theotokos,' and before the prokeimenon **"Blessed art Thou, O Lord God of our fathers"**—'the Canticle of the Fathers.' In the Kyiv-Pechersk Lavra **"A Psalm of David"** is not proclaimed.

*(Orig. p. 653)*

### According to Ancient Typika (*Po drevnim ustavam*)

In the Greek Typikon concerning the prokeimenon there is silence (the Georgian does not even mention it); the Slavic of the 14th century: 'Deacon: **Let us attend**; Priest: **Peace be unto all**; We: **And to thy spirit**; Deacon: **Wisdom**; the chanter says: **A Psalm of David**; Deacon: **Let us attend**; the chanter sings the prokeimenon of the current tone and we sing the same, then the chanter sings the verse and we the prokeimenon, and again the chanter the prokeimenon, while we sing near the end of the prokeimenon, then the chanter sings the conclusion.' In later ones there is silence.

In the Moscow Sluzhebnik of 1602 and 1647, the Old Believer Sluzhebnik and Typikon: + **Peace be unto all** and a 2nd **Let us attend**; in the remaining Slavic and Greek ones there is silence [^2461]. Inasmuch as the prokeimenon is a remnant of the Old Testament reading, which in antiquity always preceded the New Testament ones, since it was, as it were, a chanting reading of the Psalter (Introductory Chapter, p. 162), and before a reading it was always announced

=== LEAF p790 ===
...whence it was taken, then, presumably, the same was previously always done before the prokeimenon as well.

Under Arseny Sukhanov in the East the Matins Prokeimenon was sung by the choirs thrice (entire) without any exclamations or verses [^2462].

### Sunday Matins Prokeimena (*Voskresnye prokimny utreni*)

The Prokeimenon of Sunday Vespers is likewise dedicated unto the event of Christ's Resurrection, but it does not so directly relate unto this event and speaks not concerning it with such clarity as the Matins Prokeimenon, in which for the most part there is the very concept of 'resurrection.' This is because it prepares for the Gospel of the Resurrection. In addition, from the Vesperal Prokeimenon the Matins Prokeimenon differs in that it is not one and the same for each Sunday, but changes according unto the tones. Thus, of Sunday Matins prokeimena there are 8. For them there are chosen from the Psalms preeminently those verses where there is spoken of that special, direct action of Providence which the ancient Hebrew figuratively termed the rising up, the 'arising' (Heb. *qūm*), of the Lord as if from the couch of His customary rest—a word rendered in the Septuagint by *anistēmi* (Gr. ἀνίστημι), which signifies, besides rising from a couch, also resurrection. Namely, the Sunday Matins prokeimena and their verses are taken from the following psalms:

Tone 1: **"Now will I arise, saith the Lord"**—from Psalm 11:6, 7 [LXX; Masoretic 12:5, 6].
Tone 2: **"Arise, O Lord my God, in the decree"**—Psalm 7:7, 2 [printed 8, 2; LXX 7:7, 2; Masoretic 7:6, 1].
Tone 3: **"Say among the nations that the Lord reigneth"**—Psalm 95:10, 1 [LXX; Masoretic 96:10, 1].
Tone 4: **"Arise, O Lord, help us"**—Psalm 43:27, 2 [LXX; Masoretic 44:26, 1].
Tone 5: **"Arise, O Lord my God... for Thou dost reign"**—Psalm 9:33, 2 [LXX; Masoretic 10:12, 9:2].
Tone 6: **"O Lord, stir up Thy might (that is, Christ)"**—Psalm 79:3, 2 [LXX; Masoretic 80:2, 1].
Tone 7: **"Arise, O Lord my God... forget not"**—Psalm 9:33, 2 [LXX; Masoretic 10:12, 9:2].
Tone 8: **"The Lord shall reign for ever"**—Psalm 145:10, 1 [LXX; Masoretic 146:10, 1].

The theme of the prokeimena of Tones 3 and 8 coincides with the Vesperal Prokeimenon. In Tone 8, as concluding, most appropriate is 'for ever,' as indeed in general the series of prokeimena gives a certain development of thought (Tone 1 is only the promise *(Orig. p. 654)* of the Resurrection and in general of salvation, concerning which the Lord speaks openly, 'unhesitatingly,' *parrēsiasomai*, Gr. παρρησιάσομαι). As verses unto the prokeimena, as is generally done, there are taken the opening verses of those psalms wherefrom the prokeimena are drawn (a remnant of the practice when along with the responsive singing of the prokeimenon the entire psalm was sung); the exception is the Prokeimenon of Tone 1, where a verse was chosen more suited unto the prokeimenon: **"The words of the Lord are pure words"**—
"""

draft_file.parent.mkdir(parents=True, exist_ok=True)
with open(draft_file, "w", encoding="utf-8") as f:
    f.write(draft_content.strip() + "\n")
print(f"Wrote draft file: {draft_file}")
