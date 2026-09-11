"""Independent reference route for the QR-05CT Lorentzian-distance step."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05ct-report-v1"
AREA = 0.5


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _round(value, places=9):
    return round(value, places)


def _causality(points):
    n = len(points)
    out = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dt = points[j][0] - points[i][0]
                spatial = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, len(points[i])))
                if dt > 0 and spatial < dt * dt:
                    out[i][j] = True
    return out


def _chains(prec, order):
    n = len(prec)
    dist = [-1] * n
    dist[order[0]] = 0
    for j in order:
        for i in order:
            if prec[i][j] and dist[i] >= 0 and dist[i] + 1 > dist[j]:
                dist[j] = dist[i] + 1
    return dist


def _ratios(points, prec, order, ell):
    n = len(points)
    dist = _chains(prec, order)
    src = order[0]
    out = []
    for j in range(n):
        if dist[j] <= 0:
            continue
        dt = points[j][0] - points[src][0]
        spatial = sum((points[j][k] - points[src][k]) ** 2 for k in range(1, len(points[j])))
        tau2 = dt * dt - spatial
        if tau2 > 0:
            out.append(dist[j] * ell / math.sqrt(tau2))
    return out


def _stats(values):
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    return mean, math.sqrt(var)


def build_report(protocol):
    module = load_module("_qr05ct_t7_ref", MODULE_PATH)
    seed = protocol["seed"]
    rows = []
    for n in protocol["n_grid"]:
        points = module.sprinkle_diamond(2, n, seed=seed)
        prec = _causality(points)
        order = sorted(range(n), key=lambda i: points[i][0])
        mean, spread = _stats(_ratios(points, prec, order, math.sqrt(AREA / n)))
        rows.append({"n": n, "mean_ratio": _round(mean), "spread": _round(spread), "ell": _round(math.sqrt(AREA / n))})

    constant = sum(r["mean_ratio"] for r in rows) / len(rows)
    mean_stable = max(abs(r["mean_ratio"] - constant) for r in rows) <= protocol["mean_tolerance"]
    spreads = [r["spread"] for r in rows]
    spread_decreasing = all(spreads[i] > spreads[i + 1] for i in range(len(spreads) - 1))

    n_ctl = protocol["n_grid"][-1]
    pts = module.sprinkle_diamond(2, n_ctl, seed=seed)
    rng = random.Random(seed)
    keys = [rng.random() for _ in range(n_ctl)]
    prec_ctl = [[keys[i] < keys[j] for j in range(n_ctl)] for i in range(n_ctl)]
    order_ctl = sorted(range(n_ctl), key=lambda i: keys[i])
    ctl_mean, ctl_spread = _stats(_ratios(pts, prec_ctl, order_ctl, math.sqrt(AREA / n_ctl)))
    distinct = abs(ctl_mean - constant) > protocol["control_min_gap"] or ctl_spread > protocol["spread_ratio"] * spreads[-1]

    return {
        "schema": SCHEMA,
        "manifoldlike": rows,
        "constant": _round(constant),
        "mean_stable": mean_stable,
        "spread_decreasing": spread_decreasing,
        "control": {"mean_ratio": _round(ctl_mean), "spread": _round(ctl_spread), "distinct": distinct},
        "lorentzian_distance_converges": mean_stable and spread_decreasing and distinct,
    }
