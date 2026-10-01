import re

pattern = r'\s+and\s+|\s+&\s+|;|(?<!\bSt)(?<!\bSts)(?<!\bVen)(?<!\bBp)(?<!\bAp)(?<!\bAps)(?<!\bMetr)(?<!\bArchbp)(?<!\bPatr)(?<!\bMart)\.\s+'

test_strings = [
    "Prop. Nahum.",
    "Prop. Daniel and the three youths.",
    "St. Sylvester, Pope of Rome; Prop. Malachi",
    "Prop. Isaiah and Martyr Christopher.",
    "Martyr Aquilina and St. Triphyllius, Bishop of Leucosia.",
    "Forefeast of the Dormition. Prop. Micah."
]

for s in test_strings:
    cleaned = s.rstrip(".")
    parts = [p.strip() for p in re.split(pattern, cleaned, flags=re.IGNORECASE) if p.strip()]
    print(f"Original: {s}")
    print(f"Split:    {parts}")
    print("-" * 50)
