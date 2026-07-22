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
    "contact": "Tehran, Iran  |  mo.aria.am@gmail.com  |  linkedin.com/in/mo-aria-amini  |  amini-aria.github.io",
    "about": (
        "Geologist and researcher working across structural geology, geological mapping, and "
        "computational geoscience \u2014 and, in parallel, the founder of a software company "
        "building tools for the earth-science community."
    ),
    "interests": (
        "Engineering geology, structural geology, geological mapping, GIS and remote sensing, "
        "computational geoscience, scientific publishing, high-performance computing, "
        "geoheritage, and the history of earth sciences."
    ),
    "education": [
        {
            "degree": "B.Sc. in Geology",
            "period": "2022 \u2013 2026",
            "org": "Golestan University, Faculty of Earth Sciences, Gorgan, Iran",
            "notes": [
                "Graduated first in the undergraduate cohort",
                "Completed the program in seven semesters \u2014 one semester ahead of the standard curriculum",
            ],
        },
        {
            "degree": "High School Diploma, Experimental Sciences (Biology)",
            "period": "2014 \u2013 2020",
            "org": "Shahid Beheshti High School (NODET), Ahvaz, Iran",
            "notes": [],
        },
    ],
    # org is the heading; role + period follow on the next line
    "experience": [
        {"org": "Varjavand Intelligent Creative Software Co.", "role": "Chief Executive Officer (CEO)", "period": "Jul 2025 \u2013 Present"},
        {"org": "Aryan Zamin Publishing House", "role": "Director", "period": "Apr 2026 \u2013 Present"},
        {"org": "Shahid Beheshti University, Tehran, Iran", "role": "Research Collaborator", "period": "Feb 2025 \u2013 Present"},
        {"org": "Shahid Beheshti University, Tehran, Iran", "role": "Technical Manager, SARMAD High-Performance Computing (HPC) System", "period": "Feb 2025 \u2013 Present"},
        {"org": "Pars Aryan Zamin Geological Research Institute", "role": "Geologist", "period": "Feb 2023 \u2013 Present"},
        {"org": "JAMSA \u2014 Knowledge-Based Company for Gemology Science and Art Development", "role": "Research & Development (R&D) Manager", "period": "Sep 2024 \u2013 Apr 2025"},
    ],
    "books": [
        {"citation": "Ghorbani, M., & Amini, M. A. (2025). The Historiography of Earth Science in Iran: Contemporary Pioneering Geologists and Their Legacy.", "role": "Co-author"},
        {"citation": "Fathi, T. (2026). Petroleum Contamination Hydrogeology: Geological, Environmental, Legal Aspects, and Models for the Remediation of Contaminated Groundwater.", "role": "Scientific Editor"},
        {"citation": "Momenzadeh, M. (2025). The Mythical City of Zabol: The Burnt City.", "role": "Editor"},
        {"citation": "Salmati, R. (2025). A Comprehensive Guide to Geological Mapping at Scales of 1:50,000 and Larger.", "role": "Editor"},
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
    "contact": "\u062a\u0647\u0631\u0627\u0646\u060c \u0627\u06cc\u0631\u0627\u0646  |  mo.aria.am@gmail.com  |  linkedin.com/in/mo-aria-amini  |  amini-aria.github.io",
    "about": (
        "\u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633 \u0648 \u067e\u0698\u0648\u0647\u0634\u06af\u0631\u06cc \u06a9\u0647 \u062f\u0631 \u062d\u0648\u0632\u0647\u200c\u0647\u0627\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0633\u0627\u062e\u062a\u0645\u0627\u0646\u06cc\u060c "
        "\u0646\u0642\u0634\u0647\u200c\u0628\u0631\u062f\u0627\u0631\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0648 \u0698\u0626\u0648\u0633\u0627\u06cc\u0646\u0633 \u0645\u062d\u0627\u0633\u0628\u0627\u062a\u06cc \u0641\u0639\u0627\u0644\u06cc\u062a \u0645\u06cc\u200c\u06a9\u0646\u062f "
        "\u0648 \u0647\u0645\u200c\u0632\u0645\u0627\u0646\u060c \u0628\u0646\u06cc\u0627\u0646\u200c\u06af\u0630\u0627\u0631 \u06cc\u06a9 \u0634\u0631\u06a9\u062a \u0646\u0631\u0645\u200c\u0627\u0641\u0632\u0627\u0631\u06cc \u0627\u0633\u062a \u06a9\u0647 \u0628\u0631\u0627\u06cc \u062c\u0627\u0645\u0639\u0647\u200c\u06cc \u0639\u0644\u0648\u0645 "
        "\u0632\u0645\u06cc\u0646 \u0627\u0628\u0632\u0627\u0631 \u0645\u06cc\u200c\u0633\u0627\u0632\u062f."
    ),
    "interests": (
        "\u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0645\u0647\u0646\u062f\u0633\u06cc\u060c \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0633\u0627\u062e\u062a\u0645\u0627\u0646\u06cc\u060c \u0646\u0642\u0634\u0647\u200c\u0628\u0631\u062f\u0627\u0631\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc\u060c "
        "\u0633\u06cc\u0633\u062a\u0645 \u0627\u0637\u0644\u0627\u0639\u0627\u062a \u0645\u06a9\u0627\u0646\u06cc \u0648 \u0633\u0646\u062c\u0634 \u0627\u0632 \u062f\u0648\u0631\u060c \u0698\u0626\u0648\u0633\u0627\u06cc\u0646\u0633 \u0645\u062d\u0627\u0633\u0628\u0627\u062a\u06cc\u060c \u0646\u0634\u0631 \u0639\u0644\u0645\u06cc\u060c \u0645\u062d\u0627\u0633\u0628\u0627\u062a "
        "\u0628\u0627 \u06a9\u0627\u0631\u0627\u06cc\u06cc \u0628\u0627\u0644\u0627\u060c \u0645\u06cc\u0631\u0627\u062b \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u0648 \u062a\u0627\u0631\u06cc\u062e \u0639\u0644\u0648\u0645 \u0632\u0645\u06cc\u0646."
    ),
    "education": [
        {
            "degree": "\u06a9\u0627\u0631\u0634\u0646\u0627\u0633\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc",
            "period": "\u06f1\u06f4\u06f0\u06f1 \u2013 \u06f1\u06f4\u06f0\u06f5",
            "org": "\u062f\u0627\u0646\u0634\u06af\u0627\u0647 \u06af\u0644\u0633\u062a\u0627\u0646\u060c \u062f\u0627\u0646\u0634\u06a9\u062f\u0647 \u0639\u0644\u0648\u0645 \u0632\u0645\u06cc\u0646\u060c \u06af\u0631\u06af\u0627\u0646\u060c \u0627\u06cc\u0631\u0627\u0646",
            "notes": [
                "\u0631\u062a\u0628\u0647\u200c\u06cc \u0646\u062e\u0633\u062a \u0648\u0631\u0648\u062f\u06cc \u06a9\u0627\u0631\u0634\u0646\u0627\u0633\u06cc",
                "\u0641\u0631\u0627\u063a\u062a \u0627\u0632 \u062a\u062d\u0635\u06cc\u0644 \u062f\u0631 \u0647\u0641\u062a \u0646\u06cc\u0645\u200c\u0633\u0627\u0644 \u2014 \u06cc\u06a9 \u0646\u06cc\u0645\u200c\u0633\u0627\u0644 \u0632\u0648\u062f\u062a\u0631 \u0627\u0632 \u0628\u0631\u0646\u0627\u0645\u0647\u200c\u06cc \u0627\u0633\u062a\u0627\u0646\u062f\u0627\u0631\u062f",
            ],
        },
        {
            "degree": "\u062f\u06cc\u067e\u0644\u0645 \u0639\u0644\u0648\u0645 \u062a\u062c\u0631\u0628\u06cc (\u0632\u06cc\u0633\u062a\u200c\u0634\u0646\u0627\u0633\u06cc)",
            "period": "\u06f1\u06f3\u06f9\u06f3 \u2013 \u06f1\u06f3\u06f9\u06f9",
            "org": "\u062f\u0628\u06cc\u0631\u0633\u062a\u0627\u0646 \u0634\u0647\u06cc\u062f \u0628\u0647\u0634\u062a\u06cc (\u0633\u0645\u067e\u0627\u062f)\u060c \u0627\u0647\u0648\u0627\u0632\u060c \u0627\u06cc\u0631\u0627\u0646",
            "notes": [],
        },
    ],
    "experience": [
        {"org": "\u0634\u0631\u06a9\u062a \u0646\u0631\u0645\u200c\u0627\u0641\u0632\u0627\u0631\u06cc \u062e\u0644\u0627\u0642 \u0647\u0648\u0634\u0645\u0646\u062f \u0648\u0631\u062c\u0627\u0648\u0646\u062f", "role": "\u0645\u062f\u06cc\u0631\u0639\u0627\u0645\u0644", "period": "\u062a\u06cc\u0631 \u06f1\u06f4\u06f0\u06f4 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
        {"org": "\u0627\u0646\u062a\u0634\u0627\u0631\u0627\u062a \u0622\u0631\u06cc\u0646 \u0632\u0645\u06cc\u0646", "role": "\u0645\u062f\u06cc\u0631 \u0627\u0646\u062a\u0634\u0627\u0631\u0627\u062a", "period": "\u0641\u0631\u0648\u0631\u062f\u06cc\u0646 \u06f1\u06f4\u06f0\u06f5 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
        {"org": "\u062f\u0627\u0646\u0634\u06af\u0627\u0647 \u0634\u0647\u06cc\u062f \u0628\u0647\u0634\u062a\u06cc\u060c \u062a\u0647\u0631\u0627\u0646", "role": "\u0647\u0645\u06a9\u0627\u0631 \u067e\u0698\u0648\u0647\u0634\u06cc", "period": "\u0628\u0647\u0645\u0646 \u06f1\u06f4\u06f0\u06f3 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
        {"org": "\u062f\u0627\u0646\u0634\u06af\u0627\u0647 \u0634\u0647\u06cc\u062f \u0628\u0647\u0634\u062a\u06cc\u060c \u062a\u0647\u0631\u0627\u0646", "role": "\u0645\u062f\u06cc\u0631 \u0641\u0646\u06cc \u0633\u06cc\u0633\u062a\u0645 \u0627\u0628\u0631\u0631\u0627\u06cc\u0627\u0646\u0647 \u0633\u0631\u0645\u062f", "period": "\u0628\u0647\u0645\u0646 \u06f1\u06f4\u06f0\u06f3 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
        {"org": "\u0645\u0648\u0633\u0633\u0647 \u067e\u0698\u0648\u0647\u0634\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u067e\u0627\u0631\u0633 \u0622\u0631\u06cc\u0646 \u0632\u0645\u06cc\u0646", "role": "\u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633", "period": "\u0628\u0647\u0645\u0646 \u06f1\u06f4\u06f0\u06f1 \u2013 \u0627\u06a9\u0646\u0648\u0646"},
        {"org": "\u062c\u0627\u0645\u0633\u0627 \u2014 \u0634\u0631\u06a9\u062a \u062f\u0627\u0646\u0634\u200c\u0628\u0646\u06cc\u0627\u0646 \u062a\u0648\u0633\u0639\u0647 \u0639\u0644\u0645 \u0648 \u0647\u0646\u0631 \u062c\u0645\u200c\u0634\u0646\u0627\u0633\u06cc", "role": "\u0645\u062f\u06cc\u0631 \u062a\u062d\u0642\u06cc\u0642 \u0648 \u062a\u0648\u0633\u0639\u0647 (R&D)", "period": "\u0634\u0647\u0631\u06cc\u0648\u0631 \u06f1\u06f4\u06f0\u06f3 \u2013 \u0641\u0631\u0648\u0631\u062f\u06cc\u0646 \u06f1\u06f4\u06f0\u06f4"},
    ],
    "books": [
        {"citation": "\u0642\u0631\u0628\u0627\u0646\u06cc\u060c \u0645. \u0648 \u0627\u0645\u06cc\u0646\u06cc\u060c \u0645. \u0622. (\u06f1\u06f4\u06f0\u06f4). \u062a\u0627\u0631\u06cc\u062e\u200c\u0646\u06af\u0627\u0631\u06cc \u0639\u0644\u0648\u0645 \u0632\u0645\u06cc\u0646 \u062f\u0631 \u0627\u06cc\u0631\u0627\u0646: \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u0627\u0646 \u067e\u06cc\u0634\u06af\u0627\u0645 \u0645\u0639\u0627\u0635\u0631 \u0648 \u0645\u06cc\u0631\u0627\u062b \u0622\u0646\u0627\u0646.", "role": "\u0646\u0648\u06cc\u0633\u0646\u062f\u0647 \u0647\u0645\u06a9\u0627\u0631"},
        {"citation": "\u0641\u062a\u062d\u06cc\u060c \u062a. (\u06f1\u06f4\u06f0\u06f5). \u0647\u06cc\u062f\u0631\u0648\u0698\u0626\u0648\u0644\u0648\u0698\u06cc \u0622\u0644\u0648\u062f\u06af\u06cc \u0646\u0641\u062a\u06cc: \u062c\u0646\u0628\u0647\u200c\u0647\u0627\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc\u060c \u0632\u06cc\u0633\u062a\u200c\u0645\u062d\u06cc\u0637\u06cc\u060c \u062d\u0642\u0648\u0642\u06cc \u0648 \u0645\u062f\u0644\u200c\u0647\u0627\u06cc \u067e\u0627\u06a9\u200c\u0633\u0627\u0632\u06cc \u0622\u0628\u200c\u0647\u0627\u06cc \u0632\u06cc\u0631\u0632\u0645\u06cc\u0646\u06cc \u0622\u0644\u0648\u062f\u0647.", "role": "\u0648\u06cc\u0631\u0627\u0633\u062a\u0627\u0631 \u0639\u0644\u0645\u06cc"},
        {"citation": "\u0645\u0648\u0645\u0646\u200c\u0632\u0627\u062f\u0647\u060c \u0645. (\u06f1\u06f4\u06f0\u06f4). \u0634\u0647\u0631 \u0627\u0641\u0633\u0627\u0646\u0647\u200c\u0627\u06cc \u0632\u0627\u0628\u0644: \u0634\u0647\u0631 \u0633\u0648\u062e\u062a\u0647.", "role": "\u0648\u06cc\u0631\u0627\u0633\u062a\u0627\u0631"},
        {"citation": "\u0633\u0644\u0645\u0627\u062a\u06cc\u060c \u0631. (\u06f1\u06f4\u06f0\u06f4). \u0631\u0627\u0647\u0646\u0645\u0627\u06cc \u062c\u0627\u0645\u0639 \u0646\u0642\u0634\u0647\u200c\u0628\u0631\u062f\u0627\u0631\u06cc \u0632\u0645\u06cc\u0646\u200c\u0634\u0646\u0627\u0633\u06cc \u062f\u0631 \u0645\u0642\u06cc\u0627\u0633 \u06f1:\u06f5\u06f0\u06f0\u06f0\u06f0 \u0648 \u0628\u0632\u0631\u06af\u200c\u062a\u0631.", "role": "\u0648\u06cc\u0631\u0627\u0633\u062a\u0627\u0631"},
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
