from pathlib import Path

def build_cohort63_draft_and_footnotes():
    draft_path = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort63_raw_draft.md")
    footnotes_path = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort63_footnotes.txt")

    draft_path.parent.mkdir(parents=True, exist_ok=True)

    # Footnotes content
    footnotes_content = """[^2100]: *Sobranie drevnikh liturgiy* [Collection of Ancient Liturgies], St. Petersburg, 1874–1878, II, pp. 187–189.
[^2101]: Goar, J. *Euchologion*, p. 38. In the Gallican Liturgy, after the Trisagion, before the readings, there is appointed *Kyrie eleyson* or *rogationes*, by which is understood a litany, and it is restored according unto Eastern models (which ones?) in the following form:
Deacon: In peace let us pray unto the Lord. Choir: Lord, have mercy.
D.: Let us pray for the peace of the whole world, for the good estate and union of the Holy Churches of God. Ch.: Lord, have mercy.
D.: Let us pray unto the Lord for the pastors of the Church, bishops, deacons, for all the clergy and all the Christian people. Ch.: Lord, have mercy.
D.: Let us pray unto the Lord for sovereigns and all that are in authority, that they may execute the work of their governance in righteousness and love. Ch.: Christ, have mercy.
D.: Let us pray unto the Lord, that He may grant us a temperate balance of the air and an abundance of the fruits of the earth. Ch.: Christ, have mercy.
D.: Let us pray for the salvation of travelers, the sick, prisoners, and all that suffer. Ch.: Christ, have mercy.
D.: Let us pray unto the Lord for the preservation of peace among all nations. Ch.: Lord, have mercy.
D.: Let us pray unto the Lord, that He may deliver us from every evil, spiritual or temporal. Ch.: Lord, have mercy.
D.: Let us pray unto the Lord, that He may forgive our transgressions and account us worthy to live holily and receive everlasting life. Ch.: Lord, have mercy.
Thereupon follows a prayer (*collectio*) with the response of the choir: Amen (*Sobranie drevnikh liturgiy*, IV, p. 97).
[^2102]: *Testamentum*, I, 35; Rahmani, I. *Testamentum Domini nostri Jesu Christi*. Moguntiae, 1899, pp. 85–89.
[^2103]: Consequently, the prayer was kneeling.
[^2104]: *Apostolic Constitutions*, VIII, 10; cf. 13.
[^2105]: *Apostolic Constitutions*, VIII, 6.
[^2106]: In the initial litany the following petition is found only in the Paris MS No. 476.
[^2107]: From this light is shed upon the mention of seafarers: pilgrims unto Palestine frequently traveled by sea.
[^2108]: Swainson, C. A. *The Greek Liturgies*, London, 1884, pp. 246–252, 224, 228, 232; Dmitrievsky, A. *Bogosluzhenie strastnoy i paskhal'noy sedmits* [Divine Services of Passion and Paschal Weeks], Kazan, 1894, pp. 272–283.
[^2109]: Orlov, M. *Liturgiya sv. Vasiliya Velikago* [The Liturgy of St. Basil the Great], St. Petersburg, 1909, pp. 41–50; Dmitrievsky, A. *Euchologia*, Kyiv, 1901, p. 134; Goar, J. *Euchologion*, p. 52; Kekelidze, K., Archpriest. *Liturgicheskie gruzinskie pamyatniki* [Georgian Liturgical Monuments], Tiflis, 1908, pp. 49, 192.
"""

    with open(footnotes_path, "w", encoding="utf-8") as f:
        f.write(footnotes_content)
    print("Footnotes written! Total lines:", len(footnotes_content.splitlines()))

    # Draft content leaf by leaf
    leaf_p621 = """=== LEAF p621 ===
## The Litany in the Armenian Liturgy

Already entirely close unto our litanies are the diaconal petitions in the Armenian Liturgy, attributed unto St. Gregory, the Illuminator of Armenia (4th c.). After several brief litanies (such a term is not employed) at the beginning of the liturgy, here, following immediately upon the Trisagion before the "psalm of the day" and the readings, there is appointed a litany replacing our Great and Augmented [Litanies], consisting of twelve petitions, with the response unto the first nine **"Lord, have mercy"**, unto the tenth **"Unto Thee, O Lord, let us commit ourselves"**, unto the eleventh **"Lord, have mercy"** thrice, and unto the twelfth a brief prayer of the priest for the acceptance of the prayer (corresponding unto the exclamation).

1. Again and again in peace let us pray unto the Lord. 2. For the peace of the whole world and the establishment of the Holy Church ("Let us pray unto the Lord" down unto the 9th petition). 3. For all holy and Orthodox bishops. 4. For our lord, the most holy Patriarch, for the health and salvation of his soul. 5. For our archbishop or bishop. 6. For the vartabeds (the episcopal council under the Catholicos), priests, deacons, subdeacons, and all the clergy of the Church. (7. Here for the sovereign and the reigning house our present petition is employed, but only among the Russian Armenians). 8. For the souls of the departed who have fallen asleep in the true and Orthodox faith in Christ. 9. Again for the unity of our true and holy faith. 10. Ourselves and one another let us commit unto the Lord God Almighty. 11. Have mercy upon us, O Lord our God, according unto Thy great mercy; let us all say with one accord. 12. Bless, master. The priest [recites] the prayer secretly [^2100].

## The Litany in the Ambrosian Liturgy

Closer even than this litany unto our Great Litany is the *prosphonesis* (proclamation) in the ancient rite of the Ambrosian Liturgy.

"Deacon: In accordance with the duty unto Divine peace and pardon (*Divinae pacis et indulgentiae munere*), imploring with the whole heart and the whole mind, we beseech Thee (*precamur te*). People: Lord, have mercy (*Domine miserere*, and so unto each petition). Deacon: For (*pro*) the Holy Catholic Church, which is here and dispersed throughout the whole world, we beseech Thee (so each petition concludes). For our Pope"""

    leaf_p622 = """=== LEAF p622 ===
N. and our Pontiff (*pontifice*) N. and all their clergy, and all priests and ministers (*ministris*). For Thy servant N. the Emperor and Thy handmaid N. the Empress and all their army. For Thy servant N. our King and Prince (*duce*) and all his army. For the peace of the Churches, the calling of the gentiles, and the tranquillity of nations. For this city (*civitate*) and its preservation, and for all that dwell therein. For the temperate balance of the air (*aeris temperie*) and of the fruits (*fructuum*), and the fertility of the lands. For virgins, widows, orphans, prisoners, and penitents. For travelers, for those that sail by sea, *(Orig. p. 520)* in prisons, in bonds, in mines (*in metallis*), and in exile. For those who are held fast by diverse infirmities, who are tormented by unclean spirits. For those who in Thy Holy Church are bountiful in the fruits of mercy. Hear us in our every prayer and supplication, we beseech Thee. Let us all say. People: Lord, have mercy (*Domine miserere*). *Kyrie eleyson* thrice" [^2101].

## The Litany of the Testamentum and the Apostolic Constitutions

Yet in direct genetic dependence our litanies stand unto the diaconal prayers in the liturgies of the Syrian-Antiochene and Jerusalem recensions. The former are provided by the canonical-liturgical monuments of the 3rd century, the *Testamentum of Our Lord Jesus Christ*, and of the 4th–5th centuries, the *Apostolic Constitutions* (see concerning them the Introductory Chapter, pp. 70 et seq.). In both the one and the other such a diaconal prayer is appointed after the dismissal of the catechumens; in the second monument it is repeated also after the hallowing of the Gifts (the absence of a numeral in the second column signifies that the petition is found in the litany after the hallowing of the Gifts).

### Testamentum Domini

1. Let us pray unto the Lord God and our Savior Jesus Christ.
2. For the peace which is from heaven let us pray, that the Lord by His mercy may grant us peace.
3. For our faith let us pray, that the Lord may grant us unto the end to keep faithfully the faith which is in Him.
4. For concord and oneness of mind let us pray, that the Lord in"""

    leaf_p623 = """=== LEAF p623 ===
oneness of mind may preserve our spirits.
5. For patience let us pray, that the Lord in all tribulations may grant patience unto the end.
*(Orig. p. 521)*
6. For the Apostles let us pray, that the Lord may grant us to be well-pleasing unto Him, even as they also were well-pleasing unto Him, and make us worthy of their inheritance.
7. For the holy prophets let us pray, that the Lord may number us with them.
8. For the holy confessors let us pray, that the Lord God may grant us with the same mind wherewith they ended their course to finish [our life].
9. For the bishop let us pray, that our Lord may preserve him long-lived in the faith, that rightly dividing the word of truth, he may preside over the Church in purity and without blemish.
10. For the presbyters let us pray, that the Lord may not take away from them the spirit of the presbyterate, and may grant them diligence and piety unto the end.
11. For the deacons let us pray, that the Lord may grant them to run their course blamelessly, to fulfill holiness, and may remember their labor and love.
12. For the presbyteresses let us pray, that the Lord may hear their supplication, and in perfection in the grace of the Spirit may preserve their hearts and help their labor.
13. For the subdeacons, readers, and deaconesses let us pray, that the Lord may grant them to receive their reward in patience.
14. For the faithful laity let us pray, that the Lord may grant them to keep the faith in perfection.
*(Orig. p. 522)*
15. For the catechumens let us pray, that the Lord may grant them to be worthy of the laver of remission and hallow them with the sign of holiness.
16. For the kingdom let us pray, that the Lord may grant it peace.
17. For the civil authorities let us pray, that the Lord may grant them understanding and His fear.
18. For the whole world let us pray, that the Lord may provide for each, granting unto each one that which is profitable.
19. For travelers and those that sail by sea let us pray, that the Lord may guide them with the right hand of mercy.
20. For those who endure persecutions let us pray, that the Lord may grant them patience and knowledge, and bestow upon them perfect labor.
21. For the departed who have passed away from the Church let us pray, that the Lord may grant them a place of rest.
*(Orig. p. 523)*"""

    leaf_p624 = """=== LEAF p624 ===
22. For those who have fallen let us pray, that the Lord may not remember their folly and may turn away His chastisement from them.
23. For ourselves likewise, all who stand in need of prayers, let us pray, that the Lord may shelter us, and keep us in a meek spirit.
24. Let us pray, let us beseech the Lord, that He may accept our prayers.
25. Let us arise in the Holy Spirit, that having become wise thereunto, we may grow in His grace, that in His name we may be glorified and upon the foundation of the Apostles be built up; and praying, let us beseech the Lord, that He may graciously accept our supplications [^2102].

*(Orig. p. 520)*
### Apostolic Constitutions

1. Let us pray unto God through His Christ; let us all with one accord pray unto God through His Christ.
2. For the peace and good estate of the world and the Holy Churches let us pray, that the God of all things may grant us His unceasing and inalienable peace, and keep us abiding in the fullness of virtue which is according unto godliness.
*(Orig. p. 521)*
3. For the Holy Catholic and Apostolic Church which is from the ends even unto the ends [of the earth] let us pray, that the Lord may preserve it unshaken and untossed by waves, and keep it until the end of the age founded upon the rock.
4. And for the holy diocese (*oblast'*) which is in this place let us pray, that the Lord of all things may account us worthy unstintingly to pursue His super-celestial hope and render unto Him the unceasing debt of supplication.
Let us commemorate the holy martyrs, that we may be accounted worthy to be partakers of their struggle.
5. For the whole episcopate under heaven, rightly dividing the word of Thy truth, let us pray; and for our bishop James and his parishes (*oblasti*) let us pray; for our bishop Clement and his parishes let us pray; for our bishop Evodius and his parishes let us pray; that the God of mercies may grant them unto His Holy Churches in health, honor, length of days, and bestow upon them an honorable old age in godliness and righteousness.
6. And for our presbyters let us pray, that the Lord may deliver them from every unseemly and evil deed, and grant them a presbyterate sound and honorable.
7. For the whole diaconate and ministry (*hypēresia*) in Christ"""

    leaf_p625 = """=== LEAF p625 ===
let us pray, that the Lord may grant them a blameless ministry.
8. For readers, singers, virgins, widows, and orphans let us pray; for those who are in marriage and childbearing let us pray, that the Lord may have mercy upon them all.
9. For eunuchs who walk in holiness let us pray.
10. For those who are in continence and piety let us pray.
11. For those who bear fruit in the holy churches and give alms unto the poor let us pray; and for *(Orig. p. 522)* those who offer sacrifices and firstfruits unto the Lord our God let us pray, that the All-Good God may recompense them with His heavenly gifts, and grant them a hundredfold in the present world, and in that which is to come everlasting life, and bestow upon them eternal things instead of temporal, heavenly things instead of earthly.
12. For our newly enlightened brethren let us pray, that the Lord may confirm and strengthen them.
For kings and those that are in authority (*hyperochē*) let us pray, that they may be peaceably inclined toward us, that we may lead a quiet and tranquil life in all godliness and purity.
For the temperate balance of the air and the ripening of the fruits let us pray.
13. For our brethren that are in infirmity let us pray, that the Lord may deliver them from every sickness.
14. For travelers and those that sail by sea let us pray.
15. For those who are in the mines, in banishment, in prisons, and in bonds for the sake of the name of the Lord.
16. For those who labor in bitter servitude (*douleia*) let us pray.
17. For our enemies and those that hate us let us pray; for those who persecute us for the sake of the name of the Lord let us pray, that the Lord, having subdued their wrath, may scatter their fury against us.
18. For those who are outside and for the wandering let us pray, that the Lord may convert them.
19. Let us remember the infants of the Church, that the Lord, having perfected them in His fear, may bring them unto the measure of their stature.
For those who have fallen asleep in the faith let us pray.
*(Orig. p. 523)*
20. For one another let us pray, that the Lord by His grace may preserve and keep us unto the end, and deliver us from the evil one and from all the stumbling blocks of those that work iniquity, and shepherd us into His Heavenly Kingdom.
21. For every Christian soul let us pray.
22. Save us and raise us up, O God, by Thy mercy.
23. Let us arise [^2103]. Having prayed fervently, ourselves and one another let us commit unto the living God through His Christ [^2104]."""

    leaf_p626 = """=== LEAF p626 ===
Unto each petition the choir and the people, according unto the *Apostolic Constitutions*, respond **"Lord, have mercy"** [^2105].

## The Great Litany in the Liturgy of the Apostle James

In the proper sense, the first recension of the present Great Litany was the litany in the liturgy of the Jerusalem type, attributed unto the Apostle James—a liturgy in relation unto which the entire liturgy of the Asia Minor–Constantinopolitan recension (Basil the Great and John Chrysostom) is a simple abbreviation. Here the litany, it would seem, first received also its Greek name *συναπτή* (*synaptē*, already in 11th-century MSS), *καθολικὴ συναπτή* (*katholikē synaptē*) or simply *καθολική* (*katholikē*, 14th-century MSS). The litany corresponding unto our great one is here read in its full form after the kiss [of peace] before the Eucharistic prayer (anaphora), in an abbreviated form at the beginning of the liturgy, and in the number of several petitions with the petitions of the Augmented and Petitional Litanies before the Gospel and after the Gospel. In the most ancient Greek manuscript of the Liturgy of the Apostle James from the library of the University of Messina (10th c.) and in MS No. 1040 of the Sinai Library (11th c.), in the place of the first litany there is a lacuna. In its entirety in all four places of the liturgy the Great Litany is read by the manuscripts from the Basilian Monastery of Rossano (in Calabria, 11th c.) and Paris National Library No. 2509 (14th c.). The manuscript of the latter library No. 476 (14th c.) has only the opening words of the petitions, and for the litany after the kiss of peace gives only the beginning with a reference unto the earlier exposition. In its full scope (after the kiss of peace) the litany hath such a form (crosses prefixed denote petitions that enter also into the initial litany of the liturgy):

+ **"In peace let us pray unto the Lord. Save us, have mercy on us, be bountiful unto us** (Sinai MS: + **defend us**), **and preserve us, O God, by Thy grace.** + **For the peace from on high** *(Orig. p. 524)* **and the love of God toward mankind** (Sinai MS: + **oneness of mind**) **and the salvation of our souls, let us pray unto the Lord** (Paris MS No. 476 hath not this petition). + **For the peace of the whole world and the union of all the Holy Churches, let us pray unto the Lord. For this holy monastery** (the italics are absent in Paris MS No. 2509), **the Catholic and Apostolic Church which is from the ends of the earth even unto the ends thereof, let us pray unto the Lord.** (The Sinai MS instead of this petition hath: *For this holy monastery, Catholic and αποουσης (?), every city and countryside, and those who in Orthodox faith and piety of Christ dwell therein, for their peace and establishment, let us pray unto the Lord*—cf. below). + **For**"""

    leaf_p627 = """=== LEAF p627 ===
**the salvation and protection of N., our most holy Patriarch** (in the initial litany the Rossano MS: *of our most venerable fathers N. and N., the most holy Patriarch*; the Paris [MS] names the names), **of all the clergy and the Christ-loving people, let us pray unto the Lord** (this petition is not in the litany after the kiss in the Sinai and Paris [MSS]). (+) [^2106] **For our most pious and God-crowned Orthodox sovereigns** (Messina: *For our most pious and Christ-loving sovereign*), **their entire court and army, for help from heaven, protection** (the italics are absent in Messina and Paris) **and victory for them, let us pray unto the Lord** (the petition is absent in Sinai). (+) [^2106] **For the holy city of Christ our God, and for this our reigning and God-named city, for every city and countryside, and for those who in Orthodox faith and the fear of God dwell therein, for their peace and establishment, let us pray unto the Lord** (the italics are absent in Paris; the first italicized phrase and "of God" are absent in Messina; the whole is absent in Sinai, but see above). **For those who bear fruit and do good works in the holy churches of God, who remember the poor, the widows and orphans, strangers and those in need, and for those who have charged us to remember them in prayers, let us pray unto the Lord** (in Messina in the margin, and the first participle is in the past tense: "who have borne fruit"). **For those who are in old age and infirmity, the sick, the suffering, those held fast by unclean spirits, for their speedy healing and salvation from God** (Sinai: *and for every Christian soul that is afflicted and oppressed, standing in need of God's mercy and help, for the healing of the ailing*), **let us pray unto the Lord** (the petition is absent in Messina). **For those who dwell in virginity and purity, in ascetic labor and honourable wedlock, for the holy fathers and brethren who labor in asceticism in the mountains and caves and dens of the earth, let us pray unto the Lord** (in Messina in the margin). **For travelers, seafarers, Christians living in foreign lands (*xeniteuontōn*—exiles/emigrants), and for our brethren that are in captivities and banishments, in prisons and bitter servitude, for the peaceful return of each unto his home with joy, let us pray unto the Lord** (absent in Messina). — **For our fathers and brethren who are present with us and pray together with us at this holy hour and at every season, for their diligence, labor, and zeal, let us pray unto the Lord** (the petition is absent in Messina, but instead thereof: *For Christians who have come and are coming to worship in these holy places of Christ, for the peaceful return of each of them shortly unto his own with joy*; in Sinai instead of the last two petitions before the petition for the aged and sick there is this: *For Christians who come to worship in these holy places of Christ*"""

    leaf_p628 = """=== LEAF p628 ===
*, travelers, seafarers* [^2107], *exiles, and our brethren who are in capti*(Orig. p. 525)*vity, for the peaceful return of each of them unto his own*). **For every Christian soul that is afflicted and oppressed, standing in need of the mercy and help of God, for the turning back of the wandering, the health of the infirm, the deliverance of the captive, the repose of our fathers and brethren who have previously fallen asleep, let us pray unto the Lord** (before the italics is absent in Sinai, but see above; instead of the italics Messina hath: "fervently" (*ektenōs*), and before it the petition: "*For our ailing and laboring fathers and brethren, and those possessed by unclean spirits, for their speedy healing and salvation from God*"). + **For the remission of our sins and the pardon of our offenses, and that we may be delivered from all affliction, wrath, danger** (italics absent in Sinai) **and necessity, from the uprising of nations, let us pray unto the Lord. More fervently** (*ektenesteron*; absent in Messina and Sinai) **for the temperate balance of the air, peaceful rains, good dew** (italics absent in Messina), **an abundance of blessed** (Messina: *consecrated*) **fruits, the perfect beauty of the seasons, and for the crown of the year, let us pray unto the Lord.** (Only in Messina and Sinai: *For the commemoration* [Sinai: *and repose of all*] *of our holy* [Sinai: *and blessed*] *fathers, who from St. James the Apostle and Brother of the Lord and first Archbishop down unto* [a series of names differing in both MSS] *and the rest of our venerable fathers and brethren*). **That our supplication may be heard and well-pleasing before God, and that His rich mercies and bounties may be sent down upon us all, and that He may account all worthy of the Kingdom of Heaven, fervently** (Messina, Paris: *unto the Lord*) **let us pray** (the 1st and 2nd italics are absent in Paris; "fervently" is absent in Messina and Paris). + **Commemorating our all-holy, immaculate, most glorious, [(most)] blessed Lady, the Theotokos and Ever-Virgin Mary, [(the honorable bodiless Archangels)], the holy and blessed John the glorious Prophet, Forerunner, and Baptist, Stephen the First Deacon and Protomartyr, Moses, Aaron, Elijah, Elisha, Samuel, David, Daniel, the (holy) [divine, sacred, and glorious (Apostles)], (glorious) Prophets (and triumphantly victorious Martyrs), and all [with all] the saints and the righteous, that by their prayers and intercessions we may find mercy** (parentheses denote what is found only in the Messina MS; square brackets—in Sinai; italics—in Rossano and Paris; spaced type—in Rossano; for the initial litany instead of the names of the prophets after the Baptist: "the divine and"""

    leaf_p629 = """=== LEAF p629 ===
all-praised Apostles, glorious Prophets, victorious Martyrs, and all the saints..."). **People: Lord, have mercy** thrice (absent in Messina and Sinai; in the initial litany of Rossano also after the 1st petition: "People: Lord, have mercy"; at the 4th litany the same [MS] and Paris No. 2509 at the end of the litany: "People: Unto Thee, O Lord"). The Sinai [MS] hath yet a petition for the offered Gifts, and after **"Let us stand aright"** directs the deacon standing on the right to read the diptychs of the living, giving two petitions: the 1st for the bishops with an enumeration of the names of the patriarchs, the 2nd for the rest of the clergy and Christians of diverse estates; the deacon standing on the left then reads the diptychs of the departed consisting of two petitions: the 1st for the saints with an enumeration of many names, beginning with the Mother of God, the 2nd for the departed Christians of diverse estates, beginning with the presbyters, with an enumeration of the names of the emperors; "and again the deacon on the right: *For the peace and good estate of the whole world and the union of all the Holy God's* *(Orig. p. 526)* *Orthodox Churches, and for those for whom each hath offered or hath in mind, and for the standing, Christ-loving people. People: And all and each*" [^2108].

## Ancient Variants of the Great Litany

Inasmuch as the Liturgies of Basil the Great and John Chrysostom were an abbreviation, it would seem, of the Jerusalem Liturgy of the Apostle James, so also the litanies therein were an abbreviation of the litany of the latter. In the Liturgies of Basil the Great and John Chrysostom the Great Litany appears in its present form from the most ancient among the complete manuscripts known today, the oldest of which do not, however, ascend earlier than the 11th century (8th–10th century manuscripts contain only priestly prayers). In comparison with the present text of the litany, manuscripts and early printed editions of the Sluzhebnik yield for the Great Litany only the following insignificant variant readings:
The 5th petition in Greek MSS of the 11th, and at times also 14th–16th c., begins: "For our bishop, the honorable presbyterate..."; in Greek MSS of the 12th c. and the majority of the 14th–15th c., in printed Greek, and in Slavic MSS: "For our archbishop, the honorable presbyterate..."; printed Slavic put here in the first place: "For the Patriarch", later ones: "For the Patriarch N...", still later: "For the Most Holy Governing Synod".
The 6th, 7th, and 8th petitions Greek MSS of the 11th c. do not have; from the 12th c. they appear in the form: "For our most pious and God-preserved (some: 'and Christ-loving') sovereigns, their entire court..."; so also in printed Greek, but later Greek frequently omit [them] (owing to Turkish rule); the most ancient Slavic MSS—14th c.: "For the orthodox"""

    leaf_p630 = """=== LEAF p630 ===
prince, all his boyars, and his warriors"; somewhat later—15th c.: "For our pious and God-preserved princes (others: N)..."; or: "For the orthodox and God-preserved grand prince"; later still: "For the orthodox (others: and God-preserved) tsar and grand prince N"; so also the most ancient printed [editions]; later: + "and for his orthodox tsaritsa and grand duchess N, and for the orthodox tsarevnas"; "For our pious and God-preserved tsar N, and for the pious and God-preserved tsaritsa N, and for the noble tsarevich N, and for the noble tsarevnas N"; "For our sovereign the tsar and grand prince N, the sovereign tsaritsa and grand duchess N, our sovereign the tsarevich and grand prince"; still later in addition unto this: "for the most pious, most gentle, most autocratic, and God-preserved [emperor]... and for his most pious [empress]... and for the whole court...".
The 9th petition in the majority of Greek MSS of the 11th–17th c. and some Slavic of the 15th c.: "For this holy monastery and every city"; in some Greek MSS from the 15th c. and Slavic from the 13th c.: "For this city and every city"; in some Greek: "For the holy monastery or for the city"; in some Slavic: "If it be a monastery: For the holy monastery; but if it be in a city: For this city"; in others: "For this city and this holy monastery"; "For this city, if it be in a monastery: and for this holy monastery".
In the 12th petition "That we may be delivered", many MSS and printed editions after "wrath" have also "danger" (*kindynou*), besides "and necessity". After this petition 13th-century Georgian MSS have yet a petition: *(Orig. p. 527)* "And for all who stand in need of help from God, and for mercy upon them" (or "our souls").
The 13th and 14th petitions: **"Help us"** and **"Commemorating our all-holy"** are omitted by one Euchologion, presumably of the 12th–13th c., one of the 17th c., and the first Greek editions, placing also the exclamation of the Great Litany after the first Little Litany.
In the 14th petition (**"Commemorating our all-holy"**), "glorious" is found only in some 16th-century Greek MSS, printed Greek from 1838, and Slavic from 1655; some 12th-century Greek have before "with all the saints": "our father among the saints N" (the patron saint of the temple or the saint of the day?); Georgian MSS of the 13th and 17th c. have in this same place: "the holy Heavenly Hosts"; at the following Little Litany in this same place: "the holy glorious Prophet, Forerunner, and Baptist John", and at the following: "the holy and all-praised Apostles" [^2109].

## "Lord, Have Mercy" in the Litany

Inasmuch as the petitions of the litany are for the most part only an invitation unto prayer, the prayer itself in the litany is properly reduced unto the repetition of the concise **"Lord, have mercy."** Such a form of prayer cannot fail to appear poor. Yet scarcely could one find a more immediate and vivid expression for our fundamental and constant relationship unto God, from Whom man in every"""

    draft_content = "\n\n".join([leaf_p621, leaf_p622, leaf_p623, leaf_p624, leaf_p625, leaf_p626, leaf_p627, leaf_p628, leaf_p629, leaf_p630]) + "\n"

    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(draft_content)
    print("Draft written! Total lines:", len(draft_content.splitlines()), "Total bytes:", len(draft_content.encode('utf-8')))

if __name__ == '__main__':
    build_cohort63_draft_and_footnotes()
