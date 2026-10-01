import json

with open("json_db/02d_logic_temple.json", "r", encoding="utf-8") as f:
    temple_db = json.load(f)

cases = temple_db.get("specific_cases", {})

def resolve_temple_case(context, temple_cases):
    """
    Identifies which of the 34 Part V temple cases applies to the given context.
    Returns (case_id, case_data).
    """
    month = context.get("month")
    day = context.get("day")
    try:
        month = int(month) if month is not None else None
        day = int(day) if day is not None else None
    except (ValueError, TypeError):
        month, day = None, None

    dow = context.get("day_of_week")
    try:
        dow = int(dow) if dow is not None else None
    except (ValueError, TypeError):
        dow = None

    offset = context.get("pascha_offset")
    try:
        offset = int(offset) if offset is not None else None
    except (ValueError, TypeError):
        offset = None

    # 1. Outside Triodion (Fixed Date Collisions)
    if month == 9 and day == 1:
        if dow == 0:
            return "case_1b", temple_cases.get("case_1b")
        return "case_1a", temple_cases.get("case_1a")
    
    if month == 1 and day == 1:
        if dow == 0:
            return "case_2", temple_cases.get("case_2")

    # 2. In Midst of Triodion / Pentecostarion (Moveable Collisions)
    if offset is not None:
        # Pre-Lenten & Lenten Sundays
        if dow == 0:
            if offset in (-70, -63, -56, -49):
                return "case_3", temple_cases.get("case_3")
            if offset == -42:
                return "case_10", temple_cases.get("case_10")
            if offset == -28:
                return "case_14", temple_cases.get("case_14")
            if offset in (-35, -21, -14):
                return "case_13", temple_cases.get("case_13")
            if offset == -7:
                return "case_19", temple_cases.get("case_19")
            if offset == 42:
                return "case_25", temple_cases.get("case_25")
            if offset == 49:
                return "case_28", temple_cases.get("case_28")
            if offset == 56:
                return "case_31", temple_cases.get("case_31")
            if offset in (60, 63):
                return "case_32", temple_cases.get("case_32")

        # Saturdays
        if dow == 6:
            if offset == -57:
                return "case_4", temple_cases.get("case_4")
            if offset == -50:
                return "case_6", temple_cases.get("case_6")
            if offset == -43:
                return "case_9", temple_cases.get("case_9")
            if offset in (-36, -29, -22):
                return "case_12", temple_cases.get("case_12")
            if offset == -15:
                return "case_17", temple_cases.get("case_17")
            if offset == -8:
                return "case_18", temple_cases.get("case_18")
            if offset == 48:
                return "case_27", temple_cases.get("case_27")

        # Weekdays
        if dow in (1, 2, 3, 4, 5):
            # Cheesefare Weekdays
            if -55 <= offset <= -51:
                return "case_5", temple_cases.get("case_5")
            # 1st Week of Lent
            if offset == -48:
                return "case_7", temple_cases.get("case_7")
            if -47 <= offset <= -44:
                return "case_8", temple_cases.get("case_8")
            # 5th Week Wed / Thu
            if offset == -17:
                return "case_15", temple_cases.get("case_15")
            if offset == -16:
                return "case_16", temple_cases.get("case_16")
            # General Lenten Weekdays (2nd to 6th weeks)
            if -41 <= offset <= -9:
                return "case_11", temple_cases.get("case_11")

        # Passion Week & Pascha
        if -6 <= offset <= 0:
            return "case_20", temple_cases.get("case_20")

        # Pascha to Pentecost
        if offset == 50 and dow == 1:
            return "case_29", temple_cases.get("case_29")
        if 51 <= offset <= 55 and dow in (2, 3, 4, 5, 6):
            return "case_30", temple_cases.get("case_30")
        if offset == 38 and dow == 3:
            return "case_23", temple_cases.get("case_23")
        if offset == 39 and dow == 4:
            return "case_24", temple_cases.get("case_24")
        if offset == 47 and dow == 5:
            return "case_26", temple_cases.get("case_26")
        if offset in (65, 68) and dow == 5:
            return "case_33", temple_cases.get("case_33")
        if 1 <= offset <= 27:
            return "case_21", temple_cases.get("case_21")
        if 28 <= offset <= 48:
            return "case_22", temple_cases.get("case_22")

    return None, None

# Test coverage: ensure every one of the 34 cases can be resolved
tested_cases = set()

test_contexts = [
    ("case_1a", {"month": 9, "day": 1, "day_of_week": 2, "pascha_offset": 100}),
    ("case_1b", {"month": 9, "day": 1, "day_of_week": 0, "pascha_offset": 100}),
    ("case_2",  {"month": 1, "day": 1, "day_of_week": 0, "pascha_offset": -100}),
    ("case_3",  {"pascha_offset": -70, "day_of_week": 0}),
    ("case_4",  {"pascha_offset": -57, "day_of_week": 6}),
    ("case_5",  {"pascha_offset": -53, "day_of_week": 3}),
    ("case_6",  {"pascha_offset": -50, "day_of_week": 6}),
    ("case_7",  {"pascha_offset": -48, "day_of_week": 1}),
    ("case_8",  {"pascha_offset": -46, "day_of_week": 3}),
    ("case_9",  {"pascha_offset": -43, "day_of_week": 6}),
    ("case_10", {"pascha_offset": -42, "day_of_week": 0}),
    ("case_11", {"pascha_offset": -38, "day_of_week": 4}),
    ("case_12", {"pascha_offset": -36, "day_of_week": 6}),
    ("case_13", {"pascha_offset": -35, "day_of_week": 0}),
    ("case_14", {"pascha_offset": -28, "day_of_week": 0}),
    ("case_15", {"pascha_offset": -17, "day_of_week": 3}),
    ("case_16", {"pascha_offset": -16, "day_of_week": 4}),
    ("case_17", {"pascha_offset": -15, "day_of_week": 6}),
    ("case_18", {"pascha_offset": -8, "day_of_week": 6}),
    ("case_19", {"pascha_offset": -7, "day_of_week": 0}),
    ("case_20", {"pascha_offset": -3, "day_of_week": 4}),
    ("case_21", {"pascha_offset": 5, "day_of_week": 5}),
    ("case_22", {"pascha_offset": 32, "day_of_week": 2}),
    ("case_23", {"pascha_offset": 38, "day_of_week": 3}),
    ("case_24", {"pascha_offset": 39, "day_of_week": 4}),
    ("case_25", {"pascha_offset": 42, "day_of_week": 0}),
    ("case_26", {"pascha_offset": 47, "day_of_week": 5}),
    ("case_27", {"pascha_offset": 48, "day_of_week": 6}),
    ("case_28", {"pascha_offset": 49, "day_of_week": 0}),
    ("case_29", {"pascha_offset": 50, "day_of_week": 1}),
    ("case_30", {"pascha_offset": 52, "day_of_week": 3}),
    ("case_31", {"pascha_offset": 56, "day_of_week": 0}),
    ("case_32", {"pascha_offset": 63, "day_of_week": 0}),
    ("case_33", {"pascha_offset": 68, "day_of_week": 5}),
]

for expected_id, ctx in test_contexts:
    cid, cdata = resolve_temple_case(ctx, cases)
    assert cid == expected_id, f"Expected {expected_id}, got {cid} for {ctx}"
    assert cdata is not None, f"Case data missing for {cid}"
    tested_cases.add(cid)

print(f"Verified all {len(tested_cases)} of 34 temple cases map perfectly!")
