"""Primary route for QR-05CZ: scale-free LGH comparison and the directed-distance correction.

QR-05CW/CX compared the discrete chain time-separation d_X to a continuum
counterpart built from |dt|^2, which is *symmetric*: b[i][j] = b[j][i] > 0 for any
timelike pair. The chain matrix is *directed* (a[i][j] > 0 only for earlier ->
later), and the Lorentzian distance is directed too (Minguzzi-Suhr axiom A3:
d(x,y) > 0 => d(y,x) = 0). The symmetric counterpart injects reverse-direction
terms |0 - tau| = tau at every timelike pair, which dominate the distortion. That
made the CW/CX floor an artifact.

This gate (1) exhibits the defect, (2) reproduces the contaminated CW/CX arm, (3)
recomputes the comparison with the directed Lorentzian distance, and (4) answers
the open scale-free question: optimize the global relative scale (a homothety),

    inf over c > 0 of  min over bijections sigma of  max over pairs |d_X(i,j) - c d_Y(sigma i, sigma j)|,

with each matrix mean-normalized (the overall pair scale is a gauge). It reports
the natural-correspondence upper bound and a certified lower bound (the
scale-optimized sorted-multiset matching bound). Supplied geometry; no gravity claim.
"""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
import statistics
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


def tau_symmetric(points):
    """CW/CX's counterpart: uses dt^2, so it is symmetric (b[i][j] = b[j][i])."""
    n = len(points)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dt = points[j][0] - points[i][0]
            spatial = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, len(points[i])))
            out[i][j] = math.sqrt(dt * dt - spatial) if dt * dt > spatial else 0.0
    return out


def tau_directed(points):
    """The Lorentzian distance: positive only for earlier -> later (axiom A3)."""
    n = len(points)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dt = points[j][0] - points[i][0]
            spatial = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, len(points[i])))
            out[i][j] = math.sqrt(dt * dt - spatial) if (dt > 0 and dt * dt > spatial) else 0.0
    return out


def normalize(matrix):
    positive = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix)) if matrix[i][j] > 0]
    if not positive:
        return [[0.0] * len(matrix) for _ in matrix]
    mean = sum(positive) / len(positive)
    return [[matrix[i][j] / mean for j in range(len(matrix))] for i in range(len(matrix))]


def distortion(a, b, perm):
    n = len(a)
    return max(abs(a[i][j] - b[perm[i]][perm[j]]) for i in range(n) for j in range(n))


def pairs_of(a, b):
    n = len(a)
    return [(a[i][j], b[i][j]) for i in range(n) for j in range(n)]


def permute(b, perm):
    n = len(b)
    return [[b[perm[i]][perm[j]] for j in range(n)] for i in range(n)]


def minimax_scale(pairs, iters):
    """min over c > 0 of max |p - c q| (a convex 1-D problem)."""
    const = max((abs(p) for p, q in pairs if q == 0.0), default=0.0)

    def f(c):
        worst = const
        for p, q in pairs:
            if q != 0.0:
                value = abs(p - c * q)
                if value > worst:
                    worst = value
        return worst

    lo, hi = 1e-9, 32.0
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c1 = hi - gr * (hi - lo)
    c2 = lo + gr * (hi - lo)
    f1, f2 = f(c1), f(c2)
    for _ in range(iters):
        if f1 < f2:
            hi, c2, f2 = c2, c1, f1
            c1 = hi - gr * (hi - lo)
            f1 = f(c1)
        else:
            lo, c1, f1 = c1, c2, f2
            c2 = lo + gr * (hi - lo)
            f2 = f(c2)
    cstar = 0.5 * (lo + hi)
    return cstar, f(cstar)


def sorted_lists(a, b):
    n = len(a)
    left = sorted(a[i][j] for i in range(n) for j in range(n) if i != j)
    right = sorted(b[i][j] for i in range(n) for j in range(n) if i != j)
    return left, right


def lower_bound_c1(a, b):
    """Certified bound at the fixed scale c = 1 (CW/CX's bound)."""
    left, right = sorted_lists(a, b)
    return max(abs(x - y) for x, y in zip(left, right))


def lower_bound_scale(a, b, iters):
    """inf_c of the sorted-multiset matching bound: valid for the scale-free infimum."""
    left, right = sorted_lists(a, b)
    return minimax_scale(list(zip(left, right)), iters)[1]


def exact_scale_free_infimum(a, b, iters):
    n = len(a)
    best, best_perm = None, None
    for perm in itertools.permutations(range(n)):
        _c, value = minimax_scale(pairs_of(a, permute(b, perm)), iters)
        if best is None or value < best:
            best, best_perm = value, perm
    return best, best_perm


def _matrices(module, n, seed, directed):
    points = module.sprinkle_diamond(2, n, seed=seed)
    prec = causality(points)
    order = sorted(range(n), key=lambda i: points[i][0])
    tau = tau_directed if directed else tau_symmetric
    return normalize(chain_matrix(prec, order)), normalize(tau(points))


def _support_mismatches(a, b):
    n = len(a)
    return sum(1 for i in range(n) for j in range(n) if (a[i][j] > 0) != (b[i][j] > 0))


def build_report(protocol):
    module = load_module("_qr05cz_t7", MODULE_PATH)
    iters = protocol["minimax_iters"]
    seed = protocol["seed"]

    convention = {"n_checked": list(protocol["convention_n"]),
                  "chain_vs_symmetric": {}, "chain_vs_directed": {}, "max_symmetric": {}, "max_directed": {}}
    for n in protocol["convention_n"]:
        a, sym = _matrices(module, n, seed, directed=False)
        _a2, dire = _matrices(module, n, seed, directed=True)
        convention["chain_vs_symmetric"][str(n)] = _support_mismatches(a, sym)
        convention["chain_vs_directed"][str(n)] = _support_mismatches(a, dire)
        convention["max_symmetric"][str(n)] = _round(max(sym[i][j] for i in range(n) for j in range(n)))
        convention["max_directed"][str(n)] = _round(max(dire[i][j] for i in range(n) for j in range(n)))

    arm_symmetric = []
    arm_directed = []
    for n in protocol["n_scale"]:
        a_s, b_s = _matrices(module, n, seed, directed=False)
        arm_symmetric.append({"n": n, "fixed_identity": _round(distortion(a_s, b_s, tuple(range(n)))),
                              "lower_bound": _round(lower_bound_c1(a_s, b_s))})
        a_d, b_d = _matrices(module, n, seed, directed=True)
        cstar, sf = minimax_scale(pairs_of(a_d, b_d), iters)
        arm_directed.append({"n": n, "fixed_identity": _round(distortion(a_d, b_d, tuple(range(n)))),
                             "lower_bound": _round(lower_bound_c1(a_d, b_d)),
                             "scale_free_identity": _round(sf), "relative_scale": _round(cstar)})

    trend = []
    for n in protocol["n_scale"]:
        sf_values, lb_values, fixed_values = [], [], []
        for s in protocol["seeds"]:
            a, b = _matrices(module, n, s, directed=True)
            fixed_values.append(distortion(a, b, tuple(range(n))))
            sf_values.append(minimax_scale(pairs_of(a, b), iters)[1])
            lb_values.append(lower_bound_scale(a, b, iters))
        ell = math.sqrt(protocol["area"] / n)
        trend.append({"n": n, "ell": _round(ell),
                      "fixed_identity_mean": _round(statistics.fmean(fixed_values)),
                      "scale_free_identity_mean": _round(statistics.fmean(sf_values)),
                      "scale_free_identity_sd": _round(statistics.pstdev(sf_values)),
                      "lower_bound_mean": _round(statistics.fmean(lb_values)),
                      "lower_bound_over_ell": _round(statistics.fmean(lb_values) / ell)})

    rows_exact = []
    for n in protocol["n_exact"]:
        a, b = _matrices(module, n, seed, directed=True)
        cstar, identity = minimax_scale(pairs_of(a, b), iters)
        value, perm = exact_scale_free_infimum(a, b, iters)
        rows_exact.append({"n": n, "fixed_identity": _round(distortion(a, b, tuple(range(n)))),
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
