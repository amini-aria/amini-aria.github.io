# -*- coding: utf-8 -*-
"""
Bakes the SEO layer into the site: a marked block in every page's <head>
and /sitemap.xml.

The pages are hand-edited HTML, and the things Google needs to rank a
person by name are exactly the things that rot when typed by hand into
eight files: a canonical URL, reciprocal hreflang links between each
English page and its Persian twin, Open Graph / Twitter cards with
ABSOLUTE image URLs, and one consistent JSON-LD Person (same @id on both
languages, every spelling of the name, links to the outside profiles).
Before this, the site had none of the first three, and Open Graph only on
the two home pages with a relative image path that social crawlers reject.

So, like build_publications.py, the block is generated instead: this reads
each page's own <title> and <meta name="description"> (those stay
hand-written, they are copy), the identity in seo_data.py, and the jobs,
schools and awards in resume_data.py, and writes everything between
<!-- seo:start --> and <!-- seo:end -->. Run again, it produces the same
bytes, so CI can run it on every push (see
.github/workflows/update-asset-versions.yml, before the ?v= stamping) and
only commits when something actually moved.

On the publications pages the graph also lists the works themselves
(conference papers, books, the patent) with this Person as author or editor,
so the outside records Google already has of them (Civilica, ISBNs) attach
to the same entity. And when seo_data.py has an IndexNow key, the key file
the engines look for is written to the site root as well.

The sitemap carries <lastmod> from git: the last commit touching the page
that is not one of CI's own "[skip ci]" chores, so a cache-stamp bump does
not claim every page changed today. A page that mirrors another one
(publications ← resume, see data-source on #mirror-mount) takes the newer
of the two dates.

Usage:
    python3 scripts/build_seo.py           # rewrite the pages and sitemap.xml
    python3 scripts/build_seo.py --check   # exit 1 if anything would change
"""

import datetime as dt
import html as htmlmod
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import seo_data as S  # noqa: E402

ROOT = Path(__file__).parent.parent

BLOCK_START = "<!-- seo:start"
BLOCK_END = "<!-- seo:end -->"
BLOCK_RE = re.compile(r"<!-- seo:start.*?<!-- seo:end -->\n?", re.S)
HEAD_RE = re.compile(r"<head>(.*?)</head>", re.S)
HTML_LANG_RE = re.compile(r'<html\b[^>]*\blang="([^"]*)"')
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"\s*/?>')
MIRROR_SOURCE_RE = re.compile(r'<div\s+id="mirror-mount"[^>]*\bdata-source="([^"]+)"')

# Anything that belongs to the generated block and must not also appear
# hand-written elsewhere in <head> — two canonicals or two og:titles are
# worse than none.
STRAY_RE = re.compile(
    r'property="og:|property="profile:|name="twitter:|name="robots"|'
    r'name="google-site-verification"|name="msvalidate|'
    r'rel="canonical"|rel="alternate"|application/ld\+json'
)

YEAR_RE = re.compile(r"(?<!\d)(\d{4})(?!\d)")
# "Surname, I. (2025). Title." / "نام، ن. (۱۴۰۴). عنوان." -> the title
CITATION_TITLE_RE = re.compile(r"\([^)]*\)\.\s*(.+)$", re.S)
APPLICATION_NO_RE = re.compile(r"Application No\.?\s*(\d+)")

# A period that has not ended yet, in either language of resume_data.py.
CURRENT_MARKERS = ("Present", "اکنون")
LIST_COMMA = {"en": ", ", "fa": "، "}


class SeoError(ValueError):
    pass


# ---------------------------------------------------------------- helpers

def page_url(rel):
    """'fa/resume/index.html' -> 'https://amini.info/fa/resume/'."""
    tail = rel[: -len("index.html")] if rel.endswith("index.html") else rel
    return S.SITE_URL + "/" + tail


def other_lang(lang):
    return "fa" if lang == "en" else "en"


def attr(value):
    return htmlmod.escape(value, quote=True)


def compact(d):
    """Drop keys whose value is None or an empty list/dict."""
    return {k: v for k, v in d.items() if v not in (None, [], {})}


def is_current(period):
    return any(m in (period or "") for m in CURRENT_MARKERS)


def validate_pages_table(pages):
    by_path = {p["path"]: p for p in pages}
    if len(by_path) != len(pages):
        raise SeoError("seo_data.PAGES lists a path twice")
    for p in pages:
        pair = by_path.get(p["pair"])
        if pair is None:
            raise SeoError("%s: pair %s is not in PAGES" % (p["path"], p["pair"]))
        if pair["pair"] != p["path"]:
            raise SeoError("%s <-> %s: pair is not reciprocal" % (p["path"], p["pair"]))
        if pair["lang"] == p["lang"]:
            raise SeoError("%s <-> %s: pair has the same language" % (p["path"], p["pair"]))
        if pair["kind"] != p["kind"]:
            raise SeoError("%s <-> %s: pair is a different kind of page" % (p["path"], p["pair"]))
    for lang in ("en", "fa"):
        homes = [p for p in pages if p["lang"] == lang and p["kind"] == "home"]
        if len(homes) != 1:
            raise SeoError("PAGES needs exactly one home page for %s" % lang)


def home_page(pages, lang):
    return next(p for p in pages if p["lang"] == lang and p["kind"] == "home")


# ----------------------------------------------------------- structured data

def person_node(lang, data):
    other = other_lang(lang)
    name = S.SITE_NAME[lang]

    job_titles, employers, seen = [], [], set()
    for e in data.get("experience") or []:
        roles = e.get("roles") or [{"role": e.get("role"), "period": e.get("period")}]
        current = [r["role"] for r in roles if r.get("role") and is_current(r.get("period"))]
        if not current:
            continue
        job_titles.extend(current)
        if e.get("org") and e["org"] not in seen:
            seen.add(e["org"])
            employers.append(compact({"@type": "Organization", "name": e["org"], "url": e.get("url")}))

    schools = []
    for ed in data.get("education") or []:
        org = ed.get("org")
        if org:
            schools.append({"@type": "EducationalOrganization",
                            "name": re.split(r"[,،]", org)[0].strip()})

    awards = []
    for h in data.get("honors") or []:
        parts = [h.get("org"), h.get("period")]
        detail = LIST_COMMA[lang].join(p for p in parts if p)
        awards.append("%s (%s)" % (h["title"], detail) if detail else h["title"])

    languages = [{"@type": "Language", "name": l["name"]}
                 for l in data.get("languages") or [] if l.get("name")]

    return compact({
        "@type": "Person",
        "@id": S.PERSON_ID,
        "name": name,
        "alternateName": S.ALTERNATE_NAMES[lang] + [S.SITE_NAME[other]] + S.ALTERNATE_NAMES[other],
        "givenName": S.GIVEN_NAME[lang],
        "familyName": S.FAMILY_NAME[lang],
        "disambiguatingDescription": S.HEADLINE[lang],
        "description": data.get("about"),
        "url": S.SITE_URL + "/",
        "mainEntityOfPage": page_url(home_page(S.PAGES, lang)["path"]),
        "image": {
            "@type": "ImageObject",
            "url": S.SITE_URL + S.PORTRAIT["path"],
            "width": S.PORTRAIT["width"],
            "height": S.PORTRAIT["height"],
            "caption": name,
        },
        "email": S.EMAIL,
        "jobTitle": job_titles,
        "worksFor": employers,
        "alumniOf": schools,
        "memberOf": [compact(dict({"@type": "Organization"}, **m)) for m in S.MEMBER_OF[lang]],
        "award": awards,
        "knowsAbout": S.KNOWS_ABOUT[lang],
        "knowsLanguage": languages,
        "nationality": {"@type": "Country", "name": S.COUNTRY_NAME[lang]},
        "address": {
            "@type": "PostalAddress",
            "addressLocality": S.LOCALITY[lang],
            "addressCountry": S.COUNTRY_CODE,
        },
        "sameAs": S.SAME_AS,
    })


def website_node(lang):
    other = other_lang(lang)
    return {
        "@type": "WebSite",
        "@id": S.WEBSITE_ID,
        "url": S.SITE_URL + "/",
        "name": S.SITE_NAME[lang],
        "alternateName": S.ALTERNATE_NAMES[lang] + [S.SITE_NAME[other]],
        "inLanguage": ["en", "fa"],
        "publisher": {"@id": S.PERSON_ID},
        "author": {"@id": S.PERSON_ID},
        "copyrightHolder": {"@id": S.PERSON_ID},
    }


def first_year(text):
    m = YEAR_RE.search(text or "")
    return m.group(1) if m else None


def book_title(citation):
    m = CITATION_TITLE_RE.search(citation or "")
    return (m.group(1) if m else (citation or "")).strip()


def book_role_key(role):
    r = (role or "").lower()
    if "author" in r:
        return "author"
    if "editor" in r:
        return "editor"
    return "contributor"


def publication_nodes(info, data, data_en):
    """ScholarlyArticle / Book / CreativeWork nodes for the works in
    resume_data: titles in the page's language, dates, ISBNs, URLs and roles
    from the English dict (the Persian one carries Jalali years and Persian
    role names). The lists are index-aligned; check_resume_sync.py fails the
    build when their lengths differ, and a missing English twin here simply
    drops the fields that would have come from it."""
    url = info["url"]

    def twin(key, i):
        items = data_en.get(key) or []
        return items[i] if i < len(items) else {}

    nodes = []
    for i, c in enumerate(data.get("conferences") or []):
        en = twin("conferences", i)
        if not c.get("title"):
            continue
        nodes.append(compact({
            "@type": "ScholarlyArticle",
            "@id": "%s#paper-%d" % (url, i + 1),
            "name": c["title"],
            "author": {"@id": S.PERSON_ID},
            "datePublished": first_year(en.get("period")),
            "url": c.get("url") or en.get("url"),
            "identifier": c.get("doc_id") or en.get("doc_id"),
            "inLanguage": "fa" if "Persian" in (en.get("note") or "") else None,
            "publication": {"@type": "PublicationEvent", "name": c["org"]} if c.get("org") else None,
        }))
    for i, b in enumerate(data.get("books") or []):
        en = twin("books", i)
        title = book_title(b.get("citation"))
        if not title:
            continue
        node = {
            "@type": "Book",
            "@id": "%s#book-%d" % (url, i + 1),
            "name": title,
            "isbn": b.get("isbn") or en.get("isbn"),
            "datePublished": first_year(en.get("citation")),
        }
        node[book_role_key(en.get("role") or b.get("role"))] = {"@id": S.PERSON_ID}
        nodes.append(compact(node))
    for i, p in enumerate(data.get("patents") or []):
        en = twin("patents", i)
        if not p.get("title"):
            continue
        m = APPLICATION_NO_RE.search(en.get("note") or "")
        nodes.append(compact({
            "@type": "CreativeWork",
            "@id": "%s#patent-%d" % (url, i + 1),
            "name": p["title"],
            "genre": "Patent",
            "author": {"@id": S.PERSON_ID},
            "datePublished": first_year(en.get("status")),
            "identifier": m.group(1) if m else None,
            "description": p.get("summary"),
            "url": p.get("url") or en.get("url"),
        }))
    return nodes


def webpage_nodes(info, works=()):
    url = info["url"]
    node = {
        "@type": "ProfilePage" if info["kind"] == "home" else "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": info["title"],
        "description": info["description"],
        "inLanguage": info["lang"],
        "isPartOf": {"@id": S.WEBSITE_ID},
        "primaryImageOfPage": {
            "@type": "ImageObject",
            "url": S.SITE_URL + S.OG_IMAGE["path"],
            "width": S.OG_IMAGE["width"],
            "height": S.OG_IMAGE["height"],
        },
        "dateModified": info["lastmod"],
    }
    if works:
        node["hasPart"] = [{"@id": w["@id"]} for w in works]
    if info["kind"] == "home":
        node["mainEntity"] = {"@id": S.PERSON_ID}
        return [node]

    home = home_page(S.PAGES, info["lang"])
    node["about"] = {"@id": S.PERSON_ID}
    node["breadcrumb"] = {"@id": url + "#breadcrumb"}
    crumbs = {
        "@type": "BreadcrumbList",
        "@id": url + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": home["crumb"], "item": page_url(home["path"])},
            {"@type": "ListItem", "position": 2, "name": info["crumb"], "item": url},
        ],
    }
    return [node, crumbs]


NAV_NAME = {"en": "Site navigation", "fa": "ناوبری سایت"}


def navigation_node(lang):
    """The four pages of this language as SiteNavigationElements. Google says
    sitelinks come from site structure and page titles, not from markup, so
    this is a hint at best; it costs a few hundred bytes and mirrors the
    dock exactly (same order, same targets)."""
    pages = [p for p in S.PAGES if p["lang"] == lang]
    home = home_page(S.PAGES, lang)
    return {
        "@type": "ItemList",
        "@id": page_url(home["path"]) + "#nav",
        "name": NAV_NAME[lang],
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "item": {"@type": "SiteNavigationElement", "name": p["crumb"], "url": page_url(p["path"])},
            }
            for i, p in enumerate(pages)
        ],
    }


def jsonld(info, data, data_en):
    works = publication_nodes(info, data, data_en) if info["kind"] == "publications" else []
    graph = {
        "@context": "https://schema.org",
        "@graph": [person_node(info["lang"], data), website_node(info["lang"])]
        + webpage_nodes(info, works) + works + [navigation_node(info["lang"])],
    }
    text = json.dumps(graph, ensure_ascii=False, indent=2)
    # "</script>" inside a string would end the element early; "<\/" is the
    # same string to a JSON parser and harmless to the HTML one.
    return text.replace("</", "<\\/")


# ------------------------------------------------------------- head block

def render_block(info, data, data_en):
    lang, other = info["lang"], other_lang(info["lang"])
    url, pair_url = info["url"], info["pair_url"]
    en_url, fa_url = (url, pair_url) if lang == "en" else (pair_url, url)
    default_url = en_url if S.DEFAULT_LANG == "en" else fa_url
    og_image = S.SITE_URL + S.OG_IMAGE["path"]
    name = S.SITE_NAME[lang]

    lines = [
        "<!-- seo:start — generated by scripts/build_seo.py from scripts/seo_data.py; do not edit by hand -->",
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">',
        '<meta name="author" content="%s">' % attr(name),
    ]
    if S.SITE_VERIFICATION.get("google"):
        lines.append('<meta name="google-site-verification" content="%s">' % attr(S.SITE_VERIFICATION["google"]))
    if S.SITE_VERIFICATION.get("bing"):
        lines.append('<meta name="msvalidate.01" content="%s">' % attr(S.SITE_VERIFICATION["bing"]))
    lines += [
        '<link rel="canonical" href="%s">' % url,
        '<link rel="alternate" hreflang="en" href="%s">' % en_url,
        '<link rel="alternate" hreflang="fa" href="%s">' % fa_url,
        '<link rel="alternate" hreflang="x-default" href="%s">' % default_url,
    ]
    if info["kind"] == "home":
        lines += [
            '<meta property="og:type" content="profile">',
            '<meta property="profile:first_name" content="%s">' % attr(S.GIVEN_NAME[lang]),
            '<meta property="profile:last_name" content="%s">' % attr(S.FAMILY_NAME[lang]),
        ]
    else:
        lines.append('<meta property="og:type" content="website">')
    lines += [
        '<meta property="og:site_name" content="%s">' % attr(name),
        '<meta property="og:locale" content="%s">' % S.OG_LOCALE[lang],
        '<meta property="og:locale:alternate" content="%s">' % S.OG_LOCALE[other],
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:title" content="%s">' % attr(info["title"]),
        '<meta property="og:description" content="%s">' % attr(info["description"]),
        '<meta property="og:image" content="%s">' % og_image,
        '<meta property="og:image:width" content="%d">' % S.OG_IMAGE["width"],
        '<meta property="og:image:height" content="%d">' % S.OG_IMAGE["height"],
        '<meta property="og:image:alt" content="%s">' % attr(name),
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % attr(info["title"]),
        '<meta name="twitter:description" content="%s">' % attr(info["description"]),
        '<meta name="twitter:image" content="%s">' % og_image,
        '<meta name="twitter:image:alt" content="%s">' % attr(name),
        '<script type="application/ld+json">',
        jsonld(info, data, data_en),
        "</script>",
        BLOCK_END,
    ]
    return "\n".join(lines)


def page_info(page, html):
    rel = page["path"]
    head_m = HEAD_RE.search(html)
    if not head_m:
        raise SeoError("%s: no <head>" % rel)
    lang_m = HTML_LANG_RE.search(html)
    if not lang_m or lang_m.group(1) != page["lang"]:
        raise SeoError('%s: <html lang> is %r, PAGES says %r'
                       % (rel, lang_m and lang_m.group(1), page["lang"]))
    title_m = TITLE_RE.search(head_m.group(1))
    desc_m = DESC_RE.search(head_m.group(1))
    if not title_m or not title_m.group(1).strip():
        raise SeoError("%s: no <title>" % rel)
    if not desc_m or not desc_m.group(1).strip():
        raise SeoError('%s: no <meta name="description">' % rel)

    sources = [rel] + [m.lstrip("/") for m in MIRROR_SOURCE_RE.findall(html)]
    return {
        "path": rel,
        "lang": page["lang"],
        "kind": page["kind"],
        "crumb": page["crumb"],
        "url": page_url(rel),
        "pair_url": page_url(page["pair"]),
        "title": htmlmod.unescape(" ".join(title_m.group(1).split())),
        "description": htmlmod.unescape(desc_m.group(1)),
        "lastmod_paths": sources,
    }


def inject(html, block):
    rel_note = "(page)"
    if BLOCK_RE.search(html):
        new_html = BLOCK_RE.sub(lambda _m: block + "\n", html, count=1)
    else:
        m = DESC_RE.search(html)
        end = html.index("\n", m.end()) + 1 if "\n" in html[m.end():] else m.end()
        new_html = html[:end] + block + "\n" + html[end:]

    head = HEAD_RE.search(new_html).group(1)
    outside = BLOCK_RE.sub("", head)
    stray = STRAY_RE.search(outside)
    if stray:
        raise SeoError("%s: %r is hand-written in <head> outside the seo block; "
                       "remove it, the block provides it" % (rel_note, stray.group(0)))
    if new_html.count(BLOCK_START) != 1:
        raise SeoError("%s: expected exactly one seo block" % rel_note)
    return new_html


# --------------------------------------------------------------- sitemap

def render_sitemap(infos):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for info in infos:
        url, pair_url = info["url"], info["pair_url"]
        en_url, fa_url = (url, pair_url) if info["lang"] == "en" else (pair_url, url)
        default_url = en_url if S.DEFAULT_LANG == "en" else fa_url
        lines += [
            "  <url>",
            "    <loc>%s</loc>" % url,
            "    <lastmod>%s</lastmod>" % info["lastmod"],
            '    <xhtml:link rel="alternate" hreflang="en" href="%s"/>' % en_url,
            '    <xhtml:link rel="alternate" hreflang="fa" href="%s"/>' % fa_url,
            '    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % default_url,
            "  </url>",
        ]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ driver

def render_all(root, data, lastmod):
    """{relative path: new content} for every page in PAGES plus sitemap.xml.

    `data` is {"en": RESUME_EN, "fa": RESUME_FA}; `lastmod(paths)` returns
    the YYYY-MM-DD the newest of those files last changed (injected so the
    tests need no git).
    """
    validate_pages_table(S.PAGES)
    out, infos = {}, []
    for page in S.PAGES:
        rel = page["path"]
        html = (root / rel).read_text(encoding="utf-8")
        info = page_info(page, html)
        info["lastmod"] = lastmod(info["lastmod_paths"])
        try:
            out[rel] = inject(html, render_block(info, data[page["lang"]], data["en"]))
        except SeoError as e:
            raise SeoError(str(e).replace("(page)", rel, 1))
        infos.append(info)
    out["sitemap.xml"] = render_sitemap(infos)
    if S.INDEXNOW_KEY:
        out[S.INDEXNOW_KEY + ".txt"] = S.INDEXNOW_KEY + "\n"
    return out


def git_lastmod(paths):
    def git(*args):
        try:
            return subprocess.check_output(
                ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
            ).strip()
        except (subprocess.CalledProcessError, OSError):
            return ""

    # The newest commit touching any of the paths that is not one of CI's
    # own [skip ci] chores (cache-stamp bumps, regenerated documents, this
    # very block) — those touch every page and say nothing about content.
    stamp = git("log", "-1", "--format=%cI", "--fixed-strings", "--invert-grep",
                "--grep=[skip ci]", "--", *paths)
    if not stamp:
        # A file with no non-chore history yet, or a shallow clone: fall back
        # to the checkout's own commit, then to today.
        stamp = git("log", "-1", "--format=%cI")
    if not stamp:
        return dt.datetime.now(dt.timezone.utc).date().isoformat()
    return stamp[:10]


def load_resume_data():
    spec = importlib.util.spec_from_file_location("resume_data", ROOT / "scripts" / "resume_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {"en": mod.RESUME_EN, "fa": mod.RESUME_FA}


def main(argv):
    check = "--check" in argv
    try:
        outputs = render_all(ROOT, load_resume_data(), git_lastmod)
    except SeoError as e:
        print("build_seo: %s" % e)
        return 1

    changed = []
    for rel, content in outputs.items():
        path = ROOT / rel
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != content:
            changed.append(rel)
            if not check:
                path.write_text(content, encoding="utf-8")

    if check:
        if changed:
            print("build_seo: out of date: %s" % ", ".join(changed))
            print("run `python3 scripts/build_seo.py` and commit the result")
            return 1
        print("build_seo: everything current")
        return 0

    if changed:
        print("build_seo: wrote %s" % ", ".join(changed))
    else:
        print("build_seo: everything current")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
