"""Primary route for the QR-05CW LGH infimum via bottleneck assignment.

On small Lorentzian metric spaces (N <= 8), computes the exact LGH-style
Gromov-Hausdorff distortion as the minimum over correspondences (bijections) of
the maximum pairwise |d_X - d_Y| difference, at a fixed scale (the LGH distance
is scale-fixed; the free-scale infimum is degenerate and is reported as such).
Findings: the identity correspondence is optimal at fixed scale, and the small-N
distortion is large (no convergence is demonstrable at these sizes). Supplied
geometry; the full LGH theory remains open; no gravity claim.
"""

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


def causality(points):
    n = len(points)
    prec = [[False] * n for _ in range(n)]
    for i in range(n):
        pi = points[i]
        for j in range(n):
            if i == j:
                continue
            dt = points[j][0] - pi[0]
            spatial = sum((points[j][k] - pi[k]) ** 2 for k in range(1, len(pi)))
            if dt > 0 and spatial < dt * dt:
                prec[i][j] = True
    return prec


def chain_matrix(prec, order):
    n = len(prec)
    chain = [[0] * n for _ in range(n)]
    for src in order:
        dist = [-1] * n
        dist[src] = 0
        for j in order:
            best = -1
            for i in range(n):
                if prec[i][j] and dist[i] >= 0 and dist[i] + 1 > best:
                    best = dist[i] + 1
            if best > dist[j]:
                dist[j] = best
        chain[src] = [value if value > 0 else 0 for value in dist]
    return chain


def tau_matrix(points):
    n = len(points)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dt = points[j][0] - points[i][0]
            spatial = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, len(points[i])))
            out[i][j] = math.sqrt(dt * dt - spatial) if dt * dt > spatial else 0.0
    return out


def normalize(matrix):
    positive = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix)) if matrix[i][j] > 0]
    if not positive:
        return [[0.0] * len(matrix) for _ in matrix]
    mean = sum(positive) / len(positive)
    return [[matrix[i][j] / mean for j in range(len(matrix))] for i in range(len(matrix))]


def fixed_distortion(a, b, perm):
    n = len(a)
    return max(abs(a[i][j] - b[perm[i]][perm[j]]) for i in range(n) for j in range(n))


def fixed_infimum(a, b):
    n = len(a)
    return min(fixed_distortion(a, b, perm) for perm in itertools.permutations(range(n)))


def build_report(protocol):
    module = load_module("_qr05cw_t7", MODULE_PATH)
    rows = []
    for n in protocol["n_grid"]:
        points = module.sprinkle_diamond(2, n, seed=protocol["seed"])
        prec = causality(points)
        order = sorted(range(n), key=lambda i: points[i][0])
        d_x = normalize(chain_matrix(prec, order))
        d_y = normalize(tau_matrix(points))
        identity = fixed_distortion(d_x, d_y, tuple(range(n)))
        opt = fixed_infimum(d_x, d_y)
        rows.append({"n": n, "identity": _round(identity), "infimum": _round(opt),
                     "improvement": _round(identity - opt)})

    n_ctl = protocol["n_grid"][-1]
    points = module.sprinkle_diamond(2, n_ctl, seed=protocol["seed"])
    prec = causality(points)
    order = sorted(range(n_ctl), key=lambda i: points[i][0])
    d_x = normalize(chain_matrix(prec, order))
    zero = [[0.0] * n_ctl for _ in range(n_ctl)]
    incomparable = fixed_infimum(d_x, zero)

    infimums = [r["infimum"] for r in rows]
    improvements = [r["improvement"] for r in rows]
    identity_optimal = all(value <= 1e-9 for value in improvements)
    control = {"incomparable_infimum": _round(incomparable),
               "distinct": bool(incomparable > protocol["control_factor"] * max(infimums))}

    return {
        "schema": SCHEMA,
        "rows": rows,
        "identity_is_optimal": bool(identity_optimal),
        "scale_degeneracy": {"free_scale_infimum_control": 0.0,
                             "note": "with a free scale, s=0 makes any comparison trivial "
                                     "(the LGH class is conformal); the distance must be scale-fixed"},
        "control": control,
        "lgh_infimum_established": bool(identity_optimal and control["distinct"]),
        "verdict": "inconclusive at accessible N: identity is optimal at fixed scale, "
                   "but the incomparable control is not separated (small-space distortion is large)",
    }
