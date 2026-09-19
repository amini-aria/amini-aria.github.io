# -*- coding: utf-8 -*-
"""
Tests for scripts/build_seo.py.

Run with:
    python3 -m unittest scripts/test_build_seo.py

They build a throwaway copy of the site's eight pages in a temp folder and
feed the generator small fake resume dicts, so nothing here touches the real
pages or needs git.
"""

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).parent))

import build_seo as B  # noqa: E402
import seo_data as S  # noqa: E402


def basic_page(lang, title, desc, extra_head="", body=""):
    direction = "rtl" if lang == "fa" else "ltr"
    return (
        "<!DOCTYPE html>\n"
        '<html lang="%s" dir="%s">\n'
        "<head>\n"
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        "<title>%s</title>\n"
        '<meta name="description" content="%s">\n'
        "%s"
        '<link rel="icon" href="/assets/img/favicon.svg?v=abc">\n'
        '<link rel="stylesheet" href="/assets/css/style.css?v=abc">\n'
        "</head>\n"
        "<body>%s</body>\n"
        "</html>\n"
    ) % (lang, direction, title, desc, extra_head, body)


DATA_EN = {
    "about": "About EN",
    "education": [
        {"degree": "B.Sc. in Geology", "org": "Uni X, Faculty of Earth Sciences, City, Iran"},
        {"degree": "High School Diploma", "org": "School Y, Town"},
    ],
    "experience": [
        {"org": "Org A", "role": "CEO", "period": "Jul 2025 – Present", "url": "https://a.example/"},
        {"org": "Org B", "roles": [
            {"role": "Director", "period": "Apr 2026 – Present"},
            {"role": "Old Role", "period": "Mar 2023 – Apr 2026"},
        ]},
        {"org": "Org C", "role": "Past Role", "period": "2020 – 2021"},
    ],
    "honors": [{"title": "Award T", "org": "Society S", "period": "2024"}],
    "languages": [{"name": "Persian"}, {"name": "English"}],
    "books": [
        {"citation": "Doe, J., & Amini, M. A. (2025). Rocks of Iran: A Survey.", "role": "Co-author", "isbn": "978-1-00-000000-1"},
        {"citation": "Roe, R. (2026). Editing Sample.", "role": "Scientific Editor", "isbn": "978-1-00-000000-2"},
    ],
    "conferences": [
        {"title": "Paper One", "period": "2024", "org": "43rd Congress - Tehran, Iran", "tag": "Oral Presentation",
         "note": "Author: Mohammad Aria Amini \u00b7 13 pages \u00b7 Persian", "doc_id": "GSI43_064", "url": "https://civilica.com/doc/1/"},
        {"title": "Talk Two", "period": "2025", "org": "Global Summit - Berlin", "tag": "Oral Presentation",
         "note": "Authors: A, B"},
    ],
    "patents": [
        {"title": "Patent Title", "status": "Registered \u00b7 2026", "org": "Iranian Patent \u00b7 Owner and Sole Inventor",
         "note": "Application No. 140450140003008805 \u00b7 Filed 18 Dec 2025", "summary": "What it does.",
         "url": "https://ipm.example/patent"},
    ],
}

DATA_FA = {
    "about": "درباره فارسی",
    "education": [{"degree": "کارشناسی", "org": "دانشگاه ایکس، دانشکده، شهر"}],
    "experience": [
        {"org": "سازمان الف", "role": "مدیرعامل", "period": "تیر ۱۴۰۴ – اکنون"},
        {"org": "سازمان ج", "role": "گذشته", "period": "۱۳۹۹ – ۱۴۰۰"},
    ],
    "honors": [{"title": "جایزه", "org": "انجمن", "period": "۱۴۰۳"}],
    "languages": [{"name": "فارسی"}],
    "books": [
        {"citation": "دو، ج. و امینی، م. آ. (۱۴۰۴). سنگ‌های ایران: یک بررسی.", "role": "نویسنده همکار", "isbn": "978-1-00-000000-1"},
        {"citation": "رو، ر. (۱۴۰۵). نمونه ویرایش.", "role": "ویراستار علمی", "isbn": "978-1-00-000000-2"},
    ],
    "conferences": [
        {"title": "مقاله یک", "period": "۱۴۰۳", "org": "چهل و سومین گردهمایی - تهران", "doc_id": "GSI43_064", "url": "https://civilica.com/doc/1/"},
        {"title": "سخنرانی دو", "period": "۱۴۰۴", "org": "اجلاس جهانی - برلین"},
    ],
    "patents": [
        {"title": "عنوان اختراع", "status": "ثبت‌شده · ۲۰۲۶", "org": "ثبت اختراع ایران", "note": "شماره اظهارنامه: ۱۴۰۴۵۰۱۴۰۰۰۳۰۰۸۸۰۵",
         "summary": "کاری که می‌کند.", "url": "https://ipm.example/patent"},
    ],
}

DATA = {"en": DATA_EN, "fa": DATA_FA}


def fixed_lastmod(paths):
    return "2026-09-01"


def make_site(root, overrides=None):
    overrides = overrides or {}
    for page in S.PAGES:
        rel = page["path"]
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        html = overrides.get(rel) or basic_page(
            page["lang"], "Title %s" % rel, "Desc %s" % rel
        )
        path.write_text(html, encoding="utf-8")


def jsonld_of(html):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert m, "no JSON-LD block"
    return json.loads(m.group(1))


def node(graph, typ):
    return [n for n in graph["@graph"] if n["@type"] == typ]


class BuildSeoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def render(self, overrides=None, lastmod=fixed_lastmod):
        make_site(self.root, overrides)
        return B.render_all(self.root, DATA, lastmod)

    # -- placement -------------------------------------------------------

    def test_block_is_inserted_right_after_the_description(self):
        out = self.render()
        html = out["resume/index.html"]
        desc_end = html.index('<meta name="description"')
        start = html.index(B.BLOCK_START)
        end = html.index(B.BLOCK_END)
        icon = html.index('<link rel="icon"')
        self.assertLess(desc_end, start)
        self.assertLess(end, icon)
        self.assertEqual(html.count(B.BLOCK_START), 1)

    def test_rendering_twice_changes_nothing(self):
        first = self.render()
        for rel, content in first.items():
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        second = B.render_all(self.root, DATA, fixed_lastmod)
        self.assertEqual(first, second)
        # And the page outside the block is untouched.
        self.assertIn('<link rel="stylesheet" href="/assets/css/style.css?v=abc">', second["index.html"])

    def test_stray_og_tag_outside_the_block_fails_the_build(self):
        stray = basic_page("en", "T", "D", extra_head='<meta property="og:title" content="old">\n')
        with self.assertRaises(B.SeoError):
            self.render({"index.html": stray})

    def test_hreflang_on_the_language_switcher_is_not_a_stray(self):
        page = basic_page("en", "T", "D", body='<a href="/fa/" hreflang="fa">FA</a>')
        out = self.render({"index.html": page})
        self.assertIn('hreflang="fa">FA</a>', out["index.html"])

    def test_missing_description_fails_the_build(self):
        broken = basic_page("en", "T", "D").replace('<meta name="description" content="D">\n', "")
        with self.assertRaises(B.SeoError):
            self.render({"contact/index.html": broken})

    def test_html_lang_must_match_the_page_table(self):
        wrong = basic_page("en", "T", "D")  # under fa/
        with self.assertRaises(B.SeoError):
            self.render({"fa/contact/index.html": wrong})

    # -- canonical / hreflang / og -----------------------------------------

    def test_canonical_and_hreflang_pairs(self):
        out = self.render()
        fa = out["fa/resume/index.html"]
        self.assertIn('<link rel="canonical" href="https://amini.info/fa/resume/">', fa)
        self.assertIn('<link rel="alternate" hreflang="en" href="https://amini.info/resume/">', fa)
        self.assertIn('<link rel="alternate" hreflang="fa" href="https://amini.info/fa/resume/">', fa)
        self.assertIn('<link rel="alternate" hreflang="x-default" href="https://amini.info/resume/">', fa)
        en = out["resume/index.html"]
        self.assertIn('<link rel="canonical" href="https://amini.info/resume/">', en)
        self.assertIn('<link rel="alternate" hreflang="x-default" href="https://amini.info/resume/">', en)

    def test_open_graph_uses_absolute_urls_and_locales(self):
        out = self.render()
        fa = out["fa/index.html"]
        self.assertIn('<meta property="og:url" content="https://amini.info/fa/">', fa)
        self.assertIn('<meta property="og:image" content="https://amini.info/assets/img/og-image.jpg">', fa)
        self.assertIn('<meta property="og:locale" content="fa_IR">', fa)
        self.assertIn('<meta property="og:locale:alternate" content="en_US">', fa)
        self.assertIn('<meta property="og:type" content="profile">', fa)
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', fa)
        self.assertIn('<meta property="og:type" content="website">', out["contact/index.html"])

    def test_attribute_values_are_escaped_and_jsonld_is_not(self):
        page = basic_page("en", "Rocks &amp; Minerals", 'Says &quot;hi&quot; &amp; more')
        out = self.render({"contact/index.html": page})
        html = out["contact/index.html"]
        self.assertIn('<meta property="og:title" content="Rocks &amp; Minerals">', html)
        self.assertIn('<meta property="og:description" content="Says &quot;hi&quot; &amp; more">', html)
        page_node = node(jsonld_of(html), "WebPage")[0]
        self.assertEqual(page_node["name"], "Rocks & Minerals")
        self.assertEqual(page_node["description"], 'Says "hi" & more')

    # -- JSON-LD -----------------------------------------------------------

    def test_person_shares_one_id_across_languages_with_all_spellings(self):
        out = self.render()
        en = node(jsonld_of(out["index.html"]), "Person")[0]
        fa = node(jsonld_of(out["fa/index.html"]), "Person")[0]
        self.assertEqual(en["@id"], fa["@id"])
        self.assertEqual(en["name"], "Mohammad Aria Amini")
        self.assertEqual(fa["name"], "محمدآریا امینی")
        self.assertIn("محمدآریا امینی", en["alternateName"])
        self.assertIn("Aria Amini", en["alternateName"])
        self.assertIn("Mohammad Aria Amini", fa["alternateName"])
        self.assertIn("محمد آریا امینی", fa["alternateName"])
        self.assertIn("آریا امینی", fa["alternateName"])
        self.assertEqual(en["url"], "https://amini.info/")
        self.assertEqual(fa["url"], "https://amini.info/")

    def test_current_positions_become_job_titles_and_employers(self):
        out = self.render()
        en = node(jsonld_of(out["resume/index.html"]), "Person")[0]
        self.assertEqual(en["jobTitle"], ["CEO", "Director"])
        self.assertEqual([o["name"] for o in en["worksFor"]], ["Org A", "Org B"])
        self.assertEqual(en["worksFor"][0]["url"], "https://a.example/")
        self.assertEqual([o["name"] for o in en["alumniOf"]], ["Uni X", "School Y"])
        self.assertEqual(en["award"], ["Award T (Society S, 2024)"])
        self.assertEqual(en["description"], "About EN")
        fa = node(jsonld_of(out["fa/resume/index.html"]), "Person")[0]
        self.assertEqual(fa["jobTitle"], ["مدیرعامل"])
        self.assertEqual([o["name"] for o in fa["alumniOf"]], ["دانشگاه ایکس"])

    def test_home_is_a_profile_page_and_subpages_carry_breadcrumbs(self):
        out = self.render()
        home = jsonld_of(out["index.html"])
        self.assertEqual(len(node(home, "ProfilePage")), 1)
        self.assertEqual(node(home, "ProfilePage")[0]["mainEntity"], {"@id": S.PERSON_ID})
        self.assertEqual(node(home, "BreadcrumbList"), [])
        self.assertEqual(node(home, "WebSite")[0]["@id"], S.WEBSITE_ID)
        sub = jsonld_of(out["fa/publications/index.html"])
        self.assertEqual(node(sub, "ProfilePage"), [])
        crumbs = node(sub, "BreadcrumbList")[0]["itemListElement"]
        self.assertEqual([c["item"] for c in crumbs], ["https://amini.info/fa/", "https://amini.info/fa/publications/"])
        self.assertEqual(crumbs[0]["name"], "خانه")
        page = node(sub, "WebPage")[0]
        self.assertEqual(page["inLanguage"], "fa")
        self.assertEqual(page["dateModified"], "2026-09-01")
        self.assertEqual(page["breadcrumb"], {"@id": "https://amini.info/fa/publications/#breadcrumb"})

    def test_script_content_cannot_close_the_script_tag(self):
        data = {"en": dict(DATA_EN, about="x </script><b>y"), "fa": DATA_FA}
        make_site(self.root)
        out = B.render_all(self.root, data, fixed_lastmod)
        html = out["index.html"]
        self.assertNotIn("</script><b>", html)
        self.assertEqual(node(jsonld_of(html), "Person")[0]["description"], "x </script><b>y")

    # -- lastmod / sitemap -------------------------------------------------

    def test_mirrored_pages_take_their_source_into_lastmod(self):
        calls = []

        def spy(paths):
            calls.append(tuple(paths))
            return "2026-09-01"

        mount = '<div id="mirror-mount" data-source="/resume/index.html" data-titles="Books"></div>'
        page = basic_page("en", "T", "D", body=mount)
        self.render({"publications/index.html": page}, lastmod=spy)
        self.assertIn(("publications/index.html", "resume/index.html"), calls)
        self.assertIn(("resume/index.html",), calls)

    def test_sitemap_lists_every_page_with_language_alternates(self):
        out = self.render()
        root = ET.fromstring(out["sitemap.xml"])
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
        urls = root.findall("s:url", ns)
        self.assertEqual(len(urls), len(S.PAGES))
        locs = [u.find("s:loc", ns).text for u in urls]
        self.assertIn("https://amini.info/", locs)
        self.assertIn("https://amini.info/fa/contact/", locs)
        for u in urls:
            self.assertEqual(u.find("s:lastmod", ns).text, "2026-09-01")
            links = {l.get("hreflang"): l.get("href") for l in u.findall("x:link", ns)}
            self.assertEqual(set(links), {"en", "fa", "x-default"})
            self.assertEqual(links["x-default"], links["en"])
            self.assertIn(u.find("s:loc", ns).text, links.values())

    # -- publications structured data ----------------------------------------

    def test_publications_pages_describe_the_works_with_the_person_as_author(self):
        out = self.render()
        g = jsonld_of(out["publications/index.html"])
        papers = node(g, "ScholarlyArticle")
        books = node(g, "Book")
        patents = node(g, "CreativeWork")
        self.assertEqual([p["name"] for p in papers], ["Paper One", "Talk Two"])
        self.assertEqual(papers[0]["author"], {"@id": S.PERSON_ID})
        self.assertEqual(papers[0]["url"], "https://civilica.com/doc/1/")
        self.assertEqual(papers[0]["datePublished"], "2024")
        self.assertEqual(papers[0]["identifier"], "GSI43_064")
        self.assertEqual(papers[0]["inLanguage"], "fa")
        self.assertNotIn("inLanguage", papers[1])
        self.assertEqual(papers[0]["publication"]["name"], "43rd Congress - Tehran, Iran")
        self.assertEqual([b["name"] for b in books], ["Rocks of Iran: A Survey.", "Editing Sample."])
        self.assertEqual(books[0]["author"], {"@id": S.PERSON_ID})
        self.assertEqual(books[0]["isbn"], "978-1-00-000000-1")
        self.assertEqual(books[0]["datePublished"], "2025")
        self.assertEqual(books[1]["editor"], {"@id": S.PERSON_ID})
        self.assertNotIn("author", books[1])
        self.assertEqual(patents[0]["name"], "Patent Title")
        self.assertEqual(patents[0]["genre"], "Patent")
        self.assertEqual(patents[0]["datePublished"], "2026")
        self.assertEqual(patents[0]["identifier"], "140450140003008805")
        self.assertEqual(patents[0]["description"], "What it does.")
        page = node(g, "WebPage")[0]
        self.assertEqual(len(page["hasPart"]), 5)
        self.assertEqual(page["hasPart"][0], {"@id": papers[0]["@id"]})

    def test_persian_publications_take_titles_from_persian_data_and_dates_from_english(self):
        out = self.render()
        g = jsonld_of(out["fa/publications/index.html"])
        books = node(g, "Book")
        self.assertEqual(books[0]["name"], "سنگ‌های ایران: یک بررسی.")
        self.assertEqual(books[0]["datePublished"], "2025")
        self.assertEqual(books[1]["editor"], {"@id": S.PERSON_ID})
        papers = node(g, "ScholarlyArticle")
        self.assertEqual(papers[0]["name"], "مقاله یک")
        self.assertEqual(papers[0]["datePublished"], "2024")
        self.assertEqual(node(g, "CreativeWork")[0]["name"], "عنوان اختراع")

    def test_works_appear_only_on_the_publications_pages(self):
        out = self.render()
        for rel in ("index.html", "resume/index.html", "fa/contact/index.html"):
            g = jsonld_of(out[rel])
            self.assertEqual(node(g, "ScholarlyArticle") + node(g, "Book") + node(g, "CreativeWork"), [], rel)

    def test_publications_survive_missing_or_short_data(self):
        thin = {"en": {k: v for k, v in DATA_EN.items() if k not in ("books", "conferences", "patents")},
                "fa": dict(DATA_FA, books=[], conferences=DATA_FA["conferences"][:1])}
        make_site(self.root)
        out = B.render_all(self.root, thin, fixed_lastmod)
        g = jsonld_of(out["fa/publications/index.html"])
        self.assertEqual(node(g, "Book"), [])
        self.assertEqual(len(node(g, "ScholarlyArticle")), 1)
        self.assertNotIn("datePublished", node(g, "ScholarlyArticle")[0])

    def test_every_page_lists_its_languages_navigation(self):
        out = self.render()
        for rel, lang, first in (("resume/index.html", "en", "Home"), ("fa/contact/index.html", "fa", "خانه")):
            nav = node(jsonld_of(out[rel]), "ItemList")
            self.assertEqual(len(nav), 1, rel)
            items = nav[0]["itemListElement"]
            self.assertEqual(len(items), 4)
            self.assertEqual(items[0]["item"]["name"], first)
            self.assertEqual(items[0]["item"]["@type"], "SiteNavigationElement")
            self.assertEqual([i["position"] for i in items], [1, 2, 3, 4])
            self.assertTrue(all(i["item"]["url"].startswith("https://amini.info/") for i in items))
            self.assertTrue(all(("/fa/" in i["item"]["url"]) == (lang == "fa") for i in items), rel)

    # -- site verification / IndexNow ----------------------------------------

    def test_verification_tags_only_when_a_code_is_set(self):
        saved = dict(S.SITE_VERIFICATION)
        try:
            S.SITE_VERIFICATION.update({"google": "", "bing": ""})
            out = self.render()
            self.assertNotIn("google-site-verification", out["index.html"])
            self.assertNotIn("msvalidate.01", out["index.html"])
            S.SITE_VERIFICATION.update({"google": "abc123", "bing": "DEF"})
            out = self.render()
            for rel in ("index.html", "fa/resume/index.html"):
                self.assertIn('<meta name="google-site-verification" content="abc123">', out[rel])
                self.assertIn('<meta name="msvalidate.01" content="DEF">', out[rel])
        finally:
            S.SITE_VERIFICATION.clear()
            S.SITE_VERIFICATION.update(saved)

    def test_indexnow_key_file_and_payload(self):
        import indexnow as I
        out = self.render()
        key_file = S.INDEXNOW_KEY + ".txt"
        self.assertEqual(out[key_file], S.INDEXNOW_KEY + "\n")
        payload = I.payload()
        self.assertEqual(payload["host"], "amini.info")
        self.assertEqual(payload["key"], S.INDEXNOW_KEY)
        self.assertEqual(payload["keyLocation"], "https://amini.info/" + key_file)
        self.assertEqual(len(payload["urlList"]), len(S.PAGES))
        self.assertIn("https://amini.info/fa/resume/", payload["urlList"])

    def test_page_table_is_symmetric(self):
        B.validate_pages_table(S.PAGES)
        broken = [dict(p) for p in S.PAGES]
        broken[0]["pair"] = "fa/resume/index.html"
        with self.assertRaises(B.SeoError):
            B.validate_pages_table(broken)


if __name__ == "__main__":
    unittest.main()
