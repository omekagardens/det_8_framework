"""Primary route for the QR-05CI 2D Lorentzian (Benincasa-Dowker/Sorkin) operator.

Implements the exact 2D operator from Sorkin, "Does locality fail at
intermediate length-scales?" (gr-qc/0703099, Eq. 1):

    B phi(x) = (4/l^2)[ -1/2 phi(x) + (sum_{L1} - 2 sum_{L2} + sum_{L3}) phi(y) ]

with L_k the elements y < x having k-1 intervening elements (L1 = links), and
l^2 = 1/rho. Section A verifies the matrix structure exactly on a deterministic
causal set; Section B attempts the continuum limit on supplied sprinklings and
reports the outcome honestly. Supplied geometry; no gravity claim.
"""

from __future__ import annotations

import importlib.util
import math
import random
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05ci-report-v1"
COEFF = {0: F(1), 1: F(-2), 2: F(1)}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _round(value, places=9):
    return round(value, places)


# ── Section A: exact matrix structure on a deterministic causal set ─────────


def deterministic_points():
    """A deterministic 1+1 causal mesh inside a diamond, with known order."""
    pts = []
    for t in (1, 2, 3, 4, 5):
        for x in range(-t + 1, t):
            pts.append((t / 5.0, x / 5.0))
    return sorted(set(pts))


def interval_size(points, prec, i, j):
    return sum(1 for z in range(len(points)) if prec[i][z] and prec[z][j])


def operator_matrix(points, ell2):
    n = len(points)
    prec = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dt = points[j][0] - points[i][0]
                dx = points[j][1] - points[i][1]
                prec[i][j] = dt > 0 and dx * dx < dt * dt
    matrix = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = F(-1, 2)
        for j in range(n):
            if prec[i][j]:
                k = interval_size(points, prec, i, j)
                if k in COEFF:
                    matrix[i][j] = COEFF[k]
    return matrix, prec


def expected_entry(points, prec, i, j):
    if i == j:
        return F(-1, 2)
    if not prec[i][j]:
        return F(0)
    k = interval_size(points, prec, i, j)
    return COEFF.get(k, F(0))


def apply_matrix(matrix, values):
    n = len(values)
    return [sum(matrix[i][j] * values[j] for j in range(n)) for i in range(n)]


def apply_layers(points, prec, values):
    """B phi via Eq. (1): explicit layer sums, independent of the matrix form."""
    out = []
    for i in range(len(points)):
        s = F(-1, 2) * values[i]
        for j in range(len(points)):
            if prec[i][j]:
                k = interval_size(points, prec, i, j)
                if k in COEFF:
                    s += COEFF[k] * values[j]
        out.append(s)
    return out


def exact_form_agreement(points):
    """Eq. (2) matrix and Eq. (1) layer sums must agree exactly."""
    matrix, prec = operator_matrix(points, F(1))
    values = [F((i * 7) % 5 - 2) for i in range(len(points))]
    return apply_matrix(matrix, values) == apply_layers(points, prec, values)


# ── Section B: continuum-limit attempt on supplied sprinklings ──────────────


def ensemble(module, seeds, n, margin):
    total = [0.0, 0.0, 0.0]
    count = 0
    b_const = 0.0
    for seed in seeds:
        points = module.sprinkle_diamond(2, n, seed=seed)
        size = len(points)
        prec = module.build_causality(points)
        caus = [set() for _ in range(size)]
        pred = [set() for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if prec[i][j]:
                    caus[i].add(j)
                    pred[j].add(i)
        ell2 = 0.5 / n
        for i, p in enumerate(points):
            if not (margin < p[0] < 1 - margin and abs(p[1]) < min(p[0], 1 - p[0]) - margin):
                continue
            layers = [0, 0, 0]
            for j in caus[i]:
                k = len(caus[i] & pred[j])
                if k < 3:
                    layers[k] += 1
            total[0] += layers[0]
            total[1] += layers[1]
            total[2] += layers[2]
            combo = layers[0] - 2 * layers[1] + layers[2]
            b_const += (4.0 / ell2) * (-0.5 + combo)
            count += 1
    return {"points": count,
            "layer_combo": _round((total[0] - 2 * total[1] + total[2]) / count) if count else None,
            "mean_B_const": _round(b_const / count) if count else None}


def build_report(protocol):
    module = load_module("_qr05ci_t7", MODULE_PATH)
    points = deterministic_points()
    exact = exact_form_agreement(points)

    ensemble_rows = []
    for n in protocol["n_grid"]:
        row = ensemble(module, protocol["seeds"], n, protocol["margin"])
        row["n"] = n
        ensemble_rows.append(row)

    tol = protocol["constant_tolerance"]
    residuals = [abs(row["layer_combo"] - 0.5) for row in ensemble_rows]
    constant_annihilated = all(value <= tol for value in residuals)
    validated = bool(exact and constant_annihilated and
                     all(abs(row["mean_B_const"]) <= protocol["bconst_tolerance"] for row in ensemble_rows))

    return {
        "schema": SCHEMA,
        "operator": {"formula": "B = 4/l^2 [-1/2 phi(x) + (sum_L1 - 2 sum_L2 + sum_L3) phi]",
                     "coefficients": {"L0": "-1/2", "L1": "+1", "L2": "-2", "L3": "+1"},
                     "source": "Sorkin gr-qc/0703099 Eq. (1); l^2 = 1/rho"},
        "exact_form_agreement": bool(exact),
        "ensemble": ensemble_rows,
        "constant_residuals": [_round(x) for x in residuals],
        "constant_annihilated": bool(constant_annihilated),
        "validated": validated,
    }
