"""Primary route for the QR-05CN T7/T5 compatibility witness.

From ONE sprinkle, the T7 route reconstructs the conformal profile from binned
counts and the T5 route builds a kernel as a count-based functional of the same
points; the two must be the same profile up to one scale. An independently
supplied kernel with a different profile is the juxtaposition control. Supplied
geometry; no gravity claim.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cn-report-v1"


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


def reconstruct_counts(points, bins):
    counts = [0] * bins
    for x in points:
        counts[min(int(x * bins), bins - 1)] += 1
    mean = sum(counts) / bins
    return [c / mean for c in counts]


def kde_profile(points, bins, width):
    centers = [(k + 0.5) / bins for k in range(bins)]
    raw = []
    for xc in centers:
        total = 0.0
        for x in points:
            d = x - xc
            total += math.exp(-(d * d) / (2 * width * width))
        raw.append(total)
    mean = sum(raw) / bins
    return [r / mean for r in raw]


def control_profile(bins, a):
    centers = [(k + 0.5) / bins for k in range(bins)]
    raw = [1.0 + a * math.cos(2 * math.pi * xc) for xc in centers]
    mean = sum(raw) / bins
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
    points = sprinkle(protocol["n"], protocol["seed"], protocol["a"])
    p7 = reconstruct_counts(points, protocol["bins"])
    d5 = kde_profile(points, protocol["bins"], protocol["kde_width"])
    ctrl = control_profile(protocol["bins"], protocol["a"])

    c_derived = correlation(p7, d5)
    c_control = correlation(p7, ctrl)
    compatible = bool(c_derived >= protocol["corr_high"] and c_control <= protocol["corr_low"])

    return {
        "schema": SCHEMA,
        "t7_profile": [_round(v) for v in p7],
        "t5_kernel_profile": [_round(v) for v in d5],
        "control_profile": [_round(v) for v in ctrl],
        "corr_derived": _round(c_derived),
        "corr_control": _round(c_control),
        "compatible": compatible,
    }
