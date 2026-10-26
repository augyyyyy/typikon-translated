import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

footnotes_content = """[^773]: A. Hauck, *Realencyklopädie für protestantische Theologie und Kirche*, vol. V, p. 631 (E. von Dobschütz, *Euthalius*).
[^774]: St. John Chrysostom, *Homilies on the Gospel of John*, Homily 47.
[^775]: St. John Chrysostom, *Homilies on the Epistle to the Hebrews*, Homily 8: "Each week these scriptures are read unto you three times. The reader ascendeth and stateth first from whom the reading is, for instance from such and such a prophet, apostle, or evangelist, and then readeth that which followeth."
[^776]: St. John Cassian, *De Institutis Coenobiorum* (*On the Institutes of the Coenobia*), II, 6. See above, *(Orig. p. 164)*.
[^777]: Concerning the reading of the Apocalypse there is a definite indication only regarding the Gallican and Spanish Churches: Fourth Council of Toledo (633), canon 16.
[^778]: See above, *(Orig. p. 13)*.
[^779]: St. John Chrysostom, *Homilies on the Statues*, Homily 7, § 1.
[^780]: Migne, *PG*, t. 53, hom. 1, c. 1; t. 65, hom. 1, 1.
[^781]: St. Basil the Great, *Homilies on the Hexaemeron*, Homily 2, § 1.
[^782]: *Apostolic Constitutions*, V, 13 (December is called the 9th month, and January the 10th). A. Hauck, *Realencyklopädie für protestantische Theologie und Kirche*, vol. XV, p. 134.
[^783]: St. Ambrose, *Epistle 20 to Marcellina*, § 19.
[^784]: A. Hauck, *Realencyklopädie für protestantische Theologie und Kirche*, vol. XV, p. 135.
[^785]: St. Ambrose, *Epistle 20 to Marcellina*, § 25.
[^786]: *Peregrinatio Silviae* (*Itinerarium Egeriae*), §§ 33–36.
[^787]: See above, *(Orig. pp. 164–165)*.
[^788]: Blessed Augustine, *Sermo de tempore*; A. Hauck, *Realencyklopädie für protestantische Theologie und Kirche*, vol. XV, p. 135.
[^789]: St. John Chrysostom, *Homilies on the Acts of the Apostles*, Homily 4.
[^790]: Blessed Augustine, *Tractates on the Gospel of John* (*In Ioannis Evangelium tractatus*), Tractate 6, § 18.
[^791]: Blessed Augustine, *Sermon 315*, § 1.
[^792]: *Peregrinatio Silviae* (*Itinerarium Egeriae*), §§ 26, 31, 39, 43.
[^793]: Blessed Augustine, *Sermon 331*, § 1.
[^794]: Blessed Augustine, *Sermon 232*, § 1.
[^795]: Gennadius of Marseilles (*Massiliensis*), *De scriptoribus ecclesiasticis*, c. 79; Migne, *PL*, t. 58.
[^796]: A. Hauck, *Realencyklopädie für protestantische Theologie und Kirche*, vol. XV, p. 36.
[^797]: Sidonius Apollinaris, *Epistulae*, IV, 11; Migne, *PL*, t. 58. From the fact that the Gospel pericopes for Sundays in the Roman Church have as their main content the miracles of Christ, scholars conclude that these pericopes were selected during the period of the Arian controversies, that is, in the 4th century. A. Luft, *Liturgik*, vol. II, p. 316.
[^798]: See above, *(Orig. p. 62)*.
[^799]: See above, *(Orig. pp. 86 and 106)*.
[^800]: *Apostolic Constitutions*, II, 57.
[^801]: *Peregrinatio Silviae* (*Itinerarium Egeriae*), §§ 24, 27, 33, 34; unto a presbyter—§ 29; in the majority of instances it is not indicated by whom it is read—§§ 31, 35, etc. Judging by the expression "the bishop himself readeth" (§ 24), this occurred not especially frequently.
[^802]: Blessed Jerome, *Epistle to Sabinian* (*Epistula ad Sabinianum lapsum*).
[^803]: Socrates, *Historia Ecclesiastica*, VII, 5.
[^804]: Sozomen, *Historia Ecclesiastica*, VII, 19. Connected with such an ever-elevating regard toward the Gospel was the custom, which arose in certain Western Churches, of not admitting the catechumens unto the hearing of the Gospel, dismissing them prior unto its reading—a custom forbidden by the First Council of Orange (*Arausicanum*) in Gaul in 441 (canon 18) and the Council of Valencia (*Valentinum*) in Spain in the mid-6th century (canon 1).
[^805]: First Council of Toledo (400), canon 2.
[^806]: St. John Chrysostom, *Homilies on Colossians*, Homily 3.
[^807]: Blessed Augustine, *De Civitate Dei* (*The City of God*), XXII, 8.
[^808]: St. John Chrysostom, *Homilies on Matthew*, Homily 33.
[^809]: Blessed Augustine, *Epistle 165*.
[^810]: Third Council of Carthage (419), canon 1.
[^811]: An indication of this is found also in the following words of St. Cyprian concerning a newly ordained lector: "he proclaimed peace while announcing the reading" (*auspicatus est pacem, dum dedicat lectionem*), *Epistle to the Clergy of Carthage* 33 (38).
[^812]: St. John Chrysostom, *Homilies on the Acts of the Apostles*, Homily 19.
[^813]: Cf. among us before the prokeimenon of Great Vespers: "Let us attend. Peace be unto all. Wisdom. Let us attend."
[^814]: St. Ambrose, *Exposition on the Psalms*, Preface.
[^815]: Blessed Augustine, *De Civitate Dei* (*The City of God*), XXII, 8.
[^816]: Concerning the acclamation "Glory to Thee, O Lord" before the reading of the Gospel from the 4th and 5th centuries there are no reliable testimonies. In a homily on the circus or hippodrome, formerly attributed unto St. John Chrysostom, it is stated: "When the deacon beginneth the course (*dromou*) of the readings, we immediately arise, proclaiming: 'Glory to Thee, O Lord'." In the Mozarabic Liturgy (the order of which has been preserved more or less unchanged from the 6th–7th centuries), unto the naming of the prophecy and the epistle the people respond: "Thanks be to God" (*Deo gratias*). Thus originally and in certain localities the acclamation "Glory to Thee, O Lord" or the like accompanied the reading of other scriptures as well, besides the Gospel. In the Mozarabic Liturgy and in the Rule of St. Benedict of the 6th century (ch. 11), after the reading of the Gospel the people pronounce "Amen," which, according unto the explanation of other commentators, possesses here the sense: "May God grant us firmly to abide in the evangelical teaching." Bingham, *Origines Ecclesiasticae*, book XIV, ch. 3, § 3 (vol. IV, p. 82).
[^817]: A. Luft, *Liturgik*, vol. II, p. 322.
[^818]: Of all 3rd-century writers, St. Cyprian points unto this in passing: "know ye that they (the confessors) have been appointed lectors, since it was fitting to place the lamp upon the candlestick, whence it might shine unto all, and to set honorable persons in an exalted place (the ambo), where, being visible unto all the surrounding (*circumstante*) people, they might provide unto those beholding them an incitement unto glory" (*Epistle 34*, according unto others *39*).
[^819]: *Apostolic Constitutions*, II, 57.
[^820]: St. John Cassian, *De Institutis Coenobiorum* (*On the Institutes of the Coenobia*), II, 12.
[^821]: Sozomen, *Historia Ecclesiastica*, VII, 19.
[^822]: Philostorgius, *Historia Ecclesiastica*, III, 5; Migne, *PG*, t. 65.
[^823]: *Liber Pontificalis*, *Life of Anastasius I*; Bingham, *Origines Ecclesiasticae*, book XIV, ch. 3, § 3 (vol. IV, p. 81). In a letter attributed unto St. Isidore of Pelusium († c. 436 / 440) concerning the reading of the Gospel it is stated: "when through the opening of the Book of the Gospels the true Shepherd Himself appeareth, then the bishop also ariseth and putteth off from himself the habit of imitation (*to schema tes mimeseos*—meaning the omophorion), signifying thereby that the Lord Himself, the Leader of the pastorship, God and Master, is present" (book I, ep. 136; Bingham, *Origines Ecclesiasticae*, book XIV, ch. 3, § 3; vol. IV, p. 80).
[^824]: Blessed Jerome, *Contra Vigilantium* (*Against Vigilantius*), ch. 4.
[^825]: See above, *(Orig. pp. 86 ff.)*.
[^826]: Council of Carthage (397), canon 24 (33) = Council of Hippo (393), canon 36.
[^827]: Blessed Augustine, *De doctrina christiana*, II, 8.
[^828]: Pope Innocent I, *Epistle 3 to Exsuperius*, ch. 3; Bingham, *Origines Ecclesiasticae*, book XIV, ch. 3, § 14 (vol. IV, p. 94).
[^829]: Blessed Jerome, *Preface to the Books of Solomon* (*Prologus in libros Salomonis*).
[^830]: St. Athanasius the Great, *39th Festal Letter* (367).
[^831]: Rufinus of Aquileia, *Commentarius in symbolum apostolorum*, § 38.
[^832]: Eusebius of Caesarea, *Historia Ecclesiastica*, III, 16; cf. IV, 23.
[^833]: St. Cyril of Jerusalem, *Catechetical Lectures*, Lecture IV, § 22.
[^834]: Sozomen, *Historia Ecclesiastica*, VII, 19.
[^835]: Council of Carthage (397), canon 24 (33) (= Council of Hippo [393], canon 36).
[^836]: Blessed Jerome, *De viris illustribus* (*On Illustrious Men*), ch. 115.
[^837]: Second Council of Vaison (*Vasense*), canon 2 (529).
[^838]: Cyprianus of Toulon (or Cassinensis, 6th c.), *Vita Caesarii Arelatensis*; Migne, *PL*, t. 67.
[^839]: See above, *(Orig. p. 68)*.
[^840]: Eusebius of Caesarea, *Historia Ecclesiastica*, IV, 15.
[^841]: Blessed Augustine, *Sermon 12 on the Saints*, and Sermons 45, 63, 93, 101, 102, 103, 109, according unto Bingham, *Origines Ecclesiasticae*, book XIV, ch. 3, § 14 (vol. IV, p. 88). In a homily belonging probably unto the same epoch, attributed unto Blessed Augustine or Caesarius of Arles, it is stated: "when extensive passions (*passiones*) or any very long readings are read, let him who cannot stand throughout listen unto that which is read, sitting modestly and quietly, with attentive ears" (Bingham, *Origines Ecclesiasticae*, book XIV, ch. 3, § 14; vol. IV, p. 86).
[^842]: Council of Carthage, canon 24 (33) (= Council of Hippo [393], canon 36).
[^843]: Pope Gelasius I, *Decretum Gelasianum*; Migne, *PL*, t. 59.
[^844]: Blessed Augustine, *De gestis cum Emerito*; Bingham, *Origines Ecclesiasticae*, book XIV, ch. 3, § 14 (vol. IV, p. 90).
[^845]: *Apostolic Constitutions*, II, 57; VIII, 5.
[^846]: See above, *(Orig. pp. 88–89 and 161–163)*.
[^847]: St. John Chrysostom, *Homilies on 2 Thessalonians*, Homily 3.
[^848]: St. John Chrysostom, *Homilies on the Incomprehensible Nature of God*, Homily 3.
[^849]: Council of Carthage (399), canon 24.
[^850]: St. Caesarius of Arles, *Homily 12*; Migne, *PL*, t. 67; Cyprianus, *Vita Caesarii*.
[^851]: Sozomen, *Historia Ecclesiastica*, VII, 17.
[^852]: St. Basil the Great, *Homilies on the Hexaemeron*, Homily 2; cf. Homilies 7 and 9.
[^853]: Socrates, *Historia Ecclesiastica*, V, 22.
[^854]: St. John Chrysostom, *Homilies on Genesis*, Homily 4.
[^855]: Blessed Augustine, *Enarrationes in Psalmos*, Psalm 88, Sermon 2 (LXX; Masoretic Ps. 89).
[^856]: *Apostolic Constitutions*, II, 57; see below, "Persons Who Preached."
[^857]: See above, *(Orig. pp. 54, 63, and 86)*.
[^858]: St. Ambrose, *De officiis ministrorum*, book I.
[^859]: St. John Chrysostom, *Homilies on 1 Timothy*, Homily 57 (or Homily on Timothy).
[^860]: *Apostolic Constitutions*, II, 57.
[^861]: *Peregrinatio Silviae* (*Itinerarium Egeriae*), § 25.
[^862]: St. John Chrysostom, *Homilies on the Words of Isaiah* (*In illud: Vidi Dominum*), Homilies 2 and 3; Palladius, Bishop of Helenopolis (5th c.), *Dialogue on the Life of St. John Chrysostom*, § 5.
[^863]: Possidius (5th c.), *Vita Sancti Augustini*; Blessed Augustine, *Enarrationes in Psalmos*, Psalms 94 and 95 (LXX; Masoretic Pss. 95 and 96).
[^864]: Blessed Jerome, *Epistle 2 to Nepotian* (*Epistula 52 ad Nepotianum*); cf. *Epistle 61 to Pammachius* (*Epistula 57 ad Pammachium*).
[^865]: St. Cyprian of Carthage, *Epistle 2 to the Martyrs and Confessors* (*Epistula 12* / *18*).
[^866]: St. Gregory the Great, *Praefatio ad XL homilias in Evangelia*; John the Deacon, *Vita Sancti Gregorii Magni*, II, 18.
[^867]: See above, *(Orig. p. 173)*."""

target = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort17_footnotes.txt")
target.write_text(footnotes_content.strip() + "\n", encoding="utf-8")
print(f"Wrote {len(footnotes_content)} chars to {target}")
