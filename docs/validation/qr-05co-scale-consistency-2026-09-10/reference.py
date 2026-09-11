"""Independent reference route for the QR-05CO scale-consistency witness."""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05co-report-v1"


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


def _hist(points, m):
    hist = [0] * m
    for x in points:
        hist[min(int(x * m), m - 1)] += 1
    return hist


def _norm(hist):
    m = sum(hist) / len(hist)
    return [h / m for h in hist]


def _kde(points, centers, width):
    out = []
    for c in centers:
        acc = 0.0
        for x in points:
            acc += math.exp(-((x - c) ** 2) / (2.0 * width * width))
        out.append(acc)
    m = sum(out) / len(out)
    return [v / m for v in out]


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
    mf = protocol["m_fine"]
    mc = protocol["m_coarse"]
    wf = protocol["kde_width"]

    cf = _hist(pts, mf)
    cc = _hist(pts, mc)
    agg = [cf[2 * k] + cf[2 * k + 1] for k in range(mc)]
    identity = agg == cc

    pf = _norm(cf)
    pc = _norm(cc)
    agg_pf = [(pf[2 * k] + pf[2 * k + 1]) / 2.0 for k in range(mc)]
    geom_dev = max(abs(agg_pf[k] / pc[k] - 1.0) for k in range(mc))

    centers = [(k + 0.5) / mc for k in range(mc)]
    d5f = _kde(pts, centers, wf)
    d5c = _kde(pts, centers, 2.0 * wf)
    op_corr = _corr(d5f, d5c)
    op_scale = (sum(d5f) / mc) / (sum(d5c) / mc)
    op_pw = max(abs(d5f[k] / d5c[k] - 1.0) for k in range(mc))

    raw_ratio = (sum(cc) / mc) / (sum(cf) / mf)
    norm_ratio = (sum(pc) / mc) / (sum(pf) / mf)

    return {
        "schema": SCHEMA,
        "coarse_graining_identity": identity,
        "geometry_ratio_dev": _round(geom_dev),
        "geometry_consistent": geom_dev <= protocol["ratio_tol"],
        "operator_corr": _round(op_corr),
        "operator_scale_ratio": _round(op_scale),
        "operator_pointwise_dev": _round(op_pw),
        "operator_consistent": op_corr >= protocol["corr_high"] and abs(op_scale - 1.0) <= protocol["ratio_tol"],
        "bridge_coarse": _round(_corr(pc, d5c)),
        "bridge_fine": _round(_corr(pc, d5f)),
        "bridge_consistent": _corr(pc, d5c) >= protocol["corr_high"] and _corr(pc, d5f) >= protocol["corr_high"],
        "control": {
            "raw_scale_ratio": _round(raw_ratio),
            "raw_scale_consistent": abs(raw_ratio - 1.0) <= protocol["ratio_tol"],
            "normalized_scale_ratio": _round(norm_ratio),
        },
    }
