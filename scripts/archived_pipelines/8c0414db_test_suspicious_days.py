import sys
sys.path.insert(0, ".")
from engine import RuthenianEngine

re = RuthenianEngine()

test_dates = [
    ("2026-09-08", "Nativity of Theotokos"),
    ("2026-09-09", "Joachim and Anna"),
    ("2026-09-26", "John the Theologian"),
    ("2026-10-01", "Protection of Theotokos"),
    ("2026-10-26", "Demetrius"),
    ("2026-11-08", "Archangel Michael"),
    ("2026-11-12", "Josaphat"),
    ("2026-11-21", "Entrance of Theotokos"),
    ("2026-12-06", "St. Nicholas"),
    ("2026-12-09", "Immaculate Conception"),
    ("2026-12-26", "Synaxis of Theotokos"),
    ("2026-01-07", "Synaxis of Forerunner"),
    ("2026-01-30", "Three Hierarchs"),
    ("2026-03-25", "Annunciation"),
    ("2026-07-20", "Elijah"),
    ("2026-08-15", "Dormition"),
    ("2026-08-16", "Image Not-Made-By-Hands")
]

import datetime
for date_str, desc in test_dates:
    d = datetime.date.fromisoformat(date_str)
    ctx = re.get_liturgical_context(d)
    paradigm = re.identify_paradigm(ctx)
    rubrics = re.resolve_rubrics(ctx)
    print(f"{date_str} ({desc}):")
    print(f"  Paradigm Identified: {paradigm}")
    print(f"  Title: {rubrics.get('title')}")
    print(f"  Vespers Type: {rubrics.get('variables', {}).get('vespers_type')}")
    print(f"  Matins Type: {rubrics.get('variables', {}).get('matins_type')}")
    print(f"  Rank: {rubrics.get('variables', {}).get('rank')}")
