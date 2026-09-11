"""Primary route for the QR-05CH graph-Laplacian benchmark.

On a supplied flat torus, a Gaussian-weighted graph is applied to smooth test
functions and the action is fitted to the continuum Laplace-Beltrami action
Delta f = -mu f. Two eigenfunction modes must yield the same intrinsic
constant, a non-eigenfunction must fail, and the residual must decrease with
N. Supplied geometry; no gravity claim. The quarantined curvature module is
unused.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05ch-report-v1"


def _round(value, places=9):
    return round(value, places)


def sprinkle_torus(n, seed):
    rng = random.Random(seed)
    return [(rng.random(), rng.random()) for _ in range(n)]


def torus_distance(p, q):
    dx = abs(p[0] - q[0])
    dx = min(dx, 1.0 - dx)
    dy = abs(p[1] - q[1])
    dy = min(dy, 1.0 - dy)
    return math.hypot(dx, dy)


def graph_action(points, values, epsilon):
    n = len(points)
    action = []
    for i in range(n):
        total = 0.0
        for j in range(n):
            if i == j:
                continue
            total += math.exp(-(torus_distance(points[i], points[j]) ** 2) / (4 * epsilon)) * (values[j] - values[i])
        action.append(total / n)
    return action


def proportional_fit(action, values):
    numerator = sum(action[i] * values[i] for i in range(len(values)))
    denominator = sum(values[i] * values[i] for i in range(len(values)))
    slope = numerator / denominator
    residual = math.sqrt(sum((action[i] - slope * values[i]) ** 2 for i in range(len(values))))
    norm = math.sqrt(sum(action[i] ** 2 for i in range(len(values))))
    return slope, residual / norm if norm else 0.0


def _mode(points, epsilon, wave):
    values = [math.sin(wave * math.pi * p[0]) for p in points]
    slope, residual = proportional_fit(graph_action(points, values, epsilon), values)
    return values, slope, residual


def build_report(protocol):
    eps = protocol["torus_epsilon"]
    seed = protocol["seed"]
    points = sprinkle_torus(protocol["n"], seed)

    mu1 = (2 * math.pi) ** 2
    mu2 = (4 * math.pi) ** 2
    _, s1, r1 = _mode(points, eps, 2.0)   # sin(2*pi*x) -> mu = (2pi)^2
    _, s2, r2 = _mode(points, eps, 4.0)   # sin(4*pi*x) -> mu = (4pi)^2
    # The graph action acts as a Gaussian smoothing: Lf = 4*pi*eps*(e^{-eps*mu}-1) f.
    c1 = s1 / (math.exp(-eps * mu1) - 1)
    c2 = s2 / (math.exp(-eps * mu2) - 1)
    mode_gap = abs(c1 - c2) / abs(c1)

    control_values = [(p[0] - 0.5) ** 2 for p in points]   # Delta f = 2, not proportional to f
    c_slope, c_res = proportional_fit(graph_action(points, control_values, eps), control_values)

    residual_grid = []
    for n in protocol["n_grid"]:
        pts = sprinkle_torus(n, seed)
        _, _, res = _mode(pts, eps, 2.0)
        residual_grid.append({"n": n, "residual": _round(res)})
    residual_decreasing = all(residual_grid[i]["residual"] > residual_grid[i + 1]["residual"]
                              for i in range(len(residual_grid) - 1))

    prediction = 4 * math.pi * eps
    return {
        "schema": SCHEMA,
        "mode1": {"mu": _round(mu1), "slope": _round(s1), "residual": _round(r1), "constant": _round(c1)},
        "mode2": {"mu": _round(mu2), "slope": _round(s2), "residual": _round(r2), "constant": _round(c2)},
        "mode_gap": _round(mode_gap),
        "mode_independent": bool(mode_gap <= protocol["gap_tolerance"]),
        "negative_control": {"residual": _round(c_res), "local_residual": _round(r1),
                             "control_required": bool(c_res > protocol["control_factor"] * r1)},
        "residual_grid": residual_grid,
        "residual_decreasing": bool(residual_decreasing),
        "continuum": {"constant": _round(c1), "prediction_4pi_eps": _round(prediction),
                      "ratio": _round(c1 / prediction)},
    }
