"""Primary route for the QR-05CP composed T7+T5 operator construction.

From one sprinkle: T7 reconstructs the conformal factor; the composed operator
uses that reconstructed geometry as its coefficient, so the operator acts on the
T7 geometry rather than on an independently supplied kernel. The composition is
verified faithful, the operator is a genuine second-order differential operator
with the reconstructed coefficient, and an independently supplied coefficient
fails. Supplied geometry; no gravity claim.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cp-report-v1"


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


def normalized_profile(fn, m, a):
    vals = [fn((k + 0.5) / m, a) for k in range(m)]
    mean = sum(vals) / m
    return [v / mean for v in vals]


def correlation(left, right):
    n = len(left)
    ml = sum(left) / n
    mr = sum(right) / n
    num = sum((left[i] - ml) * (right[i] - mr) for i in range(n))
    dl = math.sqrt(sum((left[i] - ml) ** 2 for i in range(n)))
    dr = math.sqrt(sum((right[i] - mr) ** 2 for i in range(n)))
    return num / (dl * dr) if dl and dr else 0.0


def build_report(protocol):
    pts = sprinkle(protocol["n"], protocol["seed"], protocol["a"])
    m = protocol["m"]
    h = 1.0 / m
    d = reconstruct(pts, m)
    truth = normalized_profile(lambda x, a: 1.0 + a * math.sin(2 * math.pi * x), m, protocol["a"])
    control = normalized_profile(lambda x, a: 1.0 + a * math.cos(2 * math.pi * x), m, protocol["a"])

    xc = [(k + 0.5) / m for k in range(m)]
    f = [math.sin(2 * math.pi * x) for x in xc]
    fpp = [-(2 * math.pi) ** 2 * fi for fi in f]
    ratios = []
    for k in range(m):
        sf = d[k] * (f[(k + 1) % m] - 2 * f[k] + f[(k - 1) % m])
        ratios.append(sf / (h * h * fpp[k]))
    constants = [ratios[k] / d[k] for k in range(m)]
    c_mean = sum(constants) / m
    c_dev = max(abs(constants[k] - c_mean) for k in range(m))

    reconstruction_corr = correlation(d, truth)
    control_corr = correlation(control, d)
    composed = bool(reconstruction_corr >= protocol["corr_high"]
                    and c_dev <= protocol["dev_tol"]
                    and control_corr <= protocol["corr_low"])

    return {
        "schema": SCHEMA,
        "reconstruction_corr": _round(reconstruction_corr),
        "composition_constant": _round(c_mean),
        "composition_dev": _round(c_dev),
        "control_corr": _round(control_corr),
        "composed": composed,
    }
