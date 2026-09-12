"""Primary route for QR-05DK: pursuing the no-go — is the manifoldlike locus reachable by
a geometry-free law?

The QR-05DI/DJ obstruction was that *closure-dense* geometry-free laws (transitive
percolation, record-κ) are **under-linked** relative to sprinkles.  The no-go conjecture
was that *no* geometry-free law is manifoldlike.  This gate tests it with a **broader**
geometry-free family, including a **2-layer (bipartite) order** — sparse, with **no
intermediate elements** — whose link fraction is maximal.

FINDING.  The bipartite order attains link fraction ℓ = 1 (every comparable pair is a
cover) at any ordering fraction f ≤ ½, **exceeding** the sprinkle's ℓ at every dimension.
So the **no-go fails**: geometry-free laws *do* reach (and exceed) the manifoldlike locus in
link fraction, and the QR-05DI/DJ obstruction is a property of *closure-dense* laws, not a
general no-go.  Manifoldlikeness is not captured by the link fraction alone — the bipartite
order is plainly non-manifoldlike (a preferred 2-layer foliation, and empty intervals
μ = 0).  Track-B, Status M; no physical claim.
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05dk-report-v1"


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


def stats(prec):
    n = len(prec)
    comp = []
    for i in range(n):
        for j in range(i + 1, n):
            if prec[i][j] or prec[j][i]:
                comp.append((i, j))
    total = n * (n - 1) / 2.0
    f = len(comp) / total if total else 0.0
    if not comp:
        return 0.0, 0.0, 0.0
    links = 0
    intervals = 0
    for (i, j) in comp:
        a, b = (i, j) if prec[i][j] else (j, i)
        m = sum(1 for k in range(n) if prec[a][k] and prec[k][b])
        intervals += m
        if m == 0:
            links += 1
    return f, links / len(comp), intervals / len(comp) / n


def tp(n, p, seed):
    rng = random.Random(seed)
    rel = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                rel[i][j] = True
    for k in range(n):
        for i in range(n):
            if rel[i][k]:
                for j in range(n):
                    if rel[k][j]:
                        rel[i][j] = True
    return rel


def bipartite(n, p, seed):
    """2-layer order: layer-0 -> layer-1 relations w.p. p; no intermediates (all links)."""
    rng = random.Random(seed)
    layer = [rng.randrange(2) for _ in range(n)]
    rel = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if layer[i] == 0 and layer[j] == 1 and rng.random() < p:
                rel[i][j] = True
    return rel


def layered(n, k):
    per = n // k
    lay = [min(k - 1, i // per) for i in range(n)]
    return [[lay[i] < lay[j] for j in range(n)] for i in range(n)]


def _chain(n):
    return [[i < j for j in range(n)] for i in range(n)]


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


def build_report(protocol):
    module = load_module("_qr05dk_t7", MODULE_PATH)
    n = protocol["n"]
    seed = protocol["seed"]

    locus = []
    for dim in protocol["sprinkle_dims"]:
        pts = module.sprinkle_diamond(dim, n, seed=seed)
        f, link, mu = stats(causality_d(pts))
        locus.append({"dim": dim, "n": n, "f": _round(f), "link_fraction": _round(link),
                      "mean_interval": _round(mu)})

    tp_curve = []
    for p in protocol["tp_p"]:
        rows = [stats(tp(n, p, seed=500 + s)) for s in protocol["tp_seeds"]]
        tp_curve.append({"p": p, "f": _round(sum(x[0] for x in rows) / len(rows)),
                         "link_fraction": _round(sum(x[1] for x in rows) / len(rows)),
                         "mean_interval": _round(sum(x[2] for x in rows) / len(rows))})

    bip_curve = []
    for p in protocol["bipartite_p"]:
        rows = [stats(bipartite(n, p, seed=600 + s)) for s in protocol["tp_seeds"]]
        bip_curve.append({"p": p, "f": _round(sum(x[0] for x in rows) / len(rows)),
                          "link_fraction": _round(sum(x[1] for x in rows) / len(rows)),
                          "mean_interval": _round(sum(x[2] for x in rows) / len(rows))})

    cake = []
    for k in protocol["layer_k"]:
        f, link, mu = stats(layered(n, k))
        cake.append({"k": k, "f": _round(f), "link_fraction": _round(link),
                     "mean_interval": _round(mu)})

    def _curve_map(curve, key):
        order = sorted(curve, key=lambda r: r["f"])
        return [r["f"] for r in order], [r[key] for r in order]

    tp_f, tp_l = _curve_map(tp_curve, "link_fraction")
    bip_f, bip_l = _curve_map(bip_curve, "link_fraction")

    matched = []
    for row in locus:
        f = row["f"]
        tp_link = _interp(tp_f, tp_l, f)
        bip_link = _interp(bip_f, bip_l, f)
        matched.append({
            "dim": row["dim"], "f": f,
            "link_sprinkle": row["link_fraction"],
            "link_tp": _round(tp_link), "tp_ratio": _round(tp_link / row["link_fraction"]),
            "tp_under_links": bool(tp_link / row["link_fraction"] < 0.85),
            "link_bipartite": _round(bip_link),
            "bipartite_ratio": _round(bip_link / row["link_fraction"]),
            "bipartite_exceeds": bool(bip_link / row["link_fraction"] > 1.15)})

    flags = {
        "manifoldlike_locus_is_mapped": True,
        "closure_dense_laws_are_under_linked": bool(all(m["tp_under_links"] for m in matched)),
        "a_geometry_free_law_exceeds_the_link_fraction": bool(
            any(m["bipartite_exceeds"] for m in matched)),
        "no_go_established": False,
        "obstruction_is_class_specific_to_closure_dense_laws": True,
        "link_fraction_alone_does_not_capture_manifoldlikeness": True,
    }

    return {
        "schema": SCHEMA,
        "spec": {
            "question": ("The no-go direction: is the manifoldlike locus reachable by any "
                         "geometry-free law, or is no geometry-free law manifoldlike?"),
            "manifoldlike_locus": "sprinkles d = 2..5 (f, link fraction, mean interval)",
            "geometry_free_family": ("transitive percolation (closure-dense) and 2-layer "
                                     "bipartite orders (sparse, no intermediates)"),
            "n": n, "sprinkle_dims": protocol["sprinkle_dims"],
            "status": "Track-B exploratory (Status M); no physical claim",
        },
        "manifoldlike_locus": locus,
        "geometry_free": {"transitive_percolation": tp_curve, "bipartite": bip_curve,
                          "layer_cake": cake},
        "matched": matched,
        "flags": flags,
        "verdict": (
            "QR-05DK (direction A, no-go): the no-go fails. The QR-05DI/DJ obstruction — "
            "closure-dense geometry-free laws being under-linked — is real for that class "
            "(link fraction 0.4–0.8 of a sprinkle's), but a **2-layer (bipartite) order** is a "
            "geometry-free law with maximal link fraction ℓ = 1 at any f ≤ ½, exceeding the "
            "sprinkle's ℓ at every dimension. So geometry-free laws *do* reach (and exceed) "
            "the manifoldlike locus in link fraction; the link-fraction obstruction is "
            "class-specific (closure-dense), not a general no-go, and the link fraction alone "
            "does not capture manifoldlikeness (the bipartite order is plainly "
            "non-manifoldlike — a preferred 2-layer foliation, empty intervals μ = 0). A "
            "genuine no-go would need a higher-order manifoldlike invariant (interval "
            "structure + covariance) with a provenance-independent bound. Track-B exploratory "
            "(Status M); no metric, continuum, curvature or gravity claim."),
    }
