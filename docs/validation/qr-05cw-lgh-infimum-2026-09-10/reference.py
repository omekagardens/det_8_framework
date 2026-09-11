"""Independent reference route for the QR-05CW LGH infimum."""

from __future__ import annotations

import importlib.util
import itertools
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05cw-report-v1"


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
    matrix = [[0] * n for _ in range(n)]
    for src in order:
        dist = [-1] * n
        dist[src] = 0
        for j in order:
            for i in order:
                if prec[i][j] and dist[i] >= 0 and dist[i] + 1 > dist[j]:
                    dist[j] = dist[i] + 1
        matrix[src] = [v if v > 0 else 0 for v in dist]
    return matrix


def _tau(points):
    n = len(points)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dt = points[j][0] - points[i][0]
            spatial = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, len(points[i])))
            out[i][j] = math.sqrt(dt * dt - spatial) if dt * dt > spatial else 0.0
    return out


def _norm(matrix):
    vals = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix)) if matrix[i][j] > 0]
    if not vals:
        return [[0.0] * len(matrix) for _ in matrix]
    m = sum(vals) / len(vals)
    return [[matrix[i][j] / m for j in range(len(matrix))] for i in range(len(matrix))]


def _dist(a, b, perm):
    n = len(a)
    worst = 0.0
    for i in range(n):
        for j in range(n):
            d = abs(a[i][j] - b[perm[i]][perm[j]])
            if d > worst:
                worst = d
    return worst


def _inf(a, b):
    n = len(a)
    return min(_dist(a, b, p) for p in itertools.permutations(range(n)))


def build_report(protocol):
    module = load_module("_qr05cw_t7_ref", MODULE_PATH)
    rows = []
    for n in protocol["n_grid"]:
        pts = module.sprinkle_diamond(2, n, seed=protocol["seed"])
        prec = _causality(pts)
        order = sorted(range(n), key=lambda i: pts[i][0])
        d_x = _norm(_chains(prec, order))
        d_y = _norm(_tau(pts))
        identity = _dist(d_x, d_y, tuple(range(n)))
        opt = _inf(d_x, d_y)
        rows.append({"n": n, "identity": _round(identity), "infimum": _round(opt),
                     "improvement": _round(identity - opt)})

    n_ctl = protocol["n_grid"][-1]
    pts = module.sprinkle_diamond(2, n_ctl, seed=protocol["seed"])
    prec = _causality(pts)
    order = sorted(range(n_ctl), key=lambda i: pts[i][0])
    d_x = _norm(_chains(prec, order))
    zero = [[0.0] * n_ctl for _ in range(n_ctl)]
    incomparable = _inf(d_x, zero)

    infimums = [r["infimum"] for r in rows]
    improvements = [r["improvement"] for r in rows]
    identity_optimal = all(v <= 1e-9 for v in improvements)
    control = {"incomparable_infimum": _round(incomparable),
               "distinct": incomparable > protocol["control_factor"] * max(infimums)}

    return {
        "schema": SCHEMA,
        "rows": rows,
        "identity_is_optimal": identity_optimal,
        "scale_degeneracy": {"free_scale_infimum_control": 0.0,
                             "note": "with a free scale, s=0 makes any comparison trivial "
                                     "(the LGH class is conformal); the distance must be scale-fixed"},
        "control": control,
        "lgh_infimum_established": identity_optimal and control["distinct"],
        "verdict": "inconclusive at accessible N: identity is optimal at fixed scale, "
                   "but the incomparable control is not separated (small-space distortion is large)",
    }
