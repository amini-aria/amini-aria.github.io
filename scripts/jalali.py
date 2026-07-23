# -*- coding: utf-8 -*-
"""
Minimal, dependency-free Gregorian -> Jalali (Persian) calendar conversion,
plus helpers for Persian month names and Eastern Arabic-Indic digits.
Algorithm: standard Jalali conversion (based on the well-known public
"jdf.js" / Kazimierz Borkowski algorithm), no external packages needed.
"""

PERSIAN_MONTHS = [
    "\u0641\u0631\u0648\u0631\u062f\u06cc\u0646", "\u0627\u0631\u062f\u06cc\u0628\u0647\u0634\u062a", "\u062e\u0631\u062f\u0627\u062f",
    "\u062a\u06cc\u0631", "\u0645\u0631\u062f\u0627\u062f", "\u0634\u0647\u0631\u06cc\u0648\u0631",
    "\u0645\u0647\u0631", "\u0622\u0628\u0627\u0646", "\u0622\u0630\u0631",
    "\u062f\u06cc", "\u0628\u0647\u0645\u0646", "\u0627\u0633\u0641\u0646\u062f",
]

_PERSIAN_DIGITS = "\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9"


def to_persian_digits(s):
    return "".join(_PERSIAN_DIGITS[int(ch)] if ch.isdigit() else ch for ch in str(s))


def gregorian_to_jalali(gy, gm, gd):
    g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    j_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]

    gy2 = gy - 1600
    gm2 = gm - 1
    gd2 = gd - 1

    g_day_no = 365 * gy2 + (gy2 + 3) // 4 - (gy2 + 99) // 100 + (gy2 + 399) // 400
    for i in range(gm2):
        g_day_no += g_days_in_month[i]
    if gm2 > 1 and ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        g_day_no += 1
    g_day_no += gd2

    j_day_no = g_day_no - 79

    j_np = j_day_no // 12053
    j_day_no %= 12053

    jy = 979 + 33 * j_np + 4 * (j_day_no // 1461)
    j_day_no %= 1461

    if j_day_no >= 366:
        jy += (j_day_no - 1) // 365
        j_day_no = (j_day_no - 1) % 365

    for i in range(11):
        if j_day_no < j_days_in_month[i]:
            jm = i + 1
            jd = j_day_no + 1
            break
        j_day_no -= j_days_in_month[i]
    else:
        jm = 12
        jd = j_day_no + 1

    return jy, jm, jd


def today_jalali_string():
    """Returns e.g. '\u06f3\u06f1 \u062a\u06cc\u0631 \u06f1\u06f4\u06f0\u06f5' (day + Persian month name + year, all Persian digits)."""
    from datetime import date
    g = date.today()
    jy, jm, jd = gregorian_to_jalali(g.year, g.month, g.day)
    return f"{to_persian_digits(jd)} {PERSIAN_MONTHS[jm - 1]} {to_persian_digits(jy)}"
