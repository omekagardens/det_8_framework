"""Primary route for the QR-05CG dimension-convergence benchmark.

Measures the mean nearest-neighbour distance of supplied Minkowski sprinklings
over a range of N in d=2 (1+1) and d=4 (3+1), fits the log-log exponent, and
compares it to the covering/fill-in rate N^(−1/d). This addresses the recorded
caveat that the convergence rate was measured only in 1+1. Supplied geometry;
no emergence or gravity claim.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05cg-report-v1"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _round(value, places=12):
    return round(value, places)


def mean_nearest_neighbour(points):
    n = len(points)
    dim = len(points[0])
    total = 0.0
    for i in range(n):
        best = None
        pi = points[i]
        for j in range(n):
            if i == j:
                continue
            pj = points[j]
            squared = 0.0
            for k in range(dim):
                diff = pi[k] - pj[k]
                squared += diff * diff
            if best is None or squared < best:
                best = squared
        total += math.sqrt(best)
    return total / n


def _slope(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    numerator = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    denominator = sum((xs[i] - mx) ** 2 for i in range(n))
    return numerator / denominator


def build_report(protocol):
    mod = load_module("_qr05cg_t7", MODULE_PATH)
    curves = []
    for d in protocol["dims"]:
        means = []
        for n in protocol["n_grid"]:
            samples = []
            for seed in protocol["seeds"]:
                points = mod.sprinkle_diamond(d, n, seed=seed)
                samples.append(mean_nearest_neighbour(points))
            means.append(sum(samples) / len(samples))
        xs = [math.log(n) for n in protocol["n_grid"]]
        ys = [math.log(value) for value in means]
        exponent = _slope(xs, ys)
        expected = protocol["expected_exponent"][str(d)]
        curves.append({
            "d": d,
            "mean_nn": [_round(value) for value in means],
            "exponent": _round(exponent),
            "expected": expected,
            "abs_err": _round(abs(exponent - expected)),
            "within_tolerance": bool(abs(exponent - expected) <= protocol["tol"]),
        })
    slowest = min(curves, key=lambda c: abs(c["exponent"]))
    return {"schema": SCHEMA, "curves": curves, "slowest_dim": slowest["d"]}
