# Open Work — Prioritized Remaining Tasks

All remaining tasks, prioritized and annotated with context for seamless handoff.

---

## 🔴 Priority 1: Calendar Symbol Audit

**Status:** Not started  
**Scope:** Verify that Menaion/Calendar symbols are preserved correctly in Part 3 (`Final_Dolnytsky_part3_menaion.txt`)  
**Symbols to check:** `=`, `+`, `Влк`, `Тр`, `А-Є`, ALL CAPS, **Bold Text**  

### What to do:
1. Write or run an audit script against `Final_Dolnytsky_part3_menaion.txt`
2. Verify each symbol type appears in the correct liturgical context
3. Cross-reference against the Ukrainian source (Part 3.pdf or Part 3.txt)

---

## 🔴 Priority 2: Hieratic Pronoun Completeness Audit

**Status:** Enforced but unverified  
**Scope:** Scan all Final files for missed lowercase deity pronouns  
**Existing script:** `scratch/hieratic_pronoun_audit.py`  

### What to do:
1. Run `hieratic_pronoun_audit.py` against all 8 Final files
2. Review flagged instances for false positives (e.g., "he" referring to a saint, not God)
3. Apply corrections where genuine misses are found

---

## 🟢 Priority 3: Visual Rubrical Audit (Completed)

**Status:** 100% Complete  
**Scope:** Verified 1-to-1 against all 287 Ukrainian source scans. All findings documented in `visual_audit_log.md`.  
**Result:** Eradicated phantom anchors, resolved page boundary logic, unified all footnote anchors through `[^785]`.  


---

## 🟢 Priority 4: Glossary Appendix Finalization (Completed)

**Status:** 100% Complete  
**Result:** Generated [Final_Dolnytsky_glossary.md](file:///e:/Google%20Antigravity/Projects/Translation/Final/Final_Dolnytsky_glossary.md) with 63 entries, categorized and cross-referenced with exact source references and categories.  

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
