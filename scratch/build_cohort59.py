# -*- coding: utf-8 -*-
"""
Builder and validator for Cohort 59 of Mikhail Skaballanovich's Tolkovy Typikon.
"""
from pathlib import Path
import sys

SOURCE_TEXT = """=== LEAF p581 ===
Господу за дарование трапезы еще прежде вкушения от нее. (Этот стих заменяет собою положенное в начале дневной трапезы чтение целого 144 псалма с Отче наш). После стиха испрашивается обычным образом благословение священника: Слава и ныне. Господи помилуй 3. Благослови (таким же образом испрашивается благословение священника на выход из храма пред отпустом). «И благословляет священник трапезу», какими словами, здесь (в 1 гл. Типикона) не указано, но указано в чине дневной трапезы («о панагии»), во 2 гл. Типикона: «Христе Боже благослови ястие и питие рабом Твоим…» (окончание см. в следованной Псалтири: «яко Свят еси всегда, ныне и присно, и во веки веков, аминь»).

О самой трапезе замечено: «вкушаем представленная нам полегку, да не отяготимся на бдение». Благодарение после трапезы воссылается Пресв. Троице малым славословием (как и на дневной трапезе), а затем Пресв. Богородице тропарями «Бысть чрево Твое святая трапеза» (вместо «Достойно есть» дневной трапезы) и «Честнейшую». Затем (вместо Пс. 121: Возвеселихся о рекших мне, положенного на дневной трапезе) читается отрывок из Пс. 91, 6 и 4, 7–9: «Возвеселил ны еси Господи…», заключающий прославление Бога за насыщение и молитвенную надежду на мирный сон. Все остальные молитвословия чина о панагии, даже и прямо не относящиеся к панагии, опускаются в этом кратком чине трапезы (например, Трисвятое с Отче наш, молитва «Благодарим Тя Христе Боже наш», тропари «Боже отец наших» и «Молитвами Господи всех святых», а тотчас после «Возвеселил ны еси Господи» испрашивается благословение священника на отпуск обычным образом: Слава и ныне, Господи помилуй 3, Благослови. Отпуст также разнится от чина панагии: (вместо: «Благословен Бог милуяй и питаяй») — «С нами Бог Своею благодатию и человеколюбием всегда, и ныне и присно и во веки веков, аминь» (более подходит к ночному времени; ср. на великом повечерии «С нами Бог»). Таким образом, почти все молитвословия вечерней трапезы отличны от дневной трапезы, но самый строй, чинопоследование той и другой тот же, исключая обряд возвышения панагии.

## История

В древнейших уставах чин вечерней трапезы почти ничем не отличался от дневной трапезы; на нем также происходило возвышение блюда {с. 486} с укрухами (соответствует панагии). Так в Студ. уставе патр. Афанасия XII в. [140] и в Типиконе Пантократорского монастыря 1136 г. [141] Главное отличие

=== LEAF p582 ===
вечерней трапезы от дневной по этим уставам было то, что на первой при возвышении укрухов возглашалось «Велико имя Св. Троицы», а на второй «Пресв. Богородице помогай нам».

Но уже грузинский Шиомгвимский устав иерусалимского типа в рукописи XIII в. имеет чин вечерней трапезы без возвышения панагии.

«После вечерни звонят бубенчиками (кандия?), братия собираются тихо в трапезную и начинают «Ядят убозии и насытятся». Вставши говорят: «Явися нам свет лица Твоего» и после «Благослови» уходят в кельи до повечерия» [142].

Древнейший греческий список Иерусалимского устава (в России) Моск. Рум. муз. Сев. собр. № 491/35 XIII в. не имеет чина ни дневной, ни вечерней трапезы. Древнейший славянский Иерусалимский устав Моск. Синод. библ. № 328/383 XIV в. имеет для вечерней трапезы чин, тождественный с нынешним, со следующими отличиями: «Ядят убозии…» трижды; после трапезы игумен: «Молитвами св. отец…» Братия: «Слава Отцу…», и бывает возвышение панагии, по чину дневной трапезы; отпуст не «С нами Бог…», а «Молитвами св. отец…» [143].

{с. 487}

=== LEAF p583 ===
# 2-Я ГЛАВА ТИПИКОНА
## «ВСЕНОЩНОЕ БДЕНИЕ»
### (ВЕЛИКАЯ ВЕЧЕРНЯ И УТРЕНЯ ВОСКРЕСНЫЕ, ЧАСЫ, ЛИТУРГИЯ И ЧИН О ПАНАГИИ)

{с. 488}

=== LEAF p584 ===
# БЛАГОВЕСТ И КАЖДЕНИЕ

## Время для всенощной

Начинать всенощную положено «немного спустя после захода солнца». По восточному счету времени это будет 1-й час ночи. Таким образом, всенощная естественно начинается с наступлением ночи праздника.

## Характер благовеста

Благовест ко всякой всенощной полагается сначала в большой колокол медленно и долго, а затем во все колокола (не в 2 или 4, как для будничных служб и малых праздников, см. 9 гл. Типик.): «ударяет в великий кампан не скоро, поя Непорочны или глаголя псалом 50, тихо 12-ю. И потом вшед и вжигает лампады и уготовляет кадильницу. И тако паки изшед клеплет во вся кампаны». Таким образом, благовест полагается производить в два приема с небольшим промежутком между благовестом в один колокол и звоном во все, причем продолжительность благовеста в один колокол должна быть равна времени, в какое можно пропеть 118 псалом или 50 пс. 12 раз. Благовест ко всенощной в великие праздники в Типиконе описывается сходно с воскресным, но все же дается понять, что он должен быть торжественнее: продолжительнее и в большие колокола (на Рождество Христово «бывает благовест и потом трезвон во вся кампаны»; на Крещение: «знаменают в великое [144] и во вся тяжкая»; на Пасху: «ударяет в великое и клеплет довольно», а затем: «ударяет во вся кампаны и тяжкая и клеплет довольно») [145].

В древнейших списках Иерусалимского устава греческом Моск. Румянц. муз. Сев. собр. № 491/35 XIII в. и грузинском Шиомгвимского мон. XIII в. благовест к воскресной всенощной описывается так:

«ударяет тяжкая медленно (κρούει τὰς βαρέας σχολαίως), поя (ψάλλων) Непорочны»; затем по возжжении лампад и приготовлении кадила «знаменает в великое, потом в железное (σημαίνει τὸ μέγα εἶτα σίδηρ(ον))», по первому памятнику; «сначала в железное било, потом в великое», по второму памятнику [146].

=== LEAF p585 ===
По древнейшим славянским спискам Иерусал. устава, например, Моск. Синод. библ. № 328/383,

«ударяет в великое било глаголя Блажени непорочни раздельно на 12 частей или Верую во единаго Бога 12-ю, ударяя по един. (т. е. на каждую из 12 частей 118 псалма или на каждое «Верую» ударяет один раз, так что всего получится 12 очень медленных ударов) и тако звонит часто и кончает (в заключение ударяет чаще); посем знаменает в железное» [147] (промежутка между звонами не положено).

В дальнейших списках Иерусалим{с. 489}ского устава и в нынешнем старообрядческом:

«ударяет в великое древо тяжким ударением (старообр. + покосну) ретко… И паки изшед клеплет в великое било (не во всех списках) [148] и в железо» (или «железно бильце», «железное клепальце»).

Благовест воскресный по древним уставам не отличается от великопраздничного (даже пасхального).

## Молитва благовеста

Считая благовест некоторым священнодействием, устав указывает совершителю его — сопровождать его молитвенным чтением или пением. Благовест к бдению положено сопровождать пением Непорочных, т. е. псалма 118, или чтением 50 пс. 12 раз. Псалом 118-й, наиболее умилительный из псалмов, составлял по прежним уставам непременную принадлежность воскресной утрени, почему пением его и сопровождается благовест. Этим предписанием устава определяется вместе с тем и продолжительность благовеста: на пение 176 стихов 118 псалма или 21 ст. (50 пс.)х12 требуется не менее получаса. Из будничных служб указано сопровождать чтением 50 псалма (однократным) благовест к утрене (в 9 гл. Типикона). Сопровождение благовеста молитвою, конечно, имеет целью сообщить ему благодатное освящение. Действие благовеста на душу христианина и походит на действие молитвы и богослужения.

Сопровождение благовеста молитвою — древнейший обычай. По уставу прп. Пахомия (IV в.), «кто ударяет в било пред обедом

=== LEAF p586 ===
или пред молитвою, должен размышлять о чем-нибудь назидательном» [149]. В житии св. Кириака отшельника, духовным руководительством которого пользовался предполагаемый автор нынешнего устава (св. Савва Освященный), рассказывается, что он, ударяя в било пред началом службы, не прежде оканчивал звон, как прочтя Непорочны. (Этот обычай и возникшее из него предписание устава свидетельствует и о том, как хорошо в древности знали Псалтирь; если некоторые иноки имели обычай прочитывать ее всю ежедневно, то неудивительно знание наизусть 118 псалма). Древнейшие уставы — XIII в. — как мы видели, говорят о пении при благовесте только Непорочных. Позднейшие — XIV в. — позволяют заменять Непорочны Символом веры и 50 псалмом, очевидно вследствие того, что знание Псалтири наизусть стало более редким явлением.

## Значение каждения

Вслед за благовестом начинается в храме часть бдения, которую можно назвать безмолвною. Она состоит в каждении всего храма. То, что каждение это, требующее немало времени, полагается производить все до начала самой службы и в присутствии всех собравшихся к ней, которые пред ним приглашаются встать, равно как обстоятельность, с какою описывается это {с. 490} каждение в Типиконе, — все это делает из каждения как бы особую службу, предшествующую всенощному бдению и подготовляющую к нему, подобно тому как подготовляет к нему и благовест. Подготовление там и здесь различного рода, но от этого оно тем всестороннее. Благовест подготовляет верующих к службе звуками — музыкой. Каждение приготовляет нас к службе «вонею благоухания». Духовному, «умному» богослужению предшествует это телесное, внешнее. Фимиам возносит ум к престолу Божию, куда он направляется с нашими молитвами. Во все века и у всех народов сожжение благовоний считалось лучшей, чистейшей вещественной жертвой Богу, и из всех видов вещественной жертвы, принятых в естественных религиях, христианская Церковь удержала только эту и еще немногие (елей, вино, хлеб). И внешним видом ничто так не напоминает благодатного дыхания Духа Святого, как дым фимиама. Исполненное такого высокого символизма, каждение много способствует молитвенному настроению верующих и своим чисто телесным воздействием на человека. Благовония действуют повышающе, возбудительно на наше настроение. С этой целью устав, например, пред пасхальным бдением предписывает уже не просто каждение, а чрезвычайное наполнение храма запахом из

=== LEAF p587 ===
поставленных сосудов с курениями.

В св. Софии Константинопольской, по крайней мере пред богослужением, на котором присутствовал царь, производилось наполнение храма благовониями из особых отверстий в полу. В «Книге Паломник» архиеп. Новгородского Антония (XII в.), рассказывается об этом так:

«Церковь мощена красным мрамором, а под нею доплеко (второй пол), и подходят человецы и учинено сквозе мрамор проходи. И егда внидет царь в церковь ту, тогда понесут под испод много ксилолоя (алоэ) темьяна (фимиама) и кладут на углие и исходит воня проходы теми во церковь на воздух» [150].

По уставу грузин. Шиомгвимского мон. XIII в. кандиловжигатель между первым и вторым звоном ко всенощной кадит церковь [151].

## Особенности настоящего каждения:

### а) Совершитель его

Так как каждение в начале бдения первое в круге суточных служб, то оно совершается с особою торжественностью и описано с тою же подробностью, как в 22 гл. Типикона, посвященной каждению специально. На начало бдения каждение (как и возглас «Слава Святей…») перенесено с начала утрени. Посему, как и там, оно совершается священником, а не диаконом, — ввиду особой важности момента. (Ср. полиелей; на литургии кадит диакон, так как священник занят более важными священнодействиями).

Историческое основание для совершения настоящего каждения именно священником — то, что утреня и вечерня совершались без той торжествен{с. 491}ности, с какой литургия, а потому без диакона; а в монастырях не всегда и бывал диакон.
 
### б) Свеча при каждении

Другую особенность настоящего каждения, тоже общую у него с каждением в начале утрени и полиелейным, составляет преднесение кадящему священнику свечи. На вечерне, как службе менее торжественной, чем утреня, каждение совершается без свечи; на литургии же каждение отступает на второй план перед другими более священными действиями и потому совершается с меньшею торжественностью, тоже без свечи.

Историческим основанием этой разницы является то, что

=== LEAF p588 ===
утреня, с начала которой перенесено настоящее каждение на начало бдения, всегда начиналась ночью, до рассвета, когда ходить по храму и всем его нефам и нельзя было без светильника; вечерня же и литургия совершалась всегда днем.

Но так как каждение в начале бдения, как и утрени, не должно быть все же столь торжественно, как на полиелее, то светильник указано носить при каждении не диакону, как на полиелее, а параекклисиарху или кандиловжигателю. Впрочем, далее в скобках Типикон замечает, что в соборах и приходских храмах «действует сия диакон». В Киево-Печерской лавре только в начале утрени свечу предносит кадящему священнику инок в мантии, на бдении же диакон.

Историческое основание для уставного требования, чтобы кадящему священнику предшествовал со свечой параекклисиарх, а не диакон, — то, что бдение за отсутствием диаконов совершалось большей частью одним священником. На полиелее же иначе, потому что полиелей введен в службу, когда в монастырях большей частью имелись диаконы.

Частнее каждение пред бдением Типикон описывает следующим образом. Кандиловжигатель или параекклисиарх после благовеста зажигает свечу в подсвечнике и ставит ее пред царскими дверьми. В приходских церквах и в тех монастырях, где всенощную начинает диакон со священником, свечу носит диакон, который предносит ее священнику и при каждении алтаря.

В греческом уставе Шиомгвимского мон. XIII в. нет этого замечания о свече (кандиловжигатель прямо берет ее в руки пред возгласом). В рукописных греч. и слав. Типиконах XIII–XIV в. указывалось эту свечу или лампаду ставить среди церкви [152]. В Типиконах XV и XVI вв. указывается ставить ее или «прямо царским дверем поблизко» [153], или «посреде церкви прямо царским дверем» [154]. Так и в первых печатных изданиях устава. Царскими дверями называются главные двери из притвора в храм; они, следовательно, разумеются и здесь, почему свеча, стоящая пред ними, оказывается среди {с. 492} храма. В правленом экземпляре устава для издания 1672 г. слова «посреде церкве» и «поблизко» зачеркнуты и начиная с этого издания не вносятся в устав (в старообрядческом уставе сохранены), очевидно, потому, что под царскими дверями стали разуметь алтарные.

## Облачение священнослужителей

Поставив свечу, параекклисиарх творит поклон иерею,

=== LEAF p589 ===
которого чреда, а тот предстоятелю; иерей «отшед» (т. е. выйдя из своей стасидии) творит три поклона: пред св. дверьми (один) и на оба лика (по одному); во все это время братия сидят; иерей, войдя в алтарь, возлагает на себя епитрахиль, поцеловав на нем крест. В приходских церквах и монастырях, где всенощную начинает священник не с параекклисиархом, а с диаконом, этот порядок на практике несколько изменяется. Обыкновенно священник и диакон, имеющие служить, входят, сотворив указанные поклонения, в алтарь, и там облачаются — диакон в стихарь с орарем, священник в епитрахиль и фелонь, о чем нынешний Типикон замечает далее в скобках.

Ныне принятая практика — участие диакона в совершении великой вечерни на бдении с самого начала ее — не менее древняя, чем предписываемая Типиконом, по которой диакона заменяет параекклисиарх. Только первая ведет свое начало от порядков древнего Софийского собора («Великой церкви») в Константинополе, а вторая — от Иерусалимского устава. Это хорошо видно из того, как представлены эти подготовительные ко всенощной действия в Διάταξις'е Константинопольского патриарха Филофея (XIV в.).

«Когда настанет время, т. е. великой вечерни, отходит иерей с диаконом и творят поклоны (μετανοίας) к иконе Владыки Христа, между тем как все братья сидят; также творят и к Богородичной иконе три поклона, на середину (храма) один и на лики по одному; затем входят во святилище; диакон, взяв свой стихарь с орарем и поклонившись на восток трижды, подходит к иерею и говорит: «Благослови, Владыко, стихарь с орарем»; иерей благословляет их, говоря: «Благословен Бог наш всегда, ныне и присно, и во веки веков». Затем надевают оба присвоенные одежды. Это теперь бывает не так, но иерей один кланяется и один надевает епитрахиль и фелонь и начинает кадить с чтецом или евтаксием [155], который держит свещник».

По справедливому замечанию Гоара [156], патр. Филофей не сам составил предлагаемый им чин (Διάταξις) священнослужения, а только записал древний чин Константинопольской св. Софии. Замечание «это теперь бывает не так» показывает, что ко времени патр. Филофея этот чин вытеснялся даже из соборных и {с. 493} приходских церквей другим каким-то, очевидно чином из практики все более распространявшегося тогда Иерусалимского устава. В рассматриваемом пункте, как и в других, последний

=== LEAF p590 ===
устав дает менее торжественный чин и менее сложный; даже поклонов пред входом в алтарь меньше по Иерусалимскому уставу. (Обр. внимание, что по чину Филофея не указано поклонения св. дверям).

## Каждение алтаря

Облачившись, священник «кадит св. трапезу (престол) крестовидно окрест и весь жертвенник (алтарь) и, отворив св. двери, исходит». Св. двери обыкновенно открываются пред началом каждения, что не противоречит настоящему указанию, так как последнее выражение может означать вообще: выходит чрез открытые св. двери. «Кадит крестовидно» — отголосок той практики каждения, когда кадильница была без цепочек и ею удобно было делать крест; ныне крестовидность каждения заменена троекратностью его.

## «Возстаните» или «Повелите»

После каждения алтаря кандиловжигатель, по указанию Типикона, или диакон, по принятой практике, стоя пред св. дверьми со свечою в руке, возглашает громогласно: «Возстаните». Все встают. В греческом уставе и в наших прежних уставах на этом месте положен был возглас не «Возстаните», а «Повелите». В древнейшем списке Иерусалимского устава — грузинском Шиомгвимского мон.: «возстаните». Но в соперничающем с ним по древности Моск. Рум. муз. Сев. собр. № 491/35 — κελεύσατε. Так и во всех греческих уставах XIV в. и Διάταξις'е патр. Филофея. В рукописных славянских уставах Моск. Син. библ. № 328/383 и 329/384 XIV в.: «келепсаите», в № 332/385 — XIV в. «келепсаите, рекше встанете», в № 678/386 XV в. и др. и в первых печатных, оканчивая Иосифовским 1641 г. «келепсаите; рекше по речи исъкуству повелите», т. е. «келевсате» — эти уставы считали искусственным выражением для «возстаните». Последнее замечание удержано и нынешним старообрядческим уставом. — Κελεύσατε, «повелите», — возглас, употребляющийся по нынешнему уставу за рукоположением во пресвитера и диакона и за Преждеосвященной литургией пред словами «Свет Христов просвещает всех», — вошел в богослужение из придворного византийского церемониала. Этим возгласом церемониймейстеры приглашали сановников на царских приемах входить в те или другие залы дворца или уходить из них. В свою очередь, в Византийский двор возглас заимствован из римской практики: со
"""

DRAFT_MARKDOWN = """=== LEAF p581 ===
unto the Lord for the granting of the refectory even prior to partaking thereof. (This verse replaces the reading of the entire Psalm 144 [LXX 144 / MT 145] with the **"Our Father"**, appointed at the beginning of the midday meal). After the verse, the blessing of the priest is requested in the customary manner: **"Glory... both now... Lord, have mercy"** (three times), **"Bless"** (in the same manner the priest's blessing is requested for leaving the temple before the dismissal). **"And the priest blesses the refectory"**; in what words is not specified here (in Chapter 1 of the Typikon), but is indicated in the order of the midday meal ('On the Panagia') in Chapter 2 of the Typikon: **"O Christ God, bless the food and drink of Thy servants..."** (for the conclusion see the Sequenced Psalter [*Sledovannaya Psaltir'*]: **"for holy art Thou always, now and ever, and unto the ages of ages. Amen"**).

Concerning the meal itself, it is remarked: **"we partake lightly of that which is set before us, that we may not be weighed down for the vigil."** Thanksgiving after the refectory is offered unto the Most Holy Trinity by the Little Doxology (as also at the midday meal), and then unto the Most Holy Theotokos by the troparia **"Thy womb hath become a holy table"** (*Бысть чрево Твое святая трапеза*, in place of **"It is truly meet"** at the midday meal) and **"More honorable"** (*Честнейшую*). Then (in place of Ps. 121 [LXX 121 / MT 122]: **"I was glad when they said unto me"**, appointed at the midday meal) there is read an excerpt from Psalm 91:5 and Psalm 4:8–10 [LXX 91:5; 4:8–10 / MT 92:4; 4:7–8]: **"Thou hast made us glad, O Lord..."** (*Возвеселил ны еси Господи...*), containing the glorification of God for being satisfied and a prayerful hope for peaceful sleep. All the remaining prayers of the Order of the Panagia, even those not directly pertaining to the Panagia, are omitted in this brief order of the refectory (for example, the Trisagion with the **"Our Father"**, the prayer **"We thank Thee, O Christ our God"**, the troparia **"O God of our fathers"** and **"By the prayers, O Lord, of all the saints"**); and immediately after **"Thou hast made us glad, O Lord"** the priest's blessing for dismissal is requested in the customary manner: **"Glory... both now... Lord, have mercy"** (three times), **"Bless"**. The dismissal likewise differs from the Order of the Panagia: (in place of: **"Blessed is God Who showeth mercy and nourisheth us"**)—**"God is with us by His grace and love toward mankind, always, now and ever, and unto the ages of ages. Amen"** (more suitable for nocturnal time; cf. at Great Compline **"God is with us"**). Thus, almost all the prayers of the evening refectory are distinct from the midday meal, but the very structure, the liturgical order of both is the same, excluding the rite of the elevation of the Panagia.

## History

In the earliest Typika, the order of the evening meal differed almost not at all from the midday meal; at it there likewise occurred the elevation of the dish *(Orig. p. 486)* with fragments (*ukrukhi*, corresponding to the Panagia). Thus in the Studite Typikon of Patriarch Athanasius of the 12th c. [^1974] and in the Typikon of the Pantokrator Monastery of 1136 [^1975]. The principal distinction

=== LEAF p582 ===
of the evening refectory from the midday meal according to these Typika was that at the former, during the elevation of the fragments, there was proclaimed: **"Great is the name of the Holy Trinity"**, whereas at the latter: **"Most Holy Theotokos, help us."**

Yet already the Georgian Shiomgvime Typikon of Jerusalem type in a 13th-century manuscript possesses the order of the evening meal without the elevation of the Panagia.

'After Vespers they strike small bells (*kandya*?); the brethren gather quietly into the refectory and begin: **"The poor shall eat and be satisfied."** Arising, they say: **"The light of Thy countenance hath appeared upon us"** [Ps. 4:7 LXX / MT 4:6], and after **"Bless"** they depart unto their cells until Compline' [^1976].

The earliest Greek manuscript of the Jerusalem Typikon (in Russia), Moscow Rumyantsev Museum, Sevastyanov Collection No. 491/35 of the 13th c., has no order for either the midday or the evening meal. The earliest Slavic Jerusalem Typikon, Moscow Synodal Library No. 328/383 of the 14th c., has for the evening meal an order identical with the present one, with the following differences: **"The poor shall eat..."** is said thrice; after the meal the superior: **"By the prayers of the holy fathers..."**; the brethren: **"Glory to the Father..."**, and the elevation of the Panagia takes place according to the order of the midday meal; the dismissal is not **"God is with us..."**, but **"By the prayers of the holy fathers..."** [^1977].

*(Orig. p. 487)*

=== LEAF p583 ===
# CHAPTER 2 OF THE TYPIKON: "THE ALL-NIGHT VIGIL"
## (Sunday Great Vespers and Matins, the Hours, the Liturgy, and the Order of the Panagia)

*(Orig. p. 488)*

=== LEAF p584 ===
# THE BELL-PEAL AND CENSING

## The Appointed Time for the Vigil

It is appointed to begin the Vigil 'a little after the setting of the sun.' According to the Eastern reckoning of time, this is the 1st hour of the night. Thus, the Vigil naturally begins with the onset of the night of the feast.

## Character of the Bell-Peal

The bell-peal (*blagovest*) for every Vigil is appointed first on the great bell, slowly and at length, and then on all the bells (not on 2 or 4, as for ferial services and minor feasts, see Chapter 9 of the Typikon): 'he strikes the great bell (*kampan*) slowly, chanting the Undefiled [Psalm 118 / MT 119] or saying Psalm 50 softly 12 times. And then entering, he kindles the lamps and prepares the censer. And having thus gone forth again, he strikes upon all the bells.' Thus, the peal is appointed to be performed in two stages with a small interval between the peal on one bell and the ringing of all, wherein the duration of the peal on one bell must be equal to the time in which one can chant Psalm 118 or Psalm 50 twelve times. The bell-peal for the Vigil on Great Feasts in the Typikon is described similarly to the Sunday peal, yet it is nevertheless indicated that it must be more solemn: more prolonged and upon larger bells (on the Nativity of Christ: 'there is a bell-peal and then a festal peal [*trezvon*] on all the bells'; on Theophany: 'they signal on the great [instrument] [^1978] and on all the heavy ones'; on Pascha: 'he strikes on the great [instrument] and strikes sufficiently', and then: 'he strikes on all the bells and heavy ones and strikes sufficiently') [^1979].

In the earliest manuscripts of the Jerusalem Typikon—the Greek Moscow Rumyantsev Museum, Sevastyanov Collection No. 491/35 of the 13th c. and the Georgian manuscript of the Shiomgvime Monastery of the 13th c.—the bell-peal for the Sunday Vigil is described thus:

'he strikes the heavy instruments slowly (*κρούει τὰς βαρέας σχολαίως*), chanting (*ψάλλων*) the Undefiled'; then upon kindling the lamps and preparing the censer 'he signals upon the great [semantron], then upon the iron (*σημαίνει τὸ μέγα εἶτα σίδηρ[ον])*', according to the first monument; 'first upon the iron semantron, then upon the great', according to the second monument [^1980].

=== LEAF p585 ===
According to the earliest Slavic manuscripts of the Jerusalem Typikon, for example, Moscow Synodal Library No. 328/383:

'he strikes upon the great semantron (*bilo*), saying: **"Blessed are the undefiled"** [Ps. 118 LXX / MT 119] divided into 12 parts, or **"I believe in one God"** 12 times, striking once [upon each]' (that is, for each of the 12 parts of Psalm 118 or for each recitation of the Creed he strikes once, so that in all there will be 12 very slow strokes), 'and thus he rings frequently and finishes' (in conclusion he strikes more rapidly); 'thereafter he signals upon the iron' [^1981] (no interval between the ringings is appointed).

In subsequent manuscripts of the Jerusalem *(Orig. p. 489)* Typikon and in the present Old Believer Typikon:

'he strikes upon the great wood with a heavy stroke (Old Believer + obliquely) rarely... And having gone forth again he strikes upon the great semantron (not in all manuscripts) [^1982] and upon the iron' (or 'iron semantron-blade' [*zhelezno bil'tse*], 'iron small-semantron' [*zheleznoe klepal'tse*]).

The Sunday bell-peal according to ancient Typika does not differ from that of a Great Feast (even the Paschal peal).

## Prayer Accompanying the Bell-Peal

Regarding the bell-peal as a sacred liturgical action, the Typikon directs its performer to accompany it with prayerful reading or chanting. The peal for the Vigil is appointed to be accompanied by the chanting of the Undefiled, that is, Psalm 118 [LXX 118 / MT 119], or by reading Psalm 50 [LXX 50 / MT 51] twelve times. Psalm 118, the most compunctious of the psalms, constituted according to earlier Typika an indispensable component of Sunday Matins, for which reason the bell-peal is accompanied by its chanting. By this prescription of the Typikon there is simultaneously determined also the duration of the peal: chanting the 176 verses of Psalm 118 or the 21 verses of Psalm 50 twelve times requires no less than half an hour. Of the ferial services, it is appointed to accompany the peal for Matins with a single reading of Psalm 50 (in Chapter 9 of the Typikon). Accompanying the bell-peal with prayer, of course, has the purpose of imparting to it a grace-filled sanctification. The effect of the bell-peal upon the soul of a Christian resembles the effect of prayer and divine worship.

Accompanying the sounding of instruments with prayer is an ancient custom. According to the Rule of St. Pachomius the Great (4th c.): 'whosoever strikes the semantron before dinner

=== LEAF p586 ===
or before prayer, must meditate upon something edifying' [^1983]. In the Life of St. Cyriacus the Anchorite, under whose spiritual guidance the presumptive author of the present Typikon (St. Sabbas the Sanctified) lived, it is related that, when striking the semantron before the beginning of the service, he did not conclude the ringing until he had recited the Undefiled. (This custom and the rubrical prescription arising from it testify also to how thoroughly the Psalter was known in antiquity; if certain monks made it their custom to recite the entire Psalter daily, knowledge of Psalm 118 by heart is not surprising). The earliest Typika of the 13th c., as we have seen, speak of chanting only the Undefiled during the peal. Later Typika of the 14th c. permit replacing the Undefiled with the Creed and Psalm 50, evidently as a consequence of the fact that knowing the Psalter by heart had become a rarer phenomenon.

## Meaning of the Censing

Immediately following the bell-peal there begins in the temple a part of the Vigil that may be called silent. It consists in the censing of the entire temple. The fact that this censing, which requires considerable time, is appointed to be performed entirely before the beginning of the service itself and in the presence of all who have gathered for it, who before it are invited to stand, as well as the detail with which this *(Orig. p. 490)* censing is described in the Typikon—all this makes of the censing as it were a distinct service, preceding the All-Night Vigil and preparing for it, just as the bell-peal also prepares for it. The preparation in the one case and the other is of a different nature, but thereby all the more comprehensive. The bell-peal prepares the faithful for the service by sounds—by music. The censing prepares us for the service by the 'odor of fragrance.' This bodily, external worship precedes spiritual, 'noetic' divine worship. Incense lifts the mind unto the throne of God, whither it ascends with our prayers. In all ages and among all nations the burning of sweet spices was regarded as the finest, purest material sacrifice unto God, and of all forms of material sacrifice accepted in natural religions, the Christian Church retained only this and a few others (oil, wine, bread). And in outward appearance nothing so recalls the grace-bearing breath of the Holy Spirit as the smoke of incense. Filled with such exalted symbolism, the censing greatly fosters the prayerful disposition of the faithful also by its purely physical effect upon man. Fragrances exert an elevating, stimulating influence upon our disposition. With this purpose the Typikon, for example, before the Paschal Vigil prescribes no longer simply a censing, but an extraordinary filling of the temple with fragrance from

=== LEAF p587 ===
vessels set out with incenses.

In Hagia Sophia of Constantinople, at least before divine services attended by the Emperor, the filling of the temple with fragrances was performed from special apertures in the floor. In the *Book of the Pilgrim* (*Kniga Palomnik*) by Archbishop Anthony of Novgorod (12th c.), it is related thus concerning this:

'The church is paved with red marble, and beneath it is a *dopleko* (second floor), and men approach and passages are made through the marble. And when the emperor enters into that church, then they carry beneath much *xylaloe* (aloe) and frankincense (incense) and place them upon coals, and the fragrance issues through those passages into the church into the air' [^1984].

According to the Typikon of the Georgian Shiomgvime Monastery of the 13th c., the taper-lighter (*kandilovzhigatel'*) censes the church between the first and second bell-peal for the Vigil [^1985].

## Peculiarities of the Present Censing

### a) Its Celebrant

Inasmuch as the censing at the beginning of the Vigil is the first in the daily cycle of divine services, it is performed with special solemnity and is described with the same detail as in Chapter 22 of the Typikon, which is specifically dedicated to censing. Unto the beginning of the Vigil the censing (as also the exclamation **"Glory to the Holy..."**) was transferred from the beginning of Matins. Therefore, as there also, it is performed by the priest, and not by the deacon—in view of the exceptional importance of the moment. (Cf. the Polyeleos; at the Liturgy the deacon censes, because the priest is occupied with more important sacred actions).

The historical reason for performing this censing specifically by the priest is that Matins and Vespers were celebrated without that solemn*(Orig. p. 491)*ity with which the Liturgy was celebrated, and therefore without a deacon; and in monasteries there was not always a deacon present.

### b) The Candle at the Censing

Another peculiarity of the present censing, likewise common to it and the censing at the beginning of Matins and at the Polyeleos, is the bearing of a candle before the censing priest. At Vespers, as a service less solemn than Matins, the censing is performed without a candle; at the Liturgy, the censing recedes into the background before other, more sacred actions and is therefore performed with less solemnity, likewise without a candle.

The historical basis of this difference is that

=== LEAF p588 ===
Matins, from the beginning of which the present censing was transferred unto the beginning of the Vigil, always began at night, before dawn, when walking through the temple and all its aisles was impossible without a lamp; Vespers and the Liturgy, on the other hand, were always celebrated by day.

Yet since the censing at the beginning of the Vigil, as also of Matins, must nevertheless not be as solemn as at the Polyeleos, it is prescribed that the lamp be borne at the censing not by the deacon, as at the Polyeleos, but by the paraecclesiarch or taper-lighter. However, further on in parentheses the Typikon notes that in cathedrals and parish churches 'the deacon performs this.' In the Kyiv-Pechersk Lavra only at the beginning of Matins does a monk in a mantle bear the candle before the censing priest, whereas at the Vigil it is the deacon.

The historical basis for the rubrical requirement that the paraecclesiarch, and not the deacon, precede the censing priest with a candle is that the Vigil, owing to the absence of deacons, was celebrated for the most part by a priest alone. At the Polyeleos, however, it is otherwise, because the Polyeleos was introduced into the office when monasteries for the most part had deacons.

More particularly, the Typikon describes the censing before the Vigil in the following manner. After the bell-peal, the taper-lighter or paraecclesiarch lights a candle in a candlestick and sets it before the Royal Doors. In parish churches and in those monasteries where the deacon begins the All-Night Vigil with the priest, the candle is borne by the deacon, who bears it before the priest also during the censing of the sanctuary.

In the Greek Typikon of the Shiomgvime Monastery of the 13th c. there is no such note concerning the candle (the taper-lighter simply takes it in his hands before the exclamation). In manuscript Greek and Slavic Typika of the 13th–14th centuries it was indicated to place this candle or lamp in the midst of the church [^1986]. In Typika of the 15th and 16th centuries it is indicated to place it either 'right before the royal doors nearby' [^1987], or 'in the midst of the church right before the royal doors' [^1988]. So also in the first printed editions of the Typikon. By 'royal doors' were designated the principal doors from the narthex into the nave; they are consequently understood here as well, for which reason the candle standing before them turns out to be in the midst *(Orig. p. 492)* of the church. In the corrected copy of the Typikon for the 1672 edition, the words 'in the midst of the church' and 'nearby' were crossed out, and beginning with that edition are not inserted into the Typikon (in the Old Believer Typikon they are retained), evidently because by 'royal doors' men came to understand the holy doors of the altar screen.

## Vesting of the Sacred Ministers

Having set the candle, the paraecclesiarch makes a bow unto the priest

=== LEAF p589 ===
whose turn of service it is, and the latter unto the superior; the priest, 'having stepped forth' (that is, having left his stasidion), makes three bows: before the holy doors (one) and unto both choirs (one each); during all this time the brethren sit; the priest, having entered the altar, puts on the epitrachelion, having kissed the cross upon it. In parish churches and monasteries where the priest begins the All-Night Vigil not with a paraecclesiarch, but with a deacon, this order is somewhat altered in practice. Customarily the priest and deacon who are to serve enter the altar after making the indicated bows, and there vest—the deacon in sticharion with orarion, the priest in epitrachelion and phelonion, concerning which the present Typikon remarks further on in parentheses.

The practice accepted today—the participation of the deacon in the celebration of Great Vespers at the Vigil from its very beginning—is no less ancient than that prescribed by the Typikon, according to which the paraecclesiarch takes the deacon's place. Only the former traces its origin from the customs of the ancient cathedral of Hagia Sophia ('the Great Church') in Constantinople, while the latter traces its origin from the Jerusalem Typikon. This is well seen from how these preparatory actions for the Vigil are represented in the *Diataxis* (*Διάταξις*) of Patriarch Philotheus of Constantinople (14th c.):

'When the time arrives, that is, of Great Vespers, the priest departs with the deacon, and they make bows (*μετανοίας*) toward the icon of the Master Christ, while all the brethren sit; likewise they make three bows toward the icon of the Theotokos, one toward the center (of the church), and one each toward the choirs; then they enter into the sanctuary; the deacon, having taken his sticharion with the orarion and bowed toward the east thrice, approaches the priest and says: **"Bless, Master, the sticharion with the orarion"**; the priest blesses them, saying: **"Blessed is our God always, now and ever, and unto the ages of ages."** Then both put on their appointed vestments. This is now not so done, but the priest bows alone and alone puts on the epitrachelion and phelonion, and begins to cense with a reader or *eutaxias* [^1989], who holds the candlestick.'

According to the just observation of Goar [^1990], Patriarch Philotheus did not himself compose the order of sacred ministry (*Diataxis*) proposed by him, but only recorded the ancient order of Constantinople's Hagia Sophia. The observation 'this is now not so done' shows that by the time of Patriarch Philotheus this order was being displaced even from cathedral and *(Orig. p. 493)* parish churches by some other, evidently by the order from the practice of the Jerusalem Typikon that was spreading ever more widely at that time. In the point under consideration, as in others, the latter

=== LEAF p590 ===
Typikon gives a less solemn and less complex order; even the bows before entering the altar are fewer according to the Jerusalem Typikon. (Note that according to the order of Philotheus no veneration of the holy doors is indicated).

## Censing of the Sanctuary

Having vested, the priest 'censes the holy table (altar) crosswise round about and the entire sanctuary, and having opened the holy doors, goes forth.' The holy doors are customarily opened before the beginning of the censing, which does not contradict the present direction, since the latter expression can signify in general: he goes forth through the open holy doors. 'Censes crosswise' is an echo of that practice of censing when the censer was without chains and it was convenient to form a cross with it; today the crosswise manner of censing is replaced by its threefold repetition.

## "Arise" or "Command"

Following the censing of the sanctuary, the taper-lighter, according to the direction of the Typikon, or the deacon, according to accepted practice, standing before the holy doors with candle in hand, proclaims in a loud voice: **"Arise!"** (*Возстаните!*). All arise. In the Greek Typikon and in our earlier Typika at this place there was appointed the exclamation not **"Arise!"**, but **"Command!"** (*Повелите!*). In the earliest manuscript of the Jerusalem Typikon—the Georgian manuscript of the Shiomgvime Monastery: 'arise.' But in that competing with it in antiquity, Moscow Rumyantsev Museum, Sevastyanov Collection No. 491/35: *κελεύσατε*. So also in all Greek Typika of the 14th c. and the *Diataxis* of Patriarch Philotheus. In manuscript Slavic Typika of the Moscow Synodal Library Nos. 328/383 and 329/384 of the 14th c.: *келепсаите* [*kelepsaite*]; in No. 332/385 of the 14th c.: *келепсаите, рекше встанете* ('kelepsaite, that is, arise'); in No. 678/386 of the 15th c. and others, and in the first printed editions, ending with the edition of Patriarch Joseph in 1641: *келепсаите; рекше по речи исъкуству повелите* ('kelepsaite; that is, artificially rendered, command'); that is, these Typika regarded *kelevsate* as an artificial expression for 'arise.' This latter remark is retained also in the present Old Believer Typikon. — *Κελεύσατε* (*Keleusate*), **"Command"**, an exclamation used according to the present Typikon at the ordination of a presbyter and deacon and at the Presanctified Liturgy before the words **"The light of Christ illumines all"**, entered into divine worship from the Byzantine court ceremonial. By this exclamation masters of ceremonies invited dignitaries at imperial receptions to enter into certain halls of the palace or to depart from them. In turn, into the Byzantine court the exclamation was borrowed from Roman practice: with
"""

FOOTNOTES_TEXT = """[^1974]: MS of the Moscow Synodal Library No. 330/380, fol. 202–200 [sic].
[^1975]: Dmitrievsky, A. *Typika*, pp. LXXVII ff.
[^1976]: Kekelidze, K., Archpriest. *Liturgicheskie gruzinskie pamyatniki v otechestvennykh knigokhranilishchakh i ikh nauchnoe znachenie* [Liturgical Georgian Monuments in Russian Repositories and Their Scientific Significance]. Tiflis, 1908, p. 308.
[^1977]: MS of the Moscow Synodal Library No. 328/383, fol. 40 and verso.
[^1978]: That is, the semantron (*bilo*). The earlier terminology, adapted not to bells but to semantra, was not corrected.
[^1979]: Typikon, chap. 48, Dec. 25, Jan. 6; chap. 50, on Holy and Great Sunday of Pascha.
[^1980]: MS of the Moscow Rumyantsev Museum, Sevastyanov Collection No. 491/35, fol. 1 verso; Kekelidze, K., Archpriest. *Liturgicheskie pamyatniki*, p. 315.
[^1981]: MS of the Moscow Synodal Library No. 328/383, fol. 1 verso.
[^1982]: For example, MS of the Museum of the Kyiv Theological Academy Aa 194 (16th c.), pp. 18–19.
[^1983]: Rule 36 of St. Pachomius the Great.
[^1984]: Savvaitov, P. *Puteshestvie Novgorodskago arkhiepiskopa Antoniya v Tsar'grad v kontse XII-go stoletiya* [The Journey of Archbishop Anthony of Novgorod to Tsargrad at the End of the 12th Century]. St. Petersburg, 1872, pp. 17, 103.
[^1985]: Kekelidze, K., Archpriest. *Liturgicheskie pamyatniki*, p. 315.
[^1986]: MS of the Moscow Rumyantsev Museum, Sevastyanov Collection No. 491/35, fol. 1 verso; Moscow Synodal Library No. 328/383, fol. 1 verso and No. 329/384, fol. 13.
[^1987]: MS of the Moscow Synodal Library No. 332/385, fol. 3 verso; No. 678/386, fol. 4.
[^1988]: MS of the Moscow Synodal Library No. 331/387, fol. 4 verso.
[^1989]: *Εὐταξίας* [*Eutaxias*], according to the observation of Goar (*Euchologion sive rituale graecorum*. Venice, 1730, p. 23), is the same as *magister caeremoniarum*, an overseer of good order in the church who points out places to those entering—in antiquity such a duty lay upon the deacon, and was subsequently transferred unto the lower orders of clergy, and, as is evident from the present passage, unto orders of the same rank as the reader. In a monastery the *eutaxias* corresponds to the paraecclesiarch or taper-lighter.
[^1990]: Goar. *Euchologion*, p. 9.
"""

def main():
    root = Path(__file__).resolve().parent.parent
    mon_dir = root / "Liturgical Monuments" / "Monument 6 - 1910 Skaballanovich Typikon"
    source_file = mon_dir / "Source Text" / "1910_skaballanovich_typikon_cohort59_source.txt"
    draft_file = mon_dir / "Draft" / "1910_skaballanovich_typikon_cohort59_raw_draft.md"
    fn_file = mon_dir / "Draft" / "1910_skaballanovich_typikon_cohort59_footnotes.txt"

    source_file.parent.mkdir(parents=True, exist_ok=True)
    draft_file.parent.mkdir(parents=True, exist_ok=True)

    source_file.write_text(SOURCE_TEXT.strip() + "\n", encoding="utf-8")
    draft_file.write_text(DRAFT_MARKDOWN.strip() + "\n", encoding="utf-8")
    fn_file.write_text(FOOTNOTES_TEXT.strip() + "\n", encoding="utf-8")

    print(f"Wrote source to: {source_file}")
    print(f"Wrote draft to: {draft_file}")
    print(f"Wrote footnotes to: {fn_file}")

if __name__ == "__main__":
    main()
