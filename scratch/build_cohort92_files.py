# -*- coding: utf-8 -*-
"""
Builder script for Cohort 92 of Monument 6 (Skaballanovich Tolkovy Typikon).
Generates:
1. Source text: Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/1910_skaballanovich_typikon_cohort92_source.txt
2. Draft translation: Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort92_raw_draft.md
3. Footnotes: Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort92_footnotes.txt
"""

from pathlib import Path

source_text = """=== LEAF p911 ===

один — уповательного характера — 5 гл. (параллельный и в музыкальном отношении и по содержанию к 1 гл.: «якоже уповахом»): «Ты Господи сохраниши…» (Пс. 11, 8), а остальные хвалебного характера, более идущего к тону воскресной службы; наиболее хвалебный 4 гл.: «Яко (= о, как, ώς) возвеличишася дела Твоя…» (Пс. 103, 24); {с. 753} затем параллельные по содержанию 3 гл. «Пойте Богу нашему…» (Пс. 46, 7) и 8 гл. «Помолитеся (в евр.: «делайте обеты») и воздадите…» (Пс. 75, 12); наконец, тоже параллельные — 2 гл. «Крепость моя и пение…» (Пс. 117, 14) и 7 гл. «Господь крепость людем Своим даст…» (Пс. 28, 11). Стихами к прокимнам по обычаю служат начальные стихи псалмов, из коих взяты прокимны, исключая 2 гл., где стих Пс. 117, 18.

История
Из воскресных литургийных прокимнов дается «Иерусалимским последованием» Страстной и Пасхальной седмиц IX в. прокимен 7 гл. на вечерне Светлого четверга; уставом Великой Константинопольской церкви IX в. — прокимен 6 гл. во вторник Пятидесятницы. Все прокимны в нынешнем употреблении даются Евергетидским уставом (XI–XII в.), с той только особенностью, что прокимен 6 гл. служит и для гл. 4 [925].

Аллилуиарий
Считаясь священнее Апостола, Евангелие должно иметь пред собою и превосходнейшее подготовление. Если на утрене таким подготовлением к нему служит прокимен, то на литургии, где последний предшествует Апостолу, Евангелие должно иметь пред собою что-нибудь более исключительное. Таким и является положенная пред литургийным Евангелием песнь аллилуиа. По Апокалипсису, это будет небесная песнь вечности [926]. Кроме «аминь», это единственное еврейское выражение, которого не дерзнула коснуться рука переводчика, оставив его и в тех звуках, в которых оно вдохновлено Богом; от него веет поэтому духом глоссолалической (Вступ. гл., 41; ср. 34 и д.) таинственности, вызывающей применение его, например, при таинстве крещения (подобно Кирие елеисон при священстве). Служа припевом самых радостных (у евреев — пасхальных) псалмов в Библии, аллилуиа выступает в качестве почти неизменного припева псалмов в нашем богослужении, но это почти единственное место (другое — на великопостной и заупокойной утрене), где оно выступает в

=== LEAF p912 ===

качестве самостоятельной песни, имеющей, наоборот, при себе припевы, называемые аллилуиариями (άλληλουιάριон); это псалмические стихи, имеющие отношение к воспоминанию дня, которых обычно положено два для троекратного пения аллилуиа (каждый раз по трижды) (три стиха только в Страстную субботу). Стихи, как и в прокимне, берутся из одного псалма, часто соседние.

Чин пения аллилуиа
Пение аллилуиа предваряется возгласом «Премудрость», своею краткостью более говорящим, чем сложный возглас пред прокимном (ср. в начале литургии верных, пред «Святая святым» и на крещении «Вонмем»).
{с. 754}
Поется аллилуиа со своими стихами по гласам, напевом прокимна (на практике обычно напевом 1 гл.) по тому же чину, как прокимен, Бог Господь и аллилуиа на утрене, почему чин этот нигде не указан, т. е. чтец (ответив на «Мир ти» священника «И духови твоему») возглашает глас аллилуиа («аллилуиа, глас N»), после чего аллилуиа поет хор трижды; чтец поет (обычно возглашает) первый аллилуиарий, и хор опять аллилуиа трижды; чтец — второй аллилуиарий, хор — аллилуиа трижды (так делается в Киево-Печерской лавре, но стихи читаются). Торжественность момента усиливается происходящим тогда каждением, подготовительным к Евангелию [927].

История евангельского аллилуиа и аллилуиария
О древности предъевангельского аллилуиа может свидетельствовать существование его и в Западной Церкви в виде, очень близком к нашему. Аллилуиа пред литургийным Евангелием там состоит из двукратного пения аллилуиа, затем одного стиха и однократного опять аллилуиа; все это поется одним напевом по следующему чину, даваемому в Graduate romanum (где и ноты для аллилуиа разных праздников): «если аллилуиа, аллилуиа говорится со стихом, сначала поется аллилуиа двумя (певцами) до невмы (так называется богатая мелодия для последнего слога, — иначе jubilus), хор же повторяет аллилуиа и присоединяет невму, протягивая слог а; два певца начинают стих и хор отвечает (= продолжает стих); по окончании стиха те же два повторяют аллилуиа, и хор присоединяет одну

=== LEAF p913 ===

невму». Напев для этого аллилуиа, называвшегося «меньшим», в Римской Церкви всегда отличался особой живостью, энергией и красотой. Оно не поется во весь период Великого поста и подготовительных к нему недель (от Недели 70-цы), в будни Адвента, в посты 4 времен и вигилии. Введенное при папе Дамасе (IV в.), аллилуиа первоначально пелось лишь в пасхальное время, и только Григорий Великий (VI в.) разрешил петь его и в другие праздники. Взамен невмы впоследствии стали подставлять особый подходящий текст, сначала не ритмический и потому называвшийся prosa, а потом целые метрические песни, названные sequentia, должно быть, потому, что следующее за ними Евангелие имеет возглас пред собою: «sequentia (продолжение) S. Evangelii secundum N.» (едва ли можно вслед за Thalhofer'oм видеть здесь отзвук греч. ακολουθία); таких песней во Франции и Германии к XII в. появилось до 200, вошедших и в тамошние Миссалы, но в официальный римский Миссал секвенций вошло только 5: на Пасху, Пятидесятницу, праздник Тела, 7 скорбей Богоматери в пятницу 6 недели поста {с. 755} (Stabat mater) [928] и заупокойный (Dies irae). Это целые гимны, строк в 8–10. Пелись они по местам целым хором, а по местам отдельными певцами попеременно. В дни Четыредесятницы и подготовительные к ней, в покаянные и заупокойные дни вместо аллилуиа пред Евангелием поется так наз. tractus, состоящий из стихов (2–5, иногда 1/2 псалма и целый псалом, например в 1 воскресенье поста — 90, в Вербное — 21), большей частью псалмических, приноровленных к воспоминаниям дня, из коих, собственно, первый носит это имя, а другие наз. «стихи»; но пелись первоначально все они с амвона одним певцом без перерыва (= tractim, другие отождествляли название с ειρμός) со стороны хора, а позднее стали петь так, что стих начинали два певца, а хор продолжал; такое пение сравнивали с пением горлицы, всегда одиноким, в противоположность перекликающемуся роду обычного, антифонного или респонсорного пения, уподоблявшегося пению голубей (имелось в виду и Лк. 2, 24); уже поэтому пение tractus называлось пением плача и скорби (cantus fletus et tristitiae), и гласы для него давались 2 и 8 [929].
По мозарабскому чину аллилуиа («называемое там Lauda) поется после Евангелия: сначала аллилуиа однажды, затем стих или несколько их, и снова аллилуиа; в Великий пост, начиная со 2 Недели, Lauda состоит только из стихов без аллилуиа [930].
Что касается восточных литургий, то все они, исключая коптскую, имеющую пред Евангелием не аллилуиа, а 50 псалом, предваряют Евангелие аллилуиа: на абиссинской литургии

=== LEAF p914 ===

аллилуиа 3 после 3 стихов из начала 33 псалма произносит священник; на несторианской литургии аллилуиа 3 произносит читавший Апостол диакон и поют певцы [931].
Из православных литургических памятников древнейшее упоминание об аллилуиа пред Евангелием с указанием гласа и одного стиха из псалма в Иерусалимском канонаре VII в. в грузинской версии [932].
Из древних православных литургий об аллилуиа пред Евангелием говорят: александрийская литургия евангелиста Марка по списку XI в.: «пролог аллилуии» (ό πρόλογος τοΰ αλληλούια); литургия ап. Петра: «аллилуиа»; иерусалимская литургия ап. Иакова по списку X в.: «аллилуиа» (с членом то); XI в.: «и стихологию»; XVI в.: «певец (ψάλτης) аллилуиа (с членом)» или без «певец» [933].
По одному из древнейших списков литургии Иоанна Златоуста,
«Диакон: Премудрость. Иерей: Мир всем. Диакон: Премудрость вонмем. Затем говорит аллилуиарий»; по другому списку, «после послания (= Апостола) иерей говорит: Мир всем. Премудрость, прости. Певец: Псалом Давидов. Аллилуиа»; позднейшие списки: «Диак.: Премудрость; хор: Аллилуиа. Псалом Давидов» [934].
Печатные Служебники слав. {с. 756} Моск. 1602 г. (= старообрядческий):
«Диак.: Вонмем, премудрость, вонмем. Чтец: И духови твоему. Псалом Давидов. Аллилуиа. Певцы же поют аллилуиа».
Служ. Петра Могилы 1627 г.:
«Д.: Премудрость, вонмем. И чтец: Псалом Давидов, рек глас. Аллилуиа. Певцы же поют: Аллилуиа»;
Моск. 1647 г. так, как 1602 г., но «(поют аллилуиа) 5-ю: на правом 3-жды, на левом 2-жды».
Моск. 1658: «Чтец: Аллилуиа. Псалом Давидов».
Так и греч. печатные. Иератикон: «2-й хор поет 3-жды аллилуиа» [935].

=== LEAF p915 ===

Воскресные аллилуиарии
В противоположность воскресным прокимнам, такие же аллилуиарии взяты из псалмов в числовом их порядке, а не в разбивку: 1 гл. Пс. 17:48, 51; 2 гл. Пс. 19:2, 10; 3 гл. Пс. 30:2, 3; 4 гл. Пс. 44:5, 8; 5 гл. Пс. 88:2, 3; 6 гл. Пс. 90:1, 2; 7 гл. Пс. 91:2, 3; 8 гл. Пс. 94, 12. Не имея, подобно прокимнам и Евангелию, к которому они служат подготовлением, прямого отношения к событию воскресения, аллилуиарии содержат общее прославление Бога. Ни один из них, в противоположность некоторым из воскресных прокимнов, не имеет просительно-скорбного характера. Они то изображают царственное достоинство Христа (гл. 1, 4), то выражают надежду на Бога (гл. 3, 6), благодарение за милости (гл. 5, 7), или вообще прославление Бога (гл. 8).

История их
Нынешние воскресные аллилуиарии имеются уже в Евергетидском уставе XII в. с тем отличием, что здесь не положено аллилуиариев для 3 и 7 гласов (может быть, для них не было особых напевов), но зато для 2 гласа 2 пары, и вторая — нынешние 3 гласа, а для 8 гласа — 3 пары, из коих третья — нынешние 7 гласа, а вторая: «Призри на мя и помилуй мя», «Стопы моя направи» (Пс. 118:132, 133) [936].

Прокимны и аллилуиарии при двух памятях
Ни Типикон, ни другие богослужебные книги не дают прямого указания, как поступать при совпадении в один день прокимнов и аллилуиариев двум памятям. Но уже это молчание предполагает, что каждый из таких прокимнов и аллилуиариев должен петься полностью; а то обстоятельство, что в некоторых из таких случаев (например, в Неделю отцев около 11 октября) при втором прокимне дается и стих его, решает вопрос в направлении, совершенно противном принятой практике, — т. е. при двух прокимнах нельзя петь второй без стиха, а нужно 1-й и 2-й петь со стихом, следовательно, 1-й два раза, а второй 2 1/2 раза; аллилуиа же при 4 стихах 5 раз, и каждый раз по трижды.
{с. 757}
Апостол и Евангелие

=== LEAF p916 ===

За прокимном на литургии следует подготовленное им чтение из апостольских посланий, называемое кратко «Апостол». Он составляет почти исключительную принадлежность литургии, появляясь из других служб только на тех, которые соединялись или соединимы с литургией или составлены по образцу ее (на некоторых вечернях, некоторых последованиях таинств и т. п.). Берется Апостол из посланий апостольских, включая сюда и Деяния и исключая Апокалипсис. Кроме настоящего места, послания апостольские, но только соборные, читаются и в качестве паремий — с меньшею, чем здесь, торжественностью — по чину ветхозаветных чтений, а затем на бдении воскресном после вечерни с еще меньшею торжественностью — по чину святоотеческих чтений.

Читается Апостол чтецом или диаконом с амвона. Заголовок чтения предваряется возгласом «Премудрость». Заголовок делается в более пространной форме, чем для ветхозаветных чтений: именуется не только книга, но и автор формулой: «К N послания св. апостола N чтение». Не указана нигде формула для соборных посланий и Деяний. Обычно для первых пользуются формулой паремий: «Соборнаго послания N-ова (Петрова и т. п.) чтение», а для вторых: «От Деяний (иные: Из Деяний [937]), св. апостол чтение» (см. Минея, 9 августа, 1-я паремия). При парных посланиях не произносится нумерация (не говорится: «к коринфянам перваго послания чтение») по сравнительному безразличию этого для понимания чтения, — на том основании, что такая нумерация не указывается в заголовках посланий на паремиях. После возгласа «Вонмем» начинается самое чтение Апостола. Если Апостол не из начала книги, то в Деяниях он начинается словами «Во дни оны», в соборных посланиях «Возлюбленнии», в Павловых «Братие», в его же пастырских: «Чадо Тимофее» или «Тите» (исключая случаи, где подобное начало невозможно, см., например, Апостол 1 Нед. Великого поста), причем опускаются соединяющие с прежним союзы и делаются другие необходимые изменения текста. Заключается апостольское чтение преподанием мира чтецу: «Мир ти» и ответом его «И духови твоему».

Евангелие литургийное предваряется и заканчивается такими же возгласами, как утреннее, с тем отличием, что если служит диакон, которому в таком случае передается чтение Евангелия (почему — см. выше, с. 657— 658), то он, как некоторым образом принимающий на себя в данном случае служение, превышающее его силы и свойственное собственно священнику, просит у него на это благословение («Благослови, владыко, благовестителя…», «Бог молитвами…»), и по окончании чтения священник ему

=== LEAF p917 ===

преподает мир, отмечая при этом высоту исполненной им обязанности: «Мир ти благовествующему».
{с. 758}
История
Об образовании понятий «Апостол» и «Евангелие» и о чтецах того и другого в древности — см. Вступ. гл., 61–62, 105–106, 168–169.
На литургиях мозарабской всегда, а на несторианской в праздники бывает впереди Апостола и ветхозаветное чтение (как в древности — см. Вступ. гл., 161–162), на коптской и абиссинской три Апостола: из посланий Павловых, соборных и Деяний (см. ниже, ср. там же); на нынешней римской часто вместо Апостола (epistola) ветхозаветное чтение.
На римской литургии Апостол читает иподиакон, а Евангелие диакон; на коптской Евангелие диакон, «если умеет читать»; на абиссинской и несторианской — священник [938].
Рукописи литургии ап. Иакова указывают предварительные возгласы только пред прокимном (почти такие, как у нас — см. выше, с. 564) и не упоминают о них пред Апостолом; литургия евангелиста Марка по ркп. XI в., не упоминая о прокимне: «Мир всем. И духови твоему. Вонмем».
В греч. ркп. и печатных греч. Евхологиях на литургии Златоуста — пред Апостолом указывается только возглас «Вонмем»; но во всех слав. изданиях Служебника как ныне; так и в греч. Иератиконе [939].
На римско-католической литургии по римскому чину пред Апостолом произносится его надписание в форме: «чтение (lectio) послания блаженного Павла апостола к N», а после Апостола (a ministris respondetur): «Богу благодарение» (Deo gratias), что при нескольких Апостолах повторяется после каждого; по мозарабскому чину пред Апостолом говорит священник: «Молчание храните (silentium facite). Продолжение (Sequentia) послания Павла апостола к N; отвечает хор: Богу благодарение»; после Апостола «респонсорий: Аминь» [940].
{с. 759}
Возгласы пред Евангелием
О возгласах пред Евангелием см. выше, с. 656–657.
Начальные слова чтений буквально схожи с нашими в Римской Церкви: для Деяний: «In diebus illis», для посланий

=== LEAF p918 ===

Павловых: «Fratres» (соборные начинаются с 1 гл.), для Евангелия: «In illo tempore» [941].

Воскресные литургийные чтения
Таблица воскресных литургийных Апостолов и Евангелий (дана во введении к богослужебным Апостолу и Евангелию) и их тем.

Нед. Пасхи_Деян. 1, 1–8: явление Воскресшего; Ин. 1, 1–17: учение о Слове Божием.
2 по П. Фом._Деян. 5, 12–20: чудеса апостолов; Ин. 20, 19–31: неверие Фомы.
3, мирон._Деян. 6, 1–7: учреждение диаконов; Мк. 15, 43— 16, 8: погребение и воскресение Христово.
4, рассл._Деян. 9, 32–42: исцеление Энея; Ин. 5, 1–15: исцеление расслабленного.
5, самар._Деян. 11:19–26, 29, 30: обращение язычников; Ин. 4, 5–42: беседа с самарянкой.
6, слеп._Деян. 16, 16–34: изгнание беса из прорицательницы; Ин. 9, 1–38: исцеление слепорожденного.
7, св. оо._Деян. 20:16–18, 28–36: наставления ефесским пресвитерам; Ин. 17, 1–13: первосвященническая молитва.
{с. 760}
Нед. 50-цы_Деян. 2, 1–11: сошествие Святого Духа; Ин. 7, 37– 52; 8, 12: беседа в последний день Кущей.
Нед. 1 по 50-це_Евр. 11, 33–12, 2: вера у святых; Мф. 10:32, 33, 37, 38; 19, 27–30: исповедание Христа и самоотвержение.
2_Рим. 2, 10–16: совесть; Мф. 4, 18–23: призвание первых апостолов.
3_Рим. 5, 1–10: оправдание Кровию Христовою; Мф. 6, 22–33: свобода от житейских забот.
4_Рим. 6, 18–23: рабство греху и правде; Мф. 8, 5–13: исцеление слуги сотника.
5_Рим. 10, 1–10: оправдание верою; Мф. 8, 28–9, 1: исцеление Гадаринских бесноватых.
6_Рим. 12, 6–14: различие дарований; Мф. 9, 1–8: исцеление капернаумского расслабленного.
7_Рим. 13, 1–7: отношение к власти; Мф. 9, 27–35: исцеление 2 слепцов и немого бесноватого.
8_1 Кор. 1, 10–18: о единомыслии по поводу коринфских распрей; Мф. 14, 14–22: насыщение 5000.
9_1 Кор. 3, 9–17: огонь последнего дня; Мф. 14, 22–34: хождение по водам.

=== LEAF p919 ===

10_1 Кор. 4, 9–16: подвиги апостолов; Мф. 17, 14–23: исцеление бесноватого глухонемого.
11_Кор. 9, 2–12: бескорыстие апостольского служения; Мф. 18, 23–35: притча о безжалостном заимодавце.
12_1 Кор. 15, 1–11: воскресение и явления Христа; Мф. 19, 16–26: богатый юноша.
13_1 Кор. 16, 13–24: приветствия; Мф 21, 33–42: притча о злых виноградарях.
14_2 Кор. 1, 21–2, 4: запечатление Духом; Мф. 22, 1–14: притча о званых.
15_2 Кор. 4, 6–15: тяготы апостольства; Мф. 22, 35–46: важнейшая заповедь.
16_2 Кор. 6, 1–10: самоотвержение апостолов; Мф. 25, 14–30: притча о талантах.
17_2 Кор. 6, 16–7, 1: чистота; Мф. 15, 21–28: исцеление хананеянки.
18_2 Кор. 9, 6–11: благотворение; Лк. 5, 1–11: чудесный лов рыбы.
19_2 Кор. 11, 31–12, 9: благодатная высота Павла; Лк. 6, 31– 36: милосердие.
20_Гал. 1, 11–19: призвание ап. Павла; Лк. 7, 11–16: воскрешение сына Наинской вдовы.
21_Гал. 2, 16–20: бессилие закона; Лк. 8, 5–15: притча о сеятеле.
{с. 761}
Нед. 22 по 50-це_Гал. 6, 11–18: бессилие обрезания; Лк. 16, 19–31: притча о богатом и Лазаре.
23_Еф. 2, 4–10: спасение благодатию; Лк. 8, 26–39: исцеление гадаринского бесноватого.
24_Еф. 2, 14–22: примирение смертию Христовою; Лк. 8, 41– 56: воскрешение дочери Иаира.
25_Еф. 4, 1–6: церковное единение; Лк. 10, 25–37: притча о милосердном самарянине.
26_Еф. 5, 9–19: дела тьмы и света; Лк. 12, 16–21: притча о любостяжательном богаче.
27_Еф. 6, 10–17: духовное оружие; Лк. 13, 10–17: исцеление скорченной.
28_Кол. 1, 12–18: искупление и его Совершитель; Лк. 14, 16– 24: притча о званых.
29_Кол. 3, 4–11: умерщвление грехов; Лк. 17, 12–19: исцеление 10 прокаженных.
30_Кол. 3, 12–16: добродетели; Лк. 18, 18–27: богатый юноша.
31_1 Тим. 1, 15–17: спасение грешников; Лк. 18, 35–43: исцеление иерихонского слепца.

=== LEAF p920 ===

32_1 Тим. 4, 9–15: обязанности пастырей; Лк. 19, 1–10: Закхей.
Мытаря_2 Тим. 3, 10–15: гонения верных; Лк. 18, 10–14: притча о мытаре.
Блудного_1 Кор. 6, 12–20: блуд; Лк. 15, 11–32: притча о блудном.
Мясопуст._1 Кор. 8, 8–9, 2: ядение идоложертвенного мяса; Мф. 25, 31–46: Страшный Суд.
Сыропуст._Рим. 13, 11–14, 4: воздержание и пост; Мф. 6, 14– 21: пост.
Нед. 1 поста_Евр. 11:24–26, 32–12:2: вера пророков; Ин. 1, 43–51: призвание апостолов.
2_Евр. 1, 10–2, 3: превосходство Христа над Ангелами; Мк. 2, 1–12: исцеление капернаумского расслабленного.
3_Евр. 4, 14–5, 6: первосвященство Христа; Мк. 8, 34— 9, 1: крестоношение.
4_Евр. 6, 13–20: клятва Божия Аврааму; Мк. 9, 17–31: исцеление бесноватого глухонемого.
5_Евр. 9, 11–14: очищение Кровию Христовою; Мк. 10, 32–45: просьба Саломии.
Нед. ваий_Флп. 4, 4–9: радость о Господе; Ин. 12, 1–18: вифанская вечеря и вход в Иерусалим.
{с. 762}
Таким образом, на дни Пятидесятницы выбраны самое возвышенное Евангелие и книга Деяний, повествующая о событиях, наиболее близких к воскресению Христову, вознесению и сошествию Святого Духа. Не берутся совсем чтения из соборных посланий по меньшей определенности их христологии в сравнении с Павловыми (см. Вступ. гл., с. 60–61); Евангелие Марка из-за своей краткости заняло место после больших 2 Евангелий в качестве их дополнения. Во всем остальном книги и отделы их следуют порядку Библии; исключение для евангельских зачал — Мф. 15, 21–28 о хананеянке, поставленное последним, и Лк. 16, 19–31 о богатом и Лазаре, поставленное вместо 28 Недели на 22, потому что первое первоначально читалось пред Великим постом (см. ниже), а второе, может быть, читалось в ближайшее воскресенье к соответствующей минейной памяти (Лазаря 17 октября). Что касается, в частности, Евангелий, то нельзя не заметить, что избранные из них чтения равномерно приблизительно распределены по темам между учением и чудесами Иисуса Христа и что из другого Евангелия берутся отделы, опущенные в первом; повторяются из Лк. по сравнению с Мф. только рассказ о гадаринском чуде вследствие разностей у Мф. и Лк., притча о званных на вечерю и
"""

draft_text = """=== LEAF p911 ===

one is of a hopeful character—Tone 5 (parallel both in a musical respect and in content to Tone 1: "even as we have hoped"): **"Thou, O Lord, shalt keep us..."** (Ps. 11:8 [LXX]), while the remainder are of a laudatory character, which is more fitting for the tone of the Sunday service; the most laudatory is Tone 4: **"How *(Orig. p. 753)* magnified are Thy works, O Lord..."** (Ps. 103:24 [LXX]); then, parallel in content, Tone 3: **"Sing praises to our God..."** (Ps. 46:7 [LXX]) and Tone 8: **"Make your vows (in Heb.: 'make vows') and pay them..."** (Ps. 75:12 [LXX]); finally, likewise parallel—Tone 2: **"The Lord is my strength and my song..."** (Ps. 117:14 [LXX]) and Tone 7: **"The Lord will give strength unto His people..."** (Ps. 28:11 [LXX]). The verses to the prokeimena, according to custom, are served by the opening verses of the Psalms from which the prokeimena are taken, except for Tone 2, where the verse is Psalm 117:18 [LXX].

### History
Of the Sunday Liturgical prokeimena, the "Jerusalem Order" of Holy Week and Bright Week of the 9th century provides the Prokeimenon of Tone 7 at Vespers of Bright Thursday; the Typikon of the Great Church of Constantinople of the 9th century gives the Prokeimenon of Tone 6 on the Tuesday of Pentecost. All prokeimena in present usage are provided by the Evergetis Typikon (11th–12th c.), with the sole peculiarity that the Prokeimenon of Tone 6 serves also for Tone 4[^2759].

### The Alleluiarion
Being accounted more sacred than the Epistle (*Apostol*), the Gospel must possess before it a most excellent preparation as well. If at Matins such a preparation for it is served by the Prokeimenon, then at the Liturgy, where the latter precedes the Epistle, the Gospel must possess before it something still more exceptional. Such indeed is the chant *Alleluia*, appointed before the Liturgical Gospel. According to the Apocalypse, this will be the heavenly song of eternity[^2760]. Except for "Amen," this is the sole Hebrew expression that the hand of the translator did not dare to touch, leaving it in the very sounds in which it was inspired by God; there breathes from it, therefore, a spirit of glossolalic mystery (Introductory Chapter, p. 41; cf. p. 34 ff.), prompting its employment, for example, at the Mystery of Baptism (similar to the *Kyrie eleison* at Ordination). Serving as the refrain of the most joyful (among the Hebrews, Paschal) Psalms in the Bible, the *Alleluia* steps forth as an almost invariable refrain of the Psalms in our divine worship, but this is almost the sole place (the other being at Lenten and memorial Matins) where it steps forth in

=== LEAF p912 ===

the capacity of an independent chant possessing, on the contrary, refrains attached to itself, termed alleluiaria (*alleluiarion*, άλληλουιάριον); these are psalm verses having reference to the commemoration of the day, of which two are normally appointed for the threefold chanting of the Alleluia (each time thrice) (three verses only on Great Saturday). The verses, as in the Prokeimenon, are taken from a single Psalm, often contiguous ones.

### The Order of Chanting the Alleluia
The chanting of the Alleluia is prefaced by the exclamation: **"Wisdom!"**, which in its brevity is more eloquent than the complex exclamation before the Prokeimenon (cf. at the beginning of the Liturgy of the Faithful, before "Holy things to the holy," and at Baptism: "Let us attend!").

*(Orig. p. 754)*

The Alleluia is chanted with its verses according to the tones, to the melody of the Prokeimenon (in practice, usually to the melody of Tone 1), according to the very same order as the Prokeimenon, **"God is the Lord"**, and the Alleluia at Matins, which is why this order is nowhere explicitly prescribed—that is, the reader (having replied to the priest's "Peace be to thee" with "And to thy spirit") proclaims the tone of the Alleluia (**"Alleluia, in Tone N"**), after which the choir chants the Alleluia thrice; the reader chants (usually proclaims) the first alleluiarion verse, and the choir again chants the Alleluia thrice; the reader proclaims the second alleluiarion verse, and the choir chants the Alleluia thrice (this is done in the Kyiv-Pechersk Lavra, although the verses are read). The solemnity of the moment is heightened by the censing taking place at that time, preparatory to the Gospel[^2761].

### History of the Gospel Alleluia and Alleluiarion
Concerning the antiquity of the pre-Gospel Alleluia, its existence in the Western Church in a form very close to our own can bear witness. The Alleluia before the Liturgical Gospel there consists of a twofold chanting of the Alleluia, then a single verse, and once again a single Alleluia; all this is chanted to a single melody according to the following order provided in the *Graduale Romanum* (which also contains the musical notes for the Alleluia of the various feasts): "If the Alleluia, Alleluia is said with a verse, first the Alleluia is chanted by two (cantors) up to the neume (so called from the rich melisma upon the final syllable—otherwise *jubilus*), while the choir repeats the Alleluia and appends the neume, prolonging the syllable *a*; two cantors begin the verse and the choir responds (= continues the verse); upon the conclusion of the verse the same two repeat the Alleluia, and the choir appends a single

=== LEAF p913 ===

neume." The melody for this Alleluia, which was called the "lesser" (*alleluia minus*), in the Roman Church was always distinguished by exceptional vivacity, energy, and beauty. It is not chanted throughout the entire period of Great Lent and the weeks preparatory to it (from Septuagesima Sunday), on weekdays of Advent, during the Ember days (fasts of the Four Seasons), and on vigils. Introduced under Pope Damasus (4th c.), the Alleluia was originally chanted only during the Paschal season, and only Gregory the Great (6th c.) permitted it to be chanted on other feasts as well. In place of the neume, they subsequently began to substitute a special appropriate text, at first non-rhythmical and therefore termed *prosa*, and later entire metrical hymns, termed *sequentia*, in all likelihood because the Gospel following them has the exclamation before it: *"Sequentia Sancti Evangelii secundum N."* (one can hardly, following Thalhofer, see here an echo of the Greek ακολουθία); of such hymns in France and Germany by the 12th century there appeared up to 200, which entered into their local Missals, but into the official Roman Missal only five sequences entered: for Pascha, Pentecost, the Feast of Corpus Christi, the Seven Sorrows of the Mother of God on the Friday of the 6th week of Lent *(Orig. p. 755)* (*Stabat Mater*)[^2762], and the Requiem Mass (*Dies Irae*). These are entire hymns of some 8–10 strophes. They were chanted in some places by the whole choir, and in other places by individual cantors alternately. On the days of the Forty Days (*Quadragesima*) and those preparatory to it, and on penitential and memorial days, in place of the Alleluia before the Gospel there is chanted the so-called *tractus*, consisting of verses (2–5, sometimes half a Psalm and an entire Psalm, for example on the 1st Sunday of Lent—Psalm 90 [LXX], on Palm Sunday—Psalm 21 [LXX]), for the most part psalm verses adapted to the commemorations of the day, of which strictly speaking the first bears this name, while the others are termed "verses"; yet originally all of them were chanted from the ambo by a single cantor without interruption (= *tractim*; others identified the designation with *heirmos*) on the part of the choir, whereas later they began to chant such that two cantors began the verse and the choir continued; such chanting was compared to the singing of the turtledove, always solitary, in contrast to the alternating kind of ordinary, antiphonal or responsorial singing, likened to the cooing of doves (Luke 2:24 was also kept in view); for this reason alone the chanting of the *tractus* was termed the song of weeping and sorrow (*cantus fletus et tristitiae*), and the tones assigned to it were Tones 2 and 8[^2763].

According to the Mozarabic rite, the Alleluia (there termed *Lauda*) is chanted after the Gospel: first the Alleluia once, then a verse or several of them, and again the Alleluia; in Great Lent, beginning with the 2nd Sunday, the *Lauda* consists solely of verses without the Alleluia[^2764].

As for the Eastern liturgies, all of them, except for the Coptic, which has before the Gospel not the Alleluia but Psalm 50 [LXX], preface the Gospel with the Alleluia: in the Abyssinian (Ethiopian) Liturgy

=== LEAF p914 ===

the priest pronounces the Alleluia thrice after 3 verses from the beginning of Psalm 33 [LXX]; in the Nestorian Liturgy the deacon who read the Epistle pronounces the Alleluia thrice and the cantors chant it[^2765].

Among Orthodox liturgical monuments, the most ancient mention of the Alleluia before the Gospel with an indication of the tone and one verse from the Psalm is found in the Jerusalem Kanonarion of the 7th century in the Georgian version[^2766].

Among ancient Orthodox liturgies, the Alleluia before the Gospel is mentioned by: the Alexandrian Liturgy of Mark the Evangelist according to an 11th-century manuscript: "the prologue of the Alleluia" (ό πρόλογος τοΰ αλληλούια); the Liturgy of the Apostle Peter: "Alleluia"; the Jerusalem Liturgy of the Apostle James according to a 10th-century manuscript: "the Alleluia" (with the article *to*); 11th century: "and the stichologia"; 16th century: "the chanter (*psaltes*) the Alleluia (with the article)" or without "the chanter"[^2767].

According to one of the most ancient manuscripts of the Liturgy of John Chrysostom:
"Deacon: Wisdom. Priest: Peace be to all. Deacon: Wisdom, let us attend! Then he says the alleluiarion"; according to another manuscript: "after the Epistle, the priest says: Peace be to all. Wisdom, stand upright! Cantor: A Psalm of David. Alleluia"; later manuscripts: "Deacon: Wisdom; Choir: Alleluia. A Psalm of David"[^2768].

The printed Slavic *(Orig. p. 756)* *Sluzhebniks*, Moscow, 1602 (= the Old Believer edition):
"Deacon: Let us attend, wisdom, let us attend! Reader: And to thy spirit. A Psalm of David. Alleluia. And the cantors chant: Alleluia."
The *Sluzhebnik* of Peter Mohyla, 1627:
"Deacon: Wisdom, let us attend! And the reader: A Psalm of David, naming the tone. Alleluia. And the cantors chant: Alleluia."
Moscow, 1647, the same as 1602, but "(they chant the Alleluia) 5 times: on the right side thrice, on the left side twice."
Moscow, 1658: "Reader: Alleluia. A Psalm of David."
Likewise the Greek printed editions. The *Hieratikon*: "The 2nd choir chants the Alleluia thrice"[^2769].

=== LEAF p915 ===

### The Sunday Alleluiaria
In contrast to the Sunday prokeimena, the Sunday alleluiaria are taken from the Psalms in their numerical order, and not in scattered succession: Tone 1, Ps. 17:48, 51 [LXX]; Tone 2, Ps. 19:2, 10 [LXX]; Tone 3, Ps. 30:2, 3 [LXX]; Tone 4, Ps. 44:5, 8 [LXX]; Tone 5, Ps. 88:2, 3 [LXX]; Tone 6, Ps. 90:1, 2 [LXX]; Tone 7, Ps. 91:2, 3 [LXX]; Tone 8, Ps. 94:1, 2 [LXX]. Not having, like the prokeimena and the Gospel for which they serve as preparation, a direct relation to the event of the Resurrection, the alleluiaria contain a general glorification of God. Not one of them, in contrast to certain of the Sunday prokeimena, possesses a supplicatory or mournful character. They at times depict the royal dignity of Christ (Tones 1, 4), at times express hope in God (Tones 3, 6), thanksgiving for mercies (Tones 5, 7), or generally the glorification of God (Tone 8).

### Their History
The present Sunday alleluiaria are found already in the Evergetis Typikon of the 12th century, with the distinction that here no alleluiaria are appointed for Tones 3 and 7 (perhaps there were no special melodies for them), but instead for Tone 2 there are two pairs, and the second is the present Tone 3, while for Tone 8 there are three pairs, of which the third is the present Tone 7, and the second is: **"Look upon me and have mercy on me"**, **"Order my steps"** (Ps. 118:132, 133 [LXX])[^2770].

### Prokeimena and Alleluiaria in the Concurrence of Two Commemorations
Neither the *Typikon* nor the other liturgical books give a direct indication of how to proceed when on a single day prokeimena and alleluiaria for two commemorations coincide. Yet this very silence presupposes that each of such prokeimena and alleluiaria must be chanted in full; and the circumstance that in some of such cases (for example, on the Sunday of the Fathers around October 11) at the second prokeimenon its verse is also given, resolves the question in a direction completely contrary to accepted practice—that is, when there are two prokeimena, one cannot chant the second without a verse, but must chant both the 1st and the 2nd with their verse, consequently the 1st twice, and the second 2 1/2 times; and the Alleluia, with 4 verses, 5 times, and each time thrice.

*(Orig. p. 757)*

## THE SCRIPTURAL READINGS (EPISTLE AND GOSPEL)

=== LEAF p916 ===

Following the Prokeimenon at the Liturgy comes the reading prepared by it from the apostolic epistles, termed concisely the "Epistle" (*Apostol*). It constitutes an almost exclusive property of the Divine Liturgy, appearing among other services only in those that were united or are unifiable with the Liturgy, or are structured after its model (at certain Vespers, certain rites of the Mysteries, etc.). The Epistle is taken from the apostolic epistles, including herein the Acts of the Apostles and excluding the Apocalypse. Besides the present place, the apostolic epistles—yet only the Catholic Epistles—are read also in the capacity of Old Testament readings (*paroimiai*), with less solemnity than here, according to the order of Old Testament readings; and thereafter at the Sunday Vigil after Vespers with still less solemnity, according to the order of patristic readings.

The Epistle is read by the reader or deacon from the ambo. The title of the reading is prefaced by the exclamation: **"Wisdom!"** The title is given in a more expansive form than for the Old Testament readings: not only the book is named, but also the author, by the formula: "The reading from the Epistle of the holy Apostle N unto N." Nowhere is a formula indicated for the Catholic Epistles and the Acts. Usually for the former they utilize the formula of the *paroimiai*: "The reading from the Catholic Epistle of N (of Peter, etc.)," and for the latter: "The reading from the Acts (others: Out of the Acts[^2771]) of the Holy Apostles" (see *Menaion*, August 9, 1st *paroimia*). In the case of paired epistles, the numbering is not pronounced (one does not say: "The reading from the first Epistle to the Corinthians") owing to the comparative indifference of this for the comprehension of the reading—on the ground that such numbering is not indicated in the titles of the epistles at the *paroimiai*. Following the exclamation: **"Let us attend!"**, the reading of the Epistle itself begins. If the Epistle is not from the beginning of the book, then in the Acts it begins with the words: "In those days"; in the Catholic Epistles: "Beloved"; in the Pauline Epistles: "Brethren"; and in his Pastoral Epistles: "Child Timothy" or "Titus" (excepting cases where such a beginning is impossible; see, for example, the Epistle of the 1st Sunday of Great Lent), wherein the connecting conjunctions with what precedes are omitted and other necessary textual adjustments are made. The apostolic reading concludes with the imparting of peace to the reader: **"Peace be to thee"**, and his response: **"And to thy spirit."**

The Liturgical Gospel is prefaced and concluded with the very same exclamations as that of Matins, with the distinction that if a deacon is serving, to whom in such a case the reading of the Gospel is committed (as to why, see above, pp. 657–658), then he, as taking upon himself in this instance a ministry exceeding his rank and properly belonging to the priest, requests from him a blessing for this (**"Bless, master, the proclaimer of the good tidings..."**, **"May God, through the prayers..."**), and upon the conclusion of the reading the priest

=== LEAF p917 ===

imparts peace to him, marking thereby the exalted nature of the duty performed by him: **"Peace be to thee that announcest the good tidings."**

*(Orig. p. 758)*

### History
Concerning the development of the concepts of "Epistle" (*Apostol*) and "Gospel" (*Evangelion*), and concerning the readers of both in antiquity, see Introductory Chapter, pp. 61–62, 105–106, 168–169.

In the Mozarabic Liturgy always, and in the Nestorian on feasts, there is an Old Testament reading preceding the Epistle (as in antiquity; see Introductory Chapter, pp. 161–162); in the Coptic and Abyssinian Liturgies there are three Epistles: from the Pauline Epistles, the Catholic Epistles, and the Acts of the Apostles (see below; cf. *ibid.*); in the present Roman Mass, an Old Testament reading frequently replaces the Epistle (*epistola*).

In the Roman Liturgy, the subdeacon reads the Epistle, and the deacon reads the Gospel; in the Coptic, the deacon reads the Gospel "if he knows how to read"; in the Abyssinian and Nestorian, the priest reads it[^2772].

Manuscripts of the Liturgy of the Apostle James indicate preliminary exclamations only before the Prokeimenon (almost identical to our own; see above, p. 564) and do not mention them before the Epistle; the Liturgy of Mark the Evangelist according to an 11th-century manuscript, without mentioning the Prokeimenon, has: "Peace be to all. And to thy spirit. Let us attend!"

In Greek manuscripts and printed Greek Euchologia of the Liturgy of St. John Chrysostom, before the Epistle only the exclamation: "Let us attend!" is indicated; but in all Slavic editions of the *Sluzhebnik* it is as at present; and likewise in the Greek *Hieratikon*[^2773].

In the Roman Catholic Liturgy according to the Roman rite, before the Epistle its title is pronounced in the form: "The reading (*lectio*) of the Epistle of blessed Paul the Apostle to N," and after the Epistle (responded by the ministers): "Thanks be to God" (*Deo gratias*), which in the case of multiple Epistles is repeated after each; according to the Mozarabic rite, before the Epistle the priest says: "Keep silence (*Silentium facite*). The continuation (*Sequentia*) of the Epistle of Paul the Apostle to N; the choir responds: Thanks be to God"; after the Epistle, "Responsory: Amen"[^2774].

*(Orig. p. 759)*

### Exclamations before the Gospel
Concerning the exclamations before the Gospel, see above, pp. 656–657.

The opening words of the readings are literally similar to our own in the Roman Church: for the Acts: *"In diebus illis"*; for the Pauline

=== LEAF p918 ===

Epistles: *"Fratres"* (the Catholic Epistles begin from Chapter 1); for the Gospel: *"In illo tempore"*[^2775].

### Sunday Liturgical Readings
The table of the Sunday Liturgical Epistles and Gospels (provided in the introduction to the liturgical *Apostol* and *Evangelion*) and their themes:

- **Sunday of Pascha** — Acts 1:1–8: The Appearance of the Risen Christ; John 1:1–17: The Teaching on the Word of God.
- **2nd Sunday after Pascha (Thomas Sunday)** — Acts 5:12–20: The Miracles of the Apostles; John 20:19–31: The Unbelief of Thomas.
- **3rd Sunday (of the Myrrh-bearers)** — Acts 6:1–7: The Institution of the Deacons; Mark 15:43–16:8: The Burial and Resurrection of Christ.
- **4th Sunday (of the Paralytic)** — Acts 9:32–42: The Healing of Aeneas; John 5:1–15: The Healing of the Paralytic.
- **5th Sunday (of the Samaritan Woman)** — Acts 11:19–26, 29–30: The Conversion of the Gentiles; John 4:5–42: The Discourse with the Samaritan Woman.
- **6th Sunday (of the Blind Man)** — Acts 16:16–34: The Expulsion of the Demon from the Soothsaying Maiden; John 9:1–38: The Healing of the Man Born Blind.
- **7th Sunday (of the Holy Fathers)** — Acts 20:16–18, 28–36: Exhortations to the Ephesian Presbyters; John 17:1–13: The High Priestly Prayer.

*(Orig. p. 760)*

- **Sunday of Pentecost** — Acts 2:1–11: The Descent of the Holy Spirit; John 7:37–52; 8:12: The Discourse on the Last Day of the Feast of Tabernacles.
- **1st Sunday after Pentecost (All Saints)** — Heb. 11:33–12:2: The Faith of the Saints; Matt. 10:32, 33, 37, 38; 19:27–30: The Confession of Christ and Self-Denial.
- **2nd Sunday after Pentecost** — Rom. 2:10–16: Conscience; Matt. 4:18–23: The Calling of the First Apostles.
- **3rd Sunday after Pentecost** — Rom. 5:1–10: Justification by the Blood of Christ; Matt. 6:22–33: Freedom from Worldly Cares.
- **4th Sunday after Pentecost** — Rom. 6:18–23: Servitude to Sin and to Righteousness; Matt. 8:5–13: The Healing of the Centurion's Servant.
- **5th Sunday after Pentecost** — Rom. 10:1–10: Justification by Faith; Matt. 8:28–9:1: The Healing of the Gadarene Demoniacs.
- **6th Sunday after Pentecost** — Rom. 12:6–14: Diversity of Gifts; Matt. 9:1–8: The Healing of the Paralytic of Capernaum.
- **7th Sunday after Pentecost** — Rom. 13:1–7: Relation to Civil Authority; Matt. 9:27–35: The Healing of Two Blind Men and the Dumb Demoniac.
- **8th Sunday after Pentecost** — 1 Cor. 1:10–18: On Like-Mindedness in View of the Corinthian Dissensions; Matt. 14:14–22: The Feeding of the Five Thousand.
- **9th Sunday after Pentecost** — 1 Cor. 3:9–17: The Fire of the Last Day; Matt. 14:22–34: Walking on the Water.

=== LEAF p919 ===

- **10th Sunday after Pentecost** — 1 Cor. 4:9–16: The Labors of the Apostles; Matt. 17:14–23: The Healing of the Lunatic Deaf-Mute Boy.
- **11th Sunday after Pentecost** — 1 Cor. 9:2–12: The Selflessness of the Apostolic Ministry; Matt. 18:23–35: The Parable of the Unforgiving Debtor.
- **12th Sunday after Pentecost** — 1 Cor. 15:1–11: The Resurrection and Appearances of Christ; Matt. 19:16–26: The Rich Young Man.
- **13th Sunday after Pentecost** — 1 Cor. 16:13–24: Salutations; Matt. 21:33–42: The Parable of the Wicked Vinedressers.
- **14th Sunday after Pentecost** — 2 Cor. 1:21–2:4: Sealing by the Spirit; Matt. 22:1–14: The Parable of the Marriage Feast (Those Bidden).
- **15th Sunday after Pentecost** — 2 Cor. 4:6–15: The Hardships of the Apostleship; Matt. 22:35–46: The Great Commandment.
- **16th Sunday after Pentecost** — 2 Cor. 6:1–10: The Self-Sacrifice of the Apostles; Matt. 25:14–30: The Parable of the Talents.
- **17th Sunday after Pentecost** — 2 Cor. 6:16–7:1: Purity; Matt. 15:21–28: The Healing of the Canaanite Woman's Daughter.
- **18th Sunday after Pentecost** — 2 Cor. 9:6–11: Beneficence; Luke 5:1–11: The Miraculous Draught of Fishes.
- **19th Sunday after Pentecost** — 2 Cor. 11:31–12:9: The Grace-Filled Elevation of Paul; Luke 6:31–36: Tender Mercy.
- **20th Sunday after Pentecost** — Gal. 1:11–19: The Calling of the Apostle Paul; Luke 7:11–16: The Raising of the Son of the Widow of Nain.
- **21st Sunday after Pentecost** — Gal. 2:16–20: The Impotence of the Law; Luke 8:5–15: The Parable of the Sower.

*(Orig. p. 761)*

- **22nd Sunday after Pentecost** — Gal. 6:11–18: The Impotence of Circumcision; Luke 16:19–31: The Parable of the Rich Man and Lazarus.
- **23rd Sunday after Pentecost** — Eph. 2:4–10: Salvation by Grace; Luke 8:26–39: The Healing of the Gadarene Demoniac.
- **24th Sunday after Pentecost** — Eph. 2:14–22: Reconciliation through the Death of Christ; Luke 8:41–56: The Raising of Jairus' Daughter.
- **25th Sunday after Pentecost** — Eph. 4:1–6: Ecclesiastical Unity; Luke 10:25–37: The Parable of the Good Samaritan.
- **26th Sunday after Pentecost** — Eph. 5:9–19: The Works of Darkness and of Light; Luke 12:16–21: The Parable of the Covetous Rich Fool.
- **27th Sunday after Pentecost** — Eph. 6:10–17: The Spiritual Armor; Luke 13:10–17: The Healing of the Bowed Woman.
- **28th Sunday after Pentecost** — Col. 1:12–18: Redemption and Its Accomplisher; Luke 14:16–24: The Parable of the Great Banquet (Those Bidden).
- **29th Sunday after Pentecost** — Col. 3:4–11: The Mortification of Sins; Luke 17:12–19: The Cleansing of the Ten Lepers.
- **30th Sunday after Pentecost** — Col. 3:12–16: Virtues; Luke 18:18–27: The Rich Ruler.
- **31st Sunday after Pentecost** — 1 Tim. 1:15–17: The Salvation of Sinners; Luke 18:35–43: The Healing of the Blind Man of Jericho.

=== LEAF p920 ===

- **32nd Sunday after Pentecost** — 1 Tim. 4:9–15: Pastoral Duties; Luke 19:1–10: Zacchaeus.
- **Sunday of the Publican and the Pharisee** — 2 Tim. 3:10–15: Persecutions of the Faithful; Luke 18:10–14: The Parable of the Publican and the Pharisee.
- **Sunday of the Prodigal Son** — 1 Cor. 6:12–20: Fornication; Luke 15:11–32: The Parable of the Prodigal Son.
- **Meatfare Sunday** — 1 Cor. 8:8–9:2: The Eating of Meats Offered to Idols; Matt. 25:31–46: The Dread Judgment.
- **Cheesefare Sunday** — Rom. 13:11–14:4: Abstinence and Fasting; Matt. 6:14–21: Fasting.
- **1st Sunday of Great Lent (Sunday of Orthodoxy)** — Heb. 11:24–26, 32–12:2: The Faith of the Prophets; John 1:43–51: The Calling of the Apostles.
- **2nd Sunday of Great Lent (St. Gregory Palamas)** — Heb. 1:10–2:3: The Superiority of Christ over the Angels; Mark 2:1–12: The Healing of the Paralytic of Capernaum.
- **3rd Sunday of Great Lent (Veneration of the Cross)** — Heb. 4:14–5:6: The High Priesthood of Christ; Mark 8:34–9:1: Bearing the Cross.
- **4th Sunday of Great Lent (St. John Climacus)** — Heb. 6:13–20: The Oath of God to Abraham; Mark 9:17–31: The Healing of the Demoniac Boy.
- **5th Sunday of Great Lent (St. Mary of Egypt)** — Heb. 9:11–14: Cleansing by the Blood of Christ; Mark 10:32–45: The Request of the Sons of Zebedee (Salome's Request).
- **Palm Sunday (Sunday of Palms)** — Phil. 4:4–9: Rejoicing in the Lord; John 12:1–18: The Supper at Bethany and the Entry into Jerusalem.

*(Orig. p. 762)*

Thus, for the days of the Pentecostarion there have been chosen the most exalted Gospel and the Book of Acts, which recounts the events closest to the Resurrection of Christ, the Ascension, and the Descent of the Holy Spirit. Readings from the Catholic Epistles are not taken at all, owing to the lesser definiteness of their Christology in comparison with the Pauline Epistles (see Introductory Chapter, pp. 60–61); the Gospel of Mark, on account of its brevity, took its place after the two larger Gospels in the capacity of their supplement. In all other respects the books and their sections follow the order of the Bible; the exception for the Gospel pericopes is Matt. 15:21–28 concerning the Canaanite woman, which is placed last, and Luke 16:19–31 concerning the rich man and Lazarus, which is placed on the 22nd Sunday instead of the 28th, because the former was originally read before Great Lent (see below), while the latter, in all probability, was read on the Sunday nearest to the corresponding Menaion commemoration (St. Lazarus, October 17). As regards the Gospels in particular, one cannot fail to observe that the readings selected from them are distributed approximately evenly by topic between the teaching and the miracles of Jesus Christ, and that from another Gospel sections omitted in the first are taken; there are repeated from Luke in comparison with Matthew only the account of the Gadarene miracle (owing to the differences between Matthew and Luke), the parable of those bidden to the banquet, and
"""

footnotes_text = """[^2759]: A. Papadopoulos-Kerameus, *'Ανάλεκτα ίεροσολυμιτικής σταχυολογίας* [Analecta of Jerusalem Gleanings], 237; A. Dmitrievsky, *Τυπικά*, 150, 610.
[^2760]: Rev. 19:1, 3, 4.
[^2761]: It is improper that this censing is performed during the Epistle; the *Sluzhebnik* prescribes: "While the Alleluia is being chanted, the deacon, taking the censer with incense, approaches the priest and, receiving a blessing from him, censes the holy table round about, and the whole sanctuary, and the priest." This departure from the Typikon is connected with an erroneous, even perverse view of the Alleluia as a conclusion to the Epistle rather than as a preparation for the Gospel—a view that demeans both the Alleluia and the Gospel.
[^2762]: This sequence is now used only as a hymn at Vespers.
[^2763]: V. Thalhofer, *Handbuch der katholischen Liturgik*, Freiburg, 1912, 74–91.
[^2764]: J.-P. Migne, *Patrologia Latina*, 84, 112, 320, et al.
[^2765]: Bishop Porphyrius (Uspensky), *Verouchenie, bogosluzhenie... koptov* [Doctrine, Liturgy... of the Copts], 128; *Bogosluzhenie abissinov* [Liturgy of the Abyssinians], 59; A. Petrovsky, *Apostol'skie liturgii vostochnoy tserkvi* [Apostolic Liturgies of the Eastern Church], Appendix, 65.
[^2766]: Archpriest K. Kekelidze, *Ierusalimsky kanonar VII v.* [The Jerusalem Kanonarion of the 7th Century], Tiflis, 1912, 43, 44, et al.
[^2767]: C. A. Swainson, *The Greek Liturgies*, 16, 193, 226, 227.
[^2768]: J. Goar, *Εύχολόγιον*, 87, 91, 55; C. A. Swainson, *The Greek Liturgies*, 117.
[^2769]: *Sluzhebnik*, Moscow, 1602, fol. 98; Peter Mohyla, p. 17; Moscow, 1647, fol. 117; 1658, p. 253; *Εύχολόγιον*, Venice, 1622, 22; Athens, 1902, 58; *Ίεраτικόν*, Constantinople, 1895, 63.
[^2770]: A. Dmitrievsky, *Τυπικά*, 610.
[^2771]: On the basis of expressions in the Typikon: "The Epistle from the Acts."
[^2772]: *Missale Romanum*, g.; Bishop Porphyrius, *Verouchenie, bogosluzhenie... koptov*, 129; *Bogosluzhenie abissinov*, 60; A. Petrovsky, *Apostol'skie liturgii vostochnoy tserkvi*, Appendix, 65.
[^2773]: C. A. Swainson, *The Greek Liturgies*, 16, 116; J. Goar, *Εύχολόγιον*, 55; *Εύχολόγιον*, Athens, 1902, 58; *Ίεраτικόν*, Constantinople, 1895, 61.
[^2774]: *Missale Romanum*, 4; J.-P. Migne, *Patrologia Latina*, 85, 110–111. In the Eastern non-Chalcedonian and other non-Orthodox liturgies, the preparatory exclamations before the Epistle, as before the Gospel (see above, p. 657), grew to large proportions, especially in view of the aforementioned multiplicity of readings. In the Nestorian Liturgy, before the Old Testament reading, the reader or deacon says: "Sit in silence. The prophecy of the Prophet N, master, bless." The priest says: "May Christ bless." Before the Epistle, a special prayer is said aloud by the priest, varying for fasts and feasts, for divine assistance and understanding; the deacon says: "The Epistle of the Apostle Paul unto N, master, bless"; the priest: "May Christ bless thee in His holy teaching, that thou mayest be a radiant mirror unto them that listen unto thee"; after the Epistle, the deacon says: "Glory to the Master of the Apostle Paul" (A. Petrovsky, *Apostolic Liturgies of the Eastern Church*, Appendix, 64, 95). In the Coptic Liturgy, before the reading of the Pauline Epistles, the Catholic Epistles, and the Acts—before each reading separately—there is censing, but no exclamations of any kind are indicated; after each of the readings there is a prayer: the prayer after the 1st reading asks for understanding to comprehend it and the possibility of imitating the Apostle; after the 2nd, for being accounted worthy of the lot of the Apostles, imitating them, and preserving the Church; after the 3rd, for the acceptance of the incense and for purification. In the Abyssinian Liturgy, before the Pauline Epistle the prayer is the same as in the Coptic after it, and the exclamation of the deacon is: "The reading from the Epistle of Paul, a servant and apostle of our Savior Jesus Christ, called, chosen, set apart for the preaching of the holy Gospel, unto N; whose prayer and blessing be with us, amen"; after the reading, the deacon says: "The grace of the Father, the love of the Son, and the gift of the Holy Spirit (a paraphrase of 2 Cor. 13:13), Who descended upon the blessed and pure Apostles in the upper room of holy Zion, be multiplied upon us Christian people, unto ages of ages, amen. O holy Apostle Paul, good servant, physician of the infirm, pray and intercede for us with Christ God, that He may save our souls according to the multitude of the mercy of His holy name." The priest says: "Peace be to all," and a prayer for the abiding of God with us and for purification. Before the Catholic Epistle, the priest says: "This is the reading from the Epistle of N, a disciple and apostle of our Lord and Savior Jesus Christ, whose prayer and blessing be with us, amen"; after the reading, the deacon says 1 John 2:15–17 (on not loving the world); the people pray to the Holy Trinity for the preservation of the assembly for the sake of the holy Apostle, and for comfort. Preparation for the Acts: the deacon: "Arise for prayer"; the priest: "Peace be to all"; "And to thy spirit"; prayers the same as in the Coptic Liturgy after the Catholic Epistles and after the Acts, and two others of general content; exclamation: "The Acts of the ministers of this preaching, our fathers the Apostles, pure and filled with grace, chosen and righteous, abounding in the grace of the Holy Spirit. May their prayers and blessings preserve all of us Christians unto ages of ages, amen"; after the reading, a paraphrase of Acts 6:7 (on the increase of the believers) and: "Holy (thrice) is God the Father Almighty, Holy (thrice) is the Only-begotten Son, the living Word of the Father, Holy (thrice) is the Holy Spirit, everywhere present" (Bishop Porphyrius, *Verouchenie, bogosluzhenie... koptov*, 125–127; *Bogosluzhenie abissinov*, 56–59).
[^2775]: *Missale Romanum*, I, 2, 20.
"""

def main():
    base_dir = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon")
    source_path = base_dir / "Source Text" / "1910_skaballanovich_typikon_cohort92_source.txt"
    draft_path = base_dir / "Draft" / "1910_skaballanovich_typikon_cohort92_raw_draft.md"
    footnotes_path = base_dir / "Draft" / "1910_skaballanovich_typikon_cohort92_footnotes.txt"

    source_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.parent.mkdir(parents=True, exist_ok=True)

    source_path.write_text(source_text.strip() + "\n", encoding="utf-8")
    print(f"Wrote {source_path} ({len(source_text)} chars)")

    draft_path.write_text(draft_text.strip() + "\n", encoding="utf-8")
    print(f"Wrote {draft_path} ({len(draft_text)} chars)")

    footnotes_path.write_text(footnotes_text.strip() + "\n", encoding="utf-8")
    print(f"Wrote {footnotes_path} ({len(footnotes_text)} chars)")

if __name__ == "__main__":
    main()
