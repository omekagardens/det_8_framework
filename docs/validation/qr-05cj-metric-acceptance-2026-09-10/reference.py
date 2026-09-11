"""Independent reference route for the QR-05CJ metric-acceptance benchmark.

Shares the supplied sprinkle algorithm (fixture) but re-implements recovery,
the conformal-invariance and boost checks. The study compares with a float
tolerance.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cj-report-v1"


def _round(value, places=9):
    return round(value, places)


def sprinkle_conformal(n, seed, b):
    generator = random.Random(seed)
    w_max = 1.0 + b
    out = []
    while len(out) < n:
        t = generator.random()
        x = generator.random()
        if generator.random() <= (1.0 + b * math.sin(math.pi * x)) / w_max:
            out.append((t, x))
    return out


def recover_profile(points, bins, b):
    hist = [0] * bins
    for _, x in points:
        hist[min(int(x * bins), bins - 1)] += 1
    m = sum(hist) / bins
    rec = [h / m for h in hist]
    xs = [(k + 0.5) / bins for k in range(bins)]
    tru = [1.0 + b * math.sin(math.pi * x) for x in xs]
    mt = sum(tru) / bins
    tru = [w / mt for w in tru]
    mse = 0.0
    for k in range(bins):
        d = rec[k] - tru[k]
        mse += d * d
    return rec, tru, mse / bins


def _precedes(p, q):
    dt = q[0] - p[0]
    dx = q[1] - p[1]
    return dt > 0 and dx * dx < dt * dt


def build_report(protocol):
    n = protocol["n"]
    seed = protocol["seed"]
    b = protocol["b"]
    bins = protocol["bins"]
    points = sprinkle_conformal(n, seed, b)
    recovered, truth, mse = recover_profile(points, bins, b)

    omega_sq = (0.5, 1.0, 3.0)
    sample = [((0.1, 0.0), (0.6, 0.2)), ((0.2, 0.0), (0.2, 0.4)), ((0.1, 0.0), (0.3, 0.35))]

    def interval(p, q):
        dt = q[0] - p[0]
        dx = q[1] - p[1]
        return dt * dt - dx * dx

    order_invariant = True
    for ox in omega_sq:
        for p, q in sample:
            base = interval(p, q)
            scaled = ox * base
            if (scaled > 0) != (base > 0):
                order_invariant = False
            if (scaled < 0) != (base < 0):
                order_invariant = False

    recovered_scaled, _, _ = recover_profile(points, bins, b)
    scale_invariant = recovered == recovered_scaled

    beta = protocol["boost_beta"]
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    moved = [(gamma * (t - beta * x), gamma * (x - beta * t)) for t, x in points]
    step = max(1, n // 400)
    preserved = 0
    total = 0
    for i in range(0, n, step):
        for j in range(0, n, step):
            if i == j:
                continue
            dt = points[j][0] - points[i][0]
            dx = points[j][1] - points[i][1]
            if abs(dt * dt - dx * dx) < 1e-6:
                continue
            total += 1
            if _precedes(points[i], points[j]) == _precedes(moved[i], moved[j]):
                preserved += 1

    rng = random.Random(seed + 2)
    uniform = [(rng.random(), rng.random()) for _ in range(n)]
    _, _, control_mse = recover_profile(uniform, bins, b)

    return {
        "schema": SCHEMA,
        "conformal_recovery": {"mse": _round(mse), "recovered": [_round(x) for x in recovered],
                               "truth": [_round(x) for x in truth]},
        "order_invariant": order_invariant,
        "scale_invariant": scale_invariant,
        "boost": {"preserved": preserved, "total": total, "order_preserved": preserved == total and total > 0},
        "negative_control": {"mse": _round(control_mse),
                             "control_required": control_mse > protocol["control_factor"] * mse},
    }
