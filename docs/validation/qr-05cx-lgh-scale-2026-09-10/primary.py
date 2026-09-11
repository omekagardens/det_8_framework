"""Primary route for the QR-05CX LGH infimum at scale (branch-and-bound).

Extends QR-05CW from exhaustive search (N <= 8) to a depth-first branch-and-bound
that certifies the exact LGH-style distortion -- the minimum over correspondences
(bijections) of the maximum pairwise |d_X - d_Y| difference at a fixed scale -- on
larger small spaces (tested to N = 10; N = 11 and N = 12 are recorded boundary
runs, reproducible with `--n`). Adds a cheap certified lower bound (the
sorted-multiset matching bound), valid at any N, and sweeps it to N = 256 to make
an at-scale statement. Supplied geometry; the full LGH theory remains open; no
gravity claim.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import math
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05cx-report-v1"


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


def tau_matrix(points):
    n = len(points)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dt = points[j][0] - points[i][0]
            spatial = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, len(points[i])))
            out[i][j] = math.sqrt(dt * dt - spatial) if dt * dt > spatial else 0.0
    return out


def normalize(matrix):
    positive = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix)) if matrix[i][j] > 0]
    if not positive:
        return [[0.0] * len(matrix) for _ in matrix]
    mean = sum(positive) / len(positive)
    return [[matrix[i][j] / mean for j in range(len(matrix))] for i in range(len(matrix))]


def distortion(a, b, perm):
    n = len(a)
    return max(abs(a[i][j] - b[perm[i]][perm[j]]) for i in range(n) for j in range(n))


def brute_infimum(a, b):
    n = len(a)
    return min(distortion(a, b, perm) for perm in itertools.permutations(range(n)))


def sorted_lower_bound(a, b):
    """Certified lower bound: any bijection matches the ordered-pair multiset of
    X to that of Y, so the min over matchings (sorted matching) bounds it below."""
    left = sorted(a[i][j] for i in range(len(a)) for j in range(len(a)) if i != j)
    right = sorted(b[i][j] for i in range(len(b)) for j in range(len(b)) if i != j)
    return max(abs(x - y) for x, y in zip(left, right))


def branch_and_bound(a, b):
    """Exact infimum over bijections by depth-first branch-and-bound.

    Returns (value, permutation, nodes). Prunes a branch once its running maximum
    meets the incumbent; value ordering finds good incumbents early. The identity
    correspondence seeds the incumbent.
    """
    n = len(a)
    identity = distortion(a, b, tuple(range(n)))
    best = [identity, tuple(range(n))]

    perm = [-1] * n
    used = [False] * n
    cur = 0.0
    for i in range(n):
        chosen, chosen_cost = -1, None
        for v in range(n):
            if used[v]:
                continue
            cost = cur
            for j in range(i):
                cost = max(cost, abs(a[i][j] - b[v][perm[j]]), abs(a[j][i] - b[perm[j]][v]))
            if chosen_cost is None or cost < chosen_cost:
                chosen, chosen_cost = v, cost
        perm[i] = chosen
        used[chosen] = True
        cur = chosen_cost
    if cur < best[0]:
        best = [cur, tuple(perm)]

    nodes = [0]

    def search(i, used, perm, cur):
        nodes[0] += 1
        if cur >= best[0]:
            return
        if i == n:
            best[0] = cur
            best[1] = tuple(perm)
            return
        row = []
        for v in range(n):
            if used[v]:
                continue
            cost = cur
            for j in range(i):
                c = abs(a[i][j] - b[v][perm[j]])
                if c > cost:
                    cost = c
                c = abs(a[j][i] - b[perm[j]][v])
                if c > cost:
                    cost = c
            row.append((cost, v))
        row.sort()
        for cost, v in row:
            if cost >= best[0]:
                break
            perm[i] = v
            used[v] = True
            search(i + 1, used, perm, cost)
            used[v] = False
            perm[i] = -1

    search(0, [False] * n, [-1] * n, 0.0)
    return best[0], best[1], nodes[0]


def _incomparable_infimum(d_x, n):
    """LGH distortion to a space with no comparable pairs (all distances 0)."""
    zero = [[0.0] * n for _ in range(n)]
    return distortion(d_x, zero, tuple(range(n)))


def _matrices(module, n, seed):
    points = module.sprinkle_diamond(2, n, seed=seed)
    prec = causality(points)
    order = sorted(range(n), key=lambda i: points[i][0])
    d_x = normalize(chain_matrix(prec, order))
    d_y = normalize(tau_matrix(points))
    return d_x, d_y


def solve_n(protocol, n):
    """Exact infimum at one N (used for the tested grid and the boundary runs)."""
    module = load_module("_qr05cx_t7", MODULE_PATH)
    d_x, d_y = _matrices(module, n, protocol["seed"])
    identity = distortion(d_x, d_y, tuple(range(n)))
    infimum, perm, nodes = branch_and_bound(d_x, d_y)
    brute = brute_infimum(d_x, d_y) if n <= protocol["n_brute_max"] else None
    return {"n": n, "identity": identity, "infimum": infimum,
            "identity_optimal": infimum >= identity - 1e-9,
            "brute": brute, "nodes": nodes, "perm_is_identity": perm == tuple(range(n))}


def build_report(protocol):
    module = load_module("_qr05cx_t7", MODULE_PATH)
    rows = []
    for n in protocol["n_exact"]:
        d_x, d_y = _matrices(module, n, protocol["seed"])
        identity = distortion(d_x, d_y, tuple(range(n)))
        infimum, perm, nodes = branch_and_bound(d_x, d_y)
        brute = brute_infimum(d_x, d_y) if n <= protocol["n_brute_max"] else None
        if brute is not None and abs(brute - infimum) > 1e-9:
            raise AssertionError(f"branch-and-bound disagrees with brute force at N={n}")
        rows.append({"n": n, "identity": _round(identity), "infimum": _round(infimum),
                     "improvement": _round(identity - infimum),
                     "brute": _round(brute) if brute is not None else None})

    scale = []
    for n in protocol["n_scale"]:
        d_x, d_y = _matrices(module, n, protocol["seed"])
        scale.append({"n": n, "lower_bound": _round(sorted_lower_bound(d_x, d_y)),
                      "identity_upper": _round(distortion(d_x, d_y, tuple(range(n)))),
                      "max_dx": _round(max(d_x[i][j] for i in range(n) for j in range(n)))})

    improvements = [row["improvement"] for row in rows]
    identity_optimal = all(value <= 1e-9 for value in improvements)
    brute_agrees = all(row["brute"] is None or abs(row["brute"] - row["infimum"]) <= 1e-9 for row in rows)
    floor = min(row["lower_bound"] for row in scale)

    n_ctl = protocol["n_exact"][-1]
    d_x, _ = _matrices(module, n_ctl, protocol["seed"])
    incomparable = _incomparable_infimum(d_x, n_ctl)
    control = {"incomparable_infimum": _round(incomparable),
               "distinct": bool(incomparable > protocol["control_factor"] * max(row["infimum"] for row in rows))}

    return {
        "schema": SCHEMA,
        "rows": rows,
        "identity_is_optimal": bool(identity_optimal),
        "brute_agrees": bool(brute_agrees),
        "scale": scale,
        "certified_floor": _round(floor),
        "no_convergence_to_zero": bool(floor > protocol["floor_threshold"]),
        "control": control,
        "scale_degeneracy": {"free_scale_infimum_control": 0.0,
                             "note": "with a free scale, s=0 makes any comparison trivial "
                                     "(the LGH class is conformal); the distance must be scale-fixed"},
        "lgh_infimum_established": bool(identity_optimal and control["distinct"]),
        "verdict": "inconclusive for LGH convergence: at the fixed mean scale the exact "
                   "infimum is certified only on the exact grid (identity optimal throughout), "
                   "and beyond it a certified lower-bound floor does not vanish to N=256; the "
                   "free-scale infimum is degenerate, so the fixed scale is a convention",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="QR-05CX single-N exact infimum (boundary runs)")
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--protocol", default="protocol.json")
    args = parser.parse_args(argv)
    protocol = __import__("json").loads((HERE / args.protocol).read_bytes())
    start = time.time()
    row = solve_n(protocol, args.n)
    row["seconds"] = time.time() - start
    for key in ("n", "identity_optimal", "perm_is_identity", "nodes", "seconds", "identity", "infimum"):
        print(f"{key}: {row[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
