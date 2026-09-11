"""Independent reference route for the QR-05CP composed operator construction."""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cp-report-v1"


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


def _profile(fn, m, a):
    vals = [fn((k + 0.5) / m, a) for k in range(m)]
    mean = sum(vals) / m
    return [v / mean for v in vals]


def _corr(u, v):
    n = len(u)
    mu = sum(u) / n
    mv = sum(v) / n
    su = sum((x - mu) ** 2 for x in u)
    sv = sum((x - mv) ** 2 for x in v)
    suv = sum((u[i] - mu) * (v[i] - mv) for i in range(n))
    return suv / math.sqrt(su * sv) if su > 0 and sv > 0 else 0.0


def build_report(protocol):
    pts = sprinkle(protocol["n"], protocol["seed"], protocol["a"])
    m = protocol["m"]
    h = 1.0 / m
    d = _reconstruct(pts, m)
    truth = _profile(lambda x, a: 1.0 + a * math.sin(2 * math.pi * x), m, protocol["a"])
    control = _profile(lambda x, a: 1.0 + a * math.cos(2 * math.pi * x), m, protocol["a"])

    constants = []
    for k in range(m):
        xk = (k + 0.5) / m
        f = math.sin(2 * math.pi * xk)
        fpp = -(2 * math.pi) ** 2 * f
        fnbrs = (math.sin(2 * math.pi * ((k + 1) % m + 0.5) / m)
                 - 2 * f
                 + math.sin(2 * math.pi * ((k - 1) % m + 0.5) / m))
        ratio = (d[k] * fnbrs) / (h * h * fpp)
        constants.append(ratio / d[k])
    c_mean = sum(constants) / m
    c_dev = max(abs(c - c_mean) for c in constants)

    recon = _corr(d, truth)
    ctrl = _corr(control, d)
    composed = recon >= protocol["corr_high"] and c_dev <= protocol["dev_tol"] and ctrl <= protocol["corr_low"]

    return {
        "schema": SCHEMA,
        "reconstruction_corr": _round(recon),
        "composition_constant": _round(c_mean),
        "composition_dev": _round(c_dev),
        "control_corr": _round(ctrl),
        "composed": composed,
    }
