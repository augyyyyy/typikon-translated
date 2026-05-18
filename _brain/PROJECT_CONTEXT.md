# Dolnytsky Typikon — Master Project Context

## What This Project Is

A **scientific English translation** of the *Typikon* (liturgical rubrical manual) authored by Fr. Isydor Dolnytsky (1899), working from the **2010 Lviv reprint** edition published by the Ukrainian Greek-Catholic Church (UHKC). The translation covers the complete text including:

- Introduction & translator's preface
- Part I: Structure of Services
- Part II: General Rubrics
- Part III: Individual Rubrics for the Menaion (fixed feasts)
- Part IV: Triodion (moveable cycle) rubrics
- Part V: Temple rubrics + Calendar/Menologion with service-rank tags
- Appendix with tables
- Complete footnote corpus (785+ footnotes with mixed Greek/Latin/Slavonic citations)

## Source Edition (NON-NEGOTIABLE — READ THIS CAREFULLY)

> **⚠️ CRITICAL: THE ONLY SOURCE IS THE 2010 LVIV EDITION.**
>
> We are translating **the 2010 Lviv Ukrainian text** into English. That is the entire scope of the project.
>
> **There is no "1899 edition" in our workflow.** The 2010 book may contain text that originated in 1899 — that is irrelevant to us. Whatever is printed on the pages of the 2010 Lviv book IS our source text, full stop.
>
> **DO NOT:**
> - Frame discrepancies as "1899 text vs. 2010 text"
> - Speculate about whether content is "old" or "revised"
> - Describe corrections as "removing 1899 artifacts"
> - Compare our English against anything other than the 2010 Ukrainian pages
>
> **DO:**
> - Compare the English translation against the 2010 Ukrainian source images (`Typyk UHKC pdf/`) and OCR text (`Ukrainian TXTs/`)
> - If the English doesn't match the 2010 Ukrainian, fix the English
> - That's it. No historical analysis required.
>
> **This confusion has derailed past sessions.** A model encountered the Annunciation section (Images 120–125), decided the English was "from 1899," and spent an entire session rewriting sections and losing its place. The problem was simply that the English didn't match the 2010 Ukrainian — the fix is straightforward comparison and correction, not historical detective work.

## Project Location

```
E:\Google Antigravity\Projects\Translation\
```

## Current State (as of May 2026)

### ✅ Completed

| Milestone | Detail |
|---|---|
| **Full Translation** | All 5 parts + intro + appendix translated from Ukrainian to English |
| **Footnote Corpus** | 785 definitions, zero sequence gaps, zero temp markers |
| **Structural Integrity** | 100% enumerated list sequence match vs. Ukrainian source |
| **Vocabulary Unification** | 25 drift groups adjudicated, all clean across 8 Final files |
| **Typographical Polish** | Smart quotes, em-dashes, trailing whitespace standardized |
| **Footnote Markdown Syntax** | All markers converted to `[^N]` / `[^N]:` for MS Word/Pandoc import |
| **Tserkovne Oko Restoration** | 405 occurrences unified to proper-name form per system instructions |
| **Sluzhebnik Restoration** | Book title treated as proper name (not "Service Book") |

### 🔶 In Progress

| Task | Progress | Detail |
|---|---|---|
| **Visual Rubrical Audit** | ~51% | Verified Images 001–146 (Part 3 Menaion 100% complete). Resume at Image 147 (Part 4 Triodion). |
| **Hieratic Pronoun Audit** | Enforced but unverified | Thee/Thou/Thy applied via scripts; completeness not audited |

### ❌ Not Started

| Task | Detail |
|---|---|
| **Translation Accuracy Audit** | No line-by-line semantic verification (requires Ukrainian-literate reviewer) |
| **Calendar Symbol Audit** | `=`, `+`, `Влк`, `Тр`, `А-Є` in Part 3 not yet audited |
| **Historical Fidelity Audit** | Latin-derived terms (Monstrance, Dalmatic) not yet checked |
| **Glossary Appendix** | `scratch/typikon_terms.txt` needs conversion to publishable markdown |

## Service-Rank Tags (Part 5 Calendar)

The Menologion in Part 5 uses these standardized tags:

| Tag | Meaning |
|---|---|
| `[LORD]` | Feast of the Lord |
| `[MOG]` | Feast of the Mother of God (Theotokos) |
| `[VIGIL]` | All-Night Vigil |
| `[POL]` | Polyeleos |
| `[GT DOX]` | Great Doxology (rank on 6) |
| `[6 SM]` | Small Doxology (rank on 6) |
| `[4 A+G]` | Rank on 4 with Apostle-Gospel at Liturgy |
| `[4 TR]` | Rank on 4 with Troparion |
| `[4 NO]` | Rank on 4 without troparion |

## Related Projects (Same Ecosystem)

- **Typikon Coded** (`E:\Google Antigravity\Projects\Typikon Coded\`) — A computational engine that consumes the Dolnytsky translation as a JSON database to generate liturgical service digests. Uses a 4-tier authority hierarchy: Ordo Celebrationis 1944 → Dolnytsky Typikon → Pochaiv Anthologion → Engine Default.
- **Yasinovsky Irmologia Catalogue** — Parallel scholarly project cataloguing Prof. Yasinovsky's collection of Irmologia manuscripts, using the same Dolnytsky terminology standards.
