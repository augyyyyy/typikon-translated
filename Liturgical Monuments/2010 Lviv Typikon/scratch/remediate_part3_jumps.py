import re
from pathlib import Path

txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

print("Starting Part 3 backward jump remediation...")

# 1. Remove premature [^370] from September 12 in TXT and MD
txt = txt.replace("Kathisma is sequential[^370] (and not", "Kathisma is sequential (and not")
md = md.replace("Kathisma: sequential[^370] (and not", "Kathisma: sequential (and not")
md = md.replace("Kathisma is sequential[^370] (and not", "Kathisma is sequential (and not")

# Add [^370] to its true home: February 1 (Cheesefare Saturday, Forefeast of the Meeting, at Vespers)
# In DOCX: "V. FOREFEAST OF THE MEETING ON CHEESEFARE SATURDAY ... AT VESPERS Kathisma is sequential."
txt = txt.replace("AT VESPERS\nKathisma is sequential.\nAt \"Lord, I have cried\"", "AT VESPERS\nKathisma is sequential[^370].\nAt \"Lord, I have cried\"")
md = md.replace("##### At Vespers\n\n1. **Kathisma:** Kathisma is sequential.\n\n2. **On *\"Lord, I have cried\"*:**", "##### At Vespers\n\n1. **Kathisma:** Kathisma is sequential[^370].\n\n2. **On *\"Lord, I have cried\"*:**")
md = md.replace("##### At Vespers\n\nKathisma is sequential.\n\n", "##### At Vespers\n\nKathisma is sequential[^370].\n\n")

# 2. Fix misplaced [^381]
# Remove premature [^381] from January (after "After the Entrance - Entrance")
txt = txt.replace("Entrance[^381] and Great Prokimenon", "Entrance and Great Prokimenon")
md = md.replace("Entrance[^381] and Great Prokimenon", "Entrance and Great Prokimenon")

# Add [^381] to its true home: February 24 (Finding of the Head)
# In DOCX: "Entrance, Prokeimenon of the day from the Horologion, 3 readings to the Forerunner"
txt = txt.replace("Entrance, Prokimenon of the day from the Horologion, 3 readings to the Forerunner", "Entrance[^381], Prokimenon of the day from the Horologion, 3 readings to the Forerunner")
md = md.replace("Entrance, Prokimenon of the day from the Horologion, 3 readings to the Forerunner", "Entrance[^381], Prokimenon of the day from the Horologion, 3 readings to the Forerunner")

# 3. Fix misplaced [^393]
# Remove premature [^393] from February 24 heading
txt = txt.replace("RULES FOR THE ABOVE-MENTIONED CASES[^393]\n1. FINDING OF THE PRECIOUS HEAD", "RULES FOR THE ABOVE-MENTIONED CASES\n1. FINDING OF THE PRECIOUS HEAD")
md = md.replace("RULES FOR THE ABOVE-MENTIONED CASES[^393]\n\n#### 1. Finding of the Precious Head", "RULES FOR THE ABOVE-MENTIONED CASES\n\n#### 1. Finding of the Precious Head")
md = md.replace("RULES FOR THE ABOVE-MENTIONED CASES[^393]", "RULES FOR THE ABOVE-MENTIONED CASES")

# Add [^393] to its true home: March 24 (Forefeast of the Annunciation)
# In DOCX: "RULES FOR THE ABOVE-MENTIONED CASES 1. FOREFEAST OF THE ANNUNCIATION ON ONE OF THE FAST DAYS"
txt = txt.replace("RULES FOR THE ABOVE-MENTIONED CASES\n1. FOREFEAST OF THE ANNUNCIATION", "RULES FOR THE ABOVE-MENTIONED CASES[^393]\n1. FOREFEAST OF THE ANNUNCIATION")
md = md.replace("#### RULES FOR THE ABOVE-MENTIONED CASES\n\n##### 1. Forefeast of the Annunciation", "#### RULES FOR THE ABOVE-MENTIONED CASES[^393]\n\n##### 1. Forefeast of the Annunciation")
md = md.replace("RULES FOR THE ABOVE-MENTIONED CASES\n\n##### 1. Forefeast of the Annunciation", "RULES FOR THE ABOVE-MENTIONED CASES[^393]\n\n##### 1. Forefeast of the Annunciation")

# 4. Remove premature duplicate instances of 409, 412, 417, 418, 426, 438 from TXT and MD
# FN 409: Remove premature at TXT L1694 / MD L3517 (March 25 Akathist Eve Compline)
txt = txt.replace("After \"It is truly meet\" - Kontakion of the Feast[^409]", "After \"It is truly meet\" - Kontakion of the Feast")
md = md.replace("After *“It is truly meet”* – Kontakion of the Feast[^409]", "After *“It is truly meet”* – Kontakion of the Feast")
md = md.replace("After *It is truly meet*  Kontakion of the Feast[^409]", "After *It is truly meet*  Kontakion of the Feast")

# FN 412: Remove premature at TXT L1605 / MD L3330 (March 25 on Wednesday of Great Lent Compline)
txt = txt.replace("here on p. 26-27, that is after \"It is truly meet\" - Kontakion of the Feast[^412]", "here on p. 26-27, that is after \"It is truly meet\" - Kontakion of the Feast")
md = md.replace("here on p. 26-27, that is after *“It is truly meet”* – Kontakion of the Feast[^412]", "here on p. 26-27, that is after *“It is truly meet”* – Kontakion of the Feast")
md = md.replace("here on p. 26-27, that is after *It is truly meet*  Kontakion of the Feast[^412]", "here on p. 26-27, that is after *It is truly meet*  Kontakion of the Feast")

# FN 417: Remove premature at TXT L956 / MD L1914 (Theophany / January)
txt = txt.replace("Glory, and now: Sessional hymn of the Feast[^417];", "Glory, and now: Sessional hymn of the Feast;")
md = md.replace("Glory, and now: Sessional hymn of the Feast[^417];", "Glory, and now: Sessional hymn of the Feast;")

# FN 418: Remove premature at TXT L536 / MD L1073 (Eve of Nativity in December)
txt = txt.replace("reads the prayer \"O All-Holy Trinity\"[^418].", "reads the prayer \"O All-Holy Trinity\".")
md = md.replace("reads the prayer \"O All-Holy Trinity\"[^418].", "reads the prayer \"O All-Holy Trinity\".")

# FN 426: Remove premature at TXT L804 / MD L1597 (Circumcision on January 1)
txt = txt.replace("(\"Velychannya\"), if you have it printed in the Psalter or Menaion[^426]", "(\"Velychannya\"), if you have it printed in the Psalter or Menaion")
md = md.replace("(\"Velychannya\"), if you have it printed in the Psalter or *Menaion*[^426]", "(\"Velychannya\"), if you have it printed in the Psalter or *Menaion*")

# FN 438: Remove premature at TXT L2200 / MD L4614 (Sunday of the Holy Fathers after Ascension)
txt = txt.replace("Both now: of the Ascension[^438].", "Both now: of the Ascension.")
md = md.replace("Both now: of the Ascension[^438].", "Both now: of the Ascension.")

# 5. Fix misplaced FN 313 in MD:
# In MD L1039: it was placed on "marks four", but in DOCX it is on "O come, let us worship" inclusive[^313].
md = md.replace("marks four[^313] parts", "marks four parts")
md = md.replace("\"O come, let us worship\" inclusive.", "\"O come, let us worship\" inclusive[^313].")

# 6. Fix misplaced FN 361 in MD:
# In DOCX: "Glory, Both now: Kontakion of the Triodion[^361]."
md = md.replace("If one of these saints falls outside the *Triodion*[^361],", "If one of these saints falls outside the *Triodion*,")
md = md.replace("Both now: Kontakion of the *Triodion*.\n", "Both now: Kontakion of the *Triodion*[^361].\n")

# 7. Fix misplaced FN 367 in MD:
# In DOCX: "Friday with Saints Cyrus, John and Tryphon[^367],"
md = md.replace("When the Forefeast of the Meeting falls on Meatfare Saturday[^367],", "When the Forefeast of the Meeting falls on Meatfare Saturday,")
md = md.replace("Friday with Saints Cyrus, John and Tryphon,", "Friday with Saints Cyrus, John and Tryphon[^367],")

# 8. Fix FN 453 duplicate in TXT if any
txt = re.sub(r'(\[\^453\])\s*\[\^453\]', r'\1', txt)

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully executed Part 3 jump remediation!")
