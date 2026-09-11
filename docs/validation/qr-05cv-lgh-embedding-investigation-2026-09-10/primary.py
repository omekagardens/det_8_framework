"""Primary route for the QR-05CV LGH/embedding investigation (exact LMS core).

Research-grade investigation of a Lorentzian Gromov-Hausdorff route for causal
sets. This bounded component establishes the exact core: the discrete
chain-time-separation is a genuine Lorentzian metric space (Minguzzi-Suhr style)
whose causality relation is the causal order and which satisfies the reverse
triangle inequality exactly, while the Riemannian triangle fails. The full LGH
distance and embedding theory remain open. Supplied geometry; no gravity claim.
"""

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


def lms_axioms(prec, chain):
    n = len(prec)
    diagonal = all(chain[i][i] == 0 for i in range(n))
    causality_iff_order = all((chain[i][j] > 0) == prec[i][j] for i in range(n) for j in range(n))
    antisymmetric = all(chain[j][i] == 0 for i in range(n) for j in range(n) if chain[i][j] > 0)
    reverse_triangle = True
    for i in range(n):
        for j in range(n):
            if chain[i][j] <= 0:
                continue
            for k in range(n):
                if chain[j][k] > 0 and chain[i][k] < chain[i][j] + chain[j][k]:
                    reverse_triangle = False
                    break
    return {"A1_diagonal_zero": diagonal, "A2_causality_iff_order": causality_iff_order,
            "A3_causality_antisymmetric": antisymmetric, "A4_reverse_triangle": reverse_triangle}


def riemannian_triangle_fails(prec, chain):
    n = len(prec)
    for i in range(n):
        for k in range(n):
            if chain[i][k] > 0:
                for j in range(n):
                    if chain[i][j] == 0 and chain[j][k] == 0:
                        return True, (i, j, k, chain[i][k])
    return False, None


def build_report(protocol):
    module = load_module("_qr05cv_t7", MODULE_PATH)
    rows = []
    for d in protocol["dims"]:
        points = module.sprinkle_diamond(d, protocol["n"], seed=protocol["seed"])
        prec = causality(points)
        order = sorted(range(len(points)), key=lambda i: points[i][0])
        chain = chain_matrix(prec, order)
        axioms = lms_axioms(prec, chain)
        fails, witness = riemannian_triangle_fails(prec, chain)
        rows.append({"d": d, "axioms": axioms,
                     "all_axioms_hold": all(axioms.values()),
                     "riemannian_triangle_fails": bool(fails),
                     "witness": witness})

    return {
        "schema": SCHEMA,
        "rows": rows,
        "lms_candidate_verified": bool(all(r["all_axioms_hold"] for r in rows)
                                       and all(r["riemannian_triangle_fails"] for r in rows)),
    }
