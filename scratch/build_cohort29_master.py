# -*- coding: utf-8 -*-
"""
Master Builder for Cohort 29 (Leaves p561 to p580)
Monument: Typik of Fr. Isidore Dolnytsky (Lviv Stauropegion, 1899)
"""

import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT_ROOT / "Typikons" / "1899 Dolnytsky Typikon"

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
# Tables I & II Helper Logic
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

print("Tables helper loaded successfully.")
