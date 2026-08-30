# -*- coding: utf-8 -*-
"""
Single source of truth for the CONTENT of the downloadable resume files
(Aria-CV-En.docx / .pdf and Aria-CV-Fa.docx / .pdf).

This is a plain Python data file — no logic here, just facts. The layout
and formatting live in build_resume_docs.py, which reads these two dicts.

IMPORTANT: this file is kept in sync BY HAND with the actual content shown
on resume/index.html and fa/resume/index.html. If you update the resume
page on the site, update the matching fields here too (and re-run
build_resume_docs.py, or just push — the GitHub Action does it for you)
so the downloadable files keep matching what's on the site.

Only real, filled-in content lives here — sections that are still
bracketed placeholders on the site (Research Experience,
Certifications) are intentionally left out
of the downloadable files entirely, since an ATS-optimized resume
should never show empty/placeholder sections. Publications is not on
the site at all right now (ISI articles aren't printed yet), so it has
no entry here either.
"""

RESUME_EN = {
    "name": "Mohammad Aria Amini",
    "role": "Geology Graduate",
    "contact_parts": [
        {"text": "Tehran, Iran"},
        {"text": "mo.aria.am@gmail.com"},
        {"text": "linkedin.com/in/mo-aria-amini", "url": "https://www.linkedin.com/in/mo-aria-amini"},
        {"text": "aria-amini.ir", "url": "https://aria-amini.ir"},
    ],
    "about": (
        "I am Mohammad Aria Amini, a Bachelor's graduate in Geology and a researcher, writer, and "
        "scientific editor in the field of Earth sciences. I am interested in research, scientific "
        "writing and editing, and continuously developing my knowledge and professional skills in "
        "Earth sciences."
    ),
    "interests": (
        "My research and professional interests primarily lie in the field of Earth sciences, with "
        "a particular focus on geochemistry, petroleum geology, and topics related to subsurface "
        "resources. I am interested in studying various areas of geology, particularly geological "
        "and geochemical processes, rocks and minerals, petroleum systems, and the application of "
        "geological data to the understanding and assessment of subsurface resources. I am also "
        "interested in applying modern data processing, analytical methods, and computational "
        "technologies to Earth science research, and I continuously seek to expand my knowledge "
        "and skills in these areas."
    ),
    "education": [
        {
            "degree": "B.Sc. in Geology",
            "period": "2022 \u2013 2026",
            "org": "Golestan University, Faculty of Earth Sciences, Gorgan, Iran",
            "notes": [
                "Ranked first among incoming undergraduate students, with a Grade A average",
                "Completed the program in seven semesters \u2013 one semester ahead of the standard curriculum",
                "Completed 6 of 7 terms at Shahid Beheshti University, Tehran",
            ],
        },
        {
            "degree": "High School Diploma, Experimental Sciences",
            "period": "2017 \u2013 2020",
            "org": "Shahid Beheshti Exceptional Talents High School (NODET), Ahvaz, Iran",
            "notes": [],
        },
    ],
    # org is the heading; role + period follow on the next line
    "experience": [
        {"org": "Varjavand Intelligent Creative Software & Hardware Services Co.", "role": "Chief Executive Officer (CEO) and Chairman of the Board", "period": "Jul 2025 \u2013 Present"},
        {"org": "Arian Zamin Publishing House", "roles": [
            {"role": "Director", "period": "Apr 2026 \u2013 Present"},
            {"role": "Editorial Specialist and Publications Researcher", "period": "Mar 2023 \u2013 Apr 2026"},
        ]},
        {"org": "Pars Geological Research Center (Arian Zamin)", "role": "Geology Specialist", "period": "Feb 2023 \u2013 Present"},
        {"org": "Shahid Beheshti University, Tehran, Iran", "roles": [
            {"role": "Research Collaborator", "period": "Feb 2025 \u2013 Sep 2026"},
            {"role": "Technical Manager, SARMAD High-Performance Computing (HPC) System", "period": "Feb 2025 \u2013 Aug 2026"},
        ]},
        {"org": "Gemology Science and Art Development Co. (Gemsa), Knowledge-Based Company", "role": "Research & Development (R&D) Manager", "period": "Sep 2024 \u2013 Apr 2025"},
    ],
    "books": [
        {"citation": "Ghorbani, M., & Amini, M. A. (2025). The Historiography of Earth Science in Iran: Introducing a Number of Contemporary Pioneers.", "role": "Co-author", "isbn": "978-600-6058-43-6 (second edition onward: 978-600-6058-60-3)"},
        {"citation": "Fathi, T. (2026). Petroleum Contamination Hydrogeology: Geological, Environmental, Legal Aspects, and Models for the Remediation of Contaminated Groundwater.", "role": "Scientific Editor", "isbn": ""},
        {"citation": "Momenzadeh, M. (2025). The Mythical City of Zabol: The Burnt City.", "role": "Editor", "isbn": "978-600-6058-44-3"},
        {"citation": "Salmati, R. (2025). A Comprehensive Guide to Geological Mapping at Scales of 1:50,000 and Larger.", "role": "Editor", "isbn": "978-600-6058-42-9"},
    ],
    "conferences": [
        {
            "title": "Natural Resources (Mineral, Energy, and Water Resources) in Iran",
            "period": "2025",
            "org": "4th Global Summit on Advances in Earth Science & Climate Change (Adv. ESCC 2025) - Berlin, Germany (Virtual Presentation)",
            "tag": "Oral Presentation",
            "note": "Co-presented with Dr. Mansour Ghorbani · Distinguished Speaker · Organized by Peers Alley Media · Sep 29–30, 2025",
        },
        {
            "title": "Differences in Garnet Classification Based on Color",
            "period": "2024",
            "org": "43rd Earth Sciences Congress (National Conference) - Tehran, Iran",
            "tag": "Conference Paper",
            "note": "Co-authored with Ziba Delpasand and Fariborz Masoudi · 10 pages · Persian",
            "doc_id": "GSI43_151",
            "url": "https://civilica.com/doc/2419015/",
        },
        {
            "title": "Petrographic, Mineralization, and Alteration Study of the Choudarchay Copper Vein Deposit",
            "period": "2024",
            "org": "43rd Earth Sciences Congress (National Conference) - Tehran, Iran",
            "tag": "Oral Presentation",
            "note": "Sole author · 13 pages · Persian",
            "doc_id": "GSI43_064",
            "url": "https://civilica.com/doc/2418928/",
        },
        {
            "title": "Economic Geology of Copper and Associated Elements in the South Rayen Area, with a Focus on Gadar-e-Siah",
            "period": "2023",
            "org": "42nd Earth Sciences Congress (National Conference) - Tehran, Iran",
            "tag": "Oral Presentation",
            "note": "Co-authored with Shohreh Salkhordeh · 15 pages · Persian",
            "doc_id": "GSI42_161",
            "url": "https://civilica.com/doc/1963822/",
        },
    ],
    "patents": [
        {
            "title": "System and Method for Depth-Aware Identification and Zonation of Productive (Net Pay) Intervals in Oil Wells Using Multi-Model Probabilistic Fusion of Well-Log Data",
            "status": "Under Review",
            "org": "Iranian Patent Application · Sole Inventor",
        },
    ],
    "teaching": [
        {
            "title": "Research Week Events & Workshops Series",
            "period": "Jan 2026 – Feb 2026",
            "org": "Shahid Beheshti University, Tehran",
            "note": "Instructor · Workshop: Introduction to Parallel Processing Systems and Linux-Based High-Performance Computing Environments",
        },
    ],
    "honors": [
        {
            "title": "Top Young Earth Sciences Researcher",
            "period": "2024",
            "org": "Geological Society of Iran",
        },
    ],
    "skills": {
        "Programming Languages": ["Python", "JavaScript", "PHP", "C#", "SQL"],
        "Other Skills": ["Scientific Editing", "Academic Publishing", "LaTeX", "Git", "Docker"],
    },
    "software": {
        "Geological Software": ["ArcGIS", "QGIS", "RockWorks", "Surfer"],
        "Web Technologies": ["HTML5", "CSS3", "Bootstrap", "WordPress", "Laravel"],
    },
    "languages": [
        {"name": "Persian", "level": "Native"},
        {"name": "English", "level": "Professional Working Proficiency"},
        {"name": "French", "level": "Learning"},
    ],
    # role is the heading here (org below) — unchanged format
    "memberships": [
        {"role": "Secretary and Website Administrator", "period": "Apr 2023 \u2013 Present", "org": "Iranian Geological Society"},
        {"role": "Member of the Organizing Committee", "period": "", "org": "Five National Geological Congresses of the Iranian Geological Society"},
    ],
    "volunteer": [
        {"role": "Member, Iran Organ Donation Association", "period": "", "org": "Membership number to be added"},
    ],
}

RESUME_FA = {
    "name": "\u0645\u062d\u0645\u062f\u0622\u0631\u06cc\u0627 \u0627\u0645\u06cc\u0646\u06cc",
    "role": "\u062f\u0627\u0646\u0634\u200c\u0622\u0645\u0648\u062e\u062a\u0647\u200c\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc",
    "contact_parts": [
        {"text": "\u062a\u0647\u0631\u0627\u0646\u060c \u0627\u06cc\u0631\u0627\u0646"},
        {"text": "mo.aria.am@gmail.com"},
        {"text": "linkedin.com/in/mo-aria-amini", "url": "https://www.linkedin.com/in/mo-aria-amini"},
        {"text": "aria-amini.ir", "url": "https://aria-amini.ir"},
    ],
    "about": (
        "من محمدآریا امینی، فارغ‌التحصیل مقطع کارشناسی در رشته زمین‌شناسی و "
        "پژوهشگر، نویسنده و ویراستار علمی در حوزه علوم زمین هستم. به "
        "فعالیت‌های پژوهشی، نگارش و ویرایش علمی و یادگیری در زمینه‌های "
        "مختلف علوم زمین علاقه‌مندم و در مسیر توسعه دانش و مهارت‌های "
        "حرفه‌ای خود فعالیت می‌کنم."
    ),
    "interests": (
        "علاقه‌مندی‌های پژوهشی و حرفه‌ای من عمدتاً در زمینه علوم زمین، با "
        "تمرکز بیشتر بر ژئوشیمی، زمین‌شناسی نفت و موضوعات مرتبط با منابع "
        "زیرزمینی شکل گرفته است. به مطالعه و پژوهش در زمینه‌های مختلف "
        "زمین‌شناسی، به‌ویژه بررسی فرایندهای زمین‌شناسی و ژئوشیمیایی، "
        "سنگ‌ها و کانی‌ها، سیستم‌های نفتی و کاربرد داده‌های زمین‌شناسی در "
        "شناخت و ارزیابی منابع زیرزمینی علاقه‌مندم. همچنین به استفاده از "
        "روش‌های نوین پردازش و تحلیل داده و فناوری‌های محاسباتی در "
        "پژوهش‌های علوم زمین علاقه دارم و همواره در تلاش برای گسترش دانش "
        "و مهارت خود در این زمینه‌ها هستم."
    ),
    "education": [
        {
            "degree": "کارشناسی زمین‌شناسی",
            "period": "۱۴۰۱ – ۱۴۰۵",
            "org": "دانشگاه گلستان، دانشکده علوم زمین، گرگان، ایران",
            "notes": [
                "رتبه‌ی نخست ورودی کارشناسی با معدل گرید A",
                "فراغت از تحصیل در هفت نیم‌سال – یک نیم‌سال زودتر از برنامه‌ی استاندارد",
                "گذراندن ۶ ترم از ۷ ترم در دانشگاه شهید بهشتی تهران",
            ],
        },
        {
            "degree": "دیپلم علوم تجربی",
            "period": "۱۳۹۶ – ۱۳۹۹",
            "org": "دبیرستان استعداد درخشان شهید بهشتی (سَمپاد)، اهواز، ایران",
            "notes": [],
        },
    ],
    "experience": [
        {"org": "\u0634\u0631\u06a9\u062a \u062e\u062f\u0645\u0627\u062a \u0646\u0631\u0645\u200c\u0627\u0641\u0632\u0627\u0631\u06cc \u0648 \u0633\u062e\u062a\u200c\u0627\u0641\u0632\u0627\u0631\u06cc \u0647\u0648\u0634\u0645\u0646\u062f \u0627\u0641\u0632\u0627\u0631 \u062e\u0644\u0627\u0642 (\u0648\u064e\u0631\u062c\u0627\u0648\u064e\u0646\u062f)", "role": "\u0645\u062f\u06cc\u0631\u0639\u0627\u0645\u0644 \u0648 \u0631\u0626\u06cc\u0633 \u0647\u06cc\u0626\u062a \u0645\u062f\u06cc\u0631\u0647", "period": "\u062a\u06cc\u0631 \u06f1\u06f4\u06f0\u06f4 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
        {"org": "\u0627\u0646\u062a\u0634\u0627\u0631\u0627\u062a \u0622\u0631\u06cc\u0646 \u0632\u0645\u06cc\u0646", "roles": [
            {"role": "\u0645\u062f\u06cc\u0631 \u0627\u0646\u062a\u0634\u0627\u0631\u0627\u062a", "period": "\u0641\u0631\u0648\u0631\u062f\u06cc\u0646 \u06f1\u06f4\u06f0\u06f5 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
            {"role": "\u06a9\u0627\u0631\u0634\u0646\u0627\u0633 \u0648 \u067e\u0698\u0648\u0647\u0634\u06af\u0631 \u0627\u0646\u062a\u0634\u0627\u0631\u0627\u062a", "period": "\u0627\u0633\u0641\u0646\u062f \u06f1\u06f4\u06f0\u06f1 \u2013 \u0641\u0631\u0648\u0631\u062f\u06cc\u0646 \u06f1\u06f4\u06f0\u06f5"},
        ]},
        {"org": "\u0645\u0648\u0633\u0633\u0647 \u067e\u0698\u0648\u0647\u0634\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u067e\u0627\u0631\u0633 \u0622\u0631\u06cc\u0646 \u0632\u0645\u06cc\u0646", "role": "\u06a9\u0627\u0631\u0634\u0646\u0627\u0633 \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633", "period": "\u0628\u0647\u0645\u0646 \u06f1\u06f4\u06f0\u06f1 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
        {"org": "\u062f\u0627\u0646\u0634\u06af\u0627\u0647 \u0634\u0647\u06cc\u062f \u0628\u0647\u0634\u062a\u06cc\u060c \u062a\u0647\u0631\u0627\u0646", "roles": [
            {"role": "\u0647\u0645\u06a9\u0627\u0631 \u067e\u0698\u0648\u0647\u0634\u06cc", "period": "\u0628\u0647\u0645\u0646 \u06f1\u06f4\u06f0\u06f3 \u2013 \u0634\u0647\u0631\u06cc\u0648\u0631 \u06f1\u06f4\u06f0\u06f5"},
            {"role": "\u0645\u062f\u06cc\u0631 \u0641\u0646\u06cc \u0633\u06cc\u0633\u062a\u0645 \u0627\u0628\u0631\u0631\u0627\u06cc\u0627\u0646\u0647 \u0633\u0631\u0645\u062f", "period": "\u0628\u0647\u0645\u0646 \u06f1\u06f4\u06f0\u06f3 \u2013 \u0645\u0631\u062f\u0627\u062f \u06f1\u06f4\u06f0\u06f5"},
        ]},
        {"org": "\u0634\u0631\u06a9\u062a \u062a\u0648\u0633\u0639\u0647 \u062f\u0627\u0646\u0634 \u0648 \u0647\u0646\u0631 \u06af\u0648\u0647\u0631\u0634\u0646\u0627\u0633\u06cc (\u062c\u0650\u0645\u0633\u0627) - \u062f\u0627\u0646\u0634\u200c\u0628\u0646\u06cc\u0627\u0646", "role": "\u0645\u062f\u06cc\u0631 \u062a\u062d\u0642\u06cc\u0642 \u0648 \u062a\u0648\u0633\u0639\u0647 (R&D)", "period": "\u0634\u0647\u0631\u06cc\u0648\u0631 \u06f1\u06f4\u06f0\u06f3 \u2013 \u0641\u0631\u0648\u0631\u062f\u06cc\u0646 \u06f1\u06f4\u06f0\u06f4"},
    ],
    "books": [
        {"citation": "\u0642\u0631\u0628\u0627\u0646\u06cc\u060c \u0645. \u0648 \u0627\u0645\u06cc\u0646\u06cc\u060c \u0645. \u0622. (\u06f1\u06f4\u06f0\u06f4). \u062a\u0627\u0631\u06cc\u062e\u200c\u0646\u06af\u0627\u0631\u06cc \u062f\u0627\u0646\u0634 \u0639\u0644\u0648\u0645\u200c\u0632\u0645\u06cc\u0646 \u062f\u0631 \u0627\u06cc\u0631\u0627\u0646: \u0628\u0627 \u0645\u0639\u0631\u0641\u06cc \u0634\u0645\u0627\u0631\u06cc \u0627\u0632 \u067e\u06cc\u0634\u06af\u0627\u0645\u0627\u0646 \u0645\u0639\u0627\u0635\u0631.", "role": "\u0646\u0648\u06cc\u0633\u0646\u062f\u0647 \u0647\u0645\u06a9\u0627\u0631", "isbn": "978-600-6058-43-6"},
        {"citation": "\u0641\u062a\u062d\u06cc\u060c \u062a. (\u06f1\u06f4\u06f0\u06f5). \u0647\u06cc\u062f\u0631\u0648\u0698\u0626\u0648\u0644\u0648\u0698\u06cc \u0622\u0644\u0648\u062f\u06af\u06cc \u0646\u0641\u062a\u06cc: \u062c\u0646\u0628\u0647\u200c\u0647\u0627\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc\u060c \u0632\u06cc\u0633\u062a\u200c\u0645\u062d\u06cc\u0637\u06cc\u060c \u062d\u0642\u0648\u0642\u06cc \u0648 \u0645\u062f\u0644\u200c\u0647\u0627\u06cc \u067e\u0627\u06a9\u200c\u0633\u0627\u0632\u06cc \u0622\u0628\u200c\u0647\u0627\u06cc \u0632\u06cc\u0631\u0632\u0645\u06cc\u0646\u06cc \u0622\u0644\u0648\u062f\u0647.", "role": "\u0648\u06cc\u0631\u0627\u0633\u062a\u0627\u0631 \u0639\u0644\u0645\u06cc", "isbn": ""},
        {"citation": "\u0645\u0648\u0645\u0646\u200c\u0632\u0627\u062f\u0647\u060c \u0645. (\u06f1\u06f4\u06f0\u06f4). \u0634\u0647\u0631 \u0627\u0641\u0633\u0627\u0646\u0647\u200c\u0627\u06cc \u0632\u0627\u0628\u0644: \u0634\u0647\u0631 \u0633\u0648\u062e\u062a\u0647.", "role": "\u0648\u06cc\u0631\u0627\u0633\u062a\u0627\u0631", "isbn": ""},
        {"citation": "\u0633\u0644\u0645\u0627\u062a\u06cc\u060c \u0631. (\u06f1\u06f4\u06f0\u06f4). \u0631\u0627\u0647\u0646\u0645\u0627\u06cc \u062c\u0627\u0645\u0639 \u0646\u0642\u0634\u0647\u200c\u0628\u0631\u062f\u0627\u0631\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u062f\u0631 \u0645\u0642\u06cc\u0627\u0633 \u06f1:\u06f5\u06f0\u06f0\u06f0\u06f0 \u0648 \u0628\u0632\u0631\u06af\u200c\u062a\u0631.", "role": "\u0648\u06cc\u0631\u0627\u0633\u062a\u0627\u0631", "isbn": ""},
    ],
    "conferences": [
        {
            "title": "\u0645\u0646\u0627\u0628\u0639 \u0637\u0628\u06cc\u0639\u06cc (\u0645\u0639\u0627\u062f\u0646\u060c \u0627\u0646\u0631\u0698\u06cc \u0648 \u0645\u0646\u0627\u0628\u0639 \u0622\u0628) \u0627\u06cc\u0631\u0627\u0646",
            "period": "\u06f1\u06f4\u06f0\u06f4",
            "org": "\u0686\u0647\u0627\u0631\u0645\u06cc\u0646 \u0627\u062c\u0644\u0627\u0633 \u062c\u0647\u0627\u0646\u06cc \u067e\u06cc\u0634\u0631\u0641\u062a\u200c\u0647\u0627\u06cc \u0639\u0644\u0648\u0645 \u0632\u0645\u06cc\u0646 \u0648 \u062a\u063a\u06cc\u06cc\u0631\u0627\u062a \u0627\u0642\u0644\u06cc\u0645\u06cc (Adv. ESCC 2025) - \u0628\u0631\u0644\u06cc\u0646\u060c \u0622\u0644\u0645\u0627\u0646 (\u0627\u0631\u0627\u0626\u0647 \u0645\u062c\u0627\u0632\u06cc)",
            "tag": "\u0633\u062e\u0646\u0631\u0627\u0646\u06cc",
            "note": "\u0627\u0631\u0627\u0626\u0647 \u0645\u0634\u062a\u0631\u06a9 \u0628\u0627 \u062f\u06a9\u062a\u0631 \u0645\u0646\u0635\u0648\u0631 \u0642\u0631\u0628\u0627\u0646\u06cc \u00b7 \u062f\u0631\u06cc\u0627\u0641\u062a\u200c\u06a9\u0646\u0646\u062f\u0647 \u0639\u0646\u0648\u0627\u0646 \u0633\u062e\u0646\u0631\u0627\u0646 \u0628\u0631\u062c\u0633\u062a\u0647 (Distinguished Speaker) \u00b7 \u0628\u0631\u06af\u0632\u0627\u0631\u06a9\u0646\u0646\u062f\u0647: Peers Alley Media \u00b7 Sep 29\u201330, 2025",
        },
        {
            "title": "\u062a\u0641\u0627\u0648\u062a \u0637\u0628\u0642\u0647\u200c\u0628\u0646\u062f\u06cc \u06af\u0627\u0631\u0646\u062a \u0628\u0631 \u0645\u0628\u0646\u0627\u06cc \u0631\u0646\u06af",
            "period": "\u06f1\u06f4\u06f0\u06f3",
            "org": "چهل و سومین گردهمایی (همایش ملی) علوم زمین - تهران، ایران",
            "tag": "\u0645\u0642\u0627\u0644\u0647 \u06a9\u0646\u0641\u0631\u0627\u0646\u0633\u06cc",
            "note": "\u0646\u0648\u06cc\u0633\u0646\u062f\u06af\u0627\u0646: \u0632\u06cc\u0628\u0627 \u062f\u0644\u067e\u0633\u0646\u062f\u060c \u0641\u0631\u06cc\u0628\u0631\u0632 \u0645\u0633\u0639\u0648\u062f\u06cc\u060c \u0645\u062d\u0645\u062f\u0622\u0631\u06cc\u0627 \u0627\u0645\u06cc\u0646\u06cc \u00b7 \u06f1\u06f0 \u0635\u0641\u062d\u0647 \u00b7 \u0632\u0628\u0627\u0646: \u0641\u0627\u0631\u0633\u06cc",
            "doc_id": "GSI43_151",
            "url": "https://civilica.com/doc/2419015/",
        },
        {
            "title": "\u0628\u0631\u0631\u0633\u06cc \u067e\u062a\u0631\u0648\u06af\u0631\u0627\u0641\u06cc\u060c \u06a9\u0627\u0646\u0647\u200c\u0632\u0627\u06cc\u06cc \u0648 \u062f\u06af\u0631\u0633\u0627\u0646\u06cc \u0630\u062e\u0627\u06cc\u0631 \u06a9\u0627\u0646\u0633\u0627\u0631 \u0631\u06af\u0647\u200c\u0647\u0627\u06cc \u0645\u0633 \u0686\u0648\u062f\u0631\u0686\u0627\u06cc",
            "period": "\u06f1\u06f4\u06f0\u06f3",
            "org": "چهل و سومین گردهمایی (همایش ملی) علوم زمین - تهران، ایران",
            "tag": "\u0633\u062e\u0646\u0631\u0627\u0646\u06cc",
            "note": "\u0646\u0648\u06cc\u0633\u0646\u062f\u0647: \u0645\u062d\u0645\u062f\u0622\u0631\u06cc\u0627 \u0627\u0645\u06cc\u0646\u06cc \u00b7 \u06f1\u06f3 \u0635\u0641\u062d\u0647 \u00b7 \u0632\u0628\u0627\u0646: \u0641\u0627\u0631\u0633\u06cc",
            "doc_id": "GSI43_064",
            "url": "https://civilica.com/doc/2418928/",
        },
        {
            "title": "\u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0627\u0642\u062a\u0635\u0627\u062f\u06cc \u0645\u0633 \u0648 \u0639\u0646\u0627\u0635\u0631 \u0647\u0645\u0631\u0627\u0647 \u062f\u0631 \u0645\u062d\u062f\u0648\u062f\u0647 \u062c\u0646\u0648\u0628 \u0631\u0627\u06cc\u0646 \u0628\u0627 \u0646\u06af\u0631\u0634\u06cc \u0628\u0631 \u06af\u062f\u0627\u0631 \u0633\u06cc\u0627\u0647",
            "period": "\u06f1\u06f4\u06f0\u06f2",
            "org": "چهل و دومین گردهمایی (همایش ملی) علوم زمین - تهران، ایران",
            "tag": "\u0633\u062e\u0646\u0631\u0627\u0646\u06cc",
            "note": "\u0646\u0648\u06cc\u0633\u0646\u062f\u06af\u0627\u0646: \u0645\u062d\u0645\u062f\u0622\u0631\u06cc\u0627 \u0627\u0645\u06cc\u0646\u06cc\u060c \u0634\u0647\u0631\u0647 \u0633\u0627\u0644\u062e\u0648\u0631\u062f\u0647 \u00b7 \u06f1\u06f5 \u0635\u0641\u062d\u0647 \u00b7 \u0632\u0628\u0627\u0646: \u0641\u0627\u0631\u0633\u06cc",
            "doc_id": "GSI42_161",
            "url": "https://civilica.com/doc/1963822/",
        },
    ],
    "patents": [
        {
            "title": "سامانه و روش هوشمند شناسایی و زون‌بندی زون‌های تولیدی (Net Pay/Pay Zone) در چاه‌های نفت بر پایه همجوشی احتمالاتی چندمدلی و تحلیل عمقی داده‌های لاگ",
            "status": "در دست داوری",
            "org": "درخواست ثبت اختراع ایران · مخترع منفرد",
        },
    ],
    "teaching": [
        {
            "title": "مجموعه رویدادها و کارگاه‌های هفته پژوهش",
            "period": "دی ۱۴۰۴ – بهمن ۱۴۰۴",
            "org": "دانشگاه شهید بهشتی، تهران",
            "note": "مدرس · عنوان کارگاه: آشنایی با محیط سامانه‌های پردازش موازی و پردازش سریع مبتنی بر لینوکس",
        },
    ],
    "honors": [
        {
            "title": "برترین پژوهشگر جوان علوم زمین",
            "period": "۱۴۰۳",
            "org": "انجمن زمین‌شناسی ایران",
        },
    ],
    "skills": {
        "\u0632\u0628\u0627\u0646\u200c\u0647\u0627\u06cc \u0628\u0631\u0646\u0627\u0645\u0647\u200c\u0646\u0648\u06cc\u0633\u06cc": ["Python", "JavaScript", "PHP", "C#", "SQL"],
        "\u0633\u0627\u06cc\u0631 \u0645\u0647\u0627\u0631\u062a\u200c\u0647\u0627": ["\u0648\u06cc\u0631\u0627\u06cc\u0634 \u0639\u0644\u0645\u06cc", "\u0646\u0634\u0631 \u0622\u06a9\u0627\u062f\u0645\u06cc\u06a9", "LaTeX", "Git", "Docker"],
    },
    "software": {
        "\u0646\u0631\u0645\u200c\u0627\u0641\u0632\u0627\u0631\u0647\u0627\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc": ["ArcGIS", "QGIS", "RockWorks", "Surfer"],
        "\u0641\u0646\u0627\u0648\u0631\u06cc\u200c\u0647\u0627\u06cc \u0648\u0628": ["HTML5", "CSS3", "Bootstrap", "WordPress", "Laravel"],
    },
    "languages": [
        {"name": "\u0641\u0627\u0631\u0633\u06cc", "level": "\u0632\u0628\u0627\u0646 \u0645\u0627\u062f\u0631\u06cc"},
        {"name": "\u0627\u0646\u06af\u0644\u06cc\u0633\u06cc", "level": "\u062a\u0648\u0627\u0646\u0627\u06cc\u06cc \u06a9\u0627\u0631\u06cc \u062d\u0631\u0641\u0647\u200c\u0627\u06cc"},
        {"name": "\u0641\u0631\u0627\u0646\u0633\u0648\u06cc", "level": "\u062f\u0631 \u062d\u0627\u0644 \u06cc\u0627\u062f\u06af\u06cc\u0631\u06cc"},
    ],
    "memberships": [
        {"role": "\u062f\u0628\u06cc\u0631 \u0648 \u0645\u062f\u06cc\u0631 \u0648\u0628\u200c\u0633\u0627\u06cc\u062a", "period": "\u0641\u0631\u0648\u0631\u062f\u06cc\u0646 \u06f1\u06f4\u06f0\u06f2 \u2013 \u0627\u06a9\u0646\u0648\u0646", "org": "\u0627\u0646\u062c\u0645\u0646 \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0627\u06cc\u0631\u0627\u0646"},
        {"role": "\u0639\u0636\u0648 \u06a9\u0645\u06cc\u062a\u0647 \u0628\u0631\u06af\u0632\u0627\u0631\u06cc", "period": "", "org": "\u067e\u0646\u062c \u0647\u0645\u0627\u06cc\u0634 \u0645\u0644\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0627\u0646\u062c\u0645\u0646 \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0627\u06cc\u0631\u0627\u0646"},
    ],
    "volunteer": [
        {"role": "\u0639\u0636\u0648 \u0627\u0647\u062f\u0627\u06cc \u0639\u0636\u0648 \u0627\u06cc\u0631\u0627\u0646", "period": "", "org": "\u0634\u0645\u0627\u0631\u0647 \u0639\u0636\u0648\u06cc\u062a \u0645\u062a\u0639\u0627\u0642\u0628\u0627\u064b \u0627\u0636\u0627\u0641\u0647 \u0645\u06cc\u200c\u0634\u0648\u062f"},
    ],
}
