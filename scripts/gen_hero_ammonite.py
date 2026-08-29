# -*- coding: utf-8 -*-
"""
Generates assets/js/hero-portrait-data.js — the point data behind the
hero portrait's frame-to-ammonite morph (see assets/js/hero-portrait.js
for how it's used).

Two closed shapes, each sampled at the same N angles from the same
center so they can be linearly interpolated point-by-point:

  - HERO_MORPH_BLOB: a calm organic "living" outline (a few sine
    harmonics summed over the radius) — the frame's resting shape
    around the portrait photo.
  - HERO_MORPH_AMMONITE: the real outer silhouette of an ammonite
    shell — one full turn of a logarithmic spiral (the actual growth
    curve ammonite shells follow), closed into a loop. The radius
    jump where the turn closes (theta wraps from 2*pi back to 0) is
    softened over a short arc but deliberately kept as a visible
    step: that's the aperture, a real and recognizable feature, not
    an artifact to hide.

Plus HERO_AMMONITE_WHORLS (three more turns of the same spiral,
scaled down by GROWTH_RATIO each time — a real log spiral's earlier
whorls are mathematically just itself shifted by -2*pi, so this is
the same curve reused, not a separate shape) and HERO_AMMONITE_RIBS
(radial lines from near the center out to the outer boundary,
crossing all the whorls) — detail that fades in once the frame has
actually become the ammonite shape. This combination — a tightly
wound multi-turn spiral with full-length radiating ribs — matches the
reference the user provided directly (an ammonite fossil SVG cut-file
design), rather than a scientifically literal single-whorl rendering.

Usage:
    python3 gen_hero_ammonite.py
"""

import json
import math
from pathlib import Path

OUT = Path(__file__).parent.parent / "assets" / "js" / "hero-portrait-data.js"

N = 120
CX, CY = 50.0, 50.0
TARGET_MAX_RADIUS = 44.0  # stay safely inside the 0-100 viewBox
GROWTH_RATIO = 1.8        # how much larger the shell is at the aperture vs. the start
SEAM = 0.4                # radians blended across the aperture seam


def blob_radius(theta):
    """Additive-only waviness (each term in [0, amplitude], never
    negative) so the radius never dips below the base value at any
    angle -- including straight up, where a dip would crop into the
    top of the portrait photo. Kept gentle: this shape only needs to
    read as "softly alive", not dramatically organic."""
    r = 40.0
    r += 2.0 * (math.sin(3 * theta + 0.6) + 1) / 2
    r += 1.0 * (math.sin(5 * theta + 2.1) + 1) / 2
    return r


def blob_radius_b(theta):
    """A second variant, same additive-only style, different phases --
    continuously cross-fading between this and blob_radius() at rest is
    what makes the frame read as alive rather than a static wavy outline."""
    r = 40.0
    r += 1.6 * (math.sin(3 * theta + 2.4) + 1) / 2
    r += 1.4 * (math.sin(4 * theta + 0.3) + 1) / 2
    return r


def make_spiral_radius(a0, b):
    def spiral_radius(theta):
        return a0 * math.exp(b * theta)
    return spiral_radius


def ammonite_radius(theta, spiral_radius):
    t = theta % (2 * math.pi)
    base = spiral_radius(t)
    if t < SEAM:
        end_val = spiral_radius(2 * math.pi)
        f = t / SEAM
        f = f * f * (3 - 2 * f)  # smoothstep
        return end_val * (1 - f) + base * f
    return base


def pt(r, theta):
    return (round(CX + r * math.cos(theta), 2), round(CY + r * math.sin(theta), 2))


def main():
    thetas = [2 * math.pi * i / N for i in range(N)]

    b = math.log(GROWTH_RATIO) / (2 * math.pi)
    spiral_radius = make_spiral_radius(1.0, b)
    raw_max = max(ammonite_radius(t, spiral_radius) for t in thetas)
    a0 = TARGET_MAX_RADIUS / raw_max
    spiral_radius = make_spiral_radius(a0, b)

    # The blob is sized on its own terms (to properly cover the portrait
    # photo, close to TARGET_MAX_RADIUS) rather than scaled to match the
    # ammonite's much smaller mean radius — an earlier version forced them
    # to the same mean size, which shrank the resting blob enough to crop
    # into the photo (most visibly at the top of the head). The morph
    # legitimately contracts as the frame coils into the ammonite shape;
    # that reads as transformation, not a bug.
    blob_pts = [pt(blob_radius(t), t) for t in thetas]
    blob_pts_b = [pt(blob_radius_b(t), t) for t in thetas]
    ammo_pts = [pt(ammonite_radius(t, spiral_radius), t) for t in thetas]

    # three more turns of the same spiral, each scaled down by
    # GROWTH_RATIO — draws as a tightly-wound, multi-turn coil
    def whorl_path(scale, n_points=160):
        pts = []
        for i in range(n_points + 1):
            t = 2 * math.pi * i / n_points
            pts.append(pt(ammonite_radius(t, spiral_radius) * scale, t))
        return "M{},{} ".format(*pts[0]) + " ".join("L{},{}".format(*p) for p in pts[1:])

    whorls = [whorl_path(1 / GROWTH_RATIO), whorl_path(1 / GROWTH_RATIO**2), whorl_path(1 / GROWTH_RATIO**3)]

    # radial ribs from near the center out to the outer edge, crossing all
    # the whorls -- matches the reference cut-file design directly, rather
    # than being confined to a single whorl's band.
    N_RIBS = 26
    ribs = []
    for i in range(N_RIBS):
        t = (2 * math.pi * i / N_RIBS) + 0.1
        r_full = ammonite_radius(t, spiral_radius)
        r_out = r_full * 0.97
        r_in = max(1.5, r_full * 0.06)
        p_out, p_in = pt(r_out, t), pt(r_in, t)
        ribs.append("M{},{} L{},{}".format(*p_in, *p_out))

    lines = [
        "/* Generated by scripts/gen_hero_ammonite.py — do not hand-edit. */",
        "var HERO_MORPH_BLOB = " + json.dumps(blob_pts) + ";",
        "var HERO_MORPH_BLOB_B = " + json.dumps(blob_pts_b) + ";",
        "var HERO_MORPH_AMMONITE = " + json.dumps(ammo_pts) + ";",
        "var HERO_AMMONITE_WHORLS = " + json.dumps(whorls) + ";",
        "var HERO_AMMONITE_RIBS = " + json.dumps(ribs) + ";",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
