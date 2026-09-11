"""Independent reference route for the QR-05CU LGH distance attempt."""

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


def _chains(prec, order, source):
    n = len(prec)
    dist = [-1] * n
    dist[source] = 0
    for j in order:
        for i in order:
            if prec[i][j] and dist[i] >= 0 and dist[i] + 1 > dist[j]:
                dist[j] = dist[i] + 1
    return dist


def _tau(p, q):
    dt = q[0] - p[0]
    spatial = sum((q[k] - p[k]) ** 2 for k in range(1, len(q)))
    return math.sqrt(dt * dt - spatial) if dt * dt > spatial else 0.0


def _median(values):
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def _estimate(pairs, floor):
    if not pairs:
        return 0.0, 1.0
    cap = max(b for _, b in pairs)
    keep = [(a, b) for a, b in pairs if b >= floor * cap]
    scale = _median([b / a for a, b in keep])
    deviation = 0.0
    for a, b in keep:
        deviation += abs(scale * a - b)
    return deviation / len(keep), scale


def build_report(protocol):
    module = load_module("_qr05cu_t7_ref", MODULE_PATH)
    seed = protocol["seed"]
    floor = protocol["tau_floor"]
    rows = []
    for n in protocol["n_grid"]:
        pts = module.sprinkle_diamond(2, n, seed=seed)
        prec = _causality(pts)
        order = sorted(range(n), key=lambda i: pts[i][0])
        ell = math.sqrt(AREA / n)
        sources = order[::max(1, n // protocol["sources"])][:protocol["sources"]]

        pairs = []
        for src in sources:
            dist = _chains(prec, order, src)
            for j in range(n):
                if dist[j] > 0:
                    tau = _tau(pts[src], pts[j])
                    if tau > 0:
                        pairs.append((dist[j] * ell, tau))
        forward, scale = _estimate(pairs, floor)

        rng = random.Random(seed)
        probes = []
        while len(probes) < protocol["probes"]:
            t = rng.random()
            x = (rng.random() - 0.5) * 2 * min(t, 1 - t)
            probes.append((t, x))
        near = [min(range(n), key=lambda i: (pts[i][0] - y[0]) ** 2 + (pts[i][1] - y[1]) ** 2) for y in probes]
        cache = {}
        cpairs = []
        for a in range(len(probes)):
            ia = near[a]
            if ia not in cache:
                cache[ia] = _chains(prec, order, ia)
            for b in range(a + 1, len(probes)):
                ib = near[b]
                if ib not in cache:
                    cache[ib] = _chains(prec, order, ib)
                tau = _tau(probes[a], probes[b])
                ch = cache[ia][ib] if cache[ia][ib] > 0 else cache[ib][ia]
                if tau > 0 and ch > 0:
                    cpairs.append((ch * ell, tau))
        cover, _ = _estimate(cpairs, floor)
        rows.append({"n": n, "scale": _round(scale), "forward": _round(forward),
                     "cover": _round(cover), "d_ub": _round(max(forward, cover)), "ell": _round(ell)})

    n_ctl = protocol["n_grid"][-1]
    pts = module.sprinkle_diamond(2, n_ctl, seed=seed)
    prec = _causality(pts)
    order = sorted(range(n_ctl), key=lambda i: pts[i][0])
    ell = math.sqrt(AREA / n_ctl)
    sources = order[::max(1, n_ctl // protocol["sources"])][:protocol["sources"]]
    rng = random.Random(seed + 1)
    ctrl_pairs = []
    for src in sources:
        dist = _chains(prec, order, src)
        perm = list(range(n_ctl))
        rng.shuffle(perm)
        for j in range(n_ctl):
            if dist[j] > 0:
                tau = _tau(pts[src], pts[perm[j]])
                if tau > 0:
                    ctrl_pairs.append((dist[j] * ell, tau))
    control, _ = _estimate(ctrl_pairs, floor)

    dubs = [r["d_ub"] for r in rows]
    decreasing = all(dubs[i] > dubs[i + 1] for i in range(len(dubs) - 1))
    separates = control > protocol["control_factor"] * max(dubs)

    return {
        "schema": SCHEMA,
        "rows": rows,
        "d_ub_decreasing": decreasing,
        "control": {"distortion": _round(control), "separates": separates},
        "lgh_estimate_converges": decreasing and separates,
    }
