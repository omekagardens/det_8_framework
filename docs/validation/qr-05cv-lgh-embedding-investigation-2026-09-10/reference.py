"""Independent reference route for the QR-05CV exact LMS core."""

from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05cv-report-v1"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def build_report(protocol):
    module = load_module("_qr05cv_t7_ref", MODULE_PATH)
    rows = []
    for d in protocol["dims"]:
        pts = module.sprinkle_diamond(d, protocol["n"], seed=protocol["seed"])
        prec = _causality(pts)
        order = sorted(range(len(pts)), key=lambda i: pts[i][0])
        chain = _chains(prec, order)
        n = len(pts)

        A1 = all(chain[i][i] == 0 for i in range(n))
        A2 = True
        A3 = True
        A4 = True
        fail = False
        witness = None
        for i in range(n):
            for j in range(n):
                if (chain[i][j] > 0) != prec[i][j]:
                    A2 = False
                if chain[i][j] > 0 and chain[j][i] != 0:
                    A3 = False
                if chain[i][j] > 0:
                    for k in range(n):
                        if chain[j][k] > 0 and chain[i][k] < chain[i][j] + chain[j][k]:
                            A4 = False
        for i in range(n):
            for k in range(n):
                if chain[i][k] > 0 and not fail:
                    for j in range(n):
                        if chain[i][j] == 0 and chain[j][k] == 0:
                            fail = True
                            witness = (i, j, k, chain[i][k])
                            break
        axioms = {"A1_diagonal_zero": A1, "A2_causality_iff_order": A2,
                  "A3_causality_antisymmetric": A3, "A4_reverse_triangle": A4}
        rows.append({"d": d, "axioms": axioms, "all_axioms_hold": all(axioms.values()),
                     "riemannian_triangle_fails": fail, "witness": witness})

    return {"schema": SCHEMA, "rows": rows,
            "lms_candidate_verified": all(r["all_axioms_hold"] for r in rows)
            and all(r["riemannian_triangle_fails"] for r in rows)}
