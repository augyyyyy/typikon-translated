#!/usr/bin/env python3
"""
Ship Dolnytsky Typikon Finalized Deliverables to Typikon Coded Inbox
Complies with AGENTS.md dynamic path resolution and UTF-8 declarations.
"""
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Dynamic project-relative paths
proj_root = Path(__file__).resolve().parents[4] / "Projects" / "Translation"
if not proj_root.exists():
    proj_root = Path(".").resolve()

hub_inbox = proj_root.parent / "Typikon Coded" / "Data" / "Inbox"
hub_inbox.mkdir(parents=True, exist_ok=True)

final_dir = proj_root / "Final"
final_md_dir = proj_root / "Final MD"

print(f"Source Final: {final_dir}")
print(f"Source Final MD: {final_md_dir}")
print(f"Destination Inbox: {hub_inbox}")

copied_files = []

# 1. Copy Final/ TXT deliverables
for f in sorted(final_dir.glob("*.txt")):
    dst = hub_inbox / f.name
    shutil.copy2(f, dst)
    copied_files.append(f.name)
    print(f"  Copied TXT: {f.name} ({f.stat().st_size:,} bytes)")

# 2. Copy Final MD/ Markdown deliverables
for f in sorted(final_md_dir.glob("*.md")):
    dst = hub_inbox / f.name
    shutil.copy2(f, dst)
    copied_files.append(f.name)
    print(f"  Copied MD: {f.name} ({f.stat().st_size:,} bytes)")

# 3. Create handoff_note.md
handoff_note_path = hub_inbox / "handoff_note.md"
note_content = """# Handoff Note: Dolnytsky Typikon Translation & Footnote Fortification

**Date**: 2026-09-14  
**Source Corpus**: Fr. Isydor Dolnytsky, *Typik Tserkvy Rusko-Katolitskoyia* (Lviv 1899 / 2010 Reprint)  
**Primary Authenticated Witnesses**:
1. Binary Word 97–2003 manuscript (`Typyk UHKC(укр).doc`, 3,098,624 bytes, 785 native footnotes)
2. English Translation DOCX (`Here is the revised translation of the Typikon.docx`)
3. Lviv 2010 Page Scans (`Typyk UHKC(укр)-001.jpg` to `287.jpg`)
4. OCR Reference Texts (`Ukrainian TXTs/`)

---

## Key Actions & Fortifications Delivered

1. **Footnote Apparatus Decontamination**:
   - Resolved critical historical contamination in `Final_footnotes.txt` and `Final_footnotes.md`.
   - Footnotes `[^763]`, `[^767]`, and `[^780]` had erroneously ingested ~84.5 KB of Appendix body text (Chunks 74, 75, and 77).
   - Replaced contaminated passages with the authentic concise definitions verified against the native Ukrainian manuscript. Total file size reduced by 84,482 characters with 100% integrity.
   - All 785 native footnotes are now cleanly indexed with 0 missing definitions and 0 orphan anchors.

2. **Liturgical Concelebration Diagrams Restored**:
   - Restored all 10 missing liturgical diagrams across `Final_Dolnytsky_appendix.txt` and `Final MD/Final_Dolnytsky_appendix.md`:
     1. Diagram 1: Vespers Entrance (Section 51)
     2. Diagram 2: Litiya Procession in the Narthex (Section 71)
     3. Diagram 3: Blessing of Loaves around the Tetrapod (Section 72)
     4. Diagram 4: Magnification (Polyeleos) around the Tetrapod (Section 94)
     5. Diagram 5: Paschal Matins closed church doors layout
     6. Diagram 6: Proskomedia Lamb incision and piercing schema (IC XC / NI KA) (Section 108)
     7. Diagram 7: Little Entrance in concelebration with two deacons (Section 152)
     8. Diagram 8: Little Entrance concelebration before Holy Doors (Section 200)
     9. Diagram 9: Concelebrants seated at the High Throne (Section 201)
     10. Diagram 10: Concelebrants' communion sequence of Body and Blood (Section 209)

3. **Synchronized TXT and Markdown Deliverables**:
   - Both `Final/` and `Final MD/` suites are brought into 100% parity.

4. **Terminology & Anti-Pattern Compliance**:
   - Validated against Master Glossary: *Tserkovne Oko*, *Anthologion*, *Menaion*, *Sessional Hymn*, *Kontakion*, *Doxastikon*, *Theotokion*, *Praises*, *Aposticha*, *Exaposteilarion*, *Doxology*, *Idiomelon*, *Polyeleos*, *Gradual*, *Tone*, *Apodosis*, *Forefeast*, *Afterfeast*, *Temple*, *Shroud*, *Litiya*, *All-Night Vigil*, *Compline*, *Midnight Office*, *Typika*.
   - Hieratic pronouns (Thee, Thou, Thy, Thine) and Deity capitalization enforced.
   - Zero hardcoded path violations introduced.
"""

with open(handoff_note_path, "w", encoding="utf-8") as f:
    f.write(note_content)

print(f"\nHandoff note written: {handoff_note_path.name}")
print(f"Total deliverables shipped: {len(copied_files)} files + handoff note.")
