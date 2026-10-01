import sys
sys.path.append(r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded")

from ruthenian_engine import RuthenianEngine
from datetime import date

e = RuthenianEngine('.')

# June 24, 2026
dt = date(2026, 6, 24)
ctx = e.get_liturgical_context(dt)
ctx.pop("_almanac_used", None)
rubrics = e.resolve_rubrics(ctx)
readings = e.resolve_liturgy_readings(ctx, rubrics)
print("Context details:")
print("Day of week:", ctx.get("day_of_week"))
print("Saints:", ctx.get("saints"))
print("Readings:")
import json
print(json.dumps(readings, indent=2))
