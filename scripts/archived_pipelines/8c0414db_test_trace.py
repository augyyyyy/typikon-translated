import datetime
import sys
sys.path.insert(0, ".")
from engine import RuthenianEngine

re = RuthenianEngine()
d = datetime.date(2026, 9, 8)
ctx = re.get_liturgical_context(d)
rubrics = re.resolve_rubrics(ctx)

print("Title:", rubrics.get("title"))
print("Trace:")
for t in rubrics.get("_trace", []):
    print("  ", t)

print("\nVariables:")
for k, v in rubrics.get("variables", {}).items():
    print(f"  {k}: {v}")
