# Open Work — Prioritized Remaining Tasks

All remaining tasks, prioritized and annotated with context for seamless handoff.

---

## 🔴 Priority 1: Resume Visual Rubrical Audit

**Status:** Part 3 (Menaion) 100% complete. Overall audit ~51% complete.  
**Resume at:** Image 147 (Beginning of Part 4 Triodion)  
**Remaining:** Images 147–287 (141 images)  
**Method:** Compare English text line-by-line against 2010 Ukrainian source images  
**Files affected:** Parts 4 and 5  

### ✅ Recently Resolved Milestones (Images 124–146):
- **Matrix Error & Ghost Loop Purged:** Truncated and eliminated fabricated audit entries from past sessions. Fully restored physical image sequence alignment.
- **March 26 Boundary Logic Adjudicated:** Proven that no text is missing between March 26 and April 23.
- **Annunciation Corpus Synchronized:** Re-translated Apodosis structural sections to exactly match the concise 2010 Lviv text, eliminating historical interpolation drift.
- **July 31/August 1 Transition Remediated:** Restored complete weekday and Sunday liturgy rubrics for the Procession of the Cross, including the joint blessing of water and herbs, alongside linking anchors `[^451]`, `[^452]`, and `[^453]`.
- **Menaion Tail Purged:** Excised the large trailing duplicate footnote block (`[^279]` through `[^465]`) appended after August 31, terminating Part 3 naturally.

### What to do:
1. Load `Typyk UHKC(укр)-147.jpg`
2. Find the corresponding lines in `Final_Dolnytsky_part4_triodion.txt`
3. Verify all footnote superscripts match `[^N]` markers in the text
4. Log findings in `visual_audit_log.md`
5. Apply corrections to Final files
6. Continuously sync tracking files (`IMPLEMENTATION_PLAN.md`, `TASK_LIST.md`, `WALKTHROUGH.md`) inside the `_brain/` folder.

### Key context:
- The audit is a **footnote placement verification**, not a translation accuracy check
- Publisher anomalies should be logged but preserved (e.g., the `[^3a]` precedent)
- The detailed audit log is in `visual_audit_log.md` (2,165+ lines)
- **DO NOT** speculate about "1899 vs 2010 editions" — see `DECISION_LOG.md` → Decision 0

---

## 🟡 Priority 2: Calendar Symbol Audit

**Status:** Not started  
**Scope:** Verify that Menaion/Calendar symbols are preserved correctly in Part 3  
**Symbols to check:** `=`, `+`, `Влк`, `Тр`, `А-Є`, ALL CAPS, **Bold Text**  

### What to do:
1. Write or run an audit script against `Final_Dolnytsky_part3_menaion.txt`
2. Verify each symbol type appears in the correct liturgical context
3. Cross-reference against the Ukrainian source (Part 3.pdf or Part 3.txt)

---

## 🟡 Priority 3: Hieratic Pronoun Completeness Audit

**Status:** Enforced but unverified  
**Scope:** Scan all Final files for missed lowercase deity pronouns  
**Existing script:** `scratch/hieratic_pronoun_audit.py`  

### What to do:
1. Run `hieratic_pronoun_audit.py` against all 8 Final files
2. Review flagged instances for false positives (e.g., "he" referring to a saint, not God)
3. Apply corrections where genuine misses are found

---

## 🟡 Priority 4: Glossary Appendix Finalization

**Status:** Not started  
**Source:** `scratch/typikon_terms.txt` (57 KB draft)  
**Target:** A formal, publishable markdown appendix  

### What to do:
1. Review `scratch/typikon_terms.txt` for completeness
2. Convert to structured markdown with alphabetical sections
3. Cross-reference against the `vocabulary_standardization_matrix.md` for consistency
4. Add to Final files or create a new `Final_Dolnytsky_glossary.md`

---

## 🔵 Priority 5: Translation Accuracy Audit

**Status:** Not started — **requires Ukrainian-literate reviewer**  
**Scope:** Line-by-line verification that the English correctly renders the Ukrainian meaning  
**Risk:** The translation was produced by an AI model across many chat sessions. No human or machine review of semantic accuracy has been performed.  

> ⚠️ The structural audit confirmed no *paragraphs were dropped*, but it did NOT verify that *content within each paragraph* was correctly translated.

---

## 🔵 Priority 6: Historical Fidelity Audit

**Status:** Not started  
**Scope:** Verify that Latin-derived liturgical terms (Monstrance, Dalmatic, etc.) are translated exactly as written in the source, per system instructions §1.  

---

## 🔵 Priority 7: System Instructions Compliance Audit

**Status:** Partial  
**Remaining checks:**

| Instruction | Status |
|---|---|
| Master Terminology Glossary (§5) | ✅ 100% verified |
| Book Title Proper-Name Rule | ✅ 100% verified |
| Hieratic Pronouns (§1) | 🔶 Enforced, not fully verified |
| Deity Capitalization (§1) | 🔶 Enforced, not fully verified |
| Fidelity over Flow (§1) | ❌ Unverified |
| Historical Fidelity (§1) | ❌ Unverified |
| Calendar Symbols (§4) | ❌ Unverified |
| Footnote Mixed Content (§3) | ✅ Verified |
