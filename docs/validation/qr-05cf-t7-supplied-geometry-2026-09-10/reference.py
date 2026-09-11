"""Independent reference route for the QR-05CF T7 benchmark.

Re-implements the estimators (causality, ordering fraction, links/nullness,
conformal recovery, analytic ordering fraction) from scratch, while taking the
supplied sprinklings from the module (the fixtures). Must match the primary
report exactly after rounding.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05cf-report-v1"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _round(value, places=12):
    return round(value, places)


def _spatial(p, q):
    return math.sqrt(sum((p[k] - q[k]) ** 2 for k in range(1, len(p))))


def _precedes(p, q):
    return q[0] > p[0] and _spatial(p, q) < q[0] - p[0]


def _causality(points):
    n = len(points)
    return [[i != j and _precedes(points[i], points[j]) for j in range(n)] for i in range(n)]


def _ordering_fraction(points):
    prec = _causality(points)
    n = len(points)
    related = 0
    for i in range(n):
        for j in range(n):
            if prec[i][j]:
                related += 1
    return related / (n * (n - 1) / 2) if n > 1 else 0.0


def _analytic_r(dim):
    # r(d) = Gamma(d+1) Gamma(d/2) / [2 Gamma(3d/2)] via log-gamma.
    return math.exp(math.lgamma(dim + 1) + math.lgamma(dim / 2)
                    - math.lgamma(3 * dim / 2) - math.log(2))


def _nullness(points):
    prec = _causality(points)
    n = len(points)
    link_deltas = []
    all_deltas = []
    for i in range(n):
        for j in range(n):
            if not prec[i][j]:
                continue
            delta = (points[j][0] - points[i][0]) - _spatial(points[i], points[j])
            all_deltas.append(delta)
            is_link = True
            for k in range(n):
                if prec[i][k] and prec[k][j]:
                    is_link = False
                    break
            if is_link:
                link_deltas.append(delta)
    mean = lambda xs: sum(xs) / len(xs) if xs else 0.0
    return {"mean_link": mean(link_deltas), "mean_comparable": mean(all_deltas),
            "n_links": len(link_deltas), "n_comparable": len(all_deltas)}


def _conformal_recovery(points, b, n_bins):
    bins = [0] * n_bins
    for p in points:
        idx = min(int(p[1] * n_bins), n_bins - 1)
        bins[idx] += 1
    mean_count = sum(bins) / n_bins
    recovered = [c / mean_count for c in bins]
    xs = [(k + 0.5) / n_bins for k in range(n_bins)]
    truth = [1.0 + b * x for x in xs]
    mean_truth = sum(truth) / n_bins
    truth_norm = [w / mean_truth for w in truth]
    mse = sum((recovered[k] - truth_norm[k]) ** 2 for k in range(n_bins)) / n_bins
    return {"recovered": recovered, "truth": truth_norm, "mse": mse}


def build_report(protocol):
    mod = load_module("_qr05cf_t7_ref", MODULE_PATH)
    rows = protocol["n"]
    dims = protocol["dims"]
    seed = protocol["seed"]
    tol = protocol["dim_tolerance"]

    analytic = {d: _analytic_r(d) for d in dims}
    dimension = []
    for d in dims:
        points = mod.sprinkle_diamond(d, rows, seed=seed)
        r = _ordering_fraction(points)
        estimated = min(analytic, key=lambda key: abs(analytic[key] - r))
        dimension.append({
            "d": d,
            "r": _round(r),
            "analytic_r": _round(analytic[d]),
            "abs_err": _round(abs(r - analytic[d])),
            "within_tolerance": abs(r - analytic[d]) <= tol,
            "estimated": estimated,
            "recovers": estimated == d,
        })

    null_points = mod.sprinkle_diamond(2, protocol["nullness_n"], seed=protocol["nullness_seed"])
    nullness = _nullness(null_points)
    links_nearer = nullness["mean_link"] < nullness["mean_comparable"]

    b = protocol["conformal_b"]
    conf_points, _ = mod.conformal_sprinkle_1d(protocol["conformal_n"], b=b, seed=protocol["conformal_seed"])
    recovered = _conformal_recovery(conf_points, b, protocol["conformal_bins"])
    truth_monotone = all(recovered["truth"][i] <= recovered["truth"][i + 1]
                         for i in range(len(recovered["truth"]) - 1))
    trend_up = recovered["recovered"][-1] > recovered["recovered"][0]

    family_max = analytic[dims[0]]
    family_min = analytic[dims[-1]]
    chain_r = _ordering_fraction([(float(i), 0.0) for i in range(protocol["control_n"])])
    antichain_r = _ordering_fraction([(0.0, float(i)) for i in range(protocol["control_n"])])

    return {
        "schema": SCHEMA,
        "analytic_r": {str(d): _round(analytic[d]) for d in dims},
        "dimension": dimension,
        "nullness": {
            "mean_link": _round(nullness["mean_link"]),
            "mean_comparable": _round(nullness["mean_comparable"]),
            "n_links": nullness["n_links"],
            "n_comparable": nullness["n_comparable"],
            "links_nearer": links_nearer,
        },
        "conformal": {
            "b": b,
            "mse": _round(recovered["mse"]),
            "recovered": [_round(x) for x in recovered["recovered"]],
            "truth": [_round(x) for x in recovered["truth"]],
            "truth_monotone": truth_monotone,
            "trend_up": trend_up,
        },
        "invariance": {"invariant": bool(mod.conformal_invariance_of_order()["invariant"])},
        "negative_control": {
            "chain_r": _round(chain_r),
            "antichain_r": _round(antichain_r),
            "family_min": _round(family_min),
            "family_max": _round(family_max),
            "outside_family": chain_r > family_max and antichain_r < family_min,
        },
    }
