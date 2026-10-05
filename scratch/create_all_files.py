# -*- coding: utf-8 -*-
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = PROJECT_ROOT / "Typikons" / "1899 Dolnytsky Typikon" / "Source Text" / "1899_dolnytsky_typikon_cohort29_source.txt"
DRAFT_PATH = PROJECT_ROOT / "Typikons" / "1899 Dolnytsky Typikon" / "Draft" / "1899_dolnytsky_typikon_cohort29_raw_draft.md"
FOOTNOTES_PATH = PROJECT_ROOT / "Typikons" / "1899 Dolnytsky Typikon" / "Draft" / "1899_dolnytsky_typikon_cohort29_footnotes.txt"

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

def make_table1_cs():
    lines = [
        "| Лѣ́та Хр. | Врꙋцѣлѣ́то | Клю́чь Гран. | Лѣ́та Хр. | Врꙋцѣлѣ́то | Клю́чь Гран. | Лѣ́та Хр. | Врꙋцѣлѣ́то | Клю́чь Гран. |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    for r in range(16):
        y1 = 1901 + r
        y2 = 1917 + r
        y3 = 1933 + r if r < 8 else None
        c1 = f"*{y1}* | *{VR_CS[get_vrutselito(y1)]}* | *{KEYS_CS[get_key_idx(y1)]}*" if y1 % 4 == 0 else f"{y1} | {VR_CS[get_vrutselito(y1)]} | {KEYS_CS[get_key_idx(y1)]}"
        c2 = f"*{y2}* | *{VR_CS[get_vrutselito(y2)]}* | *{KEYS_CS[get_key_idx(y2)]}*" if y2 % 4 == 0 else f"{y2} | {VR_CS[get_vrutselito(y2)]} | {KEYS_CS[get_key_idx(y2)]}"
        if y3:
            c3 = f"*{y3}* | *{VR_CS[get_vrutselito(y3)]}* | *{KEYS_CS[get_key_idx(y3)]}*" if y3 % 4 == 0 else f"{y3} | {VR_CS[get_vrutselito(y3)]} | {KEYS_CS[get_key_idx(y3)]}"
        else:
            c3 = " | | "
        lines.append(f"| {c1} | {c2} | {c3} |")
    return "\n".join(lines)

def make_table1_en():
    lines = [
        "| Year A.D. | Dominical Letter | Boundary Key | Year A.D. | Dominical Letter | Boundary Key | Year A.D. | Dominical Letter | Boundary Key |",
        "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    for r in range(16):
        y1 = 1901 + r
        y2 = 1917 + r
        y3 = 1933 + r if r < 8 else None
        c1 = f"*{y1}* | *{VR_EN[get_vrutselito(y1)]}* | *{KEYS_EN[get_key_idx(y1)]}*" if y1 % 4 == 0 else f"{y1} | {VR_EN[get_vrutselito(y1)]} | {KEYS_EN[get_key_idx(y1)]}"
        c2 = f"*{y2}* | *{VR_EN[get_vrutselito(y2)]}* | *{KEYS_EN[get_key_idx(y2)]}*" if y2 % 4 == 0 else f"{y2} | {VR_EN[get_vrutselito(y2)]} | {KEYS_EN[get_key_idx(y2)]}"
        if y3:
            c3 = f"*{y3}* | *{VR_EN[get_vrutselito(y3)]}* | *{KEYS_EN[get_key_idx(y3)]}*" if y3 % 4 == 0 else f"{y3} | {VR_EN[get_vrutselito(y3)]} | {KEYS_EN[get_key_idx(y3)]}"
        else:
            c3 = " | | "
        lines.append(f"| {c1} | {c2} | {c3} |")
    return "\n".join(lines)

def make_table2_page_cs(start_yr, rows, col3_rows=None):
    if col3_rows is None:
        col3_rows = rows
    lines = [
        "| Лѣ́та Хр. | Врꙋцѣлѣ́то | Клю́чь Гран. | Лѣ́та Хр. | Врꙋцѣлѣ́то | Клю́чь Гран. | Лѣ́та Хр. | Врꙋцѣлѣ́то | Клю́чь Гран. |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    for r in range(rows):
        y1 = start_yr + r
        y2 = start_yr + rows + r
        y3 = start_yr + 2 * rows + r if r < col3_rows else None
        def fmt_yr(y):
            if y == 2406:
                return "2405 [2406]"
            return str(y)
        c1 = f"*{fmt_yr(y1)}* | *{VR_CS[get_vrutselito(y1)]}* | *{KEYS_CS[get_key_idx(y1)]}*" if y1 % 4 == 0 else f"{fmt_yr(y1)} | {VR_CS[get_vrutselito(y1)]} | {KEYS_CS[get_key_idx(y1)]}"
        c2 = f"*{fmt_yr(y2)}* | *{VR_CS[get_vrutselito(y2)]}* | *{KEYS_CS[get_key_idx(y2)]}*" if y2 % 4 == 0 else f"{fmt_yr(y2)} | {VR_CS[get_vrutselito(y2)]} | {KEYS_CS[get_key_idx(y2)]}"
        if y3:
            c3 = f"*{fmt_yr(y3)}* | *{VR_CS[get_vrutselito(y3)]}* | *{KEYS_CS[get_key_idx(y3)]}*" if y3 % 4 == 0 else f"{fmt_yr(y3)} | {VR_CS[get_vrutselito(y3)]} | {KEYS_CS[get_key_idx(y3)]}"
        else:
            c3 = " | | "
        lines.append(f"| {c1} | {c2} | {c3} |")
    return "\n".join(lines)

def make_table2_page_en(start_yr, rows, col3_rows=None):
    if col3_rows is None:
        col3_rows = rows
    lines = [
        "| Year A.D. | Dominical Letter | Boundary Key | Year A.D. | Dominical Letter | Boundary Key | Year A.D. | Dominical Letter | Boundary Key |",
        "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    for r in range(rows):
        y1 = start_yr + r
        y2 = start_yr + rows + r
        y3 = start_yr + 2 * rows + r if r < col3_rows else None
        def fmt_yr(y):
            if y == 2406:
                return "2405 [2406]"
            return str(y)
        c1 = f"*{fmt_yr(y1)}* | *{VR_EN[get_vrutselito(y1)]}* | *{KEYS_EN[get_key_idx(y1)]}*" if y1 % 4 == 0 else f"{fmt_yr(y1)} | {VR_EN[get_vrutselito(y1)]} | {KEYS_EN[get_key_idx(y1)]}"
        c2 = f"*{fmt_yr(y2)}* | *{VR_EN[get_vrutselito(y2)]}* | *{KEYS_EN[get_key_idx(y2)]}*" if y2 % 4 == 0 else f"{fmt_yr(y2)} | {VR_EN[get_vrutselito(y2)]} | {KEYS_EN[get_key_idx(y2)]}"
        if y3:
            c3 = f"*{fmt_yr(y3)}* | *{VR_EN[get_vrutselito(y3)]}* | *{KEYS_EN[get_key_idx(y3)]}*" if y3 % 4 == 0 else f"{fmt_yr(y3)} | {VR_EN[get_vrutselito(y3)]} | {KEYS_EN[get_key_idx(y3)]}"
        else:
            c3 = " | | "
        lines.append(f"| {c1} | {c2} | {c3} |")
    return "\n".join(lines)

print("Table helper functions defined.")
