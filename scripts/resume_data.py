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
bracketed placeholders on the site (Research Experience, Publications,
Conferences, Teaching, Honors & Awards, Certifications) are intentionally
left out of the downloadable files entirely, since an ATS-optimized resume
should never show empty/placeholder sections.
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
        "I am Mohammad Aria Amini, a researcher, scientific author, and editor specializing in "
        "Earth Sciences. Alongside conducting research and authoring scientific books and "
        "publications, I work in scientific computing, data processing and analysis, and "
        "High-Performance Computing (HPC) for computationally intensive scientific workloads. I "
        "also have experience in software development, Linux systems, server administration, and "
        "computational infrastructure, with a strong interest in integrating geoscience with "
        "modern computing technologies."
    ),
    "interests": (
        "My research and professional interests lie at the intersection of Earth Sciences and "
        "emerging technologies. I am interested in various fields of geology, scientific writing "
        "and editing, the history of Earth Sciences, and the publication of scholarly works. I "
        "also have a strong interest in scientific computing, including computational methods for "
        "pure mathematics, molecular chemistry, and geoscience, as well as High-Performance "
        "Computing (HPC), scientific programming, and the application of computational approaches "
        "to solving research problems. In addition, I am interested in Artificial Intelligence "
        "(AI) and Machine Learning (ML) and their applications in geoscience and related "
        "disciplines, as well as Linux systems, server administration, and computational "
        "infrastructure. Furthermore, I use a range of specialized geoscience and geospatial "
        "software in research projects, including ArcGIS, QGIS, Petrel, ENVI, and ERDAS IMAGINE, "
        "along with other tools for Geographic Information Systems (GIS), Remote Sensing (RS), and "
        "geological modeling. I am continuously expanding my knowledge and expertise in these "
        "technologies and their scientific applications."
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
            "period": "2014 \u2013 2020",
            "org": "Shahid Beheshti Exceptional Talents High School (NODET), Ahvaz, Iran",
            "notes": [],
        },
    ],
    # org is the heading; role + period follow on the next line
    "experience": [
        {"org": "Varjavand Intelligent Creative Software & Hardware Services Co.", "role": "Chief Executive Officer (CEO) and Chairman of the Board", "period": "Jul 2025 \u2013 Present"},
        {"org": "Arian Zamin Publishing House", "role": "Editorial Specialist and Publications Researcher", "period": "Mar 2023 \u2013 Apr 2026"},
        {"org": "Arian Zamin Publishing House", "role": "Director", "period": "Apr 2026 \u2013 Present"},
        {"org": "Shahid Beheshti University, Tehran, Iran", "roles": [
            {"role": "Research Collaborator", "period": "Feb 2025 \u2013 Present"},
            {"role": "Technical Manager, SARMAD High-Performance Computing (HPC) System", "period": "Feb 2025 \u2013 Aug 2026"},
        ]},
        {"org": "Pars Geological Research Center (Arian Zamin)", "role": "Geology Specialist", "period": "Feb 2023 \u2013 Present"},
        {"org": "Gemology Science and Art Development Co. (JAMSA), Knowledge-Based Company", "role": "Research & Development (R&D) Manager", "period": "Sep 2024 \u2013 Apr 2025"},
    ],
    "books": [
        {"citation": "Ghorbani, M., & Amini, M. A. (2025). The Historiography of Earth Science in Iran: Introducing a Number of Contemporary Pioneers.", "role": "Co-author", "isbn": "978-600-6058-43-6"},
        {"citation": "Fathi, T. (2026). Petroleum Contamination Hydrogeology: Geological, Environmental, Legal Aspects, and Models for the Remediation of Contaminated Groundwater.", "role": "Scientific Editor", "isbn": ""},
        {"citation": "Momenzadeh, M. (2025). The Mythical City of Zabol: The Burnt City.", "role": "Editor", "isbn": ""},
        {"citation": "Salmati, R. (2025). A Comprehensive Guide to Geological Mapping at Scales of 1:50,000 and Larger.", "role": "Editor", "isbn": ""},
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
        "من محمدآریا امینی، پژوهشگر، نویسنده و ویراستار علمی در حوزهٔ علوم "
        "زمین هستم. در کنار پژوهش و نگارش کتاب‌ها و نوشتارهای علمی، در "
        "زمینهٔ پردازش و تحلیل داده‌ها، برنامه‌نویسی علمی و رایانش با "
        "کارایی بالا (HPC) برای انجام پردازش‌ها و محاسبات علمی نیز "
        "فعالیت می‌کنم. همچنین در توسعهٔ نرم‌افزار، سامانه‌های "
        "لینوکسی، مدیریت سرورها و زیرساخت‌های رایانشی تجربه دارم "
        "و همواره می‌کوشم دانش زمین‌شناسی را با فناوری‌های نوین "
        "درهم آمیزم."
    ),
    "interests": (
        "علاقه‌مندی‌های پژوهشی و حرفه‌ای من در پیوند میان علوم زمین "
        "و فناوری‌های نوین شکل گرفته است. به پژوهش در شاخه‌های گوناگون "
        "زمین‌شناسی، نگارش و ویراستاری علمی، تاریخ علوم زمین و انتشار "
        "آثار پژوهشی علاقه‌مندم. همچنین به پردازش و تحلیل "
        "داده‌های ریاضیات محض، شیمی مولکولی و زمین‌شناسی، رایانش با "
        "کارایی بالا (HPC)، برنامه‌نویسی علمی و به‌کارگیری روش‌های محاسباتی "
        "در حل مسائل پژوهشی گرایش ویژه‌ای دارم. در کنار این زمینه‌ها، به "
        "هوش مصنوعی و یادگیری ماشین در علوم زمین و شاخه‌های مرتبط با "
        "آن، سامانه‌های لینوکسی، مدیریت سرورها و زیرساخت‌های رایانشی "
        "نیز علاقه‌مندم. افزون بر این، در برخی از پروژه‌های پژوهشی از "
        "نرم‌افزارهای تخصصی زمین‌شناسی و علوم مکانی، از جمله ArcGIS، "
        "QGIS، Petrel، ENVI و ERDAS IMAGINE و دیگر نرم‌افزارهای مرتبط با سامانه‌های "
        "اطلاعات جغرافیایی (GIS)، سنجش از دور (Remote Sensing) و مدل‌سازی "
        "زمین‌شناسی بهره می‌برم و همواره در پی گسترش دانش و مهارت "
        "خود در این ابزارها هستم."
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
            "period": "۱۳۹۳ – ۱۳۹۹",
            "org": "دبیرستان استعداد درخشان شهید بهشتی (سَمپاد)، اهواز، ایران",
            "notes": [],
        },
    ],
    "experience": [
        {"org": "\u0634\u0631\u06a9\u062a \u062e\u062f\u0645\u0627\u062a \u0646\u0631\u0645\u200c\u0627\u0641\u0632\u0627\u0631\u06cc \u0648 \u0633\u062e\u062a\u200c\u0627\u0641\u0632\u0627\u0631\u06cc \u0647\u0648\u0634\u0645\u0646\u062f \u0627\u0641\u0632\u0627\u0631 \u062e\u0644\u0627\u0642 (\u0648\u064e\u0631\u062c\u0627\u0648\u064e\u0646\u062f)", "role": "\u0645\u062f\u06cc\u0631\u0639\u0627\u0645\u0644 \u0648 \u0631\u0626\u06cc\u0633 \u0647\u06cc\u0626\u062a \u0645\u062f\u06cc\u0631\u0647", "period": "\u062a\u06cc\u0631 \u06f1\u06f4\u06f0\u06f4 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
        {"org": "\u0627\u0646\u062a\u0634\u0627\u0631\u0627\u062a \u0622\u0631\u06cc\u0646 \u0632\u0645\u06cc\u0646", "role": "\u06a9\u0627\u0631\u0634\u0646\u0627\u0633 \u0648 \u067e\u0698\u0648\u0647\u0634\u06af\u0631 \u0627\u0646\u062a\u0634\u0627\u0631\u0627\u062a", "period": "\u0627\u0633\u0641\u0646\u062f \u06f1\u06f4\u06f0\u06f1 \u2013 \u0641\u0631\u0648\u0631\u062f\u06cc\u0646 \u06f1\u06f4\u06f0\u06f5"},
        {"org": "\u0627\u0646\u062a\u0634\u0627\u0631\u0627\u062a \u0622\u0631\u06cc\u0646 \u0632\u0645\u06cc\u0646", "role": "\u0645\u062f\u06cc\u0631 \u0627\u0646\u062a\u0634\u0627\u0631\u0627\u062a", "period": "\u0641\u0631\u0648\u0631\u062f\u06cc\u0646 \u06f1\u06f4\u06f0\u06f5 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
        {"org": "\u062f\u0627\u0646\u0634\u06af\u0627\u0647 \u0634\u0647\u06cc\u062f \u0628\u0647\u0634\u062a\u06cc\u060c \u062a\u0647\u0631\u0627\u0646", "roles": [
            {"role": "\u0647\u0645\u06a9\u0627\u0631 \u067e\u0698\u0648\u0647\u0634\u06cc", "period": "\u0628\u0647\u0645\u0646 \u06f1\u06f4\u06f0\u06f3 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
            {"role": "\u0645\u062f\u06cc\u0631 \u0641\u0646\u06cc \u0633\u06cc\u0633\u062a\u0645 \u0627\u0628\u0631\u0631\u0627\u06cc\u0627\u0646\u0647 \u0633\u0631\u0645\u062f", "period": "\u0628\u0647\u0645\u0646 \u06f1\u06f4\u06f0\u06f3 \u2013 \u0645\u0631\u062f\u0627\u062f \u06f1\u06f4\u06f0\u06f5"},
        ]},
        {"org": "\u0645\u0648\u0633\u0633\u0647 \u067e\u0698\u0648\u0647\u0634\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u067e\u0627\u0631\u0633 \u0622\u0631\u06cc\u0646 \u0632\u0645\u06cc\u0646", "role": "\u06a9\u0627\u0631\u0634\u0646\u0627\u0633 \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633", "period": "\u0628\u0647\u0645\u0646 \u06f1\u06f4\u06f0\u06f1 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
        {"org": "\u0634\u0631\u06a9\u062a \u062a\u0648\u0633\u0639\u0647 \u062f\u0627\u0646\u0634 \u0648 \u0647\u0646\u0631 \u06af\u0648\u0647\u0631\u0634\u0646\u0627\u0633\u06cc (\u062c\u0650\u0645\u0633\u0627) - \u062f\u0627\u0646\u0634\u200c\u0628\u0646\u06cc\u0627\u0646", "role": "\u0645\u062f\u06cc\u0631 \u062a\u062d\u0642\u06cc\u0642 \u0648 \u062a\u0648\u0633\u0639\u0647 (R&D)", "period": "\u0634\u0647\u0631\u06cc\u0648\u0631 \u06f1\u06f4\u06f0\u06f3 \u2013 \u0641\u0631\u0648\u0631\u062f\u06cc\u0646 \u06f1\u06f4\u06f0\u06f4"},
    ],
    "books": [
        {"citation": "\u0642\u0631\u0628\u0627\u0646\u06cc\u060c \u0645. \u0648 \u0627\u0645\u06cc\u0646\u06cc\u060c \u0645. \u0622. (\u06f1\u06f4\u06f0\u06f4). \u062a\u0627\u0631\u06cc\u062e\u200c\u0646\u06af\u0627\u0631\u06cc \u062f\u0627\u0646\u0634 \u0639\u0644\u0648\u0645\u200c\u0632\u0645\u06cc\u0646 \u062f\u0631 \u0627\u06cc\u0631\u0627\u0646: \u0628\u0627 \u0645\u0639\u0631\u0641\u06cc \u0634\u0645\u0627\u0631\u06cc \u0627\u0632 \u067e\u06cc\u0634\u06af\u0627\u0645\u0627\u0646 \u0645\u0639\u0627\u0635\u0631.", "role": "\u0646\u0648\u06cc\u0633\u0646\u062f\u0647 \u0647\u0645\u06a9\u0627\u0631", "isbn": "978-600-6058-43-6"},
        {"citation": "\u0641\u062a\u062d\u06cc\u060c \u062a. (\u06f1\u06f4\u06f0\u06f5). \u0647\u06cc\u062f\u0631\u0648\u0698\u0626\u0648\u0644\u0648\u0698\u06cc \u0622\u0644\u0648\u062f\u06af\u06cc \u0646\u0641\u062a\u06cc: \u062c\u0646\u0628\u0647\u200c\u0647\u0627\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc\u060c \u0632\u06cc\u0633\u062a\u200c\u0645\u062d\u06cc\u0637\u06cc\u060c \u062d\u0642\u0648\u0642\u06cc \u0648 \u0645\u062f\u0644\u200c\u0647\u0627\u06cc \u067e\u0627\u06a9\u200c\u0633\u0627\u0632\u06cc \u0622\u0628\u200c\u0647\u0627\u06cc \u0632\u06cc\u0631\u0632\u0645\u06cc\u0646\u06cc \u0622\u0644\u0648\u062f\u0647.", "role": "\u0648\u06cc\u0631\u0627\u0633\u062a\u0627\u0631 \u0639\u0644\u0645\u06cc", "isbn": ""},
        {"citation": "\u0645\u0648\u0645\u0646\u200c\u0632\u0627\u062f\u0647\u060c \u0645. (\u06f1\u06f4\u06f0\u06f4). \u0634\u0647\u0631 \u0627\u0641\u0633\u0627\u0646\u0647\u200c\u0627\u06cc \u0632\u0627\u0628\u0644: \u0634\u0647\u0631 \u0633\u0648\u062e\u062a\u0647.", "role": "\u0648\u06cc\u0631\u0627\u0633\u062a\u0627\u0631", "isbn": ""},
        {"citation": "\u0633\u0644\u0645\u0627\u062a\u06cc\u060c \u0631. (\u06f1\u06f4\u06f0\u06f4). \u0631\u0627\u0647\u0646\u0645\u0627\u06cc \u062c\u0627\u0645\u0639 \u0646\u0642\u0634\u0647\u200c\u0628\u0631\u062f\u0627\u0631\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u062f\u0631 \u0645\u0642\u06cc\u0627\u0633 \u06f1:\u06f5\u06f0\u06f0\u06f0\u06f0 \u0648 \u0628\u0632\u0631\u06af\u200c\u062a\u0631.", "role": "\u0648\u06cc\u0631\u0627\u0633\u062a\u0627\u0631", "isbn": ""},
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
    ],
    "memberships": [
        {"role": "\u062f\u0628\u06cc\u0631 \u0648 \u0645\u062f\u06cc\u0631 \u0648\u0628\u200c\u0633\u0627\u06cc\u062a", "period": "\u0641\u0631\u0648\u0631\u062f\u06cc\u0646 \u06f1\u06f4\u06f0\u06f2 \u2013 \u0627\u06a9\u0646\u0648\u0646", "org": "\u0627\u0646\u062c\u0645\u0646 \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0627\u06cc\u0631\u0627\u0646"},
        {"role": "\u0639\u0636\u0648 \u06a9\u0645\u06cc\u062a\u0647 \u0628\u0631\u06af\u0632\u0627\u0631\u06cc", "period": "", "org": "\u067e\u0646\u062c \u0647\u0645\u0627\u06cc\u0634 \u0645\u0644\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0627\u0646\u062c\u0645\u0646 \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0627\u06cc\u0631\u0627\u0646"},
    ],
    "volunteer": [
        {"role": "\u0639\u0636\u0648 \u0627\u0647\u062f\u0627\u06cc \u0639\u0636\u0648 \u0627\u06cc\u0631\u0627\u0646", "period": "", "org": "\u0634\u0645\u0627\u0631\u0647 \u0639\u0636\u0648\u06cc\u062a \u0645\u062a\u0639\u0627\u0642\u0628\u0627\u064b \u0627\u0636\u0627\u0641\u0647 \u0645\u06cc\u200c\u0634\u0648\u062f"},
    ],
}
