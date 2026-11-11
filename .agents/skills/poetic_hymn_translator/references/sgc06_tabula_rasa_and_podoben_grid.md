# Universal Epigraphic Grounding (`SGC-06`), *Tabula Rasa* Registries & Podoben Grid Schema (`Rule 22`)

## 1. The Anti-Pretraining Incursion Law (`SGC-06` / `Rule 22`)
LLM agents carry pre-trained assumptions from modern liturgical handbooks, standard Byzantine Greek automela compendia, and 19th/20th-century Russian Synodal rubrics. Projecting external taxonomies onto a historical monument or conflating internal codex ink with external tradition is a critical `SGC-06` violation.

### 1.1 Five Invariant Principles
1. **Tabula Rasa Bottom-Up Ink Construction**:
   - Every monument's internal index, primitives registry (`data/liturgical_primitives_registry.json`), Podoben grid (`scripts/generate_podoben_grid.py`), or rubric catalog (`scripts/universal_corpus_extractor.py`) must be constructed **100% bottom-up from the physical ink of its leaves (`p1`..`pN`)**.
2. **Mandatory 5-Tuple Physical Attestation Locus**:
   - No liturgical model, category, or hymnographic primitive may appear in an internal monument dataset unless it possesses `>= 1` verified physical attestation tuple on a physical leaf:
     ```text
     Attestation Locus = <Physical Folio & Column, Leaf Number, Liturgical Office, Verbatim Slavonic Rubric, Governed Incipit>
     ```
   - Example: `<Fol. 14v, col. 1, p32, Great Vespers (Lord, I have cried), "Подо́бенъ: Всехва́льніи му́ченицы:", "Преблаже́нніи отцы̀ на́ши...">`.
3. **Strict Epistemic Layering (Internal vs. External Concordance)**:
   - **Internal Primary Source Layer**: Contains ONLY what is physically printed in that monument.
   - **External Comparative Layer**: Broad Byzantine Greek roots, post-Nikonian variants, cross-monument links, and general automela concordances MUST be quarantined in separate comparative datasets (`data/byzantine_automela_concordance.json`, dedicated concordance appendices, or Section 4 of review digests). Never merge external concordance rows into primary internal registries as if they were attested in the codex.
4. **Prohibition of Negative Hallucinations / Ghost Stubs**:
   - Internal codex grids and registries must never list un-invoked external textbook models with blank (`—`) or zero (`0`) attestations as if the historical codex were deficient or omitted them. Missing an external model belonging to a different liturgical cycle (e.g., Menaion vs. Octoechos) is not a codex defect.
5. **Programmatic Runtime Assertion Gate**:
   - Every primitives registry and Podoben grid builder (`scripts/generate_liturgical_primitives_registry.py`, `scripts/generate_podoben_grid.py`, `scripts/universal_corpus_extractor.py`) must programmatically assert that 100% of items in any primary monument registry satisfy `len(attested_loci) > 0`. Empty or un-attested stubs raise a fatal assertion error at runtime.

---

## 2. Canonical 3-Layer Melodic Model (`Podoben`) Grid & Normalization
Enforced by `scripts/hymnographic_gold_normalizer.py` and `data/liturgical_primitives_registry.json`:
1. **Three Layers**:
   - **Layer 1 (Ruthenian Tone)**: `*Tone 1`..`*Tone 8` (never `"Mode"` or `"Plagal"`).
   - **Layer 2 (Canonical English Incipit in Quotes)**: `Podoben: "<Canonical English Incipit>"` (matched deterministically against `data/liturgical_primitives_registry.json`).
   - **Layer 3 (Parenthetical Verbatim Slavonic Witness)**: `(<Slavonic Witness>):*` (in original orthography as printed on the leaf, enclosed in parentheses inside the italic span).
2. **Self-Modeled & Proper Melodies**:
   - **Automelon (`Самоподо́бенъ`)**: `*Tone N, Automelon (*Samopodoben*):*` or `*Tone N, Self-Modeled Melody (Самоподо́бенъ):*`.
   - **Idiomelon (`Самогла́сенъ`)**: `*Tone N, Idiomelon (*Samohlasen*):*`.
