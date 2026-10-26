# -*- coding: utf-8 -*-
"""
Full Cohort 29 Generator & Verification Script
Monument: Typik of Fr. Isidore Dolnytsky (Lviv Stauropegion, 1899)
Leaves: p561 to p580
"""

import sys
import subprocess
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT_ROOT / "Liturgical Monuments" / "1899 Dolnytsky Typikon"

SOURCE_OUT = WORKSPACE / "Source Text" / "1899_dolnytsky_typikon_cohort29_source.txt"
DRAFT_OUT = WORKSPACE / "Draft" / "1899_dolnytsky_typikon_cohort29_raw_draft.md"
FOOTNOTES_OUT = WORKSPACE / "Draft" / "1899_dolnytsky_typikon_cohort29_footnotes.txt"

# -------------------------------------------------------------
# Footnotes Content
# -------------------------------------------------------------
FOOTNOTES_CONTENT = """[^741]: See note 1 on page 427.
[^742]: The difference is revealed by adding 13 days to the Greek Pascha.
[^743]: Only the Gospel of the 28th Sunday, if it occurs before or after the Forefathers, we leave for the Sunday of the Forefathers, and on the 28th we read the ordinary one of the Forefathers alone.
"""

# -------------------------------------------------------------
# Keys & Calendrical Utilities
# -------------------------------------------------------------
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

paschas = []
for k in range(35):
    if k < 10:
        paschas.append((3, 22 + k))
    else:
        paschas.append((4, k - 9))

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

def make_pascha_diff_cs():
    diffs = [
        (1901, "А҆. 7", "А҆. 1", "Є҆ м҃ц. 1", 1921, "М. 27", "А҆. 18", "Є҆ м҃ц. 1"),
        (1902, "М. 30", "А҆. 14", "4", 1922, "А҆. 16", "А҆. 3", "5"),
        (1903, "А҆. 12", "А҆. 6", "1", 1923, "А҆. 1", "М. 26", "0"),
        (1904, "А҆. 3", "М. 28", "1", 1924, "А҆. 20", "А҆. 14", "1"),
        (1905, "А҆. 23", "А҆. 17", "1", 1925, "А҆. 12", "А҆. 6", "1"),
        (1906, "А҆. 15", "А҆. 2", "0", 1926, "А҆. 4", "А҆. 19", "4"),
        (1907, "М. 31", "А҆. 22", "5", 1927, "А҆. 17", "А҆. 11", "1"),
        (1908, "А҆. 19", "А҆. 13", "1", 1928, "А҆. 8", "А҆. 2", "1"),
        (1909, "А҆. 11", "М. 29", "0", 1929, "М. 31", "А҆. 22", "5"),
        (1910, "М. 27", "А҆. 18", "5", 1930, "А҆. 20", "А҆. 7", "1"),
        (1911, "А҆. 16", "А҆. 10", "1", 1931, "А҆. 5", "М. 30", "1"),
        (1912, "А҆. 7", "М. 25", "0", 1932, "М. 27", "А҆. 18", "5"),
        (1913, "М. 23", "А҆. 14", "5", 1933, "А҆. 16", "А҆. 3", "0"),
        (1914, "А҆. 12", "А҆. 6", "1", 1934, "А҆. 1", "М. 26", "1"),
        (1915, "А҆. 4", "М. 22", "0", 1935, "А҆. 21", "М. 15", "1"),
        (1916, "А҆. 23", "А҆. 10", "0", 1936, "А҆. 12", "М. 30", "0"),
        (1917, "А҆. 8", "А҆. 2", "1", 1937, "М. 28", "А҆. 19", "5"),
        (1918, "М. 31", "А҆. 22", "5", 1938, "А҆. 17", "А҆. 11", "1"),
        (1919, "А҆. 20", "А҆. 7", "0", 1939, "А҆. 9", "М. 27", "0"),
        (1920, "А҆. 4", "М. 29", "1", 1940, "М. 24", "А҆. 15", "5")
    ]
    lines = [
        "| Лѣ́та | Ри́мск. | Гре́ч. | Разли́ч. | Лѣ́та | Ри́мск. | Гре́ч. | Разли́ч. |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    for y1, r1, g1, d1, y2, r2, g2, d2 in diffs:
        c1 = f"*{y1}* | *{r1}* | *{g1}* | *{d1}*" if y1 % 4 == 0 else f"{y1} | {r1} | {g1} | {d1}"
        c2 = f"*{y2}* | *{r2}* | *{g2}* | *{d2}*" if y2 % 4 == 0 else f"{y2} | {r2} | {g2} | {d2}"
        lines.append(f"| {c1} | {c2} |")
    return "\n".join(lines)

def make_pascha_diff_en():
    diffs = [
        (1901, "Apr. 7", "Apr. 1", "5 [1 mo.]", 1921, "Mar. 27", "Apr. 18", "5 [1 mo.]"),
        (1902, "Mar. 30", "Apr. 14", "4", 1922, "Apr. 16", "Apr. 3", "5"),
        (1903, "Apr. 12", "Apr. 6", "1", 1923, "Apr. 1", "Mar. 26", "0"),
        (1904, "Apr. 3", "Mar. 28", "1", 1924, "Apr. 20", "Apr. 14", "1"),
        (1905, "Apr. 23", "Apr. 17", "1", 1925, "Apr. 12", "Apr. 6", "1"),
        (1906, "Apr. 15", "Apr. 2", "0", 1926, "Apr. 4", "Apr. 19", "4"),
        (1907, "Mar. 31", "Apr. 22", "5", 1927, "Apr. 17", "Apr. 11", "1"),
        (1908, "Apr. 19", "Apr. 13", "1", 1928, "Apr. 8", "Apr. 2", "1"),
        (1909, "Apr. 11", "Mar. 29", "0", 1929, "Mar. 31", "Apr. 22", "5"),
        (1910, "Mar. 27", "Apr. 18", "5", 1930, "Apr. 20", "Apr. 7", "1"),
        (1911, "Apr. 16", "Apr. 10", "1", 1931, "Apr. 5", "Mar. 30", "1"),
        (1912, "Apr. 7", "Mar. 25", "0", 1932, "Mar. 27", "Apr. 18", "5"),
        (1913, "Mar. 23", "Apr. 14", "5", 1933, "Apr. 16", "Apr. 3", "0"),
        (1914, "Apr. 12", "Apr. 6", "1", 1934, "Apr. 1", "Mar. 26", "1"),
        (1915, "Apr. 4", "Mar. 22", "0", 1935, "Apr. 21", "Mar. 15", "1"),
        (1916, "Apr. 23", "Apr. 10", "0", 1936, "Apr. 12", "Mar. 30", "0"),
        (1917, "Apr. 8", "Apr. 2", "1", 1937, "Mar. 28", "Apr. 19", "5"),
        (1918, "Mar. 31", "Apr. 22", "5", 1938, "Apr. 17", "Apr. 11", "1"),
        (1919, "Apr. 20", "Apr. 7", "0", 1939, "Apr. 9", "Mar. 27", "0"),
        (1920, "Apr. 4", "Mar. 29", "1", 1940, "Mar. 24", "Apr. 15", "5")
    ]
    lines = [
        "| Year | Roman | Greek | Difference (weeks) | Year | Roman | Greek | Difference (weeks) |",
        "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    for y1, r1, g1, d1, y2, r2, g2, d2 in diffs:
        c1 = f"*{y1}* | *{r1}* | *{g1}* | *{d1}*" if y1 % 4 == 0 else f"{y1} | {r1} | {g1} | {d1}"
        c2 = f"*{y2}* | *{r2}* | *{g2}* | *{d2}*" if y2 % 4 == 0 else f"{y2} | {r2} | {g2} | {d2}"
        lines.append(f"| {c1} | {c2} |")
    return "\n".join(lines)

# -------------------------------------------------------------
# Table III Helper Logic
# -------------------------------------------------------------
TONES_PENTECOST = [8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7]
GOSPELS_PENTECOST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

TONES_CS = ['а҃', 'в҃', 'г҃', 'д҃', 'є҃', 'ѕ҃', 'з҃', 'и҃']
GOSPELS_CS = ['а҃', 'в҃', 'г҃', 'д҃', 'є҃', 'ѕ҃', 'з҃', 'и҃', 'ѳ҃', 'і҃', 'а҃і']

def make_table3_p576_cs():
    lines = [
        "### Ча́сть 1: Столпы̀ 1–21 (А–У)",
        "| Мѣ́сяцъ | А | Б | В | Г | Д | Є | Ж | Ѕ | З | И | І | К | Л | М | Н | О | П | Р | С | Т | У | Недѣ́ля |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    # Row 1: Epiphany
    lines.append("| І҆анꙋа́рїй | | | | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 7 | 8 | 9 | 10 | По Просвѣ́щ. |")
    # Row 2: 29
    lines.append("| | | | | | | | | | | | | | | | | | | 14 | 15 | 16 | 17 | Ряд. кѳ҃. |")
    # Row 3: 30
    lines.append("| | | | | | | | | | | | | | | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | ” л҃. |")
    # Row 4: 31
    lines.append("| | | | | | | | | | | | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | ” ла҃. |")
    # Row 5: 32
    lines.append("| | | | | | | | | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | ” лв҃. |")
    # Row 6: Publican
    lines.append("| | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | Мытар. |")
    # Row 7: Pascha (March/April)
    pascha_cells = []
    for k in range(21):
        m, d = paschas[k]
        pascha_cells.append(f"*{d}*")
    lines.append(f"| Ма́ртъ / А҆прі́л. | {' | '.join(pascha_cells)} | *Па́схи.* |")
    # Rows 8-18: Sundays 1 to 11
    for n in range(1, 12):
        row_cells = []
        for k in range(21):
            pm, pd = paschas[k]
            sm, sd = add_days(pm, pd, 7 * (n + 7))
            row_cells.append(str(sd))
        t_cs = TONES_CS[TONES_PENTECOST[n - 1] - 1]
        g_cs = GOSPELS_CS[GOSPELS_PENTECOST[n - 1] - 1]
        lines.append(f"| | {' | '.join(row_cells)} | {n}-я по Сош. (Гл. {t_cs}, Є҆ѵл. {g_cs}) |")

    lines.append("\n### Ча́сть 2: Столпы̀ 22–35 (Ф–Ѧ) съ рядовы́ми оу҆каза́нїями")
    lines.append("| Ф | Х | Ѡ | Ц | Ч | Ш | Щ | Ъ | Ы | Ь | Ѣ | Ю | Ѫ | Ѧ | Недѣ́ли По Просвѣ́щ. / По Сош. | Гла́съ | Є҆ѵл. воскр. |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    lines.append("| 11 | 12 | 13 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 7 | 8 | 9 | 10 | По Просвѣ́щ. | | |")
    lines.append("| | | | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 14 | 15 | 16 | 17 | Ряд. кѳ҃. | | |")
    lines.append("| 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 21 | 22 | 23 | 24 | ” л҃. | | |")
    lines.append("| 25 | 26 | 27 | 28 | 29 | 30 | 31 | 1 | 2 | 3 | 28 | 29 | 30 | 31 | ” ла҃. | | |")
    lines.append("| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 4 | 5 | 6 | 7 | ” лв҃. | | |")
    lines.append("| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | Мытар. | | |")
    pascha_cells_r = [f"*{paschas[k][1]}*" for k in range(21, 35)]
    lines.append(f"| {' | '.join(pascha_cells_r)} | *Па́схи.* | | |")
    for n in range(1, 12):
        row_cells = [str(add_days(paschas[k][0], paschas[k][1], 7 * (n + 7))[1]) for k in range(21, 35)]
        t_cs = TONES_CS[TONES_PENTECOST[n - 1] - 1]
        g_cs = GOSPELS_CS[GOSPELS_PENTECOST[n - 1] - 1]
        lbl = "а҃. Всѣ́хъ Ст҃ы́хъ" if n == 1 else f"{n}."
        lines.append(f"| {' | '.join(row_cells)} | {lbl} | {t_cs} | {g_cs} |")
    return "\n".join(lines)

def make_table3_p576_en():
    lines = [
        "### Part 1: Columns 1–21 (Keys 1 to 21: A to U)",
        "| Month | 1 (A) | 2 (B) | 3 (V) | 4 (G) | 5 (D) | 6 (E) | 7 (Zh) | 8 (S) | 9 (Z) | 10 (I) | 11 (I) | 12 (K) | 13 (L) | 14 (M) | 15 (N) | 16 (O) | 17 (P) | 18 (R) | 19 (S) | 20 (T) | 21 (U) | Sunday Title |",
        "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    lines.append("| January | | | | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 7 | 8 | 9 | 10 | After Enlightenment |")
    lines.append("| | | | | | | | | | | | | | | | | | | 14 | 15 | 16 | 17 | 29th Ordinary |")
    lines.append("| | | | | | | | | | | | | | | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 30th Ordinary |")
    lines.append("| | | | | | | | | | | | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 31st Ordinary |")
    lines.append("| | | | | | | | | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 32nd Ordinary |")
    lines.append("| | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | Publican & Pharisee |")
    pascha_cells = [f"*{paschas[k][1]}*" for k in range(21)]
    lines.append(f"| March / April | {' | '.join(pascha_cells)} | *Pascha* |")
    for n in range(1, 12):
        row_cells = [str(add_days(paschas[k][0], paschas[k][1], 7 * (n + 7))[1]) for k in range(21)]
        t = TONES_PENTECOST[n - 1]
        g = GOSPELS_PENTECOST[n - 1]
        lines.append(f"| | {' | '.join(row_cells)} | {n} after Pentecost (Tone {t}, Gospel {g}) |")

    lines.append("\n### Part 2: Columns 22–35 (Keys 22 to 35: F to Yus M.) with Ordinary Indicators")
    lines.append("| 22 (F) | 23 (Kh) | 24 (O) | 25 (Ts) | 26 (Ch) | 27 (Sh) | 28 (Shch) | 29 (Yer) | 30 (Yery) | 31 (Yer') | 32 (Yat) | 33 (Yu) | 34 (Yus B.) | 35 (Yus M.) | Sunday Title | Tone | Gospel |")
    lines.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    lines.append("| 11 | 12 | 13 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 7 | 8 | 9 | 10 | After Enlightenment | | |")
    lines.append("| | | | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 14 | 15 | 16 | 17 | 29th Ordinary | | |")
    lines.append("| 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 21 | 22 | 23 | 24 | 30th Ordinary | | |")
    lines.append("| 25 | 26 | 27 | 28 | 29 | 30 | 31 | 1 | 2 | 3 | 28 | 29 | 30 | 31 | 31st Ordinary | | |")
    lines.append("| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 4 | 5 | 6 | 7 | 32nd Ordinary | | |")
    lines.append("| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | Publican & Pharisee | | |")
    pascha_cells_r = [f"*{paschas[k][1]}*" for k in range(21, 35)]
    lines.append(f"| {' | '.join(pascha_cells_r)} | *Pascha* | | |")
    for n in range(1, 12):
        row_cells = [str(add_days(paschas[k][0], paschas[k][1], 7 * (n + 7))[1]) for k in range(21, 35)]
        t = TONES_PENTECOST[n - 1]
        g = GOSPELS_PENTECOST[n - 1]
        lbl = "1. All Saints" if n == 1 else f"{n}."
        lines.append(f"| {' | '.join(row_cells)} | {lbl} | Tone {t} | Gospel {g} |")
    return "\n".join(lines)

def make_table3_p577_cs():
    lines = [
        "### Ча́сть 1: Столпы̀ 1–21 (Недѣ́ли 12–29 по Соше́ствїи)",
        "| Мѣ́сяцъ | А | Б | В | Г | Д | Є | Ж | Ѕ | З | И | І | К | Л | М | Н | О | П | Р | С | Т | У | Недѣ́ля |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    for n in range(12, 30):
        row_cells = []
        for k in range(21):
            pm, pd = paschas[k]
            sm, sd = add_days(pm, pd, 7 * (n + 7))
            row_cells.append(str(sd))
        t_cs = TONES_CS[TONES_PENTECOST[n - 1] - 1]
        g_cs = GOSPELS_CS[GOSPELS_PENTECOST[n - 1] - 1]
        lines.append(f"| | {' | '.join(row_cells)} | {n}-я по Сош. (Гл. {t_cs}, Є҆ѵл. {g_cs}) |")

    lines.append("\n### Ча́сть 2: Столпы̀ 22–35 (Недѣ́ли 12–29 по Соше́ствїи)")
    lines.append("| Ф | Х | Ѡ | Ц | Ч | Ш | Щ | Ъ | Ы | Ь | Ѣ | Ю | Ѫ | Ѧ | Недѣ́ля | Гла́съ | Є҆ѵл. воскр. |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for n in range(12, 30):
        row_cells = [str(add_days(paschas[k][0], paschas[k][1], 7 * (n + 7))[1]) for k in range(21, 35)]
        t_cs = TONES_CS[TONES_PENTECOST[n - 1] - 1]
        g_cs = GOSPELS_CS[GOSPELS_PENTECOST[n - 1] - 1]
        lines.append(f"| {' | '.join(row_cells)} | {n}. | {t_cs} | {g_cs} |")
    return "\n".join(lines)

def make_table3_p577_en():
    lines = [
        "### Part 1: Columns 1–21 (Sundays 12 to 29 after Pentecost)",
        "| Month | 1 (A) | 2 (B) | 3 (V) | 4 (G) | 5 (D) | 6 (E) | 7 (Zh) | 8 (S) | 9 (Z) | 10 (I) | 11 (I) | 12 (K) | 13 (L) | 14 (M) | 15 (N) | 16 (O) | 17 (P) | 18 (R) | 19 (S) | 20 (T) | 21 (U) | Sunday Title |",
        "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    for n in range(12, 30):
        row_cells = [str(add_days(paschas[k][0], paschas[k][1], 7 * (n + 7))[1]) for k in range(21)]
        t = TONES_PENTECOST[n - 1]
        g = GOSPELS_PENTECOST[n - 1]
        lines.append(f"| | {' | '.join(row_cells)} | {n} after Pentecost (Tone {t}, Gospel {g}) |")

    lines.append("\n### Part 2: Columns 22–35 (Sundays 12 to 29 after Pentecost)")
    lines.append("| 22 (F) | 23 (Kh) | 24 (O) | 25 (Ts) | 26 (Ch) | 27 (Sh) | 28 (Shch) | 29 (Yer) | 30 (Yery) | 31 (Yer') | 32 (Yat) | 33 (Yu) | 34 (Yus B.) | 35 (Yus M.) | Sunday | Tone | Gospel |")
    lines.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for n in range(12, 30):
        row_cells = [str(add_days(paschas[k][0], paschas[k][1], 7 * (n + 7))[1]) for k in range(21, 35)]
        t = TONES_PENTECOST[n - 1]
        g = GOSPELS_PENTECOST[n - 1]
        lines.append(f"| {' | '.join(row_cells)} | {n}. | Tone {t} | Gospel {g} |")
    return "\n".join(lines)

def make_table3_p578_cs():
    lines = [
        "### Ча́сть 1: Столпы̀ 1–21 (Недѣ́ли 30–32, Предпо́стныя Недѣ́ли, Февра́ль)",
        "| Мѣ́сяцъ | А | Б | В | Г | Д | Є | Ж | Ѕ | З | И | І | К | Л | М | Н | О | П | Р | С | Т | У | Недѣ́ля |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    # Sundays 30 to 32
    for n in range(30, 33):
        row_cells = [str(add_days(paschas[k][0], paschas[k][1], 7 * (n + 7))[1]) for k in range(21)]
        t_cs = TONES_CS[TONES_PENTECOST[n - 1] - 1]
        g_cs = GOSPELS_CS[GOSPELS_PENTECOST[n - 1] - 1]
        lines.append(f"| | {' | '.join(row_cells)} | {n}-я по Сош. (Гл. {t_cs}, Є҆ѵл. {g_cs}) |")

    # 11 Pre-Lenten / Epiphany rows (arithmetic progression base_d + k)
    pre_lenten_cs_labels = [
        ("Дек. / І҆ан.", [27, 28, 29, 30, 31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], "Н. (Гл. и҃, Є҆ѵл. а҃і)"),
        ("І҆анꙋа́рїй", [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "Н. (Гл. а҃, Є҆ѵл. а҃)"),
        ("І҆анꙋа́рїй", [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], "Н. (Гл. в҃, Є҆ѵл. в҃)"),
        ("І҆ан. / Февр.", [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 1, 2, 3, 4, 5, 6], "Н. (Гл. г҃, Є҆ѵл. г҃)"),
        ("І҆ан. / Февр.", [24, 25, 26, 27, 28, 29, 30, 31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "Н. (Гл. д҃, Є҆ѵл. д҃)"),
        ("І҆ан. / Февр.", [31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "Н. (Гл. є҃, Є҆ѵл. є҃)"),
        ("Февра́рь", [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], "Н. (Гл. ѕ҃, Є҆ѵл. ѕ҃)"),
        ("Февр. / Ма́ртъ", [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 1, 2, 3, 4, 5, 6], "Н. (Гл. з҃, Є҆ѵл. з҃)"),
        ("Февр. / Ма́ртъ", [21, 22, 23, 24, 25, 26, 27, 28, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "Н. (Гл. и҃, Є҆ѵл. а҃і)"),
        ("Февр. / Ма́ртъ", [28, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "Н. (Гл. а҃, Є҆ѵл. ѳ҃)"),
        ("Ма́ртъ", [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], "Н. (Гл. в҃, Є҆ѵл. і҃)")
    ]
    for m_lbl, vals, n_lbl in pre_lenten_cs_labels:
        row_str = " | ".join(str(v) for v in vals)
        lines.append(f"| {m_lbl} | {row_str} | {n_lbl} |")

    # February indicator row
    febr_left = [0, 2, 3, 4, 5, 5, 6, 5, 6, 5, 6, 7, 8, 5, 6, 7, 8, 9, 9, 9, 9]
    lines.append(f"| Февра́рь | {' | '.join(str(v) for v in febr_left)} | Клю́чь Февраля̀ |")

    lines.append("\n### Ча́сть 2: Столпы̀ 22–35 (Недѣ́ли 30–32, Предпо́стныя Недѣ́ли, Февра́ль)")
    lines.append("| Ф | Х | Ѡ | Ц | Ч | Ш | Щ | Ъ | Ы | Ь | Ѣ | Ю | Ѫ | Ѧ | Недѣ́ля | Гла́съ | Є҆ѵл. воскр. |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for n in range(30, 33):
        row_cells = [str(add_days(paschas[k][0], paschas[k][1], 7 * (n + 7))[1]) for k in range(21, 35)]
        t_cs = TONES_CS[TONES_PENTECOST[n - 1] - 1]
        g_cs = GOSPELS_CS[GOSPELS_PENTECOST[n - 1] - 1]
        lines.append(f"| {' | '.join(row_cells)} | {n}. | {t_cs} | {g_cs} |")

    pre_lenten_cs_right = [
        ([17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], "Н.", "и҃.", "а҃і."),
        ([24, 25, 26, 27, 28, 29, 30, 31, 1, 2, 3, 4, 5, 6], "Н.", "а҃.", "а҃."),
        ([31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "Н.", "в҃.", "в҃."),
        ([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "Н.", "г҃.", "г҃."),
        ([14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], "Н.", "д҃.", "д҃."),
        ([21, 22, 23, 24, 25, 26, 27, 28, 1, 2, 3, 4, 5, 6], "Н.", "є҃.", "є҃."),
        ([28, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "Н.", "ѕ҃.", "ѕ҃."),
        ([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "Н.", "з҃.", "з҃."),
        ([14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], "Н.", "и҃.", "а҃і."),
        ([21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 1, 2, 3], "Н.", "а҃.", "ѳ҃."),
        ([28, 29, 30, 31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "Н.", "в҃.", "і҃.")
    ]
    for vals, lbl, t_cs, g_cs in pre_lenten_cs_right:
        row_str = " | ".join(str(v) for v in vals)
        lines.append(f"| {row_str} | {lbl} | {t_cs} | {g_cs} |")

    febr_right = [9] * 14
    lines.append(f"| {' | '.join(str(v) for v in febr_right)} | Ѿда́н. Срѣ́т. | | |")
    return "\n".join(lines)

def make_table3_p578_en():
    lines = [
        "### Part 1: Columns 1–21 (Sundays 30 to 32, Pre-Lenten Cycle, February)",
        "| Month | 1 (A) | 2 (B) | 3 (V) | 4 (G) | 5 (D) | 6 (E) | 7 (Zh) | 8 (S) | 9 (Z) | 10 (I) | 11 (I) | 12 (K) | 13 (L) | 14 (M) | 15 (N) | 16 (O) | 17 (P) | 18 (R) | 19 (S) | 20 (T) | 21 (U) | Sunday Title |",
        "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    for n in range(30, 33):
        row_cells = [str(add_days(paschas[k][0], paschas[k][1], 7 * (n + 7))[1]) for k in range(21)]
        t = TONES_PENTECOST[n - 1]
        g = GOSPELS_PENTECOST[n - 1]
        lines.append(f"| | {' | '.join(row_cells)} | {n} after Pentecost (Tone {t}, Gospel {g}) |")

    pre_lenten_en_labels = [
        ("Dec. / Jan.", [27, 28, 29, 30, 31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], "Sunday (Tone 8, Gospel 11)"),
        ("January", [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "Sunday (Tone 1, Gospel 1)"),
        ("January", [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], "Sunday (Tone 2, Gospel 2)"),
        ("Jan. / Feb.", [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 1, 2, 3, 4, 5, 6], "Sunday (Tone 3, Gospel 3)"),
        ("Jan. / Feb.", [24, 25, 26, 27, 28, 29, 30, 31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "Sunday (Tone 4, Gospel 4)"),
        ("Jan. / Feb.", [31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "Sunday (Tone 5, Gospel 5)"),
        ("February", [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], "Sunday (Tone 6, Gospel 6)"),
        ("Feb. / March", [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 1, 2, 3, 4, 5, 6], "Sunday (Tone 7, Gospel 7)"),
        ("Feb. / March", [21, 22, 23, 24, 25, 26, 27, 28, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "Sunday (Tone 8, Gospel 11)"),
        ("Feb. / March", [28, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "Sunday (Tone 1, Gospel 9)"),
        ("March", [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], "Sunday (Tone 2, Gospel 10)")
    ]
    for m_lbl, vals, n_lbl in pre_lenten_en_labels:
        row_str = " | ".join(str(v) for v in vals)
        lines.append(f"| {m_lbl} | {row_str} | {n_lbl} |")

    febr_left = [0, 2, 3, 4, 5, 5, 6, 5, 6, 5, 6, 7, 8, 5, 6, 7, 8, 9, 9, 9, 9]
    lines.append(f"| February | {' | '.join(str(v) for v in febr_left)} | February Key Indicator |")

    lines.append("\n### Part 2: Columns 22–35 (Sundays 30 to 32, Pre-Lenten Cycle, February)")
    lines.append("| 22 (F) | 23 (Kh) | 24 (O) | 25 (Ts) | 26 (Ch) | 27 (Sh) | 28 (Shch) | 29 (Yer) | 30 (Yery) | 31 (Yer') | 32 (Yat) | 33 (Yu) | 34 (Yus B.) | 35 (Yus M.) | Sunday | Tone | Gospel |")
    lines.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for n in range(30, 33):
        row_cells = [str(add_days(paschas[k][0], paschas[k][1], 7 * (n + 7))[1]) for k in range(21, 35)]
        t = TONES_PENTECOST[n - 1]
        g = GOSPELS_PENTECOST[n - 1]
        lines.append(f"| {' | '.join(row_cells)} | {n}. | Tone {t} | Gospel {g} |")

    pre_lenten_en_right = [
        ([17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], "Sunday", "Tone 8", "Gospel 11"),
        ([24, 25, 26, 27, 28, 29, 30, 31, 1, 2, 3, 4, 5, 6], "Sunday", "Tone 1", "Gospel 1"),
        ([31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "Sunday", "Tone 2", "Gospel 2"),
        ([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "Sunday", "Tone 3", "Gospel 3"),
        ([14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], "Sunday", "Tone 4", "Gospel 4"),
        ([21, 22, 23, 24, 25, 26, 27, 28, 1, 2, 3, 4, 5, 6], "Sunday", "Tone 5", "Gospel 5"),
        ([28, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "Sunday", "Tone 6", "Gospel 6"),
        ([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "Sunday", "Tone 7", "Gospel 7"),
        ([14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], "Sunday", "Tone 8", "Gospel 11"),
        ([21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 1, 2, 3], "Sunday", "Tone 1", "Gospel 9"),
        ([28, 29, 30, 31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "Sunday", "Tone 2", "Gospel 10")
    ]
    for vals, lbl, t, g in pre_lenten_en_right:
        row_str = " | ".join(str(v) for v in vals)
        lines.append(f"| {row_str} | {lbl} | {t} | {g} |")

    febr_right = [9] * 14
    lines.append(f"| {' | '.join(str(v) for v in febr_right)} | Apodosis of the Meeting | | |")
    return "\n".join(lines)

print("Table III functions built successfully.")
