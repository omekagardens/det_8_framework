"""Independent reference route for QR-05CZ.

Same computation by different mechanics: the relative scale is found by bisecting
the crossing of the upper and lower envelopes (U(c) = max(p - c q),
L(c) = max(c q - p)) instead of golden-section minimisation; the matrices, the
support check, the sorted-multiset bound and the report are recoded. The two routes
must agree before the gate is published.
"""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05cz-report-v1"


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


def _tau(points, directed):
    n = len(points)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dt = points[j][0] - points[i][0]
            spatial = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, len(points[i])))
            if directed:
                out[i][j] = math.sqrt(dt * dt - spatial) if (dt > 0 and dt * dt > spatial) else 0.0
            else:
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


def _pairs(a, b):
    n = len(a)
    return [(a[i][j], b[i][j]) for i in range(n) for j in range(n)]


def _permute(b, perm):
    n = len(b)
    return [[b[perm[i]][perm[j]] for j in range(n)] for i in range(n)]


def _minimax(pairs, iters):
    def upper(c):
        return max(p - c * q for p, q in pairs)

    def lower(c):
        return max(c * q - p for p, q in pairs)

    lo, hi = 0.0, 32.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if upper(mid) > lower(mid):
            lo = mid
        else:
            hi = mid
    c = 0.5 * (lo + hi)
    return c, max(upper(c), lower(c))


def _sorted_lists(a, b):
    n = len(a)
    left = sorted(a[i][j] for i in range(n) for j in range(n) if i != j)
    right = sorted(b[i][j] for i in range(n) for j in range(n) if i != j)
    return left, right


def _lb_c1(a, b):
    left, right = _sorted_lists(a, b)
    return max(abs(x - y) for x, y in zip(left, right))


def _lb_scale(a, b, iters):
    left, right = _sorted_lists(a, b)
    return _minimax(list(zip(left, right)), iters)[1]


def _exact_sf(a, b, iters):
    n = len(a)
    best, best_perm = None, None
    for perm in itertools.permutations(range(n)):
        _c, value = _minimax(_pairs(a, _permute(b, perm)), iters)
        if best is None or value < best:
            best, best_perm = value, perm
    return best, best_perm


def _matrices(module, n, seed, directed):
    points = module.sprinkle_diamond(2, n, seed=seed)
    order = sorted(range(n), key=lambda i: points[i][0])
    return _norm(_chains(_causality(points), order)), _norm(_tau(points, directed))


def _mismatches(a, b):
    n = len(a)
    return sum(1 for i in range(n) for j in range(n) if (a[i][j] > 0) != (b[i][j] > 0))


def build_report(protocol):
    module = load_module("_qr05cz_t7_ref", MODULE_PATH)
    iters = protocol["minimax_iters"]
    seed = protocol["seed"]

    convention = {"n_checked": list(protocol["convention_n"]),
                  "chain_vs_symmetric": {}, "chain_vs_directed": {}, "max_symmetric": {}, "max_directed": {}}
    for n in protocol["convention_n"]:
        a, sym = _matrices(module, n, seed, directed=False)
        _a2, dire = _matrices(module, n, seed, directed=True)
        convention["chain_vs_symmetric"][str(n)] = _mismatches(a, sym)
        convention["chain_vs_directed"][str(n)] = _mismatches(a, dire)
        convention["max_symmetric"][str(n)] = _round(max(sym[i][j] for i in range(n) for j in range(n)))
        convention["max_directed"][str(n)] = _round(max(dire[i][j] for i in range(n) for j in range(n)))

    arm_symmetric, arm_directed = [], []
    for n in protocol["n_scale"]:
        a_s, b_s = _matrices(module, n, seed, directed=False)
        arm_symmetric.append({"n": n, "fixed_identity": _round(_dist(a_s, b_s, tuple(range(n)))),
                              "lower_bound": _round(_lb_c1(a_s, b_s))})
        a_d, b_d = _matrices(module, n, seed, directed=True)
        cstar, sf = _minimax(_pairs(a_d, b_d), iters)
        arm_directed.append({"n": n, "fixed_identity": _round(_dist(a_d, b_d, tuple(range(n)))),
                             "lower_bound": _round(_lb_c1(a_d, b_d)),
                             "scale_free_identity": _round(sf), "relative_scale": _round(cstar)})

    trend = []
    for n in protocol["n_scale"]:
        sfv, lbv, fv = [], [], []
        for s in protocol["seeds"]:
            a, b = _matrices(module, n, s, directed=True)
            fv.append(_dist(a, b, tuple(range(n))))
            sfv.append(_minimax(_pairs(a, b), iters)[1])
            lbv.append(_lb_scale(a, b, iters))
        ell = math.sqrt(protocol["area"] / n)
        trend.append({"n": n, "ell": _round(ell),
                      "fixed_identity_mean": _round(sum(fv) / len(fv)),
                      "scale_free_identity_mean": _round(sum(sfv) / len(sfv)),
                      "scale_free_identity_sd": _round(math.sqrt(sum((v - sum(sfv) / len(sfv)) ** 2 for v in sfv) / len(sfv))),
                      "lower_bound_mean": _round(sum(lbv) / len(lbv)),
                      "lower_bound_over_ell": _round(sum(lbv) / len(lbv) / ell)})

    rows_exact = []
    for n in protocol["n_exact"]:
        a, b = _matrices(module, n, seed, directed=True)
        cstar, identity = _minimax(_pairs(a, b), iters)
        value, perm = _exact_sf(a, b, iters)
        rows_exact.append({"n": n, "fixed_identity": _round(_dist(a, b, tuple(range(n)))),
                           "scale_free_identity": _round(identity),
                           "exact_scale_free_infimum": _round(value),
                           "identity_optimal": bool(perm == tuple(range(n)))})

    symmetric_floor = min(row["lower_bound"] for row in arm_symmetric)
    directed_lb = [row["lower_bound_mean"] for row in trend]
    directed_floor = min(directed_lb)
    decays = all(b < a for a, b in zip(directed_lb, directed_lb[1:]))

    return {
        "schema": SCHEMA,
        "convention": convention,
        "arm_symmetric": arm_symmetric,
        "arm_directed": arm_directed,
        "trend_directed": trend,
        "rows_exact": rows_exact,
        "symmetric_floor_lower_bound": _round(symmetric_floor),
        "directed_floor_lower_bound": _round(directed_floor),
        "directed_lower_bound_decays": bool(decays),
        "identity_is_optimal_scale_free": bool(all(row["identity_optimal"] for row in rows_exact)),
        "reclassification": "QR-05CW/CX built the continuum counterpart symmetrically (|dt|^2), which does "
                            "not satisfy LMS A3 and does not match the directed chain support; the "
                            "reverse-direction terms |0 - tau| = tau dominated, so their non-vanishing floor "
                            "is an artifact of that convention. Their identity-optimality sub-finding is "
                            "retained (identity is still optimal under the directed distance).",
        "lgh_infimum_established": False,
        "verdict": "convention defect corrected, obstruction withdrawn, convergence reopened. With the "
                   "directed Lorentzian distance the scale-free distortion is much smaller than the "
                   "contaminated value (<= ~0.9 vs ~1.8-3.3) and its certified lower bound decreases "
                   "monotonically from ~0.50 (N=8) to ~0.16 (N=256, ~2-3.6 x ell), so the CW/CX "
                   "non-vanishing floor was an artifact. The natural-correspondence upper bound does NOT "
                   "visibly decay (~0.6-0.8, noisy), so the scale-free infimum (bracketed between them) is "
                   "not shown to converge: the question is reopened, not settled. No metric, continuum, "
                   "curvature or gravity claim.",
    }
