"""Independent reference route for the QR-05CG dimension-convergence benchmark.

Nearest-neighbour via a full pairwise distance list, and an independent
least-squares fit written with explicit indices. Must match the primary report.
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


def _pairwise(points):
    out = []
    for i, pi in enumerate(points):
        row = []
        for j, pj in enumerate(points):
            if i == j:
                continue
            row.append(math.dist(pi, pj))
        out.append(min(row))
    return out


def mean_nearest_neighbour(points):
    nn = _pairwise(points)
    return sum(nn) / len(nn)


def _fit(xs, ys):
    count = len(xs)
    mean_x = sum(xs) / count
    mean_y = sum(ys) / count
    s_xy = 0.0
    s_xx = 0.0
    for index in range(count):
        s_xy += (xs[index] - mean_x) * (ys[index] - mean_y)
        s_xx += (xs[index] - mean_x) * (xs[index] - mean_x)
    return s_xy / s_xx


def build_report(protocol):
    mod = load_module("_qr05cg_t7_ref", MODULE_PATH)
    log_ns = [math.log(n) for n in protocol["n_grid"]]
    curves = []
    for d in protocol["dims"]:
        means = []
        for n in protocol["n_grid"]:
            per_seed = []
            for seed in protocol["seeds"]:
                points = mod.sprinkle_diamond(d, n, seed=seed)
                per_seed.append(mean_nearest_neighbour(points))
            means.append(sum(per_seed) / len(per_seed))
        exponent = _fit(log_ns, [math.log(value) for value in means])
        expected = protocol["expected_exponent"][str(d)]
        curves.append({
            "d": d,
            "mean_nn": [_round(value) for value in means],
            "exponent": _round(exponent),
            "expected": expected,
            "abs_err": _round(abs(exponent - expected)),
            "within_tolerance": abs(exponent - expected) <= protocol["tol"],
        })
    slowest = min(curves, key=lambda curve: abs(curve["exponent"]))
    return {"schema": SCHEMA, "curves": curves, "slowest_dim": slowest["d"]}
