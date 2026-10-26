# Autonomous Monument Translation Directive: {title}
## Complete Unabridged Translation Execution Specification across All {num_cohorts} Cohorts

> [!IMPORTANT]
> **Sovereign Autonomous Execution Mandate (Rule 14 of `.agents/AGENTS.md`)**  
> This directive equips the Automator / Worker Agent with the **complete codex partition schedule and autonomous loop controller** for **{title}** ({total_pages} physical pages).  
> **Zero Inter-Cohort Human Stalls**: The Automator executes continuously through Cohort 1 to Cohort {num_cohorts}, triggering backend Small Pause Gates (`scripts/run_small_pause_gate.py`) automatically between cohorts.  
> Execution yields to the Human Operator **strictly and exclusively at the Sovereign Grand Pause** when 100% of all {total_pages} leaves are translated and assembled (`remaining_pages == 0`).

---

## 1. Codex Transmission Metadata & Conservation Scope
* **Monument ID**: `{monument_id}`
* **Title**: {title}
* **Source Facsimile**: `{rel_pdf}`
* **Total Physical Pages**: **{total_pages} leaves**
* **Cohort Bounding**: Strictly **{cohort_size} physical pages** per cohort ($15 \le C \le 25$, final cohort = {last_leaf_count} leaves)
* **Total Scheduled Cohorts**: **{num_cohorts} cohorts**
* **Governing Register**: **{genre_register_upper}** (Per Master Translation Standard MTS-1)
* **Mathematical Conservation**:
  $$\mathbf{{Total\ Physical\ Pages\ in\ Codex}} \equiv \sum_{{k=1}}^{{{num_cohorts}}} C_k = ({num_cohorts_minus_1} \times {cohort_size}) + {last_leaf_count} = {total_pages} \text{{ Leaves (100.0% Closed Conservation)}}$$

---

## 2. Inviolable Liturgical Translation Standards (MTS-1 / TA-1)

### A. Universal Native Vision Mandate (Physical Ink Sovereignty)
* Inspect each 300 DPI image (`Page_{{N:04d}}.jpg`) in `{rel_ws}/Source Text/images/` directly.
* Cinnabar Rubrics: Red ink is visually identified and rendered in ceremonial italics (`*...*`); black ink is rendered in spoken/chanted prayers, psalmody, and hymnography.

### B. Ceremonial / Rubrical Register Norms ({genre_register_upper})
* Concise, imperative, and active: Use **Active Present Indicative** for all rubrical actions (*"The Priest enters the sanctuary, venerates the Holy Table, and begins..."*).
* Absolute prohibition of gratuitous legalistic *"shall"*s in ordinary liturgical rubrics.

### C. Byzantine-Ruthenian Realia & Melodic Headings
* Technical Loanwords mandatory: `Tetrapod` (never "center table"), `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
* Ruthenian Chant Headings: Tone designations must be **`Tone 1`** through **`Tone 8`** (never Greek "Mode I").
* Model Melodies: **`Podoben: "[Canonical Incipit]"`**, **`Samohlasen`** (proper melody), **`Samopodoben`**.
* Dual Incipits: Bold English followed by italicized Slavonic (*"Lord, I have cried"* (*Господи воззвахъ*)).

### D. Father Paul Doxology Standard & Hieratic Pronouns
* Full choral: *"Glory be to the Father, and to the Son, and to the Holy Spirit, now and forever, and unto the ages of ages. Amen."*
* Shorthand rubric: *"Glory... Now and forever, and unto the ages of ages:"*
* **Strict Ban**: The phrase *"for ever and ever"* is 100% prohibited.
* **100% Deity Pronoun Capitalization**: Mandatory capitalization for Divine Persons (*He, Him, His, Thou, Thee, Thy, Thine*). Clergy, celebrants, saints, and rubrical "he" remain lowercase.

### E. Scripture & Psalter (Septuagint LXX)
* Mandatory Septuagint versification across all psalm citations and biblical references.

### F. Footnote Bijectivity
* Continuous monotonic numbering across the monument: Every `[^N]` in body text must have a matching `[^N]:` definition.

---

## 3. Autonomous Multi-Cohort Loop Controller Specification

For each cohort $k \in [1, {num_cohorts}]$:

```
[COHORT LOOP: k = 1 to {num_cohorts}]
  1. INGESTION : Verify/render 300 DPI leaves p{{start}}..p{{end}} in '{rel_ws}/Source Text/images/'
  2. TRANSCRIPTION : Transcribe source ink into '{rel_ws}/Source Text/{monument_id}_cohort{{k}}_source.txt'
  3. TRANSLATION : Draft unabridged English into '{rel_ws}/Draft/{monument_id}_cohort{{k}}_raw_draft.md'
  4. FOOTNOTES : Write definitions into '{rel_ws}/Draft/{monument_id}_cohort{{k}}_footnotes.txt'
  5. SMALL PAUSE GATE : Run 'python scripts/run_small_pause_gate.py --monument {monument_id} --cohort {{k}}'
     - Gate 1: Shared_Lexicon/lint_vocabulary.py (0 violations)
     - Gate 2: scripts/hieratic_pronoun_audit.py (100% Deity capitalization)
     - Gate 3: scripts/reconcile_footnotes.py (1:1 footnote parity)
     - Gate 4: scripts/structural_audit.py (unbroken sequence)
  6. INTEGRATION : Run 'python scripts/assemble_and_sync_hub.py --monument {monument_id} --cohort {{k}}'
     - Promotes Draft -> Final MD & Final
     - Appends footnotes to Final_footnotes.txt
     - Advances ACTIVE_ORCHESTRATOR_STATE.json
  7. NEXT COHORT : If k < {num_cohorts}, immediately advance to cohort k+1. DO NOT pause for human input!
[END LOOP at k = {num_cohorts} -> REACHED SOVEREIGN GRAND PAUSE]
```

---

## 4. Complete Codex Partition Schedule ({num_cohorts} Cohorts)

{table_str}

---

## 5. Sovereign Grand Pause Termination
When Cohort {num_cohorts} completes its Small Pause Gate and final integration:
- `remaining_pages == 0`
- The entire {total_pages}-page codex is assembled in `{rel_ws}/Final MD/{monument_id}_complete.md`
- Deliverables are synchronized to `Projects/Typikon Coded/Data/Inbox/{short_title_slug}/`
- Automator halts and delivers the final Grand Pause notification to the Human Operator.
