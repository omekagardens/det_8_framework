"""Independent reference route for the QR-05CK metric reconstruction benchmark.

Shares the supplied sprinkle algorithm (fixture) but re-implements the profile
recovery, the pairwise agreement and the control independently.
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
    generator = random.Random(seed)
    w_max = 1.0 + b
    out = []
    while len(out) < n:
        t = generator.random()
        x = generator.random()
        if generator.random() <= omega2(x, b) / w_max:
            out.append((t, x))
    return out


def _bins(points, bins, offset):
    counts = [0] * bins
    for _, x in points:
        s = (x + offset) % 1.0
        counts[min(int(s * bins), bins - 1)] += 1
    return counts


def profile(points, bins, b, offset=0.0):
    counts = _bins(points, bins, offset)
    m = sum(counts) / bins
    rec = [c / m for c in counts]
    centers = [(((k + 0.5) / bins) - offset) % 1.0 for k in range(bins)]
    tru = [omega2(c, b) for c in centers]
    tm = sum(tru) / bins
    tru = [w / tm for w in tru]
    return rec, tru, counts


def _mse(a, b_list):
    total = 0.0
    for k in range(len(a)):
        d = a[k] - b_list[k]
        total += d * d
    return total / len(a)


def build_report(protocol):
    b = protocol["b"]
    bins = protocol["bins"]
    seed = protocol["seed"]

    refinement = []
    for n in protocol["n_grid"]:
        pts = sprinkle(n, seed, b)
        rec, tru, counts = profile(pts, bins, b)
        refinement.append({"n": n, "mse": _round(_mse(rec, tru)),
                           "recovered": [_round(x) for x in rec],
                           "truth": [_round(x) for x in tru],
                           "mean_count": _round(sum(counts) / bins)})

    tol = protocol["consistency_tolerance"]
    profiles = [row["recovered"] for row in refinement]
    pair_mses = []
    for i in range(len(profiles) - 1):
        pair_mses.append(_mse(profiles[i], profiles[i + 1]))
    refinement_consistent = True
    for i, value in enumerate(pair_mses):
        if value > tol * max(1.0, max(profiles[i])):
            refinement_consistent = False
    truth_mses = [row["mse"] for row in refinement]
    mse_decreasing = all(truth_mses[i] >= truth_mses[i + 1] for i in range(len(truth_mses) - 1))

    mid_n = protocol["n_grid"][len(protocol["n_grid"]) // 2]
    pts = sprinkle(mid_n, seed, b)
    base, _, _ = profile(pts, bins, b, offset=0.0)
    shifted, _, _ = profile(pts, bins, b, offset=0.5 / bins)
    grid_mse = _mse(base, shifted)

    mean_count_lowest = protocol["n_grid"][0] / bins

    rng = random.Random(seed + 7)
    uniform = [(rng.random(), rng.random()) for _ in range(mid_n)]
    rec_u, tru_u, _ = profile(uniform, bins, b)
    control_mse = _mse(rec_u, tru_u)

    return {
        "schema": SCHEMA,
        "geometry": {"b": b, "bins": bins, "profile": "1 + 4*b*x*(1-x)"},
        "refinement": refinement,
        "pair_mses": [_round(x) for x in pair_mses],
        "refinement_consistent": refinement_consistent,
        "mse_decreasing": mse_decreasing,
        "grid": {"mse_between_offsets": _round(grid_mse),
                 "robust": grid_mse <= protocol["grid_tolerance"]},
        "whole_point": {"mean_count_lowest": _round(mean_count_lowest),
                        "granularity": _round(1.0 / mean_count_lowest)},
        "negative_control": {"mse": _round(control_mse),
                             "control_required": control_mse > protocol["control_factor"] * truth_mses[-1]},
    }
