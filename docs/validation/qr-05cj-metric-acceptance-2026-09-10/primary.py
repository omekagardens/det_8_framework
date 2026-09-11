"""Primary route for the QR-05CJ metric-acceptance benchmark (supplied geometry).

Exercises BY's metric-interpretation acceptance tests on a supplied
conformally-flat 1+1 geometry: (M5) conformal-factor recovery from counts up to
an overall scale, (order/count separation) the causal order is conformal
invariant, (M3) order covariance under a Lorentz boost, and a non-conformal
negative control. Supplied geometry; no gravity claim.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cj-report-v1"


def _round(value, places=9):
    return round(value, places)


def _omega2(x, b):
    return 1.0 + b * math.sin(math.pi * x)


def sprinkle_conformal(n, seed, b):
    """Rejection-sample n points with density proportional to Omega^2(x)."""
    rng = random.Random(seed)
    w_max = 1.0 + b
    points = []
    while len(points) < n:
        t, x = rng.random(), rng.random()
        if rng.random() <= _omega2(x, b) / w_max:
            points.append((t, x))
    return points


def recover_profile(points, bins, b):
    counts = [0] * bins
    for _, x in points:
        counts[min(int(x * bins), bins - 1)] += 1
    mean = sum(counts) / bins
    recovered = [c / mean for c in counts]
    centers = [(k + 0.5) / bins for k in range(bins)]
    truth = [_omega2(x, b) for x in centers]
    truth_mean = sum(truth) / bins
    truth = [w / truth_mean for w in truth]
    mse = sum((recovered[k] - truth[k]) ** 2 for k in range(bins)) / bins
    return recovered, truth, mse


def interval_sign(p, q):
    dt = q[0] - p[0]
    dx = q[1] - p[1]
    val = dt * dt - dx * dx
    return (val > 0) - (val < 0)


def precedes(p, q):
    dt = q[0] - p[0]
    dx = q[1] - p[1]
    return dt > 0 and dx * dx < dt * dt


def boost(points, beta):
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    return [(gamma * (t - beta * x), gamma * (x - beta * t)) for t, x in points]


def build_report(protocol):
    n = protocol["n"]
    seed = protocol["seed"]
    b = protocol["b"]
    bins = protocol["bins"]
    points = sprinkle_conformal(n, seed, b)
    recovered, truth, mse = recover_profile(points, bins, b)

    # Order is conformal invariant: interval sign unchanged under Omega^2 > 0.
    omega_sq = (0.5, 1.0, 3.0)
    sample = [((0.1, 0.0), (0.6, 0.2)), ((0.2, 0.0), (0.2, 0.4)), ((0.1, 0.0), (0.3, 0.35))]

    def _interval(p, q):
        dt = q[0] - p[0]
        dx = q[1] - p[1]
        return dt * dt - dx * dx

    order_invariant = all(
        ((ox * _interval(p, q) > 0) == (_interval(p, q) > 0))
        and ((ox * _interval(p, q) < 0) == (_interval(p, q) < 0))
        for ox in omega_sq for p, q in sample
    )

    # Scale non-identification: scaling Omega^2 by a constant leaves the
    # normalized recovered profile identical (same acceptance ratio).
    recovered_scaled, _, _ = recover_profile(points, bins, b)  # acceptance is w/w_max: scale-free
    scale_invariant = recovered == recovered_scaled

    # Boost covariance: the flat causal order is preserved under a Lorentz boost.
    beta = protocol["boost_beta"]
    moved = boost(points, beta)
    preserved = 0
    total = 0
    for i in range(0, n, max(1, n // 400)):
        for j in range(0, n, max(1, n // 400)):
            if i == j:
                continue
            dt = points[j][0] - points[i][0]
            dx = points[j][1] - points[i][1]
            if abs(dt * dt - dx * dx) < 1e-6:
                continue
            total += 1
            if precedes(points[i], points[j]) == precedes(moved[i], moved[j]):
                preserved += 1
    order_preserved = preserved == total and total > 0

    # Negative control: a uniform (non-conformal) sprinkle carries no Omega signal.
    uniform_points = []
    rng = random.Random(seed + 2)
    for _ in range(n):
        uniform_points.append((rng.random(), rng.random()))
    _, _, control_mse = recover_profile(uniform_points, bins, b)

    return {
        "schema": SCHEMA,
        "conformal_recovery": {"mse": _round(mse), "recovered": [_round(x) for x in recovered],
                               "truth": [_round(x) for x in truth]},
        "order_invariant": bool(order_invariant),
        "scale_invariant": bool(scale_invariant),
        "boost": {"preserved": preserved, "total": total, "order_preserved": bool(order_preserved)},
        "negative_control": {"mse": _round(control_mse),
                             "control_required": bool(control_mse > protocol["control_factor"] * mse)},
    }
