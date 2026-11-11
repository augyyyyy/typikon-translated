# Gate 1B Anti-Slop Linter & Hieratic Pronoun Audit Reference

## 1. Anti-Slop Linter (`scripts/lint_liturgical_slop.py` — Gate 1B)
Run on any draft or final file via:
```powershell
py scripts/lint_liturgical_slop.py --target "<path/to/file.md>"
```

### 1.1 Four Prohibited Slop Categories
1. **`pseudo_archaic_slop`**:
   - Permanently banned across body text (and footnotes, except `wherefore` inside verbatim historical footnote quotes):
     `verily`, `twas`, `betwixt`, `methinks`, `hearken`, `wherefore`, `peradventure`, `forsooth`, `haply`, `effulgent`, `resplendent`, `beholden`, `lo and behold`, and `wondrous` (except in the fixed biblical incipit *"Wondrous is God in His saints"* / *"Wondrous art Thou"*).
   - **Canonical Replacements**:
     - `wherefore` → `therefore`
     - `wondrous` → `marvelous`
     - `verily` → `truly`
     - `hearken` → `give ear`
     - `resplendent` / `effulgent` → `radiant`
2. **`archaic_rubrical_verb_drift` (120+ `-eth` Verb Detector)**:
   - Rejects 3rd-person singular `-eth` verbs across both body text and footnotes (`abideth`, `beginneth`, `believeth`, `boweth`, `censeth`, `cometh`, `crieth`, `dwelleth`, `entereth`, `forgiveth`, `giveth`, `glorifieth`, `goeth`, `hearkeneth`, `intercedeth`, `judgeth`, `kisseth`, `liveth`, `loveth`, `magnifieth`, `maketh`, `partaketh`, `praiseth`, `proclaimeth`, `readeth`, `rebuketh`, `receiveth`, `rejoiceth`, `riseth`, `ruleth`, `saith`, `sanctifieth`, `saveth`, `sayeth`, `seeth`, `shineth`, `singeth`, `sitteth`, `standeth`, `taketh`, `turneth`, `vesteth`, `worshippeth`, `writeth`, etc.).
   - Non-verb `-eth` tokens (`Nazareth`, `Elizabeth`, `Sabbath`, `Gennesaret`, `twentieth`..`thousandth`, `hath`, `doth`) are whitelisted in `NON_VERB_ETH_TOKENS`.
3. **`ai_cliches_and_filler`**:
   - Rejects conversational AI filler: `testament to`, `beacon of`, `delve into`, `tapestry of`, `rich history`, `serves as a reminder`, `inextricably linked`, `pivotal moment`, `poignant`, `needless to say`, `it is important to remember`.
4. **`rubrical_shall_bombing`**:
   - Rejects `the priest/deacon/bishop/choir/reader shall bow/enter/take/cense/kiss/bless/proclaim/say/chant/vest`. Always use Active Present Indicative (`the priest bows`, `the deacon censes`).

---

## 2. Hieratic Deity Pronoun Audit (`scripts/hieratic_pronoun_audit.py` — Gate 1C)
Run via:
```powershell
py scripts/hieratic_pronoun_audit.py --target "<path/to/file.md>"
```
- **Positive Rule**: Capitalize 100% of pronouns referring to the Persons of the Holy Trinity (*He, Him, His, Himself, Thou, Thee, Thy, Thine, Thyself*).
- **Context-Sensitive Negative Rule**:
  - In Theotokia, Stavrotheotokia, and Marian canons/akathists, keep 2nd-person pronouns addressing the Mother of God (*thou, thee, thy, thine*) lowercase, while capitalizing 3rd-person pronouns referring to Christ (*He, Him, His*) within the same stanza.
  - Keep pronouns referring to saints, martyrs, hierarchs, clergy, or the devil/serpent/enemy strictly lowercase (*he, him, his*).
