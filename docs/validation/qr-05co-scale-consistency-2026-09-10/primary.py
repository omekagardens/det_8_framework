"""Primary route for the QR-05CO T7/T5 scale-consistency witness (C5).

Charter SS7.3: grouping records at different scales must give a consistent
reconstructed geometry AND a consistent T5 operator. Using one sprinkle, we
coarse-grain counts at two bin widths and build the T5 kernel at two matched
bandwidths; the intensive (normalized) reconstruction is scale-consistent while
the raw count is not. Supplied geometry; no gravity claim.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05co-report-v1"


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


def counts(points, m):
    hist = [0] * m
    for x in points:
        hist[min(int(x * m), m - 1)] += 1
    return hist


def normalized(hist):
    mean = sum(hist) / len(hist)
    return [h / mean for h in hist]


def aggregate(fine):
    return [fine[2 * k] + fine[2 * k + 1] for k in range(len(fine) // 2)]


def kde(points, centers, width):
    raw = []
    for c in centers:
        total = sum(math.exp(-((x - c) ** 2) / (2 * width * width)) for x in points)
        raw.append(total)
    mean = sum(raw) / len(raw)
    return [r / mean for r in raw]


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
    mf = protocol["m_fine"]
    mc = protocol["m_coarse"]
    wf = protocol["kde_width"]

    cf = counts(pts, mf)
    cc = counts(pts, mc)
    identity = aggregate(cf) == cc

    pf = normalized(cf)
    pc = normalized(cc)
    agg_pf = [(pf[2 * k] + pf[2 * k + 1]) / 2.0 for k in range(mc)]
    geometry_ratio_dev = max(abs(agg_pf[k] / pc[k] - 1.0) for k in range(mc))

    centers_c = [(k + 0.5) / mc for k in range(mc)]
    d5_fine = kde(pts, centers_c, wf)
    d5_coarse = kde(pts, centers_c, 2 * wf)
    operator_corr = correlation(d5_fine, d5_coarse)
    operator_scale_ratio = (sum(d5_fine) / mc) / (sum(d5_coarse) / mc)
    operator_pointwise_dev = max(abs(d5_fine[k] / d5_coarse[k] - 1.0) for k in range(mc))

    bridge_coarse = correlation(pc, d5_coarse)
    bridge_fine = correlation(pc, d5_fine)

    raw_ratio = (sum(cc) / mc) / (sum(cf) / mf)
    normalized_ratio = (sum(pc) / mc) / (sum(pf) / mf)

    return {
        "schema": SCHEMA,
        "coarse_graining_identity": bool(identity),
        "geometry_ratio_dev": _round(geometry_ratio_dev),
        "geometry_consistent": bool(geometry_ratio_dev <= protocol["ratio_tol"]),
        "operator_corr": _round(operator_corr),
        "operator_scale_ratio": _round(operator_scale_ratio),
        "operator_pointwise_dev": _round(operator_pointwise_dev),
        "operator_consistent": bool(operator_corr >= protocol["corr_high"]
                                    and abs(operator_scale_ratio - 1.0) <= protocol["ratio_tol"]),
        "bridge_coarse": _round(bridge_coarse),
        "bridge_fine": _round(bridge_fine),
        "bridge_consistent": bool(bridge_coarse >= protocol["corr_high"]
                                  and bridge_fine >= protocol["corr_high"]),
        "control": {
            "raw_scale_ratio": _round(raw_ratio),
            "raw_scale_consistent": bool(abs(raw_ratio - 1.0) <= protocol["ratio_tol"]),
            "normalized_scale_ratio": _round(normalized_ratio),
        },
    }
