# -*- coding: utf-8 -*-
"""
Generates assets/js/hero-portrait-data.js and keeps the static
<g class="hero__ammonite-detail"> markup in index.html / fa/index.html
in sync with it (that markup is the initial paint of the fully-formed
ammonite; hero-portrait.js only animates the blob<->ammonite boundary
morph itself, see that file for the timeline).

Two closed shapes, each sampled at the same N angles from the same
center so they can be linearly interpolated point-by-point:

  - HERO_MORPH_BLOB / HERO_MORPH_BLOB_B: calm organic "living" outlines
    (a few sine harmonics summed over the radius) — the frame's resting
    shape around the portrait photo, continuously cross-fading between
    the two.
  - HERO_MORPH_AMMONITE: the outer silhouette of a scientifically-
    proportioned planispiral ammonite shell (strict lateral view,
    involute coiling — each inner whorl boundary is mathematically the
    same log spiral shifted back by one full turn, so it's guaranteed
    continuous and non-self-intersecting), with a smoothed aperture
    step rather than a hard cliff.

Plus HERO_AMMONITE_WHORLS (the three whorl boundaries beneath the
outer one, each the same spiral one/two/three turns back) and
HERO_AMMONITE_RIBS / HERO_AMMONITE_DIVISIONS (curved growth ribs on
the outer whorl, and denser short chamber divisions on the inner
whorls, both tapering cleanly into the aperture instead of floating
past it) — detail that fades in once the frame has actually become the
ammonite shape.

Usage:
    python3 gen_hero_ammonite.py
"""

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_OUT = ROOT / "assets" / "js" / "hero-portrait-data.js"
HTML_FILES = [ROOT / "index.html", ROOT / "fa" / "index.html"]

N = 120
CX, CY = 50.0, 50.0
TARGET_MAX_RADIUS = 44.0  # stay safely inside the 0-100 viewBox

# ---- scientific ammonite coil ----
WHORL_SHRINK = 0.45   # L(one turn back) / L(here) -> outer whorl ~55% of total
                      # radius, inside the spec's 50-60% band
TOTAL_TURNS = 3.75    # 3 full inner turns + the 3/4-turn outer whorl
PHI_MAX_DEG = TOTAL_TURNS * 360.0
B = -math.log(WHORL_SHRINK) / (2 * math.pi)
FRACTIONAL_TURN_DEG = (TOTAL_TURNS - math.floor(TOTAL_TURNS)) * 360.0  # 270
APERTURE_CLOCK_DEG = 142.5  # aperture tip at ~4:45 o'clock
START_AZIMUTH = APERTURE_CLOCK_DEG - FRACTIONAL_TURN_DEG
SEAM_BLEND = 12.0     # degrees blended across the aperture step -- wide enough
                      # to read as a taper, not a cliff
SX = 1.186            # horizontal-only stretch about the nucleus so the
                      # silhouette reads ~1.3x wider than tall from the
                      # aperture bulge alone, per spec -- the coil growth
                      # itself stays isotropic
N_RIBS = 34
N_DIV = 15
CONVERGE_SPAN = 42.0  # degrees before the seam where ribs shorten toward the aperture


def smoothstep(f):
    f = max(0.0, min(1.0, f))
    return f * f * (3 - 2 * f)


def make_r_c(a0):
    def r_c(phi_deg):
        return a0 * math.exp(B * math.radians(phi_deg))
    return r_c


def layer_radii(clock_deg, r_c):
    """Returns (L0, L1, L2, L3): the outer whorl boundary and the three
    whorls beneath it -- each mathematically the same spiral shifted
    back by one more full turn than the last."""
    base = (clock_deg - START_AZIMUTH) % 360.0

    def radii_for_kmax(kmax):
        phi_top = base + 360.0 * kmax
        return tuple(r_c(phi_top - 360.0 * k) for k in range(4))

    if base < FRACTIONAL_TURN_DEG - SEAM_BLEND:
        return radii_for_kmax(3)
    if base > FRACTIONAL_TURN_DEG + SEAM_BLEND:
        return radii_for_kmax(2)
    lo = radii_for_kmax(3)
    hi = radii_for_kmax(2)
    f = smoothstep((base - (FRACTIONAL_TURN_DEG - SEAM_BLEND)) / (2 * SEAM_BLEND))
    return tuple(a * (1 - f) + b * f for a, b in zip(lo, hi))


def seam_signed_dist(clock_deg):
    base = (clock_deg - START_AZIMUTH) % 360.0
    return (base - FRACTIONAL_TURN_DEG + 180.0) % 360.0 - 180.0


def to_xy(r, clock_deg):
    t = math.radians(clock_deg)
    return (round(CX + SX * r * math.sin(t), 2), round(CY - r * math.cos(t), 2))


def ring_path(radius_fn, n=160):
    pts = [to_xy(radius_fn(360.0 * i / n), 360.0 * i / n) for i in range(n)]
    d = "M{},{} ".format(*pts[0]) + " ".join("L{},{}".format(*p) for p in pts[1:])
    return d + " Z"


def curved_rib(r_in, r_out, clock_deg, curl_deg):
    p_in = to_xy(r_in, clock_deg)
    p_out = to_xy(r_out, clock_deg)
    r_mid = (r_in + r_out) / 2.0
    ctrl = to_xy(r_mid, clock_deg + curl_deg)
    return "M{},{} Q{},{} {},{}".format(p_in[0], p_in[1], ctrl[0], ctrl[1], p_out[0], p_out[1])


def blob_radius(theta):
    """Additive-only waviness (each term in [0, amplitude], never
    negative) so the radius never dips below the base value at any
    angle -- including straight up, where a dip would crop into the
    top of the portrait photo. Base + amplitudes stay within [38, 44]
    (44 is the same safe radius the ammonite fits inside), leaving
    enough swing for the resting-state crossfade to read as a clearly
    moving ripple rather than a barely-visible pulse."""
    r = 38.0
    r += 4.0 * (math.sin(3 * theta + 0.6) + 1) / 2
    r += 2.0 * (math.sin(5 * theta + 2.1) + 1) / 2
    return r


def blob_radius_b(theta):
    """A second variant, same additive-only style, with both a larger
    amplitude and a wider phase/frequency separation from blob_radius()
    than before -- continuously cross-fading between the two is what
    makes the frame read as alive, and the wider separation is what
    makes that motion clearly visible instead of a subtle wobble."""
    r = 38.0
    r += 3.0 * (math.sin(3 * theta + 2.4) + 1) / 2
    r += 3.0 * (math.sin(4 * theta + 0.3) + 1) / 2
    return r


def pt(r, theta):
    return (round(CX + r * math.cos(theta), 2), round(CY + r * math.sin(theta), 2))


def fit_scale():
    """Find the uniform scale on the unit spiral (a0=1) that brings the
    widest axis-aligned extent of the (already SX-stretched) outer
    boundary to TARGET_MAX_RADIUS, so it stays inside the 0-100 viewBox
    no matter how WHORL_SHRINK/SX/TOTAL_TURNS are tuned."""
    r_c_unit = make_r_c(1.0)
    max_dx = max_dy = 0.0
    for i in range(720):
        clock_deg = 360.0 * i / 720
        L0 = layer_radii(clock_deg, r_c_unit)[0]
        x, y = to_xy(L0, clock_deg)
        max_dx = max(max_dx, abs(x - CX))
        max_dy = max(max_dy, abs(y - CY))
    return TARGET_MAX_RADIUS / max(max_dx, max_dy)


def build_ammonite_group(whorls, ribs, divisions):
    parts = ['<path class="ammonite-whorl" d="{}"/>'.format(w) for w in whorls]
    parts += ['<path class="ammonite-rib" d="{}"/>'.format(r) for r in ribs]
    parts += ['<path class="ammonite-division" d="{}"/>'.format(d) for d in divisions]
    return '<g class="hero__ammonite-detail">' + "".join(parts) + "</g>"


def sync_html(new_group):
    pattern = re.compile(r'<g class="hero__ammonite-detail">.*?</g>', re.S)
    for path in HTML_FILES:
        text = path.read_text(encoding="utf-8")
        new_text, count = pattern.subn(lambda m: new_group, text, count=1)
        if count != 1:
            raise RuntimeError("hero__ammonite-detail group not found in {}".format(path))
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print("synced", path)
        else:
            print("unchanged", path)


def main():
    thetas = [2 * math.pi * i / N for i in range(N)]
    blob_pts = [pt(blob_radius(t), t) for t in thetas]
    blob_pts_b = [pt(blob_radius_b(t), t) for t in thetas]

    r_c = make_r_c(fit_scale())

    ammo_pts = []
    for t in thetas:
        clock_deg = (math.degrees(t) + 90.0) % 360.0
        L0 = layer_radii(clock_deg, r_c)[0]
        ammo_pts.append(to_xy(L0, clock_deg))

    whorls = [ring_path(lambda cd, k=k: layer_radii(cd, r_c)[k]) for k in (1, 2, 3)]

    ribs = []
    for i in range(N_RIBS):
        clock_deg = 360.0 * i / N_RIBS
        d = seam_signed_dist(clock_deg)
        if abs(d) < 4.0:
            continue  # skip the rib landing right on the aperture rim itself
        L0, L1, _, _ = layer_radii(clock_deg, r_c)
        r_in, r_out = L1 * 1.03, L0 * 0.96
        if -CONVERGE_SPAN < d < 0:
            # shrink by pulling the inner end toward the rim, so the rib
            # stays anchored to the true outer margin instead of floating
            f = smoothstep(-d / CONVERGE_SPAN)
            r_in = r_in + (r_out - r_in) * 0.6 * f
        ribs.append(curved_rib(r_in, r_out, clock_deg, curl_deg=11.0))

    divisions = []
    for i in range(N_DIV):
        clock_deg = 360.0 * i / N_DIV + (360.0 / N_DIV) / 2.0
        if abs(seam_signed_dist(clock_deg)) < 18.0:
            continue  # keep the umbilicus clean where the whorl tapers fastest
        L0, L1, L2, _ = layer_radii(clock_deg, r_c)
        divisions.append(curved_rib(L2 * 1.05, L1 * 0.97, clock_deg, curl_deg=6.0))

    lines = [
        "/* Generated by scripts/gen_hero_ammonite.py — do not hand-edit. */",
        "var HERO_MORPH_BLOB = " + json.dumps(blob_pts) + ";",
        "var HERO_MORPH_BLOB_B = " + json.dumps(blob_pts_b) + ";",
        "var HERO_MORPH_AMMONITE = " + json.dumps(ammo_pts) + ";",
        "var HERO_AMMONITE_WHORLS = " + json.dumps(whorls) + ";",
        "var HERO_AMMONITE_RIBS = " + json.dumps(ribs) + ";",
        "var HERO_AMMONITE_DIVISIONS = " + json.dumps(divisions) + ";",
        "",
    ]
    DATA_OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", DATA_OUT)

    sync_html(build_ammonite_group(whorls, ribs, divisions))


if __name__ == "__main__":
    main()
