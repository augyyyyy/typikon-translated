import sys
sys.path.insert(0, ".")
from datetime import date
from ruthenian_engine import RuthenianEngine

engine_stamford = RuthenianEngine(base_dir=".", version="stamford_2014")
engine_lviv = RuthenianEngine(base_dir=".", version="lviv")

dt = date(2026, 2, 25)

ctx_stam = engine_stamford.get_liturgical_context(dt)
rub_stam = engine_stamford.resolve_rubrics(ctx_stam)
enr_stam = {**ctx_stam, **rub_stam.get("variables", {}), "variables": rub_stam.get("variables", {})}
enr_stam["overrides"] = rub_stam.get("overrides", {})

ctx_lviv = engine_lviv.get_liturgical_context(dt)
rub_lviv = engine_lviv.resolve_rubrics(ctx_lviv)
enr_lviv = {**ctx_lviv, **rub_lviv.get("variables", {}), "variables": rub_lviv.get("variables", {})}
enr_lviv["overrides"] = rub_lviv.get("overrides", {})

stich_stam = engine_stamford.resolve_vespers_stichera(enr_stam)
stich_lviv = engine_lviv.resolve_vespers_stichera(enr_lviv)

print("STAMFORD:")
print("Rubrics title:", rub_stam.get("title"))
print("Rubrics overrides:", rub_stam.get("overrides"))
print("Stichera:", stich_stam)

print("\nLVIV:")
print("Rubrics title:", rub_lviv.get("title"))
print("Rubrics overrides:", rub_lviv.get("overrides"))
print("Stichera:", stich_lviv)
