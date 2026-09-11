"""Independent reference route for the QR-05CR no-double-counting audit."""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cr-report-v1"


def _round(value, places=9):
    return round(value, places)


def _rho(x, a):
    return 1.0 + a * math.sin(2 * math.pi * x)


def sprinkle(n, seed, a):
    generator = random.Random(seed)
    top = 1.0 + a
    out = []
    while len(out) < n:
        x = generator.random()
        if generator.random() <= _rho(x, a) / top:
            out.append(x)
    return out


def _reconstruct(points, m):
    hist = [0] * m
    for x in points:
        hist[min(int(x * m), m - 1)] += 1
    mean = sum(hist) / m
    return [h / mean for h in hist]


def _pw(d, values, k, m):
    return d[k] * (values[(k + 1) % m] - 2.0 * values[k] + values[(k - 1) % m])


def _dv(d, values, k, m):
    a = (d[k] + d[(k + 1) % m]) * (values[(k + 1) % m] - values[k])
    b = (d[k] + d[(k - 1) % m]) * (values[k] - values[(k - 1) % m])
    return 0.5 * (a - b)


def build_report(protocol):
    pts = sprinkle(protocol["n"], protocol["seed"], protocol["a"])
    m = protocol["m"]
    d = _reconstruct(pts, m)
    ones = [1.0] * m
    xc = [(k + 0.5) / m for k in range(m)]
    f = [math.sin(2 * math.pi * x) for x in xc]

    pw_source = max(abs(_pw(d, ones, k, m)) for k in range(m))
    dv_source = max(abs(_dv(d, ones, k, m)) for k in range(m))
    pw_total = sum(_pw(d, f, k, m) for k in range(m))
    dv_total = sum(_dv(d, f, k, m) for k in range(m))

    recovered = []
    for k in range(m):
        mu2 = d[k] * 1.0 + (-2.0 * d[k]) * 0.0 + d[k] * 1.0
        recovered.append(mu2 / 2.0)
    coefficient_dev = max(abs(recovered[k] - d[k]) for k in range(m))

    source = [0.1 * math.cos(2 * math.pi * x) for x in xc]
    flagged = max(abs(_pw(d, ones, k, m) + source[k]) for k in range(m))

    no_double_counting = (pw_source < 1e-12 and dv_source < 1e-12
                          and abs(dv_total) < 1e-9 and coefficient_dev < 1e-12 and flagged > 1e-3)

    return {
        "schema": SCHEMA,
        "source_term": {"pointwise_max": _round(pw_source), "divergence_max": _round(dv_source),
                        "no_source": pw_source < 1e-12 and dv_source < 1e-12},
        "flux": {"divergence_total": _round(dv_total), "pointwise_total": _round(pw_total),
                 "conservative_form_required": abs(pw_total) > 1e-6},
        "coefficient_matches_t7": {"max_dev": _round(coefficient_dev), "matches": coefficient_dev < 1e-12},
        "source_control": {"added_source_max": _round(flagged), "flagged": flagged > 1e-3},
        "no_double_counting": no_double_counting,
    }
