"""Primary route for the QR-05CL T5 local-kernel continuum (wave-like) benchmark.

A local conservative kernel on a periodic lattice generates a wave-like operator
whose continuum coefficients are the kernel's second moments (record_kernel
physics T5). Section A checks quadratics exactly, B measures the h^2 convergence
to the continuum wave operator, C shows the coefficient is the kernel moment,
and D is the drift control (an asymmetric kernel is drift-diffusion, not a pure
wave operator). Supplied geometry; no gravity claim.
"""

from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cl-report-v1"


def _round(value, places=9):
    return round(value, places)


def second_moment(kernel, h):
    return sum(w * (j * h) ** 2 for j, w in kernel.items())


def first_moment(kernel, h):
    return sum(w * (j * h) for j, w in kernel.items())


def generator_point(f, kernel, h, x0):
    return sum(w * (f(x0 + j * h) - f(x0)) for j, w in kernel.items())


def periodic_generator(values, kernel, n):
    out = [0.0] * n
    for i in range(n):
        total = 0.0
        for j, w in kernel.items():
            total += w * (values[(i + j) % n] - values[i])
        out[i] = total
    return out


def wave_operator(grid, m, spatial, temporal):
    h = 1.0 / m
    mu_s = second_moment(spatial, h)
    mu_t = second_moment(temporal, h)
    out = [[0.0] * m for _ in range(m)]
    for i in range(m):
        column = [grid[i][k] for k in range(m)]
        tgen = periodic_generator(column, temporal, m)
        for k in range(m):
            row = [grid[ii][k] for ii in range(m)]
            sgen = periodic_generator(row, spatial, m)
            out[i][k] = (2.0 / mu_t) * tgen[k] - (2.0 / mu_s) * sgen[i]
    return out


def build_report(protocol):
    spatial = {int(k): float(v) for k, v in protocol["spatial"].items()}
    temporal = {int(k): float(v) for k, v in protocol["temporal"].items()}
    h0 = protocol["h0"]
    x0 = protocol["x0"]

    quadratic = lambda x: x * x
    linear = lambda x: x
    s_q = generator_point(quadratic, spatial, h0, x0)
    t_q = generator_point(quadratic, temporal, h0, x0)
    expected = second_moment(spatial, h0)
    exact_quadratics = {
        "S_x2": _round(s_q), "T_t2": _round(t_q), "moment": _round(expected),
        "match": bool(abs(s_q - expected) < 1e-12 and abs(t_q - second_moment(temporal, h0)) < 1e-12),
    }

    rows = []
    for m in protocol["grid"]:
        h = 1.0 / m
        grid = [[math.sin(2 * math.pi * i * h) + math.sin(2 * math.pi * k * h)
                 for k in range(m)] for i in range(m)]
        out = wave_operator(grid, m, spatial, temporal)
        errors = []
        for i in range(m):
            for k in range(m):
                box = -(2 * math.pi) ** 2 * math.sin(2 * math.pi * k * h) + (2 * math.pi) ** 2 * math.sin(2 * math.pi * i * h)
                errors.append(abs(out[i][k] - box))
        rows.append({"m": m, "h": _round(h), "mean_abs_error": _round(sum(errors) / len(errors))})

    xs = [math.log(row["h"]) for row in rows]
    ys = [math.log(row["mean_abs_error"]) for row in rows]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    slope = sum((xs[i] - mx) * (ys[i] - my) for i in range(len(xs))) / sum((xs[i] - mx) ** 2 for i in range(len(xs)))

    # Coefficient is the kernel moment: S(x^2) / ((1/2) mu_2 * 2) = 1 for every kernel.
    coefficient_rows = []
    for name, kernel in protocol["kernels"].items():
        kk = {int(k): float(v) for k, v in kernel.items()}
        s_val = generator_point(quadratic, kk, h0, x0)
        pred = second_moment(kk, h0)
        coefficient_rows.append({"kernel": name, "S_x2": _round(s_val), "moment": _round(pred),
                                 "ratio": _round(s_val / pred if pred else 0.0)})

    symmetric = first_moment(spatial, h0)
    asymmetric = {int(k): float(v) for k, v in protocol["asymmetric"].items()}
    asym_drift = first_moment(asymmetric, h0)

    return {
        "schema": SCHEMA,
        "exact_quadratics": exact_quadratics,
        "convergence": rows,
        "convergence_exponent": _round(slope),
        "coefficient_from_moment": coefficient_rows,
        "drift": {"symmetric_first_moment": _round(symmetric),
                  "asymmetric_first_moment": _round(asym_drift),
                  "asymmetric_is_drift": bool(abs(symmetric) < 1e-12 and abs(asym_drift) > 1e-6)},
    }
