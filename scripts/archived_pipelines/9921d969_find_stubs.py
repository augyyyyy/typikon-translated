import sys
import os
from datetime import date
sys.path.insert(0, "c:/Users/augus/OneDrive/Documents/Google Antigravity/Projects/Typikon Coded")
from ruthenian_engine import RuthenianEngine
from typikon_digest_generator import TypikonDigestGenerator

engine = RuthenianEngine(base_dir="c:/Users/augus/OneDrive/Documents/Google Antigravity/Projects/Typikon Coded")
gen = TypikonDigestGenerator(engine)

target_date = date(2026, 2, 16)
context = engine.get_liturgical_context(target_date)
rubrics = engine.resolve_rubrics(context)
booklet = gen.generate_full_service(context, rubrics)

print("Generated booklet lines with [STUB]:")
for line in booklet.split("\n"):
    if "[STUB]" in line:
        print(line)
