"""Primary route for the QR-05CU Minguzzi-Suhr LGH distance attempt (bounded).

Estimates the Lorentzian Gromov-Hausdorff distance between a supplied Minkowski
sprinkling (with the discrete chain-time-separation) and the continuum manifold,
via the natural correspondence and an optimized scale. This is a bounded UPPER
estimate, not the Minguzzi-Suhr infimum; the embedding theory and the
manifoldlikeness of the limit remain open. Supplied geometry; no gravity claim.
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05cu-report-v1"
AREA = 0.5


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


def chains_from(prec, order, source):
    n = len(prec)
    dist = [-1] * n
    dist[source] = 0
    for j in order:
        for i in range(n):
            if prec[i][j] and dist[i] >= 0 and dist[i] + 1 > dist[j]:
                dist[j] = dist[i] + 1
    return dist


def time_sep(p, q):
    dt = q[0] - p[0]
    spatial = sum((q[k] - p[k]) ** 2 for k in range(1, len(q)))
    return math.sqrt(dt * dt - spatial) if dt * dt > spatial else 0.0


def median(values):
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def lgh_estimate(pairs, floor):
    """Bounded distortion of the natural correspondence after a scale fit."""
    if not pairs:
        return 0.0, 1.0
    max_t = max(b for _, b in pairs)
    usable = [(a, b) for a, b in pairs if b >= floor * max_t]
    scale = median([b / a for a, b in usable])
    deviation = sum(abs(scale * a - b) for a, b in usable) / len(usable)
    return deviation, scale


def build_report(protocol):
    module = load_module("_qr05cu_t7", MODULE_PATH)
    seed = protocol["seed"]
    floor = protocol["tau_floor"]
    rows = []
    for n in protocol["n_grid"]:
        points = module.sprinkle_diamond(2, n, seed=seed)
        prec = causality(points)
        order = sorted(range(n), key=lambda i: points[i][0])
        ell = math.sqrt(AREA / n)
        step = max(1, n // protocol["sources"])
        sources = order[::step][:protocol["sources"]]

        pairs = []
        for src in sources:
            dist = chains_from(prec, order, src)
            for j in range(n):
                if dist[j] > 0:
                    tau = time_sep(points[src], points[j])
                    if tau > 0:
                        pairs.append((dist[j] * ell, tau))
        forward, scale = lgh_estimate(pairs, floor)

        rng = random.Random(seed)
        probes = []
        while len(probes) < protocol["probes"]:
            t = rng.random()
            x = (rng.random() - 0.5) * 2 * min(t, 1 - t)
            probes.append((t, x))
        nearest = [min(range(n), key=lambda i: (points[i][0] - y[0]) ** 2 + (points[i][1] - y[1]) ** 2)
                   for y in probes]
        cache = {}
        cover_pairs = []
        for a in range(len(probes)):
            ia = nearest[a]
            if ia not in cache:
                cache[ia] = chains_from(prec, order, ia)
            for b in range(a + 1, len(probes)):
                ib = nearest[b]
                if ib not in cache:
                    cache[ib] = chains_from(prec, order, ib)
                tau = time_sep(probes[a], probes[b])
                chain = cache[ia][ib] if cache[ia][ib] > 0 else cache[ib][ia]
                if tau > 0 and chain > 0:
                    cover_pairs.append((chain * ell, tau))
        cover, _ = lgh_estimate(cover_pairs, floor)
        d_ub = max(forward, cover)
        rows.append({"n": n, "scale": _round(scale), "forward": _round(forward),
                     "cover": _round(cover), "d_ub": _round(d_ub), "ell": _round(ell)})

    # control: a random correspondence of the chain distances
    n_ctl = protocol["n_grid"][-1]
    pts = module.sprinkle_diamond(2, n_ctl, seed=seed)
    prec = causality(pts)
    order = sorted(range(n_ctl), key=lambda i: pts[i][0])
    ell = math.sqrt(AREA / n_ctl)
    step = max(1, n_ctl // protocol["sources"])
    sources = order[::step][:protocol["sources"]]
    rng = random.Random(seed + 1)
    control_pairs = []
    for src in sources:
        dist = chains_from(prec, order, src)
        perm = list(range(n_ctl))
        rng.shuffle(perm)
        for j in range(n_ctl):
            if dist[j] > 0:
                tau = time_sep(pts[src], pts[perm[j]])
                if tau > 0:
                    control_pairs.append((dist[j] * ell, tau))
    control, _ = lgh_estimate(control_pairs, floor)

    dubs = [r["d_ub"] for r in rows]
    decreasing = all(dubs[i] > dubs[i + 1] for i in range(len(dubs) - 1))
    separates = control > protocol["control_factor"] * max(dubs)

    return {
        "schema": SCHEMA,
        "rows": rows,
        "d_ub_decreasing": bool(decreasing),
        "control": {"distortion": _round(control), "separates": bool(separates)},
        "lgh_estimate_converges": bool(decreasing and separates),
    }
