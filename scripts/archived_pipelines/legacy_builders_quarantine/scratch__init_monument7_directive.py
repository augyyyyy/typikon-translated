from pathlib import Path

content = '''# Autonomous Monument Translation Directive: Opisanie Liturgicheskikh Rukopisei Vol. 1: Typika (Aleksei Dmitrievsky, Kyiv, 1895)
## Complete Unabridged Translation Execution Specification across All 109 Cohorts

> [!IMPORTANT]
> **Sovereign Autonomous Execution Mandate (Rule 14 of `.agents/AGENTS.md`)**  
> This directive equips the Automator / Worker Agent with the **complete codex partition schedule and autonomous loop controller** for **Opisanie Liturgicheskikh Rukopisei Vol. 1: Typika (Aleksei Dmitrievsky, Kyiv, 1895)** (1,090 physical pages).  
> **Zero Inter-Cohort Human Stalls**: The Automator executes continuously through Cohort 1 to Cohort 109, triggering backend Small Pause Gates (`scripts/run_small_pause_gate.py`) automatically between cohorts.  
> Execution yields to the Human Operator **strictly and exclusively at the Sovereign Grand Pause** when 100% of all 1,090 leaves are translated and assembled (`remaining_pages == 0`).

---

## 1. Codex Transmission Metadata & Conservation Scope
* **Monument ID**: `1895_dmitrievsky_vol1`
* **Title**: Opisanie Liturgicheskikh Rukopisei Vol. 1: Typika (Aleksei Dmitrievsky, Kyiv, 1895)
* **Source Facsimile**: `Historical Typikons/1895-Dmitrievsky-Opisanie-Vol1-Typika-Part1.pdf`
* **Total Physical Pages**: **1,090 leaves**
* **Cohort Bounding**: Strictly **10 physical pages** per cohort
* **Total Scheduled Cohorts**: **109 cohorts** (109 x 10 = 1,090 leaves)
* **Governing Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)
* **Mathematical Conservation**:
  $$\\mathbf{Total\\ Physical\\ Pages\\ in\\ Codex} \\equiv \\sum_{k=1}^{109} C_k = 109 \\times 10 = 1090 \\text{ Leaves (100.0% Closed Conservation)}$$

---

## 2. Inviolable Liturgical Translation Standards (MTS-1 / TA-1)

### A. Universal Native Vision Mandate (Physical Ink Sovereignty)
* Inspect each 300 DPI image (`Page_0001.jpg`..`Page_1090.jpg` / `p{N}.jpg`) in `Liturgical Monuments/Monument 7 - 1895 Dmitrievsky Vol 1/Source Text/images/` directly via the NTFS junction to the Drive E: master vault.

### B. Scholarly Critical & Rubrical Register Norms (SCHOLARLY_CRITICAL)
* Precise, academic English for Dmitrievsky's scholarly descriptions, textual apparatus, and codicological commentaries.
* Active Present Indicative for ceremonial rubrics (*"The priest enters the sanctuary..."*).
* Zero rubrical "shall"-bombing.

### C. Incipits & Dual Transcriptions
* Bold English incipits followed by italicized Greek/Slavonic originals in parentheses.
* Byzantine and Slavonic liturgical realia maintained (*Tetrapod, Klepalo, Aer, Kolyvo, Sluzhebnik*).

### D. Father Paul Doxology Standard & Hieratic Pronouns
* Doxology: *"now and forever, and unto the ages of ages. Amen."* (Strict ban on *"for ever and ever"*).
* 100% capitalization on Holy Trinity Divine Persons (*He, Him, His, Thou, Thee, Thy, Thine*).

### E. Scripture & Psalter (Septuagint LXX)
* Mandatory LXX Septuagint versification with bracketed Masoretic parallels where needed.

### F. Footnote Bijectivity
* Continuous monotonic numbering across the monument: Every `[^N]` in body text must have an exact corresponding definition `[^N]:` in the footnotes file.

---

## 3. Autonomous Multi-Cohort Loop Controller Specification

For each cohort $k \\in [1, 109]$:
1. INGESTION: Verify 300 DPI leaves p{start}..p{end} in `Source Text/images/`.
2. TRANSCRIPTION: Transcribe source ink into `Source Text/1895_dmitrievsky_vol1_cohort{k}_source.txt`.
3. TRANSLATION: Draft unabridged English into `Draft/1895_dmitrievsky_vol1_cohort{k}_raw_draft.md`.
4. FOOTNOTES: Write definitions into `Draft/1895_dmitrievsky_vol1_cohort{k}_footnotes.txt`.
5. SMALL PAUSE GATE: Run `py scripts/run_small_pause_gate.py --monument 1895_dmitrievsky_vol1 --cohort {k}`.
6. INTEGRATION: Run `py scripts/assemble_and_sync_hub.py --monument 1895_dmitrievsky_vol1 --cohort {k}`.
7. ADVANCE: Advance immediately to cohort $k+1$ without pausing.

---

## 4. Complete Codex Partition Schedule (109 Cohorts)

| Cohort | Physical Pages | Leaf Count | Status | Target Deliverables |
|---|---|---|---|---|
'''

rows = []
for k in range(1, 110):
    sp = (k - 1) * 10 + 1
    ep = k * 10
    rows.append(f'| **Cohort {k:02d}** | pp. {sp}–{ep} | 10 leaves | `PENDING` | `cohort{k:02d}_source.txt` / `raw_draft.md` |')

table = '\n'.join(rows)

footer = '''

---

## 5. Sovereign Grand Pause Termination
When Cohort 109 completes its Small Pause Gate and final integration:
- `remaining_pages == 0`
- The entire 1,090-page codex is assembled in `Liturgical Monuments/Monument 7 - 1895 Dmitrievsky Vol 1/Final MD/1895_dmitrievsky_vol1_complete.md`
- Deliverables are synchronized to `Projects/Typikon Coded/Data/Inbox/1895_Dmitrievsky_Opisanie_Vol1/`
- Automator halts and delivers the final Grand Pause notification to the Human Operator.
'''

p = Path(r'Liturgical Monuments/Monument 7 - 1895 Dmitrievsky Vol 1/AUTONOMOUS_MONUMENT_DIRECTIVE.md')
p.write_text(content + table + footer, encoding='utf-8')
print('Wrote AUTONOMOUS_MONUMENT_DIRECTIVE.md successfully, length:', len(p.read_text(encoding='utf-8')))
