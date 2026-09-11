"""Independent reference route for the QR-05CN T7/T5 compatibility witness."""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cn-report-v1"


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


def _counts(points, bins):
    hist = [0] * bins
    for x in points:
        idx = min(int(x * bins), bins - 1)
        hist[idx] += 1
    m = sum(hist) / bins
    return [h / m for h in hist]


def _kde(points, bins, width):
    out = []
    for k in range(bins):
        xc = (k + 0.5) / bins
        acc = 0.0
        for x in points:
            acc += math.exp(-((x - xc) ** 2) / (2.0 * width * width))
        out.append(acc)
    m = sum(out) / bins
    return [v / m for v in out]


def _control(bins, a):
    vals = [1.0 + a * math.cos(2 * math.pi * ((k + 0.5) / bins)) for k in range(bins)]
    m = sum(vals) / bins
    return [v / m for v in vals]


def _corr(u, v):
    n = len(u)
    mu = sum(u) / n
    mv = sum(v) / n
    su = sum((x - mu) ** 2 for x in u)
    sv = sum((x - mv) ** 2 for x in v)
    suv = sum((u[i] - mu) * (v[i] - mv) for i in range(n))
    if su <= 0 or sv <= 0:
        return 0.0
    return suv / math.sqrt(su * sv)


def build_report(protocol):
    pts = sprinkle(protocol["n"], protocol["seed"], protocol["a"])
    p7 = _counts(pts, protocol["bins"])
    d5 = _kde(pts, protocol["bins"], protocol["kde_width"])
    ctrl = _control(protocol["bins"], protocol["a"])
    cd = _corr(p7, d5)
    cc = _corr(p7, ctrl)
    return {
        "schema": SCHEMA,
        "t7_profile": [_round(v) for v in p7],
        "t5_kernel_profile": [_round(v) for v in d5],
        "control_profile": [_round(v) for v in ctrl],
        "corr_derived": _round(cd),
        "corr_control": _round(cc),
        "compatible": cd >= protocol["corr_high"] and cc <= protocol["corr_low"],
    }
