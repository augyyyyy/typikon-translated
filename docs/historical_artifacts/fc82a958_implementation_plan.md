# Implementation Plan: Typikon Translation Remediation

This plan outlines the remediation of the translation errors, text omissions, and formatting discrepancies detected during the bilingual semantic and visual audits of the UHKC Typikon English translation.

## User Review Required

> [!IMPORTANT]
> **Approval and Handoff Warning**:
> This plan identifies severe text omissions and mistranslations (including a completely dropped liturgical section on Page 182 and gross mistranslations like rendering "recite" as "refuse" and "Come, let us worship" as "Confirm, O God").
> 
> You must review this remediation checklist and approve the changes. Once approved, I will apply these corrections, run regression tests, and prepare the handoff package for the downstream Hub (`Typikon Coded`).

---

## Proposed Changes & Remediation Checklist

Below is the structured remediation plan grouped by component files.

### 1. Introduction Deliverable

#### [MODIFY] [Final_Dolnytsky_intro.txt](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/Final/Final_Dolnytsky_intro.txt)
- **Restore Page Numbers**: Re-integrate the dropped page numbers (e.g., "42", "44", "46") into the introduction text as parenthetical or editorial indicators to match the Ukrainian layout.
- **Remove Interpolated Heading**: Remove the added heading `"RUBRICS OF THE TRIODION"` after `"PART IV"` as it is an unauthorized addition.
- **Restore Standing Heading**: Restore the standalone heading `"ПРАВИЛО"` ("RULE") instead of merging it into the subsequent line.
- **Integrate Footnote 1**: Restore the missing footnote marker `[^1]` and define it in `Final_footnotes.txt`: `[^1]: Title of the original text: "Typikon of the Ruthenian Catholic Church". "Ruthenian" is the ancient name of Ukrainians.`
- **Remove Interpolated Glosses**: Remove the interpolated terms `[GIFTS]` (from “THE PRESANCTIFIED [GIFTS]”) and `(Ordo Celebrationis)` to maintain 1:1 fidelity with the source text.
- **Standardize Book Title Translation**: Standardize the translation of `"Устав богослужень"` as "Rule of Divine Services" for consistency across the document.

---

### 2. Part I: Structure of Services

#### [MODIFY] [Final_Dolnytsky_part1_structure.txt](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/Final/Final_Dolnytsky_part1_structure.txt)
- **Correct Clergy Capitalization**:
  - Lowercase all pronouns referring to the priest, deacon, or saints (e.g., change `"He exits"`, `"His right hand"`, `"He takes"`, `"He puts"`, `"when He exclaims"`, `"He places"`, `"His right hand"` to lowercase `he` or `his`).
- **Remove Service Book Gloss**: Remove the parenthetical explanation `(lit. "Service Book")` next to `Sluzhebnik` to enforce strict compliance with the standalone terminology rule.
- **Correct Doxology Addition**: In segment 2, remove `"and Undivided"` from the Trinitarian doxology (the source contains only *„животворній”* / "Life-Creating").
- **Restore Paragraph Structure**: Re-merge the split paragraph under “4. Prokimenon and Reading” to match the source's single-paragraph structure.
- **Standardize Glossary Terms**: Replace `"Vigil"` with the canonical **"All-Night Vigil"** globally (e.g., in Compline and Vespers instructions).
- **Correct Major Psalm Incipit Mistranslation**:
  - In section 6, correct the incorrect psalm reference `"psalm 'Blessed be the name of the Lord'"` to the actual psalm incipit **"psalm 'I will bless the Lord'"** (Psalm 33:1).
- **Correct Major Psalm Verse Mistranslation**:
  - Correct the incorrect translation of the psalm verse `"rich men have turned poor"` to the literal translation **"they shall not lack any good thing"** (or "no good thing shall be lacking") to match *„Ніякого блага не забракне”*.
- **Reconcile Footnote Markers**: Remove extraneous footnote markers (`[^15]`, `[^16]`, `[^17]`, `[^18]`, `[^19]`, `[^20]`, `[^21]`) which do not exist in the Ukrainian source segment.
- **Correct Priestly Exclamation**: Remove the interpolated `"He Who Is"` from the blessing formula (change `"Blessed is He Who Is, and is pre-glorified, Christ our God"` to **"Blessed and pre-glorified Christ our God"**).
- **Correct Critical Hours Opening Mistranslation**:
  - In Chunk 12, correct the gross mistranslation where **„Прийдіте, поклонімся”** (Come, let us worship) was rendered as **“Confirm, O God”**.
- **Translate Liturgical Book Names**: Translate **„часо- або молитвослові”** to **"Horologion or Prayer Book"** instead of leaving them as transliterated Slavonic words.
- **Correct Dismissal Commemoration**: Correct the garbled phrase `"whose Dormition and holy martyr (Name)"` to **"whose Dormition we celebrate, and of the holy martyr (Name), whose memory we today honour"**.
- **Fix Chunk 15 Footnote Mismatch**:
  - **CRITICAL**: Chunk 15 was found to contain an entirely unrelated block of footnotes (`[^20]–[^43]`) instead of translating the actual Ukrainian source text regarding "Vespers with the Liturgy". We must translate the Ukrainian text starting with **„ОБХІД З ВЕЧІРНЕЮ Й ЛІТУРГІЄЮ”** ("Vespers with the Liturgy") and replace the footnote block.

---

### 3. Part II: General Rubrics

#### [MODIFY] [Final_Dolnytsky_part2_general_rubrics.txt](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/Final/Final_Dolnytsky_part2_general_rubrics.txt)
- **Remove Bracketed Clarifications**: Purge unauthorized bracketed insertions (`[sung]`, `[commemorated]`, `[on one day]`).
- **Correct Numerical Kathismata translation**: Change `“two of the current tone”` to **“two appointed”** (or "two successive") to match *„дві чергових”*.
- **Correct Feast Terminology**: Change `"Forefeast"` to **"Afterfeast"** where the source uses *посвяттям*.
- **Correct Hymn Identification**:
  - Correct the resurrection stichera name from `"Having Beheld the Resurrection of Christ"` to the actual source hymn **“Jesus is risen”** (matching *„Воскрес Ісус”*).
- **Capitalize Liturgical Books**: Capitalize **"Theotokion"** and **"Typikon"** globally (change lowercase occurrences to uppercase).
- **Correct Patron Translation**: Change `"patron"` to **"temple"** (or "of the church" depending on context) to match the Ukrainian *храму*.
- **Correct Typika Reference**: Change `"the Beatitudes"` to **"Typika"** where the source refers to *зображальний*.
- **Correct Saint's Hymnography**: Change `"Songs of the saint"` to **"Kontakion and Ikos of the saint"** (matching *„Пісні святого, якщо має”*).
- **Correct Idiomela Translation**: Change `"Heirmologic"` to **"Idiomela"** (or "Idiomelic") to match *„самогласних”*.
- **Correct Dismissal Word Order**: Change `"Dismissal great"` to **"the Great Dismissal"**.
- **Correct Saint's Pronouns**: Change capitalized pronouns referring to saints (`"He"`, `"His"`) to lowercase.
- **Remove Extraneous Footnotes**: Remove unsupported footnote markers (`[^89]–[^99]`, `[^100]–[^118]`, `[^153]`, `[^144]`, `[^143]`).
- **Correct Typikon Terminology**: In note 7, change `"rubric"` to **"rule"** (or "Typikon") to match *устав*.
- **Correct Mistranslation of "Recite"**:
  - **CRITICAL**: Correct the gross mistranslation where **„відмовляємо”** (we say/recite) was translated as **“we refuse”** (e.g., in "we refuse alternatingly", change to **"we say alternatingly"**).
- **Correct Tone Number**: In "Saint with Polyeleos", correct the canon tone from Tone **8** to Tone **2** to match the Ukrainian *голос 2-й*.
- **Correct Feast Commemoration Order**: In the Vespers section, correct the order from `"to the saint, afterwards - to the saint"` to **"to the feast, afterwards - to the saint"**.
- **Standardize Liturgical Terms**:
  - Replace `"Megalynaria"` with the canonical **"Magnifications"** globally.
  - Replace `"Lytia"` with the canonical **"Litiya"** globally.

---

### 4. Part III: Menaion

#### [MODIFY] [Final_Dolnytsky_part3_menaion.txt](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/Final/Final_Dolnytsky_part3_menaion.txt)
- **Correct Clergy Capitalization**: Lowercase pronouns referring to the priest or bishop.
- **Align Footnote Markers**: Correct any missing or duplicated footnotes identified in the visual log (e.g. Page 129, 133).

---

### 5. Part IV: Triodion

#### [MODIFY] [Final_Dolnytsky_part4_triodion.txt](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/Final/Final_Dolnytsky_part4_triodion.txt)
- **Correct Troparion Identification (Page 167)**:
  - Change the troparion title from `"Today is salvation"` to **"Save, O Lord"** to match *„Спаси, Господи”*.
- **Remove Bold Formatting (Page 168)**: Remove bolding from headings and subheadings (e.g., "ON WEDNESDAY EVENING") to align with the plain-text style of the source page.
- **Correct Troparion Phrasing (Page 168)**: Change `"Canons two: ... contains 4th, 8th and 9th Odes, which also in these odes takes the first place"` to match the sequential flow, removing `[making]`.
- **Remove Extraneous Footnotes (Page 171)**: Remove markers `[^650]`, `[^649]`, `[^640]` from Item 10, and `[^576]` from Item 12.
- **Remove Extraneous Footnotes (Page 172)**: Remove markers `[^646]`, `[^606]`, `[^579]` from Matins Item 3.
- **Restore Crucial Liturgical Paragraph (Page 177)**:
  - Position the Small Compline rubric properly under its own subsection, ensuring it is not merged with the Vespers rubric.
- **Restore Critical Dropped Sentence (Page 179)**:
  - **CRITICAL**: Restore the completely dropped sentence:
    > *"We suppose, however, that it is proper to cense not only at the Sessional Hymns, but also at all the other Gospels, for the censing takes place not for the sake of the Sessional Hymns, but for the sake of the Gospels; however, only around the holy table, as our Triodia have, which mention the censing only of the holy table. Everything should be censed only twice, that is at the 1st Gospel and at the Canon, at the heirmos of the 9th Ode."*
  - Relocate footnote marker `[^589]` to its correct physical position.
- **Align and Format Headings (Page 180-181)**:
  - Center and bold headers: `"ERECTION OF THE TOMB OF GOD"`, `"ROYAL HOURS"`, `"TYPIKA"`.
  - Format the notes structure: `On Great Friday / AT VESPERS / Notes`. Bold the `RUBRIC` heading.
- **RESTORE COMPLETELY MISSING LITURGICAL SECTION (Page 182)**:
  - **HIGH PRIORITY**: Translate and insert the missing text describing the burial procession, Shroud placement, and troparia (translated text provided in the visual log for Page 182).
- **Restore Bilingual Paragraph (Page 183)**:
  - Translate and insert the missing paragraph explaining the transfer of the Shroud icon.
- **Restore Missing Footnote Marker (Page 184)**:
  - Insert `[^606]` at the sentence: *"at the 9th we do not sing 'More honorable'[^606]"*.
- **Correct Procession Footnote Placement (Page 187)**:
  - Move the footnote marker `[^615]` to follow "immediately closed" inside the sentence, rather than at the end of the paragraph.
- **Restore Dropped Sections in Late Triodion**:
  - **Page 208**: Translate and restore the missing section (Notes on the monstrance and dismissal).
  - **Page 210**: Translate and restore the missing section (Section 2 of Part IV).

---

### 6. Part V: Temple and Calendar Statutes

#### [MODIFY] [Final_Dolnytsky_part5_temple.txt](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/Final/Final_Dolnytsky_part5_temple.txt)
- **Restore Missing Calendar Entries (Page 222)**: Translate and restore the calendar entries for late November and December.
- **Restore Vigil List (Page 230)**: Translate and restore the list of All-Night Vigils.
- **Restore Temple Statutes (Page 232)**: Translate and restore the missing section of temple statutes.
- **Format Tables and Grids (Pages 234-246)**: Re-align tabular columns and leap year markings in the Perpetual Tables to match the visual grid of the printed page.
- **Restore Missing Headings (Page 247)**: Insert the missing Ukrainian headings at the bottom of the page.

---

### 7. Appendix Deliverable

#### [MODIFY] [Final_Dolnytsky_appendix.txt](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/Final/Final_Dolnytsky_appendix.txt)
- **Restore Tetrapod and Diskos Diagrams (Pages 253, 257, 263, 264)**:
  - Ensure spatial layouts, Tetrapod coordinates, and Diskos particle placement text diagrams are properly formatted and placed in their respective chapters.
- **Restore Deacon Arm Crossing (Page 269)**: Restore the dropped sentence: `"...and the deacon, crossing his arms, bows..."`.
- **Restore Concelebrant Bowing (Page 271)**: Insert the dropped paragraph: `"It is proper for concelebrants..."`.
- **Restore Concluding Exclamations (Page 279)**: Restore the complete list of ten concluding exclamations.
- **Fix Paragraph Renumbering (Pages 281-287)**:
  - Renumber Appendix paragraphs from `229–236` to **`224–231`**, and align all subsequent numbers through paragraph `287` to match the Lviv source.

---

### 8. Master Footnotes Corpus

#### [MODIFY] [Final_footnotes.txt](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/Final/Final_footnotes.txt)
- **Correct Footnote 531**: Restore the missing Greek text and translation.
- **Correct Footnote 533**: Restore the missing Greek text and translation.
- **Correct Footnote 537**: Revise to be a direct translation of the Latin Nilles quote instead of an expanded historical explanation.
- **Correct Footnote 542**: Remove unauthorized details about the 842 council and restrict to the 785 council.
- **Correct Footnote 544**: Correct the typo `Каноновєς` to `Κανονες`.
- **Correct Footnote 551**: Correct `"After the 50th Psalm"` to **"After the 8th Psalm"** to match the Ukrainian source *„По 8-му псалмі”*.
- **Correct Footnote 559**: Include the missing text `"And with the exposition of the Holy Mysteries"`.
- **Correct Footnote 605**: Restore the complete Ukrainian translation of the Greek Patriarch citation.
- **Correct Footnote 616**: Restore the missing Greek quote `...συγγραψаμενος λέγει...`.
- **Correct Footnote 741**: Restore the missing text: `"All -- according to the general rubric of the past weeks"`.
- **Correct Footnote 755**: Correct content mismatch.
- **Correct Footnote 760**: Restore missing sub-item about the chalice veil.
- **Correct Footnote 769**: Correct the translation to **"He holds the book..."**.
- **Correct Footnote 777**: Correct text translation to match the scan exactly.

---

## Verification Plan

### Automated Checks
- Run the formatting validation scripts (`full_terminology_audit.py`, `hieratic_pronoun_audit.py`, `structural_audit.py`) against the updated `Final/` directory.
- Verify that 100% of the footnote markers in the modified text files map to a valid definition in `Final_footnotes.txt` with zero gaps.

### Manual Verification
- Review the modified sections of `Final_Dolnytsky_part4_triodion.txt` (specifically the newly inserted Page 182 burial rubrics and Page 179 censing rules) to verify syntactic flow.
- Deploy the corrected files to the downstream Hub's inbox (`Projects/Typikon Coded/Data/Inbox/`) and run the Hub's parser to verify error-free ingestion.
