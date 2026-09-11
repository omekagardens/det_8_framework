"""Independent reference route for the QR-05CH graph-Laplacian benchmark.

Shares the supplied torus sprinkling (fixture) but re-implements the action and
the proportionality fit with different loop structure.
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
    generator = random.Random(seed)
    return [(generator.random(), generator.random()) for _ in range(n)]


def torus_distance(p, q):
    deltas = []
    for k in range(2):
        d = abs(p[k] - q[k])
        deltas.append(min(d, 1.0 - d))
    return math.sqrt(deltas[0] ** 2 + deltas[1] ** 2)


def _action(points, values, epsilon):
    n = len(points)
    result = []
    for i in range(n):
        terms = []
        for j in range(n):
            if i == j:
                continue
            terms.append(math.exp(-(torus_distance(points[i], points[j]) ** 2) / (4.0 * epsilon))
                         * (values[j] - values[i]))
        result.append(sum(terms) / n)
    return result


def _fit(action, values):
    numerator = sum(a * v for a, v in zip(action, values))
    denominator = sum(v * v for v in values)
    slope = numerator / denominator
    diff = [(a - slope * v) for a, v in zip(action, values)]
    residual = math.sqrt(sum(d * d for d in diff))
    norm = math.sqrt(sum(a * a for a in action))
    return slope, (residual / norm if norm else 0.0)


def _mode(points, epsilon, wave):
    values = [math.sin(wave * math.pi * p[0]) for p in points]
    return _fit(_action(points, values, epsilon), values)


def build_report(protocol):
    eps = protocol["torus_epsilon"]
    seed = protocol["seed"]
    points = sprinkle_torus(protocol["n"], seed)

    mu1 = (2 * math.pi) ** 2
    mu2 = (4 * math.pi) ** 2
    s1, r1 = _mode(points, eps, 2.0)
    s2, r2 = _mode(points, eps, 4.0)
    c1 = s1 / (math.exp(-eps * mu1) - 1)
    c2 = s2 / (math.exp(-eps * mu2) - 1)
    mode_gap = abs(c1 - c2) / abs(c1)

    control_values = [(p[0] - 0.5) ** 2 for p in points]
    c_slope, c_res = _fit(_action(points, control_values, eps), control_values)

    residual_grid = []
    for n in protocol["n_grid"]:
        pts = sprinkle_torus(n, seed)
        _, res = _mode(pts, eps, 2.0)
        residual_grid.append({"n": n, "residual": _round(res)})
    residual_decreasing = all(residual_grid[i]["residual"] > residual_grid[i + 1]["residual"]
                              for i in range(len(residual_grid) - 1))

    prediction = 4 * math.pi * eps
    return {
        "schema": SCHEMA,
        "mode1": {"mu": _round(mu1), "slope": _round(s1), "residual": _round(r1), "constant": _round(c1)},
        "mode2": {"mu": _round(mu2), "slope": _round(s2), "residual": _round(r2), "constant": _round(c2)},
        "mode_gap": _round(mode_gap),
        "mode_independent": mode_gap <= protocol["gap_tolerance"],
        "negative_control": {"residual": _round(c_res), "local_residual": _round(r1),
                             "control_required": c_res > protocol["control_factor"] * r1},
        "residual_grid": residual_grid,
        "residual_decreasing": residual_decreasing,
        "continuum": {"constant": _round(c1), "prediction_4pi_eps": _round(prediction),
                      "ratio": _round(c1 / prediction)},
    }
