import sys
sys.path.insert(0, ".")
from datetime import date
from ruthenian_engine import RuthenianEngine

engine = RuthenianEngine(base_dir=".", version="royal_doors", paschalion="gregorian")

milestones = [
    (date(2026, 1, 25), "Publican & Pharisee"),
    (date(2026, 2, 1), "Prodigal Son"),
    (date(2026, 2, 7), "Meatfare Saturday"),
    (date(2026, 2, 8), "Meatfare Sunday"),
    (date(2026, 2, 15), "Cheesefare Sunday"),
    (date(2026, 2, 16), "Clean Monday"),
    (date(2026, 2, 22), "Sunday of Orthodoxy (Lent 1)"),
    (date(2026, 3, 28), "Lazarus Saturday"),
    (date(2026, 3, 29), "Palm Sunday"),
    (date(2026, 4, 2), "Holy Thursday"),
    (date(2026, 4, 3), "Holy Friday"),
    (date(2026, 4, 4), "Holy Saturday"),
    (date(2026, 4, 5), "Holy Pascha"),
    (date(2026, 4, 6), "Bright Monday"),
    (date(2026, 4, 12), "Thomas Sunday"),
    (date(2026, 5, 14), "Ascension"),
    (date(2026, 5, 24), "Pentecost"),
    (date(2026, 5, 31), "All Saints Sunday"),
]

for dt, name in milestones:
    ctx = engine.get_liturgical_context(dt)
    rub = engine.resolve_rubrics(ctx)
    vars_res = rub.get("variables", {})
    over_res = rub.get("overrides", {})
    vv = str(vars_res.get("vespers_type"))
    vo = str(over_res.get("vespers_type"))
    m = str(vars_res.get("matins_type"))
    l = str(vars_res.get("liturgy_type"))
    poly = str(vars_res.get("has_polyeleos"))
    dox = str(vars_res.get("doxology_type"))
    print(f"{name:30} ({dt}) | V_var: {vv:22} | V_over: {vo:20} | M: {m:22} | L: {l:22} | P: {poly:5} | D: {dox:15}")
