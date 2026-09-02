# -*- coding: utf-8 -*-
"""
Generates assets/js/hero-portrait-data.js and keeps the static skull path
in index.html / fa/index.html in sync with it.

The hero portrait frame is one continuous boundary, not two crossfading
layers: the same <path> data drives the visible stroked frame and the
clip-path around the photo, so when the boundary animates the photo
window changes shape with it.

Two closed shapes, sampled to the same N points so they can be linearly
interpolated point by point:

  - HERO_MORPH_BLOB / HERO_MORPH_BLOB_B: calm organic "living" outlines
    (a few sine harmonics summed over the radius) — the frame's resting
    shape around the photo, continuously cross-fading between the two.
  - HERO_MORPH_SKULL: the outer silhouette of the site's brand mark, the
    dinosaur skull that sits beside the name in the header, mirrored on
    the vertical axis so it faces the same way the portrait does.

The silhouette keeps every one of the mark's own corners — the extra
points needed to reach N are inserted along its longest edges, never in
place of a vertex — so at the end of the morph the boundary is the mark
exactly, not a smoothed approximation of it. N is well above the mark's
own corner count so those fillers also even out the spacing: the teeth
are a dense cluster of corners and the cranium is a few long edges, and
without the fillers that mismatch is what makes the outline crawl
mid-morph. The point order is then
rolled (and reversed if needed) to whichever alignment minimises the
total distance travelled from the blob, which is what keeps the morph
from twisting on its way there.

HERO_SKULL_PATH is the full mark, holes and all, in the same coordinate
space; hero-portrait.js fades it in over the silhouette once the
boundary has actually become that shape.

Usage:
    python3 scripts/gen_hero_portrait.py
"""

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_OUT = ROOT / "assets" / "js" / "hero-portrait-data.js"
HTML_FILES = [ROOT / "index.html", ROOT / "fa" / "index.html"]

N = 320
CX, CY = 50.0, 50.0
TARGET_HALF_EXTENT = 44.0  # stay safely inside the 0-100 viewBox


# ---------------------------------------------------------------- blob ----
def blob_radius(theta):
    """Additive-only waviness (each term in [0, amplitude], never
    negative) so the radius never dips below the base value at any
    angle -- including straight up, where a dip would crop into the top
    of the portrait photo."""
    r = 38.0
    r += 4.0 * (math.sin(3 * theta + 0.6) + 1) / 2
    r += 2.0 * (math.sin(5 * theta + 2.1) + 1) / 2
    return r


def blob_radius_b(theta):
    """A second variant with a larger amplitude and a wider phase and
    frequency separation from blob_radius(); continuously cross-fading
    between the two is what makes the resting frame read as alive."""
    r = 38.0
    r += 3.0 * (math.sin(3 * theta + 2.4) + 1) / 2
    r += 3.0 * (math.sin(4 * theta + 0.3) + 1) / 2
    return r


def pt(r, theta):
    return [round(CX + r * math.cos(theta), 2), round(CY + r * math.sin(theta), 2)]


# --------------------------------------------------------------- skull ----
def read_brand_path():
    """The brand mark is the single source of truth: read it straight out
    of the header rather than keeping a second copy of it here."""
    html = HTML_FILES[0].read_text(encoding="utf-8")
    svg = re.search(r'<span class="brand__mark"[^>]*>(<svg.*?</svg>)</span>', html, re.S)
    if not svg:
        raise RuntimeError("brand__mark svg not found in index.html")
    return re.search(r'<path d="([^"]+)"', svg.group(1)).group(1)


def parse_subpaths(d):
    subs = []
    for chunk in d.split("Z"):
        chunk = chunk.strip()
        if not chunk:
            continue
        pts = [(float(a), float(b))
               for a, b in re.findall(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", chunk)]
        if len(pts) >= 3:
            subs.append(pts)
    if not subs:
        raise RuntimeError("no closed subpaths in brand mark")
    return subs


def transform_all(subs):
    """Mirror on the vertical axis, then scale and centre the whole mark
    so its widest axis spans 2 * TARGET_HALF_EXTENT about (50, 50)."""
    mirrored = [[(-x, y) for x, y in sp] for sp in subs]
    flat = [p for sp in mirrored for p in sp]
    xs = [p[0] for p in flat]
    ys = [p[1] for p in flat]
    mx, my = (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0
    half = max(max(xs) - min(xs), max(ys) - min(ys)) / 2.0
    s = TARGET_HALF_EXTENT / half
    return [[(CX + (x - mx) * s, CY + (y - my) * s) for x, y in sp] for sp in mirrored]


def densify(poly, n):
    """Resample a closed polygon to exactly n points, keeping every
    original vertex and spending the surplus on the longest edges."""
    m = len(poly)
    if n < m:
        raise RuntimeError("cannot keep %d corners in %d points" % (m, n))
    edges = [math.dist(poly[i], poly[(i + 1) % m]) for i in range(m)]
    total = sum(edges)
    surplus = n - m

    # largest-remainder apportionment, so the extra points land where the
    # gaps between corners are actually widest
    exact = [surplus * e / total for e in edges]
    extra = [int(x) for x in exact]
    for i in sorted(range(m), key=lambda i: exact[i] - extra[i], reverse=True)[:surplus - sum(extra)]:
        extra[i] += 1

    out = []
    for i in range(m):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % m]
        out.append((ax, ay))
        for k in range(1, extra[i] + 1):
            f = k / (extra[i] + 1)
            out.append((ax + (bx - ax) * f, ay + (by - ay) * f))
    if len(out) != n:
        raise RuntimeError("densify produced %d points, wanted %d" % (len(out), n))
    return out


def best_alignment(target, reference):
    """Pick the rotation and winding of `target` that leaves each point
    closest to its opposite number in `reference` — the alignment that
    makes the morph travel in a straight line instead of swirling."""
    n = len(reference)
    best, best_cost = None, float("inf")
    for candidate in (target, target[::-1]):
        for off in range(n):
            cost = 0.0
            for i in range(n):
                px, py = candidate[(i + off) % n]
                qx, qy = reference[i]
                cost += (px - qx) ** 2 + (py - qy) ** 2
            if cost < best_cost:
                best_cost, best = cost, [candidate[(i + off) % n] for i in range(n)]
    return best, best_cost


def path_from(subs):
    parts = []
    for sp in subs:
        parts.append("M" + " L".join("%.2f,%.2f" % (x, y) for x, y in sp) + " Z")
    return " ".join(parts)


def sync_html(skull_d):
    tag = '<path class="hero__skull-fill" id="portrait-skull-path" d="{}" fill-rule="evenodd"/>'.format(skull_d)
    pattern = re.compile(r'<path class="hero__skull-fill"[^>]*/>')
    for path in HTML_FILES:
        text = path.read_text(encoding="utf-8")
        new_text, count = pattern.subn(lambda m: tag, text, count=1)
        if count != 1:
            raise RuntimeError("hero__skull-fill path not found in %s" % path)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print("synced", path)
        else:
            print("unchanged", path)


def main():
    thetas = [2 * math.pi * i / N for i in range(N)]
    blob_pts = [pt(blob_radius(t), t) for t in thetas]
    blob_pts_b = [pt(blob_radius_b(t), t) for t in thetas]

    subs = transform_all(parse_subpaths(read_brand_path()))
    outline, cost = best_alignment(densify(subs[0], N), [(p[0], p[1]) for p in blob_pts])
    skull_pts = [[round(x, 2), round(y, 2)] for x, y in outline]

    print("skull: %d subpaths, %d corners kept, mean morph travel %.2f units"
          % (len(subs), len(subs[0]), math.sqrt(cost / N)))

    lines = [
        "/* Generated by scripts/gen_hero_portrait.py — do not hand-edit. */",
        "var HERO_MORPH_BLOB = " + json.dumps(blob_pts) + ";",
        "var HERO_MORPH_BLOB_B = " + json.dumps(blob_pts_b) + ";",
        "var HERO_MORPH_SKULL = " + json.dumps(skull_pts) + ";",
        "",
    ]
    DATA_OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", DATA_OUT)

    sync_html(path_from(subs))


if __name__ == "__main__":
    main()
