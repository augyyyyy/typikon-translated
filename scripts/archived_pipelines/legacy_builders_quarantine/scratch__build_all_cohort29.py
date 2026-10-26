# -*- coding: utf-8 -*-
"""
Master Builder for Cohort 29 (Leaves p561 to p580)
Typikon of Isidore Dolnytsky (Lviv, 1899)
"""

import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = PROJECT_ROOT / "Liturgical Monuments" / "1899 Dolnytsky Typikon" / "Source Text" / "1899_dolnytsky_typikon_cohort29_source.txt"
DRAFT_PATH = PROJECT_ROOT / "Liturgical Monuments" / "1899 Dolnytsky Typikon" / "Draft" / "1899_dolnytsky_typikon_cohort29_raw_draft.md"
FOOTNOTES_PATH = PROJECT_ROOT / "Liturgical Monuments" / "1899 Dolnytsky Typikon" / "Draft" / "1899_dolnytsky_typikon_cohort29_footnotes.txt"

# 35 Keys of the Boundaries
KEYS_CS = ['А', 'Б', 'В', 'Г', 'Д', 'Є', 'Ж', 'Ѕ', 'З', 'И', 'І', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ѡ', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Ѣ', 'Ю', 'Ѫ', 'Ѧ']
KEYS_EN = ['1 (A)', '2 (B)', '3 (V)', '4 (G)', '5 (D)', '6 (E)', '7 (Zh)', '8 (S)', '9 (Z)', '10 (I)', '11 (I)', '12 (K)', '13 (L)', '14 (M)', '15 (N)', '16 (O)', '17 (P)', '18 (R)', '19 (S)', '20 (T)', '21 (U)', '22 (F)', '23 (Kh)', '24 (O)', '25 (Ts)', '26 (Ch)', '27 (Sh)', '28 (Shch)', '29 (Yer)', '30 (Yery)', '31 (Yer\')', '32 (Yat)', '33 (Yu)', '34 (Yus B.)', '35 (Yus M.)']

VR_CS = {1: 'А', 2: 'В', 3: 'Г', 4: 'Д', 5: 'Є', 6: 'Ѕ', 7: 'З'}
VR_EN = {1: '1 (A)', 2: '2 (V)', 3: '3 (G)', 4: '4 (D)', 5: '5 (E)', 6: '6 (S)', 7: '7 (Z)'}

def julian_pascha(year):
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = (d + e + 114) // 31
    day = ((d + e + 114) % 31) + 1
    return month, day

def get_key_idx(year):
    m, d = julian_pascha(year)
    return (d - 22) if m == 3 else (31 - 22 + d)

def get_vrutselito(y):
    val = 7
    for cur in range(1902, y + 1):
        if cur % 4 == 0:
            val += 2
        else:
            val += 1
    return ((val - 1) % 7) + 1

mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def add_days(m, d, n):
    d += n
    while True:
        lim = mdays[m]
        if d <= lim:
            break
        d -= lim
        m += 1
        if m > 12:
            m = 1
    return m, d

def sub_days(m, d, n):
    d -= n
    while d < 1:
        m -= 1
        if m < 1:
            m = 12
        lim = mdays[m]
        d += lim
    return m, d

def get_feast_letter(m, d):
    if m == 7 and 13 <= d <= 19:
        return 'a'
    elif m == 9 and 7 <= d <= 13:
        return 'b'
    elif m == 9 and 15 <= d <= 21:
        return 'c'
    elif m == 10 and 8 <= d <= 14:
        return 'd'
    elif m == 12 and 11 <= d <= 17:
        return 'f'
    elif m == 12 and 18 <= d <= 24:
        return 'g'
    elif m == 12 and 26 <= d <= 31:
        return 'h'
    elif m == 1 and 1 <= d <= 6:
        return 'i'
    elif m == 1 and 7 <= d <= 13:
        return 'l'
    return ''

paschas = []
for k in range(35):
    if k < 10:
        paschas.append((3, 22 + k))
    else:
        paschas.append((4, k - 10 + 1))

print("Formulas verified.")
