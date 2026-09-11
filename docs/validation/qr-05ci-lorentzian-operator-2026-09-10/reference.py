"""Independent reference route for the QR-05CI 2D Lorentzian operator.

Re-implements the matrix construction and the ensemble layer measurement with
different loop structure. The study compares with a float tolerance.
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05ci-report-v1"
WEIGHTS = [F(1), F(-2), F(1)]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _round(value, places=9):
    return round(value, places)


def _prec(points):
    n = len(points)
    out = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dt = points[j][0] - points[i][0]
                dx = points[j][1] - points[i][1]
                out[i][j] = dt > 0 and dx * dx < dt * dt
    return out


def deterministic_points():
    pts = set()
    for t in (1, 2, 3, 4, 5):
        for x in range(-t + 1, t):
            pts.add((t / 5.0, x / 5.0))
    return sorted(pts)


def _interior(prec, i, j):
    return sum(1 for z in range(len(prec)) if prec[i][z] and prec[z][j])


def exact_form_agreement(points):
    prec = _prec(points)
    n = len(points)

    def entry(i, j):
        if i == j:
            return F(-1, 2)
        if not prec[i][j]:
            return F(0)
        k = _interior(prec, i, j)
        return WEIGHTS[k] if k < 3 else F(0)

    values = [F((i * 7) % 5 - 2) for i in range(n)]
    via_matrix = []
    for i in range(n):
        total = F(0)
        for j in range(n):
            total += entry(i, j) * values[j]
        via_matrix.append(total)
    via_layers = []
    for i in range(n):
        total = F(-1, 2) * values[i]
        for j in range(n):
            if prec[i][j]:
                k = _interior(prec, i, j)
                if k < 3:
                    total += WEIGHTS[k] * values[j]
        via_layers.append(total)
    return via_matrix == via_layers


def ensemble(module, seeds, n, margin):
    totals = [0, 0, 0]
    count = 0
    bconst = 0.0
    for seed in seeds:
        points = module.sprinkle_diamond(2, n, seed=seed)
        prec = module.build_causality(points)
        size = len(points)
        desc = [set() for _ in range(size)]
        anc = [set() for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if prec[i][j]:
                    desc[i].add(j)
                    anc[j].add(i)
        ell2 = 0.5 / n
        for i in range(size):
            t, x = points[i]
            if not (margin < t < 1 - margin and abs(x) < min(t, 1 - t) - margin):
                continue
            layers = [0, 0, 0]
            for j in desc[i]:
                k = len(desc[i] & anc[j])
                if k < 3:
                    layers[k] += 1
            for k in range(3):
                totals[k] += layers[k]
            combo = layers[0] - 2 * layers[1] + layers[2]
            bconst += (4.0 / ell2) * (-0.5 + combo)
            count += 1
    combo_mean = (totals[0] - 2 * totals[1] + totals[2]) / count if count else None
    return {"points": count,
            "layer_combo": _round(combo_mean) if combo_mean is not None else None,
            "mean_B_const": _round(bconst / count) if count else None}


def build_report(protocol):
    module = load_module("_qr05ci_t7_ref", MODULE_PATH)
    exact = exact_form_agreement(deterministic_points())
    rows = []
    for n in protocol["n_grid"]:
        row = ensemble(module, protocol["seeds"], n, protocol["margin"])
        row["n"] = n
        rows.append(row)
    tol = protocol["constant_tolerance"]
    residuals = [abs(row["layer_combo"] - 0.5) for row in rows]
    constant_annihilated = all(value <= tol for value in residuals)
    validated = bool(exact and constant_annihilated and
                     all(abs(row["mean_B_const"]) <= protocol["bconst_tolerance"] for row in rows))
    return {
        "schema": SCHEMA,
        "operator": {"formula": "B = 4/l^2 [-1/2 phi(x) + (sum_L1 - 2 sum_L2 + sum_L3) phi]",
                     "coefficients": {"L0": "-1/2", "L1": "+1", "L2": "-2", "L3": "+1"},
                     "source": "Sorkin gr-qc/0703099 Eq. (1); l^2 = 1/rho"},
        "exact_form_agreement": exact,
        "ensemble": rows,
        "constant_residuals": [_round(x) for x in residuals],
        "constant_annihilated": constant_annihilated,
        "validated": validated,
    }
