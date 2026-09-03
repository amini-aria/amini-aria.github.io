# -*- coding: utf-8 -*-
"""
Rewrites the ?v=... cache-busting query string on every CSS/JS
reference across all HTML pages to the current commit's short SHA.

Before this, the version string was a date typed by hand into each
HTML file (e.g. style.css?v=20260802c) — easy to forget to bump, and
when that happened a browser that had already cached the old file kept
serving it silently after a deploy, with no way to tell without a hard
refresh. This runs from CI (see
.github/workflows/update-asset-versions.yml) whenever style.css or
app.js/lab.js actually change, so it's automatic and there's nothing
to remember when editing them by hand.

Usage:
    python3 update_asset_versions.py
"""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent

HTML_FILES = [
    "index.html",
    "resume/index.html",
    "publications/index.html",
    "contact/index.html",
    "fa/index.html",
    "fa/resume/index.html",
    "fa/publications/index.html",
    "fa/contact/index.html",
]

# Matches href="/assets/css/whatever.css" or src="/assets/js/whatever.js",
# with or without an existing ?v=... suffix, and rewrites the suffix.
ASSET_PATTERN = re.compile(
    r'((?:href|src)="/assets/(?:css|js)/[a-zA-Z0-9_.-]+\.(?:css|js))(?:\?v=[^"]*)?(")'
)


def main():
    version = subprocess.check_output(
        ["git", "rev-parse", "--short=10", "HEAD"], cwd=ROOT, text=True
    ).strip()

    changed = []
    for rel in HTML_FILES:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        new_text = ASSET_PATTERN.sub(rf"\1?v={version}\2", text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed.append(rel)

    # The ?v= above only fixes CSS and JS. The HTML page that carries those
    # URLs is itself cached by GitHub Pages (max-age=600) and by the browser's
    # own heuristics, so a visitor can hold a stale page that keeps asking for
    # the previous version of everything, and nothing in the deploy tells them
    # otherwise. Publishing the same stamp as a tiny uncacheable file gives the
    # page a way to ask "am I the current build?" — see the version guard in
    # assets/js/app.js. Written every run, changed or not, so it always agrees
    # with the SHA the assets were stamped with.
    (ROOT / "version.json").write_text(
        '{"v": "%s"}\n' % version, encoding="utf-8"
    )

    if changed:
        print(f"bumped to {version} in: {', '.join(changed)}")
    else:
        print("no HTML files needed a version bump")
    print(f"wrote version.json ({version})")


if __name__ == "__main__":
    main()
