# Process Autopsy Manual (PA-1): Post-Grand-Pause Forensic Protocol
## Operational Standard for Tooling, Infrastructure, and Workflow Evolution

---

## 1. Purpose & Preamble
In the translation of the 400-year Byzantine-Ruthenian Typikon corpus (20 volumes, 8,966+ physical pages), translation quality is a direct mathematical consequence of process health. 

While the **Sovereign Orchestrator Agent (Chat 1)** manages translation cohorts and the **Ephemeral Reviewer (Eye 4)** conducts the Grand Pause textual inspection, the **Tooling & Infrastructure Developer Agent (Chat 2)** conducts the **Post-Grand-Pause Process Autopsy**.

> [!IMPORTANT]
> **The Process Autopsy Principle**:  
> The autopsy does **NOT** re-litigate the translated words of the monument. Instead, it inspects the **machinery, friction points, retries, and toolchain gaps** that occurred during the translation cycle, engineering **permanent, universal patches** so the entire 20-monument corpus becomes progressively faster, more deterministic, and zero-hallucination.

---

## 2. Triggering the Autopsy
A Process Autopsy is triggered whenever:
1. The Human Operator signals that a **Grand Pause** has concluded for a cohort or complete edition.
2. An entry with status `READY_FOR_AUTOPSY` is logged in `scratch/triage_inbox.jsonl`.
3. An unexpected catastrophic gate failure or rework cycle stalls an ongoing cohort.

---

## 3. The 4 Data Ingestion Pillars (Full Triangulation)
To conduct an evidence-based autopsy without speculation, the developer agent ingests four data sources:

1. **Human Operator Debrief Notes**: Subjective feedback on friction, pauses, perceived latency, or manual steering required.
2. **Audit & Gate Reports (`Audit_Reports/*.json`)**: Quantitative failure counts, orphaned footnotes, vocabulary flags, and pronoun false-positives.
3. **Git Commit History & Diffs (`git log`, `git diff`)**: Exact lines of rework, prompt churn, and file restructurings during the cohort run.
4. **Handoff Notes & Orchestrator Telemetry**: Context, leaf counts, physical scan issues, and decisions documented in the deliverable dossier or Hub Inbox.

---

## 4. The 5 Core Evaluation Dimensions

### Dimension 1: Leaf Extraction & Gemini Native Vision Fidelity
* **Scan Ingestion Quality**: Were 300 DPI PNG facsimiles extracted without compression loss or clipping?
* **Physical Ink Discrimination**: Did Gemini Native Vision successfully isolate red cinnabar rubrics from black choral text?
* **Drop Capitals & Ornamentation**: Were liturgical initials, asterisks, and marginal annotations preserved?
* **OCR Layer Independence**: Did the agent rely strictly on physical facsimile ink without inheriting corrupted digital OCR layers?

### Dimension 2: Register & Syntactic Cadence
* **Genre Register Fidelity**: Did the text adhere strictly to its stratified genre (Juridical, Rubrical, Hymnographic, Scholarly)?
* **Verbal Mood**: Were liturgical actions rendered in the Active Present Indicative? Was statutory "shall" restricted to legal mandates?
* **Realia Preservation**: Were Byzantine technical loanwords (*Tetrapod, Klepalo, Aer, Kolyvo, Plashchanytsia, Sluzhebnik*) preserved without generic Western approximations?

### Dimension 3: Small Pause Gate & Linter Friction
* **Vocabulary Linting**: How many iterations were required to pass `lint_vocabulary.py`? Were there false-positive flags?
* **Footnote Bijectivity**: Were any orphaned markers or numbering gaps detected between body text and apparatus?
* **Deity Pronoun Verification**: Did deterministic regexes accurately identify Divine Person pronouns without flagging clergy, saints, or rubrical actors?

### Dimension 4: Agentic Orchestration & Cognitive Load
* **Context & Token Efficiency**: Did the orchestrator experience context compaction, timeout, or runaway generation loops?
* **Subagent Task Handoff**: Were task assignments clear? Did worker subagents adhere to the evidence gate?
* **Human Operator Interventions**: How many manual prompt nudges, file re-creations, or corrections were required by the human operator?

### Dimension 5: Universal Hardening Patches & Regression Evidence
* **Root-Cause Resolution**: Every issue identified must be resolved at the root level (e.g. lexicon expansion, regex fortification, DPI adjustment).
* **The Universal Patch Mandate**: Brittle, one-off overrides are strictly forbidden. All patches must apply across all 20 monuments.
* **Evidence Gate**: Patches must pass automated regression testing against completed golden baselines (`Liturgical Monuments/2010 Lviv Typikon/Final/` and `Liturgical Monuments/1891 Lviv Synod/Final/`).

---

## 5. Ledger Architecture & Scorecard Template
Every autopsy is recorded in the permanent ledger at `docs/process_autopsies/PA-{INDEX}_{MONUMENT_SLUG}.md`:

```markdown
# Process Autopsy PA-XXX: [Monument Name - Cohort / Scope]
**Date**: YYYY-MM-DD  
**Auditor**: Tooling & Infrastructure Developer Agent (Chat 2)  
**Target Monument**: `Typikons/<Monument>/`  
**Scope**: Physical pp. X–Y (Leaves pA–pB)  

---

## 1. Executive Summary & Pipeline Health Score
* **Total Translation Cycle Time**: ...
* **Small Pause Iterations**: ...
* **Operator Interventions**: ...
* **Overall Process Health**: [EXEMPLARY | SOUND | FRICTION_HEAVY | CRITICAL_STALL]

---

## 2. Forensic Analysis across the 5 Dimensions
### Dimension 1: Leaf Extraction & Gemini Vision Fidelity
...
### Dimension 2: Register & Syntactic Cadence
...
### Dimension 3: Small Pause Gate & Linter Friction
...
### Dimension 4: Agentic Orchestration & Operator Interventions
...
### Dimension 5: Universal Hardening Patches & Evidence Gate
...

---

## 3. Deployed Universal Patches
| Patch ID | Component | File Modified | Permanent Improvement |
|---|---|---|---|
| P-001 | Lexicon | `master_liturgical_vocabulary.json` | Added missing realia term whitelist |
| P-002 | Linter | `Shared_Lexicon/lint_vocabulary.py` | Added regex boundary protection |

---

## 4. Regression Test Sign-Off
* `py scratch/search_anti_patterns.py`: [PASS/FAIL]
* Golden Baseline 2010 Typikon: [PASS/FAIL]
* Golden Baseline 1891 Synod: [PASS/FAIL]
```
