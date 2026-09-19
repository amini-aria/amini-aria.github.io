# -*- coding: utf-8 -*-
"""
Tells the IndexNow search engines (Bing, Yandex, Seznam, Naver) that the
site's pages changed, so they fetch them now rather than on their next
scheduled crawl. Google does not take part in IndexNow; for Google the
sitemap submitted in Search Console is the equivalent.

The key in seo_data.INDEXNOW_KEY is public by design. The engines confirm it
belongs to this host by fetching https://amini.info/<key>.txt, which
build_seo.py writes to the site root. Run from CI at the end of every push
(see .github/workflows/update-asset-versions.yml). All eight pages are sent
each time; the site is small enough that "what changed" is not worth
tracking.

Best-effort: prints the response and always exits 0, so a hiccup at the API
can never fail a deploy.

Usage:
    python3 scripts/indexnow.py
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import seo_data as S  # noqa: E402
from build_seo import page_url  # noqa: E402

ENDPOINT = "https://api.indexnow.org/indexnow"


def payload():
    host = S.SITE_URL.split("://", 1)[-1].rstrip("/")
    return {
        "host": host,
        "key": S.INDEXNOW_KEY,
        "keyLocation": "%s/%s.txt" % (S.SITE_URL, S.INDEXNOW_KEY),
        "urlList": [page_url(p["path"]) for p in S.PAGES],
    }


def main():
    if not S.INDEXNOW_KEY:
        print("indexnow: no key in seo_data.py, nothing sent")
        return 0
    body = payload()
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            # 200 = taken, 202 = taken but the key is not verified yet (the
            # first push, before Pages has published the key file).
            print("indexnow: HTTP %d for %d urls" % (res.status, len(body["urlList"])))
    except urllib.error.HTTPError as e:
        print("indexnow: HTTP %d %s" % (e.code, e.reason))
    except (urllib.error.URLError, OSError) as e:
        print("indexnow: request failed: %s" % e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
