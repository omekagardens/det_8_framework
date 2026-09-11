"""Primary route for the QR-05CQ T7 adversarial non-manifoldlike control.

Charter SS7.4: the geometric estimators must not confuse recovery with emergence.
The ordering-fraction dimension estimator alone is fooled by a non-manifoldlike
order tuned to the same ordering fraction; a joint test with the link fraction
(the share of comparable pairs that are links) rejects it. Supplied geometry; no
gravity claim.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05cq-report-v1"


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


def ordering_and_link_fraction(prec):
    n = len(prec)
    caus = [set(j for j in range(n) if prec[i][j]) for i in range(n)]
    pred = [set(i for i in range(n) if prec[i][j]) for j in range(n)]
    comparable = sum(len(caus[i]) for i in range(n))
    links = 0
    for i in range(n):
        for j in caus[i]:
            if not (caus[i] & pred[j]):
                links += 1
    r = comparable / (n * (n - 1) / 2) if n > 1 else 0.0
    link_fraction = links / comparable if comparable else 0.0
    return r, link_fraction


def bipartite_matrix(n):
    half = n // 2
    prec = [[False] * n for _ in range(n)]
    for i in range(half):
        for j in range(half, n):
            prec[i][j] = True
    return prec


def chain_matrix(n):
    return [[i < j for j in range(n)] for i in range(n)]


def antichain_matrix(n):
    return [[False] * n for _ in range(n)]


def build_report(protocol):
    module = load_module("_qr05cq_t7", MODULE_PATH)
    n = protocol["n"]
    tol = protocol["dim_tolerance"]
    link_threshold = protocol["link_threshold"]

    manifoldlike = []
    for d in protocol["dims"]:
        points = module.sprinkle_diamond(d, n, seed=protocol["seed"])
        r, lf = ordering_and_link_fraction(causality(points))
        analytic = module.myrheim_meyer_ordering_fraction(d)
        dim_ok = abs(r - analytic) <= tol
        link_ok = lf <= link_threshold
        manifoldlike.append({"d": d, "r": _round(r), "analytic": _round(analytic),
                             "link_fraction": _round(lf), "dim_ok": bool(dim_ok),
                             "link_ok": bool(link_ok), "consistent": bool(dim_ok and link_ok)})

    adversarial = []
    for ident, matrix in (("bipartite", bipartite_matrix(n)), ("chain", chain_matrix(n)),
                          ("antichain", antichain_matrix(n))):
        r, lf = ordering_and_link_fraction(matrix)
        analytic_two = module.myrheim_meyer_ordering_fraction(2)
        dim_ok = abs(r - analytic_two) <= tol
        link_ok = lf <= link_threshold
        adversarial.append({"id": ident, "r": _round(r), "link_fraction": _round(lf),
                            "dim_fooled": bool(dim_ok), "link_ok": bool(link_ok),
                            "rejected": bool(not (dim_ok and link_ok))})

    manifold_max_link = max(row["link_fraction"] for row in manifoldlike)
    bip = next(row for row in adversarial if row["id"] == "bipartite")
    separates = bool(manifold_max_link <= link_threshold < bip["link_fraction"]
                     and all(row["consistent"] for row in manifoldlike)
                     and bip["dim_fooled"] and bip["rejected"])

    return {
        "schema": SCHEMA,
        "manifoldlike": manifoldlike,
        "adversarial": adversarial,
        "discriminator": {"link_threshold": link_threshold,
                          "manifold_max_link": _round(manifold_max_link),
                          "bipartite_link": bip["link_fraction"],
                          "separates": separates},
    }
