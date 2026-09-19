# -*- coding: utf-8 -*-
"""
Single source of truth for the site's SEO IDENTITY: who the site is about,
how the name is spelled in each language, which outside profiles are the
same person, and which pages exist in which language.

This is a plain data file — no logic. scripts/build_seo.py reads it (and
resume_data.py, for jobs, schools and awards) and bakes the result into a
marked block in every page's <head> plus /sitemap.xml. Edit here, run
`python3 scripts/build_seo.py`, and every page follows; never edit the
generated block in the HTML by hand, CI overwrites it on the next push.

Why the spellings matter: Google ranks an entity, not a string. Someone
typing "محمد آریا امینی" (with a space), "آریا امینی" or "Aria Amini" has
to land on the same Person as "Mohammad Aria Amini" — alternateName in the
structured data is what tells Google those are one person, and sameAs is
what ties that person to the LinkedIn/Civilica/GitHub profiles Google
already knows about.
"""

SITE_URL = "https://amini.info"
DEFAULT_LANG = "en"          # what hreflang="x-default" points at

# Stable identifiers for the two nodes every page shares. The same @id on
# the English and Persian pages is what lets Google merge them into one
# entity instead of two half-known people.
PERSON_ID = SITE_URL + "/#person"
WEBSITE_ID = SITE_URL + "/#website"

# The first form is what the pages themselves use (h1, <title>). The rest
# are the forms people actually type into Google.
SITE_NAME = {"en": "Mohammad Aria Amini", "fa": "محمدآریا امینی"}
GIVEN_NAME = {"en": "Mohammad Aria", "fa": "محمدآریا"}
FAMILY_NAME = {"en": "Amini", "fa": "امینی"}
ALTERNATE_NAMES = {
    "en": ["Aria Amini", "M. A. Amini"],
    "fa": ["محمد آریا امینی", "آریا امینی"],
}

# One line that says what he is; shown to Google as disambiguatingDescription
# (the full "about" paragraph comes from resume_data.py).
HEADLINE = {
    "en": "Geologist, Earth sciences researcher and scientific editor based in Tehran, Iran",
    "fa": "زمین‌شناس، پژوهشگر علوم زمین و ویراستار علمی، تهران، ایران",
}

KNOWS_ABOUT = {
    "en": ["Geology", "Petroleum Geology", "Geochemistry", "Economic Geology",
           "Petrography", "Earth Sciences", "Scientific Editing",
           "High-Performance Computing"],
    "fa": ["زمین‌شناسی", "زمین‌شناسی نفت", "ژئوشیمی", "زمین‌شناسی اقتصادی",
           "پتروگرافی", "علوم زمین", "ویراستاری علمی",
           "محاسبات با کارایی بالا (HPC)"],
}

# Kept explicit rather than parsed out of the "Professional Memberships"
# prose in resume_data.py: three entries, and a name is a name.
MEMBER_OF = {
    "en": [
        {"name": "Geological Society of Iran"},
        {"name": "Geological Society of America", "url": "https://www.geosociety.org/"},
        {"name": "American Association of Petroleum Geologists", "url": "https://www.aapg.org/"},
    ],
    "fa": [
        {"name": "انجمن زمین‌شناسی ایران"},
        {"name": "انجمن زمین‌شناسی آمریکا (GSA)", "url": "https://www.geosociety.org/"},
        {"name": "انجمن زمین‌شناسان نفت آمریکا (AAPG)", "url": "https://www.aapg.org/"},
    ],
}

EMAIL = "aria@amini.info"
LOCALITY = {"en": "Tehran", "fa": "تهران"}
COUNTRY_NAME = {"en": "Iran", "fa": "ایران"}
COUNTRY_CODE = "IR"

# Public profiles that are this same person. Add ORCID, Google Scholar or
# ResearchGate here when they exist — each one is another vote for the entity.
SAME_AS = [
    "https://www.linkedin.com/in/mo-aria-amini",
    "https://civilica.com/p/511149/",
    "https://github.com/amini-aria",
    "https://instagram.com/daily.aria",
    "https://t.me/aria_amini",
]

# Ownership codes from Google Search Console / Bing Webmaster Tools ("HTML
# tag" method). Empty means the tag is not emitted. Paste the code, run
# build_seo.py (or just push) and every page carries it.
SITE_VERIFICATION = {
    "google": "",   # <meta name="google-site-verification" content="...">
    "bing": "",     # <meta name="msvalidate.01" content="...">
}

# IndexNow (Bing, Yandex, Seznam, Naver; Google does not take part). The key
# is public by design: engines confirm it by fetching /<key>.txt, which
# build_seo.py writes to the site root, and CI pings api.indexnow.org with
# every page after each push (scripts/indexnow.py). Empty disables both.
INDEXNOW_KEY = "57c3e44f309e6c0f38183a247b2e69be"

PORTRAIT = {"path": "/assets/img/portrait.jpg", "width": 640, "height": 800}
OG_IMAGE = {"path": "/assets/img/og-image.jpg", "width": 1200, "height": 630}
OG_LOCALE = {"en": "en_US", "fa": "fa_IR"}

# Every published page, its language, and its translation. `crumb` is the
# label used in the breadcrumb trail (the home page's crumb is the first
# item of every other page's trail in that language). `kind` "home" gets
# ProfilePage + og:type=profile; everything else is a plain WebPage.
PAGES = [
    {"path": "index.html",                 "lang": "en", "pair": "fa/index.html",              "kind": "home",         "crumb": "Home"},
    {"path": "resume/index.html",          "lang": "en", "pair": "fa/resume/index.html",       "kind": "resume",       "crumb": "Resume"},
    {"path": "publications/index.html",    "lang": "en", "pair": "fa/publications/index.html", "kind": "publications", "crumb": "Research"},
    {"path": "contact/index.html",         "lang": "en", "pair": "fa/contact/index.html",      "kind": "contact",      "crumb": "Contact"},
    {"path": "fa/index.html",              "lang": "fa", "pair": "index.html",                 "kind": "home",         "crumb": "خانه"},
    {"path": "fa/resume/index.html",       "lang": "fa", "pair": "resume/index.html",          "kind": "resume",       "crumb": "رزومه"},
    {"path": "fa/publications/index.html", "lang": "fa", "pair": "publications/index.html",    "kind": "publications", "crumb": "پژوهش"},
    {"path": "fa/contact/index.html",      "lang": "fa", "pair": "contact/index.html",         "kind": "contact",      "crumb": "ارتباط"},
]
