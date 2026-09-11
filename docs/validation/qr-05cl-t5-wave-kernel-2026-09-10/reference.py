"""Independent reference route for the QR-05CL T5 wave-kernel benchmark."""

from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cl-report-v1"


def _round(value, places=9):
    return round(value, places)


def _mu2(kernel, h):
    total = 0.0
    for j, w in kernel.items():
        total += w * (j * h) * (j * h)
    return total


def _mu1(kernel, h):
    total = 0.0
    for j, w in kernel.items():
        total += w * j * h
    return total


def _gen_point(f, kernel, h, x0):
    total = 0.0
    for j, w in kernel.items():
        total += w * (f(x0 + j * h) - f(x0))
    return total


def _periodic(values, kernel, n):
    result = []
    for i in range(n):
        terms = []
        for j, w in kernel.items():
            terms.append(w * (values[(i + j) % n] - values[i]))
        result.append(sum(terms))
    return result


def _wave(grid, m, spatial, temporal):
    h = 1.0 / m
    ms = _mu2(spatial, h)
    mt = _mu2(temporal, h)
    result = [[0.0] * m for _ in range(m)]
    for i in range(m):
        temp = _periodic([grid[i][k] for k in range(m)], temporal, m)
        for k in range(m):
            spatial_vals = _periodic([grid[ii][k] for ii in range(m)], spatial, m)
            result[i][k] = (2.0 / mt) * temp[k] - (2.0 / ms) * spatial_vals[i]
    return result


def build_report(protocol):
    spatial = {int(k): float(v) for k, v in protocol["spatial"].items()}
    temporal = {int(k): float(v) for k, v in protocol["temporal"].items()}
    h0 = protocol["h0"]
    x0 = protocol["x0"]
    sq = lambda x: x * x

    s_q = _gen_point(sq, spatial, h0, x0)
    t_q = _gen_point(sq, temporal, h0, x0)
    expected = _mu2(spatial, h0)
    exact = {"S_x2": _round(s_q), "T_t2": _round(t_q), "moment": _round(expected),
             "match": abs(s_q - expected) < 1e-12 and abs(t_q - _mu2(temporal, h0)) < 1e-12}

    rows = []
    for m in protocol["grid"]:
        h = 1.0 / m
        grid = [[math.sin(2 * math.pi * i * h) + math.sin(2 * math.pi * k * h) for k in range(m)]
                for i in range(m)]
        out = _wave(grid, m, spatial, temporal)
        errs = []
        for i in range(m):
            for k in range(m):
                target = (-(2 * math.pi) ** 2 * math.sin(2 * math.pi * k * h)
                          + (2 * math.pi) ** 2 * math.sin(2 * math.pi * i * h))
                errs.append(abs(out[i][k] - target))
        rows.append({"m": m, "h": _round(h), "mean_abs_error": _round(sum(errs) / len(errs))})

    log_h = [math.log(r["h"]) for r in rows]
    log_e = [math.log(r["mean_abs_error"]) for r in rows]
    count = len(rows)
    mh = sum(log_h) / count
    me = sum(log_e) / count
    num = 0.0
    den = 0.0
    for idx in range(count):
        num += (log_h[idx] - mh) * (log_e[idx] - me)
        den += (log_h[idx] - mh) ** 2
    slope = num / den

    coefficients = []
    for name, kernel in protocol["kernels"].items():
        kk = {int(k): float(v) for k, v in kernel.items()}
        val = _gen_point(sq, kk, h0, x0)
        pred = _mu2(kk, h0)
        coefficients.append({"kernel": name, "S_x2": _round(val), "moment": _round(pred),
                             "ratio": _round(val / pred if pred else 0.0)})

    asym = {int(k): float(v) for k, v in protocol["asymmetric"].items()}
    return {
        "schema": SCHEMA,
        "exact_quadratics": exact,
        "convergence": rows,
        "convergence_exponent": _round(slope),
        "coefficient_from_moment": coefficients,
        "drift": {"symmetric_first_moment": _round(_mu1(spatial, h0)),
                  "asymmetric_first_moment": _round(_mu1(asym, h0)),
                  "asymmetric_is_drift": abs(_mu1(spatial, h0)) < 1e-12 and abs(_mu1(asym, h0)) > 1e-6},
    }
