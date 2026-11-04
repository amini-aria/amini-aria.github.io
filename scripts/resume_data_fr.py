# -*- coding: utf-8 -*-
"""
The French resume (Aria-CV-Fr.docx / .pdf). A plain data file with the same
shape as RESUME_EN in resume_data.py, read by build_resume_docs.py.

There is no French page on the site, so this is kept in sync with RESUME_EN
by hand: when the English entry changes, change it here too.
scripts/check_resume_sync.py fails the build if the two stop having the same
sections and entries.

Wording: French marks gender on job titles (étudiant/étudiante,
directeur/directrice), so roles are written with nouns of function
("Direction", "Assistanat d'enseignement") and epicene titles ("Responsable",
"Spécialiste", "Bénévole"), and the about text avoids agreement altogether.
Coursera course titles and organisations stay in English, as issued.
"""

# French labels for the headings and link text in build_resume_docs.py,
# keyed by the English label used there.
LABELS_FR = {
    "About": "À propos",
    "Interests": "Centres d’intérêt",
    "Education": "Formation",
    "Professional Experience": "Expérience professionnelle",
    "Website: ": "Site web : ",
    "Research & Investigative Experience": "Recherche et investigations",
    "Books": "Livres",
    "ISBN: ": "ISBN : ",
    "Conferences": "Conférences",
    "National Sci-Doc ID: ": "Identifiant national du document scientifique : ",
    "View on Civilica": "Voir sur Civilica",
    "Paper Title:": "Titre de la communication :",
    "Patents": "Brevets",
    "View on Iranian Patent Office": "Voir sur le site de l’office iranien des brevets",
    "View Patent Registration Certificate": "Voir le certificat d’enregistrement du brevet",
    "Teaching Activities": "Activités d’enseignement",
    "Honors & Awards": "Distinctions et prix",
    "Technical & Specialized Skills": "Compétences techniques et spécialisées",
    "Languages": "Langues",
    "Professional Memberships": "Adhésions professionnelles",
    "Voluntary & Social Activities": "Activités bénévoles et sociales",
    "Certificates, Licenses & Courses": "Certificats, licences et formations",
    "View certificate": "Voir le certificat",
    "Certificates": "Certificats",
    "Standard ID ": "Identifiant de norme ",
    "View license": "Voir la licence",
    "Licenses": "Licences",
    "Courses": "Formations",
    "Last updated: ": "Dernière mise à jour : "
}

RESUME_FR = {
    "name": "Mohammad Aria Amini",
    "role": "Master en géologie pétrolière (en cours)",
    "contact_parts": [
        {
            "text": "Téhéran, Iran"
        },
        {
            "text": "aria@amini.info",
            "url": "mailto:aria@amini.info"
        },
        {
            "text": "linkedin.com/in/mo-aria-amini",
            "url": "https://www.linkedin.com/in/mo-aria-amini"
        },
        {
            "text": "amini.info",
            "url": "https://amini.info"
        }
    ],
    "about": "Je m’appelle Mohammad Aria Amini. Je prépare un master en géologie pétrolière et j’exerce des activités de recherche, de rédaction et d’édition scientifique dans le domaine des sciences de la Terre. La recherche, l’écriture et l’édition scientifiques m’intéressent, et je développe en permanence mes connaissances et mes compétences professionnelles en sciences de la Terre.",
    "interests": "Mes intérêts de recherche et mes centres d’intérêt professionnels relèvent principalement des sciences de la Terre, avec un accent particulier sur la géochimie, la géologie pétrolière et les questions liées aux ressources du sous-sol. J’étudie différents domaines de la géologie, notamment les processus géologiques et géochimiques, les roches et les minéraux, les systèmes pétroliers et l’utilisation des données géologiques pour comprendre et évaluer les ressources du sous-sol. Je m’intéresse également à l’application du traitement moderne des données, des méthodes analytiques et des technologies de calcul à la recherche en sciences de la Terre, et je cherche constamment à approfondir mes connaissances et mes compétences dans ces domaines.",
    "education": [
        {
            "degree": "Master en géologie pétrolière",
            "period": "oct. 2026 – aujourd’hui",
            "org": "Université Shahid Beheshti, Téhéran, Iran",
            "notes": []
        },
        {
            "degree": "Licence en géologie",
            "period": "2022 – 2026",
            "org": "Université du Golestan, Faculté des sciences de la Terre, Gorgan, Iran",
            "notes": [
                "Premier rang de la promotion à l’entrée en licence, avec une moyenne de niveau A",
                "Cursus achevé en sept semestres, soit un semestre de moins que le programme standard",
                "6 des 7 semestres effectués à l’Université Shahid Beheshti, Téhéran"
            ]
        },
        {
            "degree": "Diplôme de fin d’études secondaires, sciences expérimentales",
            "period": "2017 – 2020",
            "org": "Lycée pour élèves à haut potentiel Shahid Beheshti (NODET), Ahvaz, Iran",
            "notes": []
        }
    ],
    "experience": [
        {
            "org": "Varjavand Intelligent Creative Software & Hardware Services Co.",
            "role": "Chief Executive Officer (CEO) et présidence du conseil d’administration",
            "period": "juil. 2025 – aujourd’hui",
            "tag": "Temps plein",
            "url": "https://varjavand.org/",
            "url_text": "varjavand.org"
        },
        {
            "org": "Maison d’édition Arian Zamin",
            "roles": [
                {
                    "role": "Direction",
                    "period": "avr. 2026 – aujourd’hui",
                    "tag": "Temps plein"
                },
                {
                    "role": "Spécialiste de l’édition et de la recherche éditoriale",
                    "period": "mars 2023 – avr. 2026",
                    "tag": "Temps partiel"
                }
            ]
        },
        {
            "org": "Centre de recherche géologique Pars (Arian Zamin)",
            "role": "Spécialiste en géologie",
            "period": "févr. 2023 – aujourd’hui",
            "tag": "Temps plein"
        },
        {
            "org": "Gemology Science and Art Development Co. (Gemsa), entreprise fondée sur la connaissance",
            "role": "Responsable recherche et développement (R&D)",
            "period": "sept. 2024 – avr. 2025",
            "tag": "Temps plein"
        }
    ],
    "research": [
        {
            "title": "Stage universitaire",
            "period": "mai 2025 – août 2025",
            "org": "Compagnie nationale iranienne du pétrole",
            "note": "Rapport de stage : National Iranian South Oilfields Company, département des opérations géologiques · Note : A"
        },
        {
            "title": "Recherche et développement",
            "period": "sept. 2024 – avr. 2025",
            "org": "Gemology Science and Art Development Co. (Gemsa)",
            "note": "Recherche sur la spectroscopie Raman par des méthodes spectrophotométriques · Supervision : Pr Fariborz Masoudi (professeur titulaire)"
        },
        {
            "title": "Collaboration de recherche et responsable de l’infrastructure HPC",
            "period": "oct. 2024 – aujourd’hui",
            "org": "Institut des plantes médicinales et des matières premières, Université Shahid Beheshti",
            "note": "Conception, mise en place et exploitation de l’infrastructure de calcul et de l’environnement de traitement du groupe · Assistance directe à l’exécution et à la compilation de code, et accompagnement des utilisateurs · Supervision : Dr Hassan Rezadoost Chahardehi (maître de conférences)",
            "email": "h_rezadoost@sbu.ac.ir"
        },
        {
            "title": "Collaboration de recherche et responsable du centre de calcul (HPC) de chimie physique",
            "period": "avr. 2025 – aujourd’hui",
            "org": "Faculté de chimie et de pétrole, Université Shahid Beheshti, Téhéran",
            "note": "Gestion et développement de l’infrastructure HPC de la faculté au service de la recherche en chimie computationnelle et en chimie physique · Assistance également à la gestion des utilisateurs, à la compilation de code et à l’exécution des calculs · Supervision : Pr Mansour Zahedi (professeur titulaire)",
            "email": "m-zahedi@sbu.ac.ir"
        },
        {
            "title": "Recherche en sciences de la Terre et en pétrole",
            "period": "janv. 2023 – aujourd’hui",
            "org": "Centre de recherche géologique Pars (Arian Zamin)",
            "note": "Recherche en géologie économique, gîtes minéraux et géologie pétrolière, incluant l’analyse de données pétrographiques et géochimiques · Supervision : Pr Mansour Ghorbani (professeur titulaire)",
            "email": "m-ghorbani@sbu.ac.ir"
        }
    ],
    "books": [
        {
            "citation": "Ghorbani, M., et Amini, M. A. (2025). L’historiographie des sciences de la Terre en Iran : présentation de plusieurs pionniers contemporains.",
            "role": "Coécriture",
            "isbn": "978-600-6058-43-6"
        },
        {
            "citation": "Fathi, T. (2026). Hydrogéologie de la contamination pétrolière : aspects géologiques, environnementaux et juridiques, et modèles de dépollution des eaux souterraines contaminées.",
            "role": "Édition scientifique",
            "isbn": "978-600-6058-60-3",
            "isbn_label": "ISBN (à partir de la deuxième édition) : "
        },
        {
            "citation": "Momenzadeh, M. (2025). La cité mythique de Zabol : la Ville brûlée.",
            "role": "Édition",
            "isbn": "978-600-6058-44-3"
        },
        {
            "citation": "Salmati, R. (2025). Guide complet de la cartographie géologique aux échelles du 1/50 000 et supérieures.",
            "role": "Édition",
            "isbn": "978-600-6058-42-9"
        }
    ],
    "conferences": [
        {
            "title": "Natural Resources (Mineral, Energy, and Water Resources) in Iran",
            "period": "2025",
            "org": "4th Global Summit on Advances in Earth Science & Climate Change (Adv. ESCC 2025) - Berlin, Allemagne (présentation à distance)",
            "tag": "Communication orale",
            "note": "Auteurs : Mansour Ghorbani, Mohammad Aria Amini (présentation) · Distinction « Distinguished Speaker » · Organisé par Peers Alley Media · 29-30 sept. 2025"
        },
        {
            "title": "Différences dans la classification des grenats selon la couleur",
            "period": "2024",
            "org": "43e Congrès des sciences de la Terre (conférence nationale) - Téhéran, Iran",
            "tag": "Article de conférence",
            "note": "Auteurs : Ziba Delpasand, Fariborz Masoudi, Mohammad Aria Amini · 10 pages · en persan",
            "doc_id": "GSI43_151",
            "url": "https://civilica.com/doc/2419015/"
        },
        {
            "title": "Étude pétrographique, de la minéralisation et de l’altération du gisement filonien de cuivre de Choudarchay",
            "period": "2024",
            "org": "43e Congrès des sciences de la Terre (conférence nationale) - Téhéran, Iran",
            "tag": "Communication orale",
            "note": "Mohammad Aria Amini · 13 pages · en persan",
            "doc_id": "GSI43_064",
            "url": "https://civilica.com/doc/2418928/"
        },
        {
            "title": "Géologie économique du cuivre et des éléments associés dans le sud de la région de Rayen, avec un accent sur Gadar-e-Siah",
            "period": "2023",
            "org": "42e Congrès des sciences de la Terre (conférence nationale) - Téhéran, Iran",
            "tag": "Communication orale",
            "note": "Auteurs : Mohammad Aria Amini, Shohreh Salkhordeh · 15 pages · en persan",
            "doc_id": "GSI42_161",
            "url": "https://civilica.com/doc/1963822/"
        }
    ],
    "patents": [
        {
            "title": "Système et procédé d’identification et de zonation, tenant compte de la profondeur, des intervalles productifs (net pay) dans les puits de pétrole par fusion probabiliste multimodèle des données diagraphiques",
            "status": "Enregistré · 2026",
            "org": "Brevet iranien · Titulaire, invention individuelle",
            "note": "Demande n° 140450140003008805 · Dépôt : 18 déc. 2025 (1404/09/27) · Enregistrement n° 114471 · Publication : 23 sept. 2026 (1405/07/01) · CIB : E21B 43/00",
            "summary": "Système logiciel tenant compte de la profondeur qui normalise et contrôle la qualité des données diagraphiques de plusieurs puits, construit des variables fondées sur la profondeur, entraîne plusieurs classifieurs, calibre leurs probabilités et les fusionne en étiquettes de zone par profondeur, accompagnées d’un indice d’incertitude.",
            "url": "https://ipm.ssaa.ir/Issue-IssueResult?page=1&DecNo=140450140003008805&IssueId=7007e91773564b4d891344f2a232e917&RN=",
            "certificate_url": "/assets/files/licenses/redacted-image.png"
        }
    ],
    "teaching": [
        {
            "title": "Assistanat d’enseignement (TA) — Services techniques d’ingénierie minière et réglementation minière",
            "period": "févr. 2026 – sept. 2026",
            "org": "Université Shahid Beheshti, Téhéran, Faculté des sciences de la Terre",
            "note": "Cours destiné aux étudiants de géologie en 8e semestre de licence · Supervision : Pr Mansour Ghorbani (professeur titulaire)",
            "email": "m-ghorbani@sbu.ac.ir"
        },
        {
            "title": "Assistanat d’enseignement (TA) — Pétrologie ignée",
            "period": "oct. 2025 – févr. 2026",
            "org": "Université Shahid Beheshti, Téhéran, Faculté des sciences de la Terre",
            "note": "Cours destiné aux étudiants de géologie en 3e semestre de licence · Supervision : Pr Mansour Ghorbani (professeur titulaire)",
            "email": "m-ghorbani@sbu.ac.ir"
        },
        {
            "title": "Assistanat d’enseignement (TA) — Pétrologie ignée",
            "period": "oct. 2024 – févr. 2025",
            "org": "Université Shahid Beheshti, Téhéran, Faculté des sciences de la Terre",
            "note": "Cours destiné aux étudiants de géologie en 3e semestre de licence · Supervision : Pr Mansour Ghorbani (professeur titulaire)",
            "email": "m-ghorbani@sbu.ac.ir"
        },
        {
            "title": "Cycle d’événements et d’ateliers de la Semaine de la recherche",
            "period": "janv. 2026 – févr. 2026",
            "org": "Université Shahid Beheshti, Téhéran",
            "note": "Animation d’atelier · Introduction aux systèmes de traitement parallèle et aux environnements de calcul haute performance sous Linux"
        }
    ],
    "honors": [
        {
            "title": "Distinction « Top Young Earth Sciences Researcher »",
            "period": "2024",
            "org": "Société géologique d’Iran",
            "note": "Décernée pour la communication « Étude pétrographique, de la minéralisation et de l’altération du gisement filonien de cuivre de Choudarchay »"
        }
    ],
    "skills": {
        "Sciences de la Terre et géologie pétrolière": [
            "Géologie pétrolière",
            "Géochimie",
            "Pétrographie et analyse de lames minces",
            "Cartographie géologique",
            "Interprétation de données géologiques",
            "Sédimentologie et stratigraphie",
            "Géologie structurale et tectonique"
        ],
        "Logiciels et outils spécialisés en géosciences": [
            "ArcGIS / ArcGIS Pro",
            "QGIS",
            "Google Earth Engine",
            "ENVI",
            "RockWorks",
            "Petrel"
        ],
        "Programmation, calcul et analyse de données": [
            "Python",
            "MATLAB",
            "C#",
            "JavaScript",
            "PHP",
            "Bash / scripts shell",
            "Analyse et visualisation de données",
            "Modélisation et analyse de données géoscientifiques",
            "Traitement de données à grande échelle",
            "Calcul haute performance (HPC)"
        ],
        "Infrastructure, systèmes et réseaux": [
            "Linux",
            "Administration de systèmes Linux",
            "Administration de serveurs",
            "Réseaux informatiques",
            "Gestion d’infrastructures réseau",
            "Virtualisation et gestion de machines virtuelles",
            "Infrastructure de centres de données",
            "Gestion de serveurs et de ressources de calcul"
        ],
        "Logiciels généraux et outils de productivité": [
            "Microsoft Office (Word, Excel, PowerPoint)",
            "Git",
            "GitHub",
            "Environnements en ligne de commande",
            "Documentation technique"
        ]
    },
    "languages": [
        {
            "name": "Persan",
            "level": "Langue maternelle"
        },
        {
            "name": "Anglais",
            "level": "Compétence professionnelle",
            "tests": [
                {
                    "name": "GRE General Test",
                    "date_range": "Passé le 11 déc. 2024 · Expire le 11 déc. 2029",
                    "summary": "Verbal Reasoning 166/170 · Quantitative Reasoning 166/170 · Analytical Writing 4,0/6,0 (63e centile)"
                },
                {
                    "name": "TOEFL iBT",
                    "date_range": "Passé le 1er janv. 2025 · Expire le 1er janv. 2027",
                    "summary": "Score total 102/120 · Reading 30/30 · Listening 27/30 · Writing 28/30 · Speaking 17/30"
                }
            ]
        },
        {
            "name": "Français",
            "level": "En cours d’apprentissage"
        }
    ],
    "memberships": [
        {
            "role": "Membre de la Société géologique d’Iran",
            "period": "oct. 2022 – aujourd’hui",
            "org": "Membre titulaire de la société, avec également le secrétariat exécutif et la gestion du site web de la Société géologique d’Iran"
        },
        {
            "role": "Membre de la Geological Society of America (GSA)"
        },
        {
            "role": "Membre de l’American Association of Petroleum Geologists (AAPG)"
        }
    ],
    "volunteer": [
        {
            "role": "Bénévole en soutien à l’hôpital et au complexe de réadaptation Mahak et à leurs patients",
            "period": "mars 2023 – aujourd’hui",
            "org": "MAHAK — Association de soutien aux enfants atteints de cancer",
            "notes": [
                "Secours humanitaire et aide en cas de catastrophe · Identifiant MAHAK : 020175959 · N° d’adhésion MAHAK : 10704"
            ]
        },
        {
            "role": "Bénévole, mission d’ambassade pour le don d’organes",
            "period": "avr. 2023 – aujourd’hui",
            "org": "Société iranienne du don d’organes",
            "notes": [
                "Santé"
            ]
        },
        {
            "role": "Bénévole pour le don d’organes",
            "period": "août 2019 – aujourd’hui",
            "org": "Société iranienne du don d’organes",
            "notes": [
                "Secours humanitaire et aide en cas de catastrophe · N° d’adhésion : 3751462 (ehda.ir)"
            ]
        },
        {
            "role": "Bénévole",
            "period": "avr. 2023 – aujourd’hui",
            "org": "Centre d’innovation du Croissant-Rouge iranien",
            "notes": [
                "Secours humanitaire et aide en cas de catastrophe"
            ]
        },
        {
            "role": "Membre de soutien",
            "period": "avr. 2023 – aujourd’hui",
            "org": "Association caritative Raad",
            "notes": [
                "Soutien aux vétérans et aux personnes en situation de handicap physique · N° d’adhésion : 421297",
                "L’association Raad est une organisation caritative privée qui soutient et accompagne les personnes en situation de handicap physique."
            ]
        }
    ],
    "certifications": {
        "specializations": [
            {
                "title": "Petroleum Engineering with AI Applications",
                "meta": "Spécialisation Coursera · 5 cours",
                "courses": [
                    {
                        "title": "Hydrocarbon Exploration and Production",
                        "period": "2025",
                        "id": "EVKUGMGT45RP",
                        "url": "https://www.coursera.org/account/accomplishments/records/EVKUGMGT45RP"
                    },
                    {
                        "title": "From Wellhead to Refinery: Midstream Oil and Gas Processing",
                        "period": "2025",
                        "id": "RO8QDU44OUOL",
                        "url": "https://www.coursera.org/account/accomplishments/records/RO8QDU44OUOL"
                    },
                    {
                        "title": "Natural Gas Production and Processing",
                        "period": "2025",
                        "id": "IGS15UQQFRV4",
                        "url": "https://www.coursera.org/account/accomplishments/records/IGS15UQQFRV4"
                    },
                    {
                        "title": "AI & ML Applications in Oil and Gas Industry",
                        "period": "2025",
                        "id": "O4Y2QT274ZI3",
                        "url": "https://www.coursera.org/account/accomplishments/records/O4Y2QT274ZI3"
                    },
                    {
                        "title": "Utilities, Safety & Environmental Care in Oil & Gas Industry",
                        "period": "2025",
                        "id": "UQWIYV2XAVAV",
                        "url": "https://www.coursera.org/account/accomplishments/records/UQWIYV2XAVAV"
                    }
                ],
                "cred_label": "Voir le certificat de la spécialisation",
                "cred_url": "https://www.coursera.org/account/accomplishments/specialization/B4YTG7OK3VTG"
            },
            {
                "title": "Introduction to Environmental Science",
                "meta": "Spécialisation Coursera · 3 cours",
                "courses": [
                    {
                        "title": "Environmental Science",
                        "period": "2024",
                        "id": "67L7TVDOHCS4",
                        "url": "https://www.coursera.org/account/accomplishments/records/67L7TVDOHCS4"
                    },
                    {
                        "title": "Population, Food, and Soil",
                        "period": "2024",
                        "id": "E1UHZEYRKK2T",
                        "url": "https://www.coursera.org/account/accomplishments/records/E1UHZEYRKK2T"
                    },
                    {
                        "title": "Energy and Environment",
                        "period": "2024",
                        "id": "TAEBBTUG4LV3",
                        "url": "https://www.coursera.org/account/accomplishments/records/TAEBBTUG4LV3"
                    }
                ],
                "cred_label": "Voir le certificat de la spécialisation",
                "cred_url": "https://www.coursera.org/account/accomplishments/specialization/6YGL16PGMYOE"
            },
            {
                "title": "Google Digital Marketing & E-commerce Professional Certificate",
                "meta": "Certificat professionnel Coursera · 7 cours",
                "courses": [
                    {
                        "title": "Foundations of Digital Marketing and E-commerce",
                        "period": "2024",
                        "id": "ADAC17OAAUTM",
                        "url": "https://www.coursera.org/account/accomplishments/records/ADAC17OAAUTM"
                    },
                    {
                        "title": "Attract and Engage Customers with Digital Marketing",
                        "period": "2024",
                        "id": "BYDLT1NC85UY",
                        "url": "https://www.coursera.org/account/accomplishments/records/BYDLT1NC85UY"
                    },
                    {
                        "title": "From Likes to Leads: Interact with Customers Online",
                        "period": "2024",
                        "id": "OY3RTJ0FB1O9",
                        "url": "https://www.coursera.org/account/accomplishments/records/OY3RTJ0FB1O9"
                    },
                    {
                        "title": "Think Outside the Inbox: Email Marketing",
                        "period": "2025",
                        "id": "J8KTD6HZ13TU",
                        "url": "https://www.coursera.org/account/accomplishments/records/J8KTD6HZ13TU"
                    },
                    {
                        "title": "Assess for Success: Marketing Analytics and Measurement",
                        "period": "2025",
                        "id": "Z4TCNOZKS8MI",
                        "url": "https://www.coursera.org/account/accomplishments/records/Z4TCNOZKS8MI"
                    },
                    {
                        "title": "Make the Sale: Build, Launch, and Manage E-commerce Stores",
                        "period": "2025",
                        "id": "TOTMC7EZJCGQ",
                        "url": "https://www.coursera.org/account/accomplishments/records/TOTMC7EZJCGQ"
                    },
                    {
                        "title": "Satisfaction Guaranteed: Develop Customer Loyalty Online",
                        "period": "2025",
                        "id": "7IHL2H68QMKE",
                        "url": "https://www.coursera.org/account/accomplishments/records/7IHL2H68QMKE"
                    }
                ],
                "cred_label": "Voir le certificat professionnel",
                "cred_url": "https://www.coursera.org/account/accomplishments/professional-cert/FUR8P4I0Q1JT"
            }
        ],
        "courses": [
            {
                "title": "Sustainable Neighborhoods",
                "org": "Johns Hopkins University",
                "period": "2025",
                "id": "PD3013GV4N42",
                "url": "https://www.coursera.org/account/accomplishments/records/PD3013GV4N42"
            },
            {
                "title": "Sustainable Transportation Networks and Streetscapes",
                "org": "Johns Hopkins University",
                "period": "2025",
                "id": "BQ9NUFWQ8JHO",
                "url": "https://www.coursera.org/account/accomplishments/records/BQ9NUFWQ8JHO"
            },
            {
                "title": "Wind Energy",
                "org": "Technical University of Denmark (DTU)",
                "period": "2025",
                "id": "BF3120EB7YPC",
                "url": "https://www.coursera.org/account/accomplishments/records/BF3120EB7YPC"
            },
            {
                "title": "Sustainable Regional Principles, Planning and Transportation",
                "org": "Johns Hopkins University",
                "period": "2025",
                "id": "HIHAH8WSFR95",
                "url": "https://www.coursera.org/account/accomplishments/records/HIHAH8WSFR95"
            },
            {
                "title": "Our Earth: Its Climate, History, and Processes",
                "org": "University of Manchester",
                "period": "2023",
                "id": "6Y537YJ5QH9J",
                "url": "https://www.coursera.org/account/accomplishments/records/6Y537YJ5QH9J"
            },
            {
                "title": "Extinctions: Past, Present, & Future",
                "org": "Emory University",
                "period": "2023",
                "id": "EK5WJUBLEB92",
                "url": "https://www.coursera.org/account/accomplishments/records/EK5WJUBLEB92"
            },
            {
                "title": "Electric Power Systems",
                "org": "University at Buffalo",
                "period": "2023",
                "id": "QFFR5N2AQ26W",
                "url": "https://www.coursera.org/account/accomplishments/records/QFFR5N2AQ26W"
            },
            {
                "title": "Introduction to GIS Mapping",
                "org": "University of Toronto",
                "period": "2023",
                "id": "RXDSMTEBNYCY",
                "url": "https://www.coursera.org/account/accomplishments/records/RXDSMTEBNYCY"
            },
            {
                "title": "Solar Energy Basics",
                "org": "The State University of New York",
                "period": "2023",
                "id": "PTMSZ9B6KQ8F",
                "url": "https://www.coursera.org/account/accomplishments/records/PTMSZ9B6KQ8F"
            },
            {
                "title": "Oil & Gas Industry Operations and Markets",
                "org": "Duke University",
                "period": "2023",
                "id": "G7DYSPR7M3RR",
                "url": "https://www.coursera.org/account/accomplishments/records/G7DYSPR7M3RR"
            },
            {
                "title": "Unity: Design & Deform Meshes for 3D Geometry Control",
                "org": "EDUCBA",
                "period": "2025",
                "id": "PAOC4O9D4ALK",
                "url": "https://www.coursera.org/account/accomplishments/records/PAOC4O9D4ALK"
            },
            {
                "title": "Positive Psychiatry and Mental Health",
                "org": "The University of Sydney",
                "period": "2025",
                "id": "LQ39UU674WEF",
                "url": "https://www.coursera.org/account/accomplishments/records/LQ39UU674WEF"
            },
            {
                "title": "Firm Level Economics: Markets and Allocations",
                "org": "University of Illinois Urbana-Champaign",
                "period": "2024",
                "id": "XICPQ5ZM9KSV",
                "url": "https://www.coursera.org/account/accomplishments/records/XICPQ5ZM9KSV"
            },
            {
                "title": "Introduction to Web Development",
                "org": "University of California, Davis",
                "period": "2024",
                "id": "OISIZ0VHN9AP",
                "url": "https://www.coursera.org/account/accomplishments/records/OISIZ0VHN9AP"
            },
            {
                "title": "How to Write and Publish a Scientific Paper",
                "org": "École Polytechnique",
                "period": "2024",
                "id": "TRG7BMSS8Q9I",
                "url": "https://www.coursera.org/account/accomplishments/records/TRG7BMSS8Q9I"
            },
            {
                "title": "Firm Level Economics: Consumer and Producer Behavior",
                "org": "University of Illinois Urbana-Champaign",
                "period": "2024",
                "id": "1JH025ZXSAFZ",
                "url": "https://www.coursera.org/account/accomplishments/records/1JH025ZXSAFZ"
            },
            {
                "title": "Build a Full Website using WordPress",
                "org": "Coursera",
                "period": "2023",
                "id": "FLH3PRW9CBDC",
                "url": "https://www.coursera.org/account/accomplishments/records/FLH3PRW9CBDC"
            },
            {
                "title": "COVID-19 Contact Tracing",
                "org": "Johns Hopkins University",
                "period": "2023",
                "id": "CTXPE9DBBSWB",
                "url": "https://www.coursera.org/account/accomplishments/records/CTXPE9DBBSWB"
            },
            {
                "title": "High Stakes Leadership: Leading in Times of Crisis",
                "org": "University of Michigan",
                "period": "2023",
                "id": "XWTEBYE99LJU",
                "url": "https://www.coursera.org/account/accomplishments/records/XWTEBYE99LJU"
            }
        ],
        "certificates": [
            {
                "title": "Certificat de compétence professionnelle — Développement sous WordPress (CMS)",
                "org": "Organisation iranienne de la formation technique et professionnelle",
                "standard_id": "7321205300201",
                "cert_no": "42245009",
                "period": "2025",
                "url": "/assets/files/certificates/wordpress-cms-developer-certificate.pdf"
            },
            {
                "title": "Certificat de compétence professionnelle — Orfèvrerie",
                "org": "Organisation iranienne de la formation technique et professionnelle",
                "standard_id": "7313207900301",
                "cert_no": "42788555",
                "period": "2025",
                "url": "/assets/files/certificates/goldsmith-certificate.pdf"
            },
            {
                "title": "Petroleum Engineering with AI Applications",
                "org": "Spécialisation Coursera",
                "label": "Voir le certificat de la spécialisation",
                "url": "https://www.coursera.org/account/accomplishments/specialization/B4YTG7OK3VTG"
            },
            {
                "title": "Introduction to Environmental Science",
                "org": "Spécialisation Coursera",
                "label": "Voir le certificat de la spécialisation",
                "url": "https://www.coursera.org/account/accomplishments/specialization/6YGL16PGMYOE"
            },
            {
                "title": "Google Digital Marketing & E-commerce Professional Certificate",
                "org": "Certificat professionnel Coursera",
                "label": "Voir le certificat professionnel",
                "url": "https://www.coursera.org/account/accomplishments/professional-cert/FUR8P4I0Q1JT"
            }
        ],
        "licenses": [
            {
                "title": "Varjavand Intelligent Creative Software Co. — Licence d’activité",
                "org": "Organisation du commerce informatique de la province de Téhéran",
                "url": "/assets/files/licenses/varjavand-company-activity-license.jpg"
            },
            {
                "title": "Licence d’activité à domicile — Intelligence artificielle",
                "url": "/assets/files/licenses/ai-home-business-license.pdf"
            },
            {
                "title": "Licence d’activité à domicile — Conception d’architecture de systèmes logiciels",
                "url": "/assets/files/licenses/software-architecture-home-business-license.pdf"
            },
            {
                "title": "Licence d’activité à domicile — Conception de bijoux et d’orfèvrerie",
                "url": "/assets/files/licenses/jewelry-design-home-business-license.pdf"
            },
            {
                "title": "Licence d’activité à domicile — Taille de pierres précieuses et semi-précieuses",
                "url": "/assets/files/licenses/gemstone-cutting-home-business-license.pdf"
            },
            {
                "title": "Licence d’activité à domicile — Programmation logicielle",
                "url": "/assets/files/licenses/software-programming-home-business-license.pdf"
            },
            {
                "title": "Licence d’activité — Services d’installation et de configuration de logiciels et activités connexes (personne morale)"
            }
        ]
    }
}
