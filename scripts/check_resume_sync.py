# -*- coding: utf-8 -*-
"""
Fails the build when the resume pages and resume_data.py disagree.

The downloadable .docx/.pdf are built from scripts/resume_data.py, but the
resume pages are hand-edited HTML. Those are two sources for one set of
facts, and nothing used to notice when they drifted apart: "Research
Experience" went from a bracketed placeholder to three real entries on the
site and simply never appeared in the documents, because resume_data.py
was never given a matching key and the build workflow did not even run on
a change to the pages.

This checks the three things that actually drift:

  1. every section on the page has a data key, and vice versa
  2. the sections appear in the same order in both
  3. a section holds the same number of entries in both

It deliberately does not compare wording. Copy is edited constantly and a
checker that fought over punctuation would be turned off within a week;
these three catch the structural mistakes that silently ship a wrong
document.

Usage:
    python3 scripts/check_resume_sync.py
"""

import html
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

# page block title (EN, FA) -> key in RESUME_EN / RESUME_FA.
# `counted` is False for prose and chip-grid sections, where "entries" on
# the page and items in the data are not the same kind of thing.
SECTIONS = [
    ("About",                          "درباره من",                              "about",          False),
    ("Education",                      "تحصیلات",                                "education",      True),
    ("Professional Experience",        "تجربه حرفه‌ای",                          "experience",     True),
    ("Research Experience",            "تجربه پژوهشی",                           "research",       True),
    ("Books",                          "کتاب‌ها",                                "books",          True),
    ("Conferences",                    "کنفرانس‌ها",                             "conferences",    True),
    ("Patents",                        "اختراعات",                               "patents",        True),
    ("Teaching Activities",            "فعالیت‌های تدریس",                       "teaching",       True),
    ("Honors & Awards",                "افتخارات و جوایز",                       "honors",         True),
    ("Languages",                      "زبان‌ها",                                "languages",      False),
    ("Professional Memberships",       "عضویت‌های حرفه‌ای",                      "memberships",    True),
    ("Voluntary & Social Activities",  "سوابق داوطلبانه و فعالیت‌های اجتماعی",   "volunteer",      True),
    ("Technical & Specialized Skills", "مهارت‌های فنی و تخصصی",                  "skills",         False),
    ("Courses, Certificates & Licenses", "دوره‌ها، گواهی‌ها و مجوزها",           "certifications", False),
]

ENTRY_RE = re.compile(r'<div class="(?:resume__entry|pub-card)[ "]')


def load_data():
    spec = importlib.util.spec_from_file_location("resume_data", ROOT / "scripts" / "resume_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def page_sections(path):
    """[(title, entry_count)] in the order they appear on the page."""
    text = path.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r'<section class="resume__block[^"]*">(.*?)</section>', text, re.S):
        body = m.group(1)
        t = re.search(r'<p class="resume__block-title">(.*?)</p>', body)
        if not t:
            continue
        title = html.unescape(re.sub(r"<[^>]+>", "", t.group(1))).strip()
        out.append((title, len(ENTRY_RE.findall(body))))
    return out


def check(lang, page_path, data):
    problems = []
    idx = 0 if lang == "EN" else 1
    expected = [(s[idx], s[2], s[3]) for s in SECTIONS]
    found = page_sections(page_path)

    known = {title for title, _, _ in expected}
    for title, _ in found:
        if title not in known:
            problems.append(
                '%s: the page has a "%s" section with no key in resume_data.py — '
                "it will be missing from the downloadable files" % (lang, title)
            )

    page_titles = [t for t, _ in found]
    for title, key, _ in expected:
        if title not in page_titles:
            problems.append('%s: resume_data.py has "%s" but the page has no "%s" section' % (lang, key, title))
        if key not in data:
            problems.append('%s: no "%s" key in resume_data.py' % (lang, key))

    ordered = [t for t in page_titles if t in known]
    wanted = [t for t, _, _ in expected if t in page_titles]
    if ordered != wanted:
        problems.append(
            "%s: section order differs.\n     page: %s\n     data: %s" % (lang, " → ".join(ordered), " → ".join(wanted))
        )

    counts = dict(found)
    for title, key, counted in expected:
        if not counted or title not in counts or key not in data:
            continue
        if not isinstance(data[key], list):
            continue
        if counts[title] != len(data[key]):
            problems.append(
                '%s: "%s" has %d entries on the page but %d in resume_data.py'
                % (lang, title, counts[title], len(data[key]))
            )
    return problems


def main():
    data = load_data()
    problems = []
    problems += check("EN", ROOT / "resume" / "index.html", data.RESUME_EN)
    problems += check("FA", ROOT / "fa" / "resume" / "index.html", data.RESUME_FA)

    if problems:
        print("Resume page and resume_data.py are out of sync:\n")
        for p in problems:
            print("  - " + p)
        print("\nUpdate scripts/resume_data.py so the downloadable files match the site.")
        return 1

    print("Resume pages and resume_data.py agree on every section, order and entry count.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
