import sys
sys.path.insert(0, ".")
from datetime import date
from ruthenian_engine import RuthenianEngine

engine = RuthenianEngine(base_dir=".", version="royal_doors", paschalion="gregorian")
ctx = engine.get_liturgical_context(date(2026, 1, 25))
rub = engine.resolve_rubrics(ctx)

print("Title:", rub.get("title"))
print("Overrides:", rub.get("overrides"))
print("Variables vespers_type:", rub.get("variables", {}).get("vespers_type"))
print("Trace:")
for t in rub.get("_trace", []):
    print(" ", t)
