import os
import sys
from pathlib import Path

draft_text = """=== LEAF p981 ===
Deacon: Let us pray unto the Lord for the preservation of peace among all nations.

Choir: Lord, have mercy.

D.: Let us pray unto the Lord, that He may deliver us from all evil, both spiritual and temporal.

Ch.: Lord, have mercy.

D.: Let us pray unto the Lord, that He may forgive our transgressions and vouchsafe us to live holily and to obtain life eternal.

Ch.: Lord, have mercy. Then follows the prayer (*collectio*) with the response of the choir: Amen (*Collection of Ancient Liturgies*, IV, 97).

268. *Testament* [of Our Lord], I, 35; I. Rahmani, *Testamentum Domini nostri Jesu Christi*, Mainz [Moguntiae], 1889, pp. 85–89.

269. Consequently, the prayer was wont to be kneeling [genuflective].

270. *Apostolic Constitutions*, VIII, 10; cf. 13.

271. *Apostolic Constitutions*, VIII, 6.

272. In the initial litany, the following petition is found only in the Paris manuscript No. 476.

273. From this light is shed upon the mention of them that sail: pilgrims unto Palestine frequently traveled by sea.

274. C. A. Swainson, *The Greek Liturgies*, pp. 246–252, 224, 228, 232; A. Dmitrievsky, *Divine Services of Passion and Paschal Weeks* [*Богослужение страстной и пасхальной седмицы*], pp. 272–283.

275. Archpriest Orlov, *The Liturgy of St. Basil the Great* [*Литургия св. Василия Великого*], pp. 41–50; A. Dmitrievsky, *Euchologia* [*Евхологионы*], p. 134; J. Goar, *Euchologion*, p. 52; Archpriest K. Kekelidze, *Liturgical Monuments of Georgia* [*Литургические грузинские памятники*], pp. 49, 192.

276. Epictetus, *Enchiridion*, II, 7.

277. Ps. 4:2 [MT 4:1]; 6:3 [MT 6:2]; 9:14 [MT 9:13]; 24:16 [MT 25:16]; 25:11 [MT 26:11]; 26:7 [MT 27:7]; 30:10 [MT 31:9]; 40:5, 11 [MT 41:4, 10]; 55:2 [MT 56:1]; 56:2 [MT 57:1]; 85:3 [MT 86:3], etc. Cf. Matt. 9:27; 15:22; 17:14; 20:30; Mark 10:47; Luke 16:24; 17:13; 18:38–39; J. B. Lüft, *Liturgik*, Mainz, 1844, II, p. 69.

278. It is possible that the original forms of the acclamation were, as occasionally in the Armenian Liturgy: “Save, O Lord,” “Save, O Lord, and have mercy,” and as in the Malabar Liturgy: “Our Lord, have mercy upon us” (*Collection of Ancient Liturgies*, II, 193, 199; A. Petrovsky, *Apostolic Liturgies* [*Апостольские литургии*], Appendix, p. 63).

279. St. Augustine, *Epistle* 178.

280. Radulphus de Rivo (of Tongres), *De canonum observantia propositiones*, propos. 23.

281. Council of Vaison [Concilium Vasense], Canon 3.

282. St. Gregory the Great, *Epistles*, VII, 12; II, 63.

283. Cap. VI, 205, 197; J. B. Lüft, *Liturgik*, II, p. 70.

284. J. Mabillon, *Commentarius in ordinem Romanum*, II, 34.

285. Prov. 16:4; Heb. 2:10; John 17:4.

286. 1 Pet. 5:11 according unto certain codices.

287. 1 Tim. 1:17; 1 Pet. 4:11; Rev. 1:6; 1 Tim. 6:16. “Glory and dominion” is the customary concluding doxology also in

=== LEAF p982 ===
the Euchologion attributed unto Serapion, Bishop of Thmuis, of the 4th century (A. Dmitrievsky, *The 4th-Century Euchologion of Serapion, Bishop of Thmuis* [*Евхологий IV в. Серапиона, еп. Тмуитского*], Kyiv, 1894).

288. *First Epistle of Clement of Rome*, 20:12; 61:3; *Teaching of the Twelve Apostles* [*Didache*], 8:3; 9:3; 10:3; *Apostolic Constitutions*, VIII, 11, 20.

289. Matt. 5:13 [sic, 6:13] (in the Syriac text: “The kingdom and the glory”); *Apostolic Constitutions*, VII, 47; VIII, 12.

290. Jude 25; Rev. 5:13; *1 Clement* 64; *Martyrdom of Polycarp*, 20:2, 21.

291. *1 Clement* 65:2; *Apostolic Constitutions*, VIII, 13, 15.

292. Rev. 7:12; E. von der Goltz, *Das Gebet in der ältesten Christenheit*, p. 158.

293. C. A. Swainson, *The Greek Liturgies*, pp. 220, 222, 228, 246, 266, 302.

294. F. X. Funk, *Didascalia et Constitutiones Apostolorum*, Paderborn, 1905, II, p. 189. — Akin unto our exclamations, only far more extensive, is the concluding doxology at the Jewish Paschal supper: “For unto Thee, O Lord our God and God of our fathers, appertaineth song, praise, glory, hymn, dominion, sovereignty, honor, majesty, hallowing, kingdom, blessing, and thanksgiving from henceforth and unto the ages” (I. Karabinov, *The Eucharistic Prayer* [*Евхаристическая молитва*], p. 5). Cf. 1 Chron. 29:11.

295. 1 Tim. 2:1.

296. St. John Chrysostom, *Homily 6 on 1 Timothy*.

297. Bar. 1:10–12; cf. 1 Esdr. 6:10 [Ezra 6:10].

298. Flavius Josephus, *Jewish War* [*De Bello Judaico*], II, 11.

299. St. Cyprian of Carthage, *To Demetrian* [*Ad Demetrianum*].

300. St. Optatus of Milevis, *Against the Donatists* [*Contra Donatistas*], 3.

301. Eusebius, *Ecclesiastical History*, IV, 60.

302. Pope Felix, *Epistle to the Eastern Churches*; Pope Gelasius, *Epistle to the Bishops of Dardania*.

303. Evagrius Scholasticus, *Ecclesiastical History*, III, 34.

304. J. B. Lüft, *Liturgik*, II, p. 56.

305. *Concilia Germaniae*, I, 244; J. B. Lüft, *Liturgik*, II, p. 52.

306. Capitulary of Charlemagne of the year 801, ch. 1.

307. It is thought that this removal was made originally in the Papal States, where the Pope was likewise sovereign, and was disseminated during the Reformation era when kings began to embrace it. Yet the commemoration of the king was preserved in entirely Catholic lands. The Council of Prague of 1605 requireth “always to preserve and sacredly observe the ancient and laudable custom of our Church—to pray during the celebration of the Liturgy for the Pope, the Primate, the King, and the Queen” (canon 19).

308. J. B. Lüft, *Liturgik*, II, pp. 58–61.

309. C. A. Swainson, *The Greek Liturgies*, pp. 32, 284; *Collection of Ancient Liturgies*,

=== LEAF p983 ===
p. 216; Bishop Porphyrius [Uspensky], *Doctrine and Divine Worship of the Copts* [*Вероучение, богослужение... коптов*], pp. 142, 196, 214; *Divine Services of the Abyssinians* [*Богослужение абиссин*], pp. 52, 61, 66; A. Petrovsky, *Apostolic Liturgies* [*Апостольские литургии*], p. 75.

310. Greek MS of the Moscow Rumiantsev Museum, Sevastianov Collection No. 491/35 of the 13th century, fol. 2v; Moscow Synodal Library No. 381 of the 13th–14th century, fol. 1; Slavonic MS of the Moscow Synodal Library No. 328/383 of the 14th century, fol. 3; No. 678/386 of the 15th century, fol. 5v.

311. *Typikon* [Τυπικόν], Venice [Βενετία], 1643, fol. 2; Archpriest K. Kekelidze, *Liturgical Monuments of Georgia* [*Литургические грузинские памятники*], p. 316.

312. MS of the Museum of the Kyiv Theological Academy, Aa 194, p. 21; Old Believer Typikon, fol. 5v (10).

313. C. B. Moll, *Der Psalter*, Bielefeld, 1859, I, p. 43.

314. St. Symeon of Thessalonica, *On the Divine Prayer*, ch. 332 (296).

315. *Breviarium Romanum*, *pars verna*, pp. 339–340, 344.

316. Archpriest K. Nikolsky, *Manual for the Study of the Typikon of Divine Worship of the Orthodox Church* [*Пособие к изучению устава богослужения...*], St. Petersburg, p. 191.

317. Archpriest K. Kekelidze, *Liturgical Monuments of Georgia*, p. 316; MSS of the Moscow Synodal Library No. 328/383, fol. 3; No. 329/384, fol. 14; No. 678/386, fol. 5; Museum of the Kyiv Theological Academy, Aa 194, p. 21.

318. Old Believer Typikon, fol. 5v (10v).

319. The 2nd and 3rd exclamations are given in full in the Sluzhebnik at the Liturgy of the Presanctified Gifts, and the 1st also at Vespers.

320. *Apostolic Constitutions*, VIII, 13.

321. C. A. Swainson, *The Greek Liturgies*, pp. 218, 238, 302, 320, 219.

322. J. Goar, *Euchologion*, pp. 2–3.

323. MS of the Moscow Rumiantsev Museum, Sevastianov Collection No. 491/35, fol. 2v; Moscow Synodal Library No. 381, fol. 1v.

324. Cardinal Giovanni Bona, *De divina psalmodia*, Cologne [Coloniae Agrippinae], 1667, pp. 614–620.

325. St. Gregory the Theologian, *Oration on New Sunday* [*Oratio in novam Dominicam*]; Dionysius the Areopagite, *On the Divine Names*, ch. 1.

326. St. John of Damascus, *Exact Exposition of the Orthodox Faith* [*De Fide Orthodoxa*], IV, 23.

327. Archimandrite (Archbishop) Modest [Strelbitsky], *On the Church Octoechos* [*О церковном Октоихе*], Vilna, 1865, p. 28.

328. J. B. Pitra, *Juris ecclesiastici Graecorum historia et monumenta*, Rome, 1868, II, p. 209.

329. MSS of the Moscow Synodal Typography Library No. 285/142/1206, fol. 21v; Moscow Synodal Library No. 330/380, fol. 260; No. 336/388, fol. 350; Old Believer Typikon, fol. 5v (10v). In the MS of the Moscow Theological Academy Library No. 137 of the Old Believer [Raskolnik] department, these refrains are set to musical notation.

330. Matt. 5:17; Archbishop Benjamin (Krasnopevkov-Rumovsky), *The New Tablet* [*Новая скрижаль*], in 4 parts, St. Petersburg, 1858, part I, p. 14.

331. St. Gregory the Theologian, *Poem 33*; Polychronius, *On Job*, Preface; St. Epiphanius of Salamis, *On Weights and Measures* [*De mensuris et ponderibus*]; St. Amphilochius of Iconium, *Iambics to Seleucus* [*Iambi ad Seleucum*]; St. John of Damascus, *Exact Exposition of the Orthodox Faith*, IV, 18.

332. I. Karabinov, *The Lenten Triodion* [*Постная Триодь*], St. Petersburg, 1910, p. 71.

=== LEAF p984 ===
333. A. Papadopoulos-Kerameus, *Analecta of Jerusalem Gleanings* [᾿Ανάλεκτα ἱεροσολυμιτικῆς σταχυολογίας], St. Petersburg, 1894, II, p. 119.

334. *Hypotyposis*, §§ 5, 17; *Diatyposis*, § 4; A. Dmitrievsky, *Typika* [Τυπικά], pp. 231, 232.

335. St. Symeon of Thessalonica, *On the Divine Prayer*, ch. 332 (296).

336. St. Symeon of Thessalonica, *On the Divine Prayer*, ch. 341 (305); cf. 314 (278), where the Praises stichera are termed *hymns* [ὕμνοι].

337. Archpriest K. Kekelidze, *Liturgical Monuments of Georgia*, p. 352.

338. Archpriest K. Kekelidze, *Liturgical Monuments of Georgia*, p. 355.

339. Citations—see p. 105, note.

340. J. Goar, *Euchologion*, p. 3.

341. St. Symeon of Thessalonica, *On the Divine Prayer*, ch. 332 (296).

342. Toscani, *Ad typicum graecum*, p. 52; A. Dmitrievsky, *Typika*, pp. 800, 607.

343. MS of the Moscow Synodal Library No. 330/380, fols. 3v, 7v, 12.

344. Archpriest K. Kekelidze, *Liturgical Monuments of Georgia*, p. 316; MS of the Moscow Rumiantsev Museum, Sevastianov Collection No. 491/35, fol. 3.

345. Typikon of San Nicola di Casole [Николо-Касулянский Типикон], ch. 12. The biographer of St. John of Damascus stateth concerning him that he set the beginning of his first book with the words “Thy victorious right hand” [*Cheti-Minei*, December 4]. A certain Slavonic MS attributeth unto St. John of Damascus not the Octoechos, but only the Heirmologion (Archbishop Philaret [Gumilevsky], *Historical Survey of the Hymnographers and Hymnody of the Greek Church* [*Исторический обзор песнопевцев и песнопения греческой Церкви*], Chernihiv, 1864, p. 261).

346. Only the Octoechos in chapter 4 in the text calleth them “the creation of Anatolius” [*творение Анатолиево*].

347. V. P-sky [Petrovsky], “On the Author of the Sunday and Other Stichera Termed in Slavonic Liturgical Books ‘Eastern’ or Anatolian” [*Об авторе воскресных и др. стихир, называемых в слав. богосл. книгах «восточными» или Анатолиевыми*], *Rukovodstvo dlia selskikh pastyrei*, 1894, I, p. 222.

348. Archbishop Philaret [Gumilevsky], *Historical Survey of the Hymnographers and Hymnody of the Greek Church*, Chernihiv, 1864, p. 193.

349. See note 4 on p. 545.

350. A. Dmitrievsky, *Typika*, pp. 800, 607; MS of the Moscow Synodal Library No. 330/380, fols. 3v, 9v, 12.

351. Thus is it proposed in V. Rozanov, *Typikon of Divine Worship of the Orthodox Church* [*Богослужебный устав Православной Церкви*], Moscow, 1902, p. 59.

352. Archpriest K. Nikolsky, *Manual for the Study of the Typikon*, p. 204.

353. See note 1 on p. 543.

354. MS of the Moscow Synodal Library No. 328/383, fols. 191, 192; likewise in other MSS.

355. Archimandrite (Archbishop) Modest, *On the Church Octoechos*, Vilna, 1865, pp. 122–126.

356. In certain monasteries, the first half of the refrain is proclaimed by the canonarch, and the choir chants only the second half.

=== LEAF p985 ===
357. Before the Dogmatikon, since it is chanted without a canonarch, in the Kyiv-Caves Lavra the canonarch proclaims: “Both now (or: Glory... Both now...), Tone N, Theotokion Dogmatikon: *The universal glory that budded forth from men*...” and the like.

358. St. Symeon of Thessalonica, *On the Divine Prayer*, ch. 332 (296).

359. Citations above.

360. St. Symeon of Thessalonica, *On the Divine Prayer*, ch. 347 (311).

361. St. Symeon of Thessalonica, *On the Divine Prayer*, ch. 333 (297).

362. According unto the Evergetis Typikon, at the litiya before the Liturgy on the feast of the Annunciation, when the procession reached the entrance doors of the temple, there was chanted the troparion unto the Most Holy Theotokos: “Rejoice, O Door of God” (A. Dmitrievsky, *Typika*, p. 431), demonstrating that the Church hath ever regarded the temple doors as an image of the Mother of God, and the solemn entrance through them as an image of the Incarnation.

363. St. Symeon of Thessalonica, *On the Divine Prayer*, ch. 333 (297).

364. Isa. 6:3.

365. The connection of Vespers with the agape; cf. also Introductory Chapter, pp. 85–86.

366. In the Typikon it is stated: “having traced a cross with the censer” [*начертав крест с кадильницею*]; this is too literal a translation of the Greek *μετὰ τοῦ θυμιάματος*: *μετά* signifieth only the instrument of the action (I. Mansvetov, *Church Typikon* [*Церковный устав*], p. 344).

367. In greater detail, with additions unto the Typikon and Sluzhebnik established by general and local practice, the order of the entrance is set forth in the *Order of Matins, Vespers, and the Midnight Office* [*Последование утрени, вечерни и полунощницы*], published by the Kyiv-Caves Lavra in 1861 and 1884. According unto this *Order*, the deacon before the entrance censes round about the Holy Table, and the priest kisses the Holy Table; upon going forth through the North Door they proceed behind the ambo; when they halt, the deacon censes the icons and the priest, takes the censer in his left hand and the orarion in his right, and asks for the blessing of the entrance; unto the priest's blessing of the entrance the deacon responds “Amen,” censes the priest again and the choirs, and, taking his stand in the Royal Doors, awaits the completion of the Theotokion; upon entering the altar, the deacon censes the Holy Table and the High Place, while the priest kisses the Holy Table and stands at the High Place to the right of the Holy Table facing west; the deacon goes forth again through the Royal Doors, censes the people, and upon returning into the altar censes the front of the Holy Table and the priest, after which he stands at the High Place to the left of the Holy Table; here he stands with the priest unto the conclusion of the prokeimenon, making the exclamations unto it.

368. Archpriest K. Kekelidze, *Liturgical Monuments of Georgia*, p. 316; MSS of the Moscow Rumiantsev Museum, Sevastianov Collection No. 491/35, fol. 3; Moscow Synodal Library No. 381 (Greek), fol. 1v; No. 329/384 (Slavonic), fol. 14; Museum of the Kyiv Theological Academy, Aa 194, p. 22; Old Believer Typikon, fol. 6 (11).

369. J. Goar, *Euchologion*, p. 3.

370. *Hieratikon* [Ἱερατικόν], Constantinople, 1895, p. 8.

=== LEAF p986 ===
371. J. Goar, *Euchologion*, p. 240.

372. D. F. Belyaev, *Byzantina*, II, pp. 149 ff.

373. D. F. Belyaev, *Byzantina*, II, p. 35.

374. Pseudo-Codinus, *De officiis*, VI, 45; Balsamon, in *Syntagma* [Σύνταγμα τῶν θείων καὶ ἱερῶν κανόνων], ed. G. A. Rhalles and M. Potles, Athens, 1852–1859, IV, p. 544.

375. T. Tobler, *Itinera et descriptiones Terrae Sanctae*, I, 2, p. 301; cf. A. Dmitrievsky, *Divine Services of Passion and Paschal Weeks in the Holy City of Jerusalem in the 9th–10th Centuries* [*Богослужение страстной и пасхальной седмиц во св. Иерусалиме IX–X в.*], Kyiv, 1894, p. 98.

376. Hieromonk Ambrose [Ornatsky], *History of the Russian Hierarchy* [*История российской иерархии*], Moscow, 1807, pp. 316, 830; A. Golubtsov, “Cathedral Typika (Chinowniki)” [*Соборные чиновники*], *Chteniya v Imperatorskom obshchestve istorii i drevnostei rossiiskikh*, Moscow, 1907, IV (223), pp. 251–258.

377. MS of the Dresden Royal Library No. 140, fols. 132v, 21v; Archpriest M. Lisitsyn, *The Original Slavonic-Russian Typikon* [*Первоначальный славяно-русский Типикон*], St. Petersburg, 1911, p. 233.

378. MS of the Moscow Synodal Library No. 330/380, fols. 1, 3v.

379. A. Dmitrievsky, *Euchologia*, p. 486.

380. *Stoglav*, St. Petersburg, D. E. Kozhanchikov ed., 1863, p. 142; A. Golubtsov, *Cathedral Typika (Chinowniki)*, pp. 127–144.

381. In the Roman Catholic Church even now there is something analogous unto our entrances, while in certain ancient rites of the Latin Liturgy there was an entrance entirely according unto our order. Thus, in the Gallican Liturgy at the very beginning after the “introit,” at the Canticle of Zechariah, “the priest, representing Christ coming into the world, appeareth before the congregation, preceded by the deacon bearing the Gospel and ministers carrying lights, in token of the Gospel light brought into the world by Jesus Christ.” In like manner in this liturgy there are carried from the side altar unto the high altar by the deacon the paten [*patena*, diskos] with the bread, and by the priest the chalice with the wine before the consecration of the Gifts (*Collection of Ancient Liturgies*, IV, 102). In the current Roman rite of the Mass, unto our Little Entrance there correspondeth at its beginning the so-called *introitus* (“entrance”), consisting of an antiphon and psalm proper unto each feast, during which the priest, after incensing the altar, approacheth from its right side unto the center with hands folded upon his breast, having previously made a bow of the head unto the cross. Unto the Great Entrance in the Roman Catholic Mass there correspondeth the carrying before the Mass of the chalice and other Eucharistic vessels from the sacristy unto the altar, preceded by an acolyte with the Missal at the ringing of a bell.

382. “God” appertaineth unto the whole Holy Trinity. In the Typikon of MS Moscow Synodal Library No. 329/384, fol. 29: “O God” [*Боже*].

383. According unto the expression in Pliny's epistle; see Introductory Chapter, p. 49.

384. In the same MS: “giving life unto all the world, for Whose sake all the

=== LEAF p987 ===
world glorifieth Thee.”

385. Apparently, the germ of the hymn *“O Joyous Light”* [*Свете тихий / Phos Hilaron*] is given in a certain prayer of the *Egyptian Church Order* (see Introductory Chapter, p. 72) in its Ethiopic recension; therein is found the following section:
“Rule concerning the bringing in of the lamp at Vespers in the assembly. When evening is come, the deacon bringeth in the lamp (cf. the entrance). The bishop greeteth the assembly: *The Lord be with you all.* The people answer: *And with thy spirit* (cf. now *“Peace be unto all”* after the entrance). The bishop: *Let us give thanks unto the Lord.* The people: *It is meet* (cf.: *“Thou art worthy”*) *and right, majesty and praise be unto Him* (cf. Introductory Chapter, p. 125). But he ought not to say: *Lift up your hearts*; for this is said only at the Oblation. The bishop: *We thank Thee, O God, through Thy Son, our Lord Jesus Christ, that Thou hast enlightened us by the revelation of the immaterial Light. Having finished the length of the day and reached the beginning of the night, having been satisfied with the light of day which Thou didst create for our contentment, we now lack not evening light by Thy mercy. We sanctify and glorify Thee through Thine only-begotten Son, our Lord Jesus Christ, through Whom and with Whom unto Thee be glory and might and honor now...*” (I. Karabinov, *The Eucharistic Prayer*, p. 15).

386. St. Basil the Great, *To Amphilochius on the Holy Spirit*, 29, 73.

387. Archbishop Philaret [Gumilevsky], *Historical Survey of the Hymnographers and Hymnody of the Greek Church*, Chernihiv, 1864, p. 73; Archbishop Sergius (Spassky), *Complete Menologion of the East* [*Полный месяцеслов Востока*], in 2 vols., Vladimir, 1901–1902, vol. II, p. 273.

388. MS of the Moscow Synodal Library No. 330/380, fols. 251–253.

389. Archpriest K. Kekelidze, *Liturgical Monuments of Georgia*, p. 316; MS of the Moscow Rumiantsev Museum, Sevastianov Collection No. 491/35, fol. 3; Moscow Synodal Library No. 381, fol. 2; *Typikon* [Τυπικόν], Venice, 1643, fol. 2v.

390. No. 518, fol. 2v; No. 524, fol. 62v; N. Odintsov, *Public and Private Divine Worship in Ancient Russia prior to the 16th Century* [*Общественное и частное богослужение в древней России до XVI в.*], p. 91.

391. MS of the Moscow Synodal Library No. 328/383 of the 14th century, fol. 3.

392. *Ibid.*, No. 329/384, fol. 14.

393. *Ibid.*, No. 678/386 of the 15th century, fol. 5v; Museum of the Kyiv Theological Academy, Aa 194 of the 16th century, p. 22.

394. Old Believer Typikon, fol. 6 (11).

395. *Stoglav*, ch. 5, quest. 33; ch. 6.

396. Council of Laodicea, Canon 17.

397. *Collection of Ancient Liturgies*, II, p. 19.

=== LEAF p988 ===
398. St. John Chrysostom, *Homilies on Psalm 41 [MT 42]*.

399. C. A. Swainson, *The Greek Liturgies*, p. 226.

400. J.-P. Migne, *Patrologia Latina*, 85, col. 165, and elsewhere.

401. Deut. 23:6; 4 Kings 9:22, 31 [2 Kings 9:22, 31].

402. Matt. 10:12; John 20:19, 21.

403. Judg. 6:12; Ruth 2:4; 2 Chron. 15:2; Luke 1:28; cf. Matt. 28:20; 1 Cor. 16:23; 2 Cor. 13:13 [sic, 3:11 / 13:13], and elsewhere.

404. J. B. Lüft, *Liturgik*, II, p. 77.

405. Tertullian, *De praescriptione haereticorum*, ch. 41.

406. First Council of Braga [Concilium Bracarense I], Canon 21.

407. C. A. Swainson, *The Greek Liturgies*, p. 193; P. Syrku, *On the History of the Revision of Books in Bulgaria* [*К истории исправления книг в Болгарии*], II, p. 223.

408. C. A. Swainson, *The Greek Liturgies*, p. 226, and elsewhere.

409. J.-P. Migne, *Patrologia Latina*, 85, col. 165, and elsewhere.

410. Archpriest Orlov, *The Liturgy of St. Basil the Great*, p. 78.

411. C. A. Swainson, *The Greek Liturgies*, pp. 16, 226, 244.

412. St. Symeon of Thessalonica, *On the Divine Prayer*, ch. 339 (300).

413. Archpriest Orlov, *The Liturgy of St. Basil the Great*, p. 78; J. Goar, *Euchologion*, p. 154.

414. Somewhat differently in I. Mansvetov, *Church Typikon*, p. 154, and A. Dmitrievsky, *Divine Services of Passion and Paschal Weeks in the Holy City of Jerusalem in the 9th–10th Centuries*, p. 319.

415. For citations see above, p. 560, nn. 4–6; p. 561, nn. 1–2; Old Believer Typikon, fol. 6v (11v).

416. MS of the Moscow Synodal Library No. 330/380, fols. 115v, 129, 34v.

417. MS of the Moscow Synodal Typography Library No. 285/1206/142, fol. 13.

418. For citations see above, p. 135, nn. 1–5.

419. MS of the Moscow Synodal Library No. 678/386 of the 15th century, fol. 5v; Museum of the Kyiv Theological Academy, Aa 94 of the 16th century, p. 22.

420. *Collection of Ancient Liturgies*, II, p. 21.

421. “Glory to God in the highest” was chanted at certain ancient liturgies, and is chanted at present in the Roman Mass; cf. among us before the Liturgy.

422. The designation of this litany as the “augmented” [*сугубая*, *ektene*] is not in use in liturgical books and is not entirely accurate, yet for clarity and brevity it is convenient.

423. In ancient monuments it was termed simply the litany [*ektenes* / ἐκтеνής], whereas the Great Litany was called *synapte* [συναпτή], and the Litany of Supplication *aiteseis* [αἰτήσεις, petitions]. So, for example, in the Evergetis Typikon (A. Dmitrievsky, *Typika*, p. 607). The name *ektenes* is correctly translated into Slavonic as “diligent supplication” [*прилежное моление*]; in the Liturgy of St. Mark the Evangelist before the words of institution concerning the Body the deacon proclaims: *ekteinate* [ἐκτείνατε, “pray fervently”], before the words concerning the Blood: *eti*

=== LEAF p989 ===
*ekteinate* [ἔτι ἐκτείνατε, “pray yet more fervently”] (C. A. Swainson, *The Greek Liturgies*, p. 52).

424. St. Symeon of Thessalonica, *On the Divine Prayer*, ch. 338 (302).

425. In the Slavonic text, the words of the Greek appear to have been transposed.

426. *Kopiaō* [κοпιάω]—to labor unto exhaustion (Matt. 6:28). Thus were the gravediggers [copiatae / κοпιαταί] called, of whom Constantine the Great formed a special corporation, exempt from taxes and subject unto ecclesiastical authority, and consequently a certain order of the clergy. Hardly are they meant here and placed prior unto the chanters because they were higher than they (Archbishop Benjamin [Krasnopevkov-Rumovsky], *The New Tablet*, in 4 parts, St. Petersburg, 1858, p. 26); rather, the manual laborers of the monastery are meant here, and they are placed prior unto the chanters on account of the arduousness of their service.

427. C. A. Swainson, *The Greek Liturgies*, p. 229.

428. J. Goar, *Euchologion*, p. 92.

429. A. Dmitrievsky, *Divine Services of Passion and Paschal Weeks*, p. 264; *Euchologia*, p. 133.

430. The petition “for them that bear fruit” [*о плодоносящих*], not encountered in the earlier monuments of the Augmented Litany, arose from a special litany—the “prayer of fruit-bearing” [εὐχὴ καρпоφορίας], appointed in the Liturgy of St. James the Apostle after the *Our Father* and *Holy things unto the holy* (the later copies of the Liturgy of St. James, e.g. Paris 14th century, no longer have this litany), containing a supplication for “them that have brought fruits” [καρпоφορησάντων], wherein those who brought bread and wine for the Eucharist are intended (in antiquity, perhaps also other provisions for the agape). This litany contained 1–3 petitions—for the archbishop, clergy, and people (Messina, Rossano, and Sinai MSS), and together with or in place of this (Paris 14th century) for help unto all the afflicted (“for every soul that is in sorrow,” or the like) and for the repose of the departed; and then, either after or between these petitions (in the Messina and Sinai MSS and the Holy Sepulchre *Order of Passion and Paschal Weeks* of the 9th–12th centuries), also a petition for them that brought fruits in such forms: “For them that have brought oblations this day, that they may receive protection, remission, and participation in eternal life having ineffably ended their course [?], let us pray” (Jerusalem *Order*); “Again for the salvation and remission of sins of our brother who hath brought an offering” (Messina); “For the health, salvation, and remission of the sins of the servants of God, N. and N., who have brought fruits this day” (Sinai) (C. A. Swainson, *The Greek Liturgies*, p. 312; A. Dmitrievsky, *Divine Services of Passion and Paschal Weeks in Jerusalem in the 9th–10th Centuries*, pp. 30, 284).

431. A. Dmitrievsky, *Euchologia*, p. 84.

432. That is, the present petition for the Sovereign. It is cited in full in this place, at the end of the litany, in the Sluzhebnik of Moscow Synodal Library No. 40 of the 14th–15th century, with an addition unto the present text: “let us all say for him,

=== LEAF p990 ===
praying diligently: O Holy Lord, hear and have mercy.”

433. In full the petition in the indicated Sluzhebnik: “[Unto] the Lord God the voice of our prayer and to have mercy also upon us unto health and salvation...”. And then yet another petition: “Again we pray for the [brethren] in Christ” (our brotherhood?).

434. Archpriest Orlov, *The Liturgy of St. Basil the Great*, pp. 88–101; A. Dmitrievsky, *Euchologia*, pp. 226, 608; *Zapiski Istoriko-filologicheskago fakulteta Imperatorskago S.-Peterburgskago universiteta*, vol. XXV, iss. 2; P. Syrku, *Liturgical Works of Patriarch Euthymius of Turnovo* [*Литургические труды патриарха Евфимия Терновского*], St. Petersburg, 1890, pp. 35, 187; *Typikon* MS of the Moscow Synodal Library No. 381, fol. 32v.

435. *Sluzhebnik*, Kyiv, 1629, pp. 20–22, 134–137.

436. E.g. in 2 MSS belonging unto a private individual (Baroness Burdett-Coutts in London) and utilized by Swainson, *The Greek Liturgies*, pp. 100, 155.

437. P. Syrku, *Liturgical Works of Patriarch Euthymius of Turnovo*, pp. 15, 60.

438. J. Goar, *Euchologion*, pp. 56, 137; C. A. Swainson, *The Greek Liturgies*, pp. 118, 155.

439. *Sluzhebnik*, published by the St. Nicholas Edinoverie Monastery, Moscow, 1904, fol. 5 (17v–19v).

440. *Ibid.*, fols. 26 (101 ff.); 39 (154v ff.); 52 (103 ff.).

441. *Euchologion* [Εὐχολόγιον], Athens, 1902, pp. 22–23; *Hieratikon* [Ἱερατικόν], Constantinople, 1895, pp. 63–64.

442. *Collection of Ancient Liturgies*, II, p. 30.

443. C. A. Swainson, *The Greek Liturgies*, pp. 222–225, 230, 231, 252, 253.

444. J. Goar, *Euchologion*, p. 154.

445. Archpriest Orlov, *The Liturgy of St. Basil the Great*, pp. 88–101.

446. Archpriest K. Kekelidze, *Liturgical Monuments of Georgia*, p. 144.

447. N. Odintsov, *The Order of Public and Private Divine Worship in Ancient Russia prior to the 16th Century* [*Порядок общественного и частного богослужения в древней России до XVI в.*], St. Petersburg, 1881, pp. 91, 188; cf. pp. 61, 62.

448. A. Dmitrievsky, *Euchologia*, p. 162.

449. N. Odintsov, *The Order of Public and Private Divine Worship*, p. 188.

450. J. Goar, *Euchologion*, pp. 31, 37.

451. *Sluzhebnik*, Kyiv, 1829, pp. 30–33, 20–23, and elsewhere.

452. *Sluzhebnik*, Moscow, published by the St. Nicholas Edinoverie Monastery, 1904, fols. 26 (101 ff.), 39 (154v ff.), 52 (103 ff.).

453. *Apostolic Constitutions*, VII, 48.

454. A. P. U. [Bishop Porphyrius Uspensky], *Doctrine, Divine Worship... of the Copts*, p. 92; B. Turaev, *Horologion of the Ethiopic Church*, p. 25.

455. “An angel of peace,” but lit. “of peace” [ἄγγελον εἰρήνης]—see below.

456. “Pardon and remission” [συγγνώμην καὶ ἄφεσιν]: the first is excusing, condescension; the second is complete forgiveness; “of sins and transgressions” [ἁμαρτιῶν καὶ πλημмеλημάτων]: the first is grave sins; the second is sins of negligence, omission. See below for the ancient Slavonic translation.

457. “Ending” [*кончины*], *ta tele* [τὰ τέλη]—in the plural number, because such an
"""

draft_path = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort99_raw_draft.md")
draft_path.parent.mkdir(parents=True, exist_ok=True)
draft_path.write_text(draft_text.strip() + "\n", encoding='utf-8')
print(f"Written updated draft: {draft_path}, size: {len(draft_text)} chars")
