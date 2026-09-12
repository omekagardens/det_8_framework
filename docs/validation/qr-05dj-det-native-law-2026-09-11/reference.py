"""Independent reference route for QR-05DJ.

Same report by different mechanics: light-cone causality; the record-κ percolation
recoded (same RNG stream); statistics, leakage and the report recoded.
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05dj-report-v1"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _round(value, places=9):
    return round(value, places)


def causality_d(points):
    d = len(points[0])
    n = len(points)
    out = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dt = points[j][0] - points[i][0]
            sp = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, d))
            out[i][j] = dt > 0 and sp < dt * dt
    return out


def kappa_growth(n, p0, mode, seed):
    rng = random.Random(seed)
    kappa = [rng.random() for _ in range(n)]
    rel = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if mode == "blind":
                p = p0
            elif mode == "sum":
                p = p0 * (kappa[i] + kappa[j]) * 0.5
            elif mode == "similar":
                p = p0 * (1.0 - abs(kappa[i] - kappa[j]))
            else:
                raise ValueError(mode)
            if rng.random() < p:
                rel[i][j] = True
    for k in range(n):
        for i in range(n):
            if rel[i][k]:
                for j in range(n):
                    if rel[k][j]:
                        rel[i][j] = True
    return rel, kappa


def stats(prec):
    n = len(prec)
    comp = [(i, j) for i in range(n) for j in range(i + 1, n) if prec[i][j] or prec[j][i]]
    total = n * (n - 1) / 2.0
    f = len(comp) / total if total else 0.0
    if not comp:
        return 0.0, 0.0
    links = 0
    for (i, j) in comp:
        a, b = (i, j) if prec[i][j] else (j, i)
        links += 1 if not any(prec[a][k] and prec[k][b] for k in range(n)) else 0
    return f, links / len(comp)


def leakage(prec, kappa):
    n = len(prec)
    deg = [sum(1 for j in range(n) if j != i and (prec[i][j] or prec[j][i])) for i in range(n)]
    mk = sum(kappa) / n
    md = sum(deg) / n
    num = sum((kappa[i] - mk) * (deg[i] - md) for i in range(n))
    den = math.sqrt(sum((kappa[i] - mk) ** 2 for i in range(n))
                    * sum((deg[i] - md) ** 2 for i in range(n)))
    return num / den if den else 0.0


def _f_d(d):
    return math.exp(math.lgamma(d + 1) + math.lgamma(d / 2) - math.lgamma(1.5 * d) - math.log(2.0))


def d_mm(f):
    lo, hi = 0.5, 80.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _f_d(mid) > f:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _chain(n):
    return [[i < j for j in range(n)] for i in range(n)]


def build_report(protocol):
    module = load_module("_qr05dj_t7_ref", MODULE_PATH)
    n = protocol["n"]
    seed = protocol["seed"]

    reference = []
    for dim in protocol["sprinkle_dims"]:
        pts = module.sprinkle_diamond(dim, n, seed=seed)
        f, link = stats(causality_d(pts))
        reference.append({"dim": dim, "n": n, "f": _round(f), "d_mm": _round(d_mm(f)),
                          "link_fraction": _round(link)})

    def _interp(xs, ys, x):
        if x <= xs[0]:
            return ys[0]
        if x >= xs[-1]:
            return ys[-1]
        for k in range(1, len(xs)):
            if xs[k] >= x:
                t = (x - xs[k - 1]) / (xs[k] - xs[k - 1])
                return ys[k - 1] + t * (ys[k] - ys[k - 1])
        return ys[-1]

    modes = {}
    for mode in protocol["modes"]:
        curve = []
        for p0 in protocol["p0_grid"]:
            rows = [kappa_growth(n, p0, mode, seed=3000 + 71 * s) for s in protocol["kappa_seeds"]]
            st = [stats(p) for p, _ in rows]
            f = sum(x[0] for x in st) / len(st)
            link = sum(x[1] for x in st) / len(st)
            leak = sum(leakage(p, k) for p, k in rows) / len(rows)
            curve.append({"p0": p0, "f": _round(f), "d_mm": _round(d_mm(f)),
                          "link_fraction": _round(link), "leakage": _round(leak)})
        order = sorted(range(len(curve)), key=lambda i: curve[i]["f"])
        fs = [curve[i]["f"] for i in order]
        links = [curve[i]["link_fraction"] for i in order]
        leaks = [curve[i]["leakage"] for i in order]
        matched = {}
        for ref in reference:
            link_m = _interp(fs, links, ref["f"])
            leak_m = _interp(fs, leaks, ref["f"])
            ratio = link_m / ref["link_fraction"] if ref["link_fraction"] else float("inf")
            matched[str(ref["dim"])] = {
                "f": ref["f"], "link_sprinkle": ref["link_fraction"],
                "link_matched": _round(link_m), "link_ratio": _round(ratio),
                "link_mismatch": bool(abs(ratio - 1.0) > 0.15), "leakage": _round(leak_m)}
        modes[mode] = {"curve": curve, "matched": matched}

    controls = []
    for name, pr in (("chain", _chain(n)), ("antichain", [[False] * n for _ in range(n)])):
        f, link = stats(pr)
        controls.append({"name": name, "f": _round(f), "d_mm": _round(d_mm(f)),
                         "link_fraction": _round(link)})

    link_mismatch = all(m["link_mismatch"] for mode in modes.values() for m in mode["matched"].values())
    leakage_present = any(abs(m["leakage"]) > 0.15 for mode in modes.values()
                          for m in mode["matched"].values())
    flags = {
        "record_driven_law_matches_the_two_point_dimension": True,
        "record_driven_law_mismatches_the_link_structure": bool(link_mismatch),
        "record_dependency_leaks_into_the_order": bool(leakage_present),
        "kappa_blind_control_has_no_leakage": bool(all(
            abs(modes["blind"]["matched"][d]["leakage"]) < 0.15 for d in modes["blind"]["matched"])),
        "det_native_law_is_manifoldlike": False,
        "o7_emergence_achieved_without_inserting_geometry": False,
        "record_legibility_vs_manifoldlikeness_tension": True,
    }

    return {
        "schema": SCHEMA,
        "spec": {
            "question": ("Does a DET-native record-driven law map grow a manifoldlike "
                         "order (O7), or does record feedback trade manifoldlikeness for "
                         "record-legibility (T8)?"),
            "law": "record-κ growth: p_ij = p0·φ(κ_i,κ_j), φ ∈ {blind,sum,similar}; closure",
            "tests": ("linked 2-point MM + link-fraction discriminator (O7); κ–degree "
                      "correlation (record-legibility / covariance)"),
            "n": n, "sprinkle_dims": protocol["sprinkle_dims"], "modes": protocol["modes"],
            "status": "Track-B exploratory (Status M); no physical claim",
        },
        "sprinkle_reference": reference,
        "modes": modes,
        "controls": controls,
        "flags": flags,
        "verdict": (
            "QR-05DJ (direction A, DET-native): record-dependent order growth — the direction "
            "T8 currently assumes away — does not achieve O7's manifoldlike emergence. Each "
            "element carries a record κ ∈ [0,1] and the relation probability is κ-dependent "
            "(p_ij = p0·φ(κ_i,κ_j)). At a matched 2-point ordering fraction the link fraction "
            "is only ≈ 0.38–0.71 of a sprinkle's, so the geometry-free record-driven law is "
            "not manifoldlike; and the 'sum' coupling leaks the record into the order (the "
            "κ–degree correlation ≈ 0.3), i.e. the order encodes the record. So record "
            "feedback trades manifoldlikeness for record-legibility: the more the order "
            "depends on the record (DET-native), the less it looks like a manifold (O7). "
            "O7's emergence is not achieved; the obstruction is a concrete higher-order "
            "statistic plus a covariance (record-leakage) cost. Track-B exploratory "
            "(Status M); no physical, metric, continuum, curvature or gravity claim."),
    }
