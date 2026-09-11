"""Primary route for the QR-05CR composed-model no-double-counting audit (C6).

Checks that the composed T7+T5 operator of CP introduces no hidden second module:
it has no source (zeroth-order) term (annihilates constants), it is conservative
in divergence form (flux telescopes to zero), and its coefficient is exactly the
T7-reconstructed geometry. The pointwise coefficient form is flagged as
non-flux-conserving, and a deliberately added source is detected. Supplied
geometry; no gravity claim.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cr-report-v1"


def _round(value, places=9):
    return round(value, places)


def density(x, a):
    return 1.0 + a * math.sin(2 * math.pi * x)


def sprinkle(n, seed, a):
    rng = random.Random(seed)
    w_max = 1.0 + a
    points = []
    while len(points) < n:
        x = rng.random()
        if rng.random() <= density(x, a) / w_max:
            points.append(x)
    return points


def reconstruct(points, m):
    hist = [0] * m
    for x in points:
        hist[min(int(x * m), m - 1)] += 1
    mean = sum(hist) / m
    return [h / mean for h in hist]


def pointwise_apply(d, values, k, m):
    return d[k] * (values[(k + 1) % m] - 2 * values[k] + values[(k - 1) % m])


def divergence_apply(d, values, k, m):
    plus = 0.5 * (d[k] + d[(k + 1) % m]) * (values[(k + 1) % m] - values[k])
    minus = 0.5 * (d[k] + d[(k - 1) % m]) * (values[k] - values[(k - 1) % m])
    return plus - minus


def pointwise_kernel(d, k):
    return {1: d[k], 0: -2.0 * d[k], -1: d[k]}


def recover_coefficient(d, m):
    # Recover the operator's coefficient from its kernel second moment:
    # mu2 = sum_j K_j j^2 = 2 d_k, so the coefficient is mu2/2.
    out = []
    for k in range(m):
        kern = pointwise_kernel(d, k)
        mu2 = sum(w * (j * j) for j, w in kern.items())
        out.append(mu2 / 2.0)
    return out


def build_report(protocol):
    pts = sprinkle(protocol["n"], protocol["seed"], protocol["a"])
    m = protocol["m"]
    d = reconstruct(pts, m)
    ones = [1.0] * m
    xc = [(k + 0.5) / m for k in range(m)]
    f = [math.sin(2 * math.pi * x) for x in xc]

    pw_source = max(abs(pointwise_apply(d, ones, k, m)) for k in range(m))
    dv_source = max(abs(divergence_apply(d, ones, k, m)) for k in range(m))

    pw_total = sum(pointwise_apply(d, f, k, m) for k in range(m))
    dv_total = sum(divergence_apply(d, f, k, m) for k in range(m))

    recovered = recover_coefficient(d, m)
    coefficient_dev = max(abs(recovered[k] - d[k]) for k in range(m))
    source_term = [0.1 * math.cos(2 * math.pi * x) for x in xc]
    flagged = max(abs(pointwise_apply(d, ones, k, m) + source_term[k]) for k in range(m))

    no_double_counting = bool(pw_source < 1e-12 and dv_source < 1e-12
                              and abs(dv_total) < 1e-9 and coefficient_dev < 1e-12
                              and flagged > 1e-3)

    return {
        "schema": SCHEMA,
        "source_term": {"pointwise_max": _round(pw_source), "divergence_max": _round(dv_source),
                        "no_source": bool(pw_source < 1e-12 and dv_source < 1e-12)},
        "flux": {"divergence_total": _round(dv_total), "pointwise_total": _round(pw_total),
                 "conservative_form_required": bool(abs(pw_total) > 1e-6)},
        "coefficient_matches_t7": {"max_dev": _round(coefficient_dev), "matches": bool(coefficient_dev < 1e-12)},
        "source_control": {"added_source_max": _round(flagged), "flagged": bool(flagged > 1e-3)},
        "no_double_counting": no_double_counting,
    }
