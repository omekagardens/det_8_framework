"""Primary route for the QR-05CF supplied-geometry (T7) benchmark.

Runs the existing ``det8/models/order_count_geometry.py`` estimators on
supplied Minkowski sprinklings and a conformal sprinkling, with a fixed-seed,
deterministic report. Nothing here derives geometry; it verifies that the T7
estimators work on *known* data and that a non-diamond control fails.
"""

from __future__ import annotations

import importlib.util
import json
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


def build_report(protocol):
    mod = load_module("_qr05cf_t7", MODULE_PATH)
    rows = protocol["n"]
    dims = protocol["dims"]
    seed = protocol["seed"]
    tol = protocol["dim_tolerance"]

    analytic = {d: mod.myrheim_meyer_ordering_fraction(d) for d in dims}
    dimension = []
    for d in dims:
        points = mod.sprinkle_diamond(d, rows, seed=seed)
        r = mod.ordering_fraction(points)
        estimated = mod.estimate_dimension(points, analytic)
        dimension.append({
            "d": d,
            "r": _round(r),
            "analytic_r": _round(analytic[d]),
            "abs_err": _round(abs(r - analytic[d])),
            "within_tolerance": bool(abs(r - analytic[d]) <= tol),
            "estimated": estimated,
            "recovers": bool(estimated == d),
        })

    null_rows = protocol["nullness_n"]
    null_points = mod.sprinkle_diamond(2, null_rows, seed=protocol["nullness_seed"])
    null_prec = mod.build_causality(null_points)
    nullness = mod.link_nullness(null_points, null_prec)
    links_nearer = bool(nullness["mean_link_nullness"] < nullness["mean_comparable_nullness"])

    b = protocol["conformal_b"]
    conf_points, weight = mod.conformal_sprinkle_1d(protocol["conformal_n"], b=b, seed=protocol["conformal_seed"])
    recovered = mod.recover_conformal_factor(conf_points, weight, b=b, n_bins=protocol["conformal_bins"])
    truth_monotone = all(recovered["truth"][i] <= recovered["truth"][i + 1]
                         for i in range(len(recovered["truth"]) - 1))
    trend_up = recovered["recovered"][-1] > recovered["recovered"][0]

    invariance = mod.conformal_invariance_of_order()

    family_max = analytic[dims[0]]
    family_min = analytic[dims[-1]]
    chain_r = mod.ordering_fraction([(float(i), 0.0) for i in range(protocol["control_n"])])
    antichain_r = mod.ordering_fraction([(0.0, float(i)) for i in range(protocol["control_n"])])
    outside_family = bool(chain_r > family_max and antichain_r < family_min)

    return {
        "schema": SCHEMA,
        "analytic_r": {str(d): _round(analytic[d]) for d in dims},
        "dimension": dimension,
        "nullness": {
            "mean_link": _round(nullness["mean_link_nullness"]),
            "mean_comparable": _round(nullness["mean_comparable_nullness"]),
            "n_links": nullness["n_links"],
            "n_comparable": nullness["n_comparable"],
            "links_nearer": links_nearer,
        },
        "conformal": {
            "b": b,
            "mse": _round(recovered["mse"]),
            "recovered": [_round(x) for x in recovered["recovered"]],
            "truth": [_round(x) for x in recovered["truth"]],
            "truth_monotone": bool(truth_monotone),
            "trend_up": bool(trend_up),
        },
        "invariance": {"invariant": bool(invariance["invariant"])},
        "negative_control": {
            "chain_r": _round(chain_r),
            "antichain_r": _round(antichain_r),
            "family_min": _round(family_min),
            "family_max": _round(family_max),
            "outside_family": outside_family,
        },
    }
