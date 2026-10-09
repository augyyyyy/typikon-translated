# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

p = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort30_raw_draft.md")
content = p.read_text(encoding="utf-8")
content = content.replace("and the other answers: **\"May Almighty God", "and the other brother answers: **\"May Almighty God")
p.write_text(content, encoding="utf-8")
print("Updated raw draft.")
