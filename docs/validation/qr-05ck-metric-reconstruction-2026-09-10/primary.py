"""Primary route for the QR-05CK metric reconstruction / refinement benchmark.

On a supplied conformally-flat 1+1 geometry Omega^2(x)=1+4b*x*(1-x), reconstruct
the conformal factor from counts at three densities and verify (BY M6)
refinement consistency, grid/position robustness, the whole-point granularity
of a count-based estimate (BG), and a non-conformal control. Supplied geometry;
no gravity claim.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05ck-report-v1"


def _round(value, places=9):
    return round(value, places)


def omega2(x, b):
    return 1.0 + 4.0 * b * x * (1.0 - x)


def sprinkle(n, seed, b):
    rng = random.Random(seed)
    w_max = 1.0 + b
    points = []
    while len(points) < n:
        t, x = rng.random(), rng.random()
        if rng.random() <= omega2(x, b) / w_max:
            points.append((t, x))
    return points


def profile(points, bins, b, offset=0.0):
    counts = [0] * bins
    for _, x in points:
        shifted = (x + offset) % 1.0
        counts[min(int(shifted * bins), bins - 1)] += 1
    mean = sum(counts) / bins
    recovered = [c / mean for c in counts]
    centers = [(((k + 0.5) / bins - offset) % 1.0) for k in range(bins)]
    truth = [omega2(c, b) for c in centers]
    tmean = sum(truth) / bins
    truth = [w / tmean for w in truth]
    return recovered, truth, counts


def mse(a, b_list):
    return sum((a[k] - b_list[k]) ** 2 for k in range(len(a))) / len(a)


def build_report(protocol):
    b = protocol["b"]
    bins = protocol["bins"]
    seed = protocol["seed"]

    refinement = []
    for n in protocol["n_grid"]:
        points = sprinkle(n, seed, b)
        recovered, truth, counts = profile(points, bins, b)
        refinement.append({"n": n, "mse": _round(mse(recovered, truth)),
                           "recovered": [_round(x) for x in recovered],
                           "truth": [_round(x) for x in truth],
                           "mean_count": _round(sum(counts) / bins)})

    tol = protocol["consistency_tolerance"]
    profiles = [row["recovered"] for row in refinement]
    pair_mses = [mse(profiles[i], profiles[i + 1]) for i in range(len(profiles) - 1)]
    refinement_consistent = all(value <= tol * max(1.0, max(profiles[i])) for i, value in enumerate(pair_mses))
    truth_mses = [row["mse"] for row in refinement]
    mse_decreasing = all(truth_mses[i] >= truth_mses[i + 1] for i in range(len(truth_mses) - 1))

    mid_n = protocol["n_grid"][len(protocol["n_grid"]) // 2]
    points = sprinkle(mid_n, seed, b)
    base, _, _ = profile(points, bins, b, offset=0.0)
    shifted, _, _ = profile(points, bins, b, offset=0.5 / bins)
    grid_mse = mse(base, shifted)
    grid_robust = grid_mse <= protocol["grid_tolerance"]

    lowest = protocol["n_grid"][0]
    mean_count_lowest = lowest / bins
    granularity = 1.0 / mean_count_lowest

    uniform = []
    rng = random.Random(seed + 7)
    for _ in range(mid_n):
        uniform.append((rng.random(), rng.random()))
    recovered_u, truth_u, _ = profile(uniform, bins, b)
    control_mse = mse(recovered_u, truth_u)

    return {
        "schema": SCHEMA,
        "geometry": {"b": b, "bins": bins, "profile": "1 + 4*b*x*(1-x)"},
        "refinement": refinement,
        "pair_mses": [_round(x) for x in pair_mses],
        "refinement_consistent": bool(refinement_consistent),
        "mse_decreasing": bool(mse_decreasing),
        "grid": {"mse_between_offsets": _round(grid_mse), "robust": bool(grid_robust)},
        "whole_point": {"mean_count_lowest": _round(mean_count_lowest),
                        "granularity": _round(granularity)},
        "negative_control": {"mse": _round(control_mse),
                             "control_required": bool(control_mse > protocol["control_factor"] * truth_mses[-1])},
    }
