# -*- coding: utf-8 -*-
"""
Bakes the publications pages out of the resume pages.

The publications page has no content of its own: it shows four sections
(Research Experience, Books, Conferences, Patents) that are authored once,
on the resume page. That was done in the browser — fetch /resume/index.html,
clone the matching .resume__block sections into #mirror-mount — which kept
the single source of truth but shipped a page that is roughly a viewport
tall until the fetch comes back. The dock is sticky against the bottom of
the document, so when the sections finally arrive the page grows by a couple
of thousand pixels and the bar snaps down with it (measured: 489px, ~18ms
after load). Arriving through a cross-document view transition, that lands
in the middle of the animation and reads as the page jumping.

So the same clone happens here instead, at build time, and the page ships
complete: correct height on the first frame, nothing to snap, and the
sections readable without scripts, exactly as they are on the resume page. The mirror
in app.js stays as a fallback for a mount that is still empty (someone
editing the resume page by hand and previewing before CI has run).

Run from CI on every push (see .github/workflows/update-asset-versions.yml)
before the ?v= stamping, so any asset URLs copied in get stamped too.

Usage:
    python3 build_publications.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

PAGES = ["publications/index.html", "fa/publications/index.html"]

MOUNT_RE = re.compile(r'(<div\s+id="mirror-mount"[^>]*>)', re.S)
BLOCK_OPEN_RE = re.compile(r'<section\b[^>]*\bclass="[^"]*\bresume__block\b[^"]*"[^>]*>')
TITLE_RE = re.compile(r'class="resume__block-title"[^>]*>(.*?)</', re.S)


def matching_close(html, start, tag):
    """Offset just past the </tag> closing the <tag> that opens at `start`.

    Depth counting rather than a parser because the block has to come out of
    the source byte for byte -- reserialising it would quietly reformat
    whitespace that the layout depends on. Comments are skipped so a commented
    out tag cannot throw the count off.
    """
    token_re = re.compile(r"<!--|-->|<%s\b|</%s\s*>" % (tag, tag))
    depth = 0
    pos = start
    in_comment = False
    for m in token_re.finditer(html, start):
        tok = m.group(0)
        if in_comment:
            if tok == "-->":
                in_comment = False
            continue
        if tok == "<!--":
            in_comment = True
        elif tok == "<" + tag:
            depth += 1
        elif tok.startswith("</" + tag):
            depth -= 1
            if depth == 0:
                return m.end()
        pos = m.end()
    raise ValueError("unclosed <%s> at offset %d (scanned to %d)" % (tag, start, pos))


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def collect(source_html, wanted):
    """The wanted .resume__block sections, in the order the page asked for."""
    found = {}
    for m in BLOCK_OPEN_RE.finditer(source_html):
        end = matching_close(source_html, m.start(), "section")
        block = source_html[m.start():end]
        title_m = TITLE_RE.search(block)
        if not title_m:
            continue
        title = strip_tags(title_m.group(1))
        if title in wanted and title not in found:
            # Deliberately not carrying the runtime mirror's .reveal class over.
            # That class starts an element at opacity 0 and waits for an
            # observer to bring it in, which is right for a section that
            # arrives after a fetch and wrong for one that was in the HTML all
            # along -- it would leave the whole page blank without scripts,
            # while the same sections on the resume page just show.
            found[title] = block
    return [found[t] for t in wanted if t in found], [t for t in wanted if t not in found]


def main():
    failed = False
    for rel in PAGES:
        path = ROOT / rel
        html = path.read_text(encoding="utf-8")

        mount = MOUNT_RE.search(html)
        if not mount:
            print("%s: no #mirror-mount" % rel)
            failed = True
            continue

        open_tag = mount.group(1)
        source_rel = re.search(r'data-source="([^"]+)"', open_tag).group(1).lstrip("/")
        titles = [
            t.strip()
            for t in re.search(r'data-titles="([^"]*)"', open_tag).group(1).split("|")
        ]

        source_html = (ROOT / source_rel).read_text(encoding="utf-8")
        blocks, missing = collect(source_html, titles)
        if missing:
            print("%s: no section titled %s in %s" % (rel, ", ".join(missing), source_rel))
            failed = True
            continue

        inner_end = matching_close(html, mount.start(), "div") - len("</div>")
        new_html = (
            html[:mount.end()]
            + "\n" + "\n".join(blocks) + "\n  "
            + html[inner_end:]
        )
        if new_html != html:
            path.write_text(new_html, encoding="utf-8")
            print("%s: mirrored %d sections from %s" % (rel, len(blocks), source_rel))
        else:
            print("%s: already current" % rel)

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
