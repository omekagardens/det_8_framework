"""Independent reference route for the QR-05CQ adversarial control."""

from __future__ import annotations

import importlib.util
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


def _fractions(prec):
    n = len(prec)
    desc = [set() for _ in range(n)]
    anc = [set() for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if prec[i][j]:
                desc[i].add(j)
                anc[j].add(i)
    comparable = sum(len(desc[i]) for i in range(n))
    links = 0
    for i in range(n):
        for j in desc[i]:
            if len(desc[i] & anc[j]) == 0:
                links += 1
    r = comparable / (n * (n - 1) / 2.0) if n > 1 else 0.0
    lf = links / comparable if comparable else 0.0
    return r, lf


def _bipartite(n):
    half = n // 2
    return [[i < half <= j for j in range(n)] for i in range(n)]


def _chain(n):
    return [[i < j for j in range(n)] for i in range(n)]


def _antichain(n):
    return [[False] * n for _ in range(n)]


def build_report(protocol):
    module = load_module("_qr05cq_t7_ref", MODULE_PATH)
    n = protocol["n"]
    tol = protocol["dim_tolerance"]
    link_threshold = protocol["link_threshold"]

    manifoldlike = []
    for d in protocol["dims"]:
        pts = module.sprinkle_diamond(d, n, seed=protocol["seed"])
        r, lf = _fractions(_causality(pts))
        analytic = module.myrheim_meyer_ordering_fraction(d)
        dim_ok = abs(r - analytic) <= tol
        link_ok = lf <= link_threshold
        manifoldlike.append({"d": d, "r": _round(r), "analytic": _round(analytic),
                             "link_fraction": _round(lf), "dim_ok": dim_ok,
                             "link_ok": link_ok, "consistent": dim_ok and link_ok})

    adversarial = []
    for ident, matrix in (("bipartite", _bipartite(n)), ("chain", _chain(n)), ("antichain", _antichain(n))):
        r, lf = _fractions(matrix)
        analytic_two = module.myrheim_meyer_ordering_fraction(2)
        dim_ok = abs(r - analytic_two) <= tol
        link_ok = lf <= link_threshold
        adversarial.append({"id": ident, "r": _round(r), "link_fraction": _round(lf),
                            "dim_fooled": dim_ok, "link_ok": link_ok, "rejected": not (dim_ok and link_ok)})

    manifold_max_link = max(row["link_fraction"] for row in manifoldlike)
    bip = next(row for row in adversarial if row["id"] == "bipartite")
    separates = (manifold_max_link <= link_threshold < bip["link_fraction"]
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
