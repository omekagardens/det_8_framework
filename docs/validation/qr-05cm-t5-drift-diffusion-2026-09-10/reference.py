"""Independent reference route for the QR-05CM T5 drift-diffusion benchmark."""

from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cm-report-v1"


def _round(value, places=9):
    return round(value, places)


def _d(x, a):
    return 1.0 + a * math.sin(2 * math.pi * x)


def _v(x, b):
    return b * math.cos(2 * math.pi * x)


def _moments(x, h, a, b):
    return (2 * h * _v(x, b), 2 * h * h * _d(x, a))


def _site(values, ds, vs, i, m):
    plus = values[(i + 1) % m]
    minus = values[(i - 1) % m]
    return ds[i] * (plus - 2 * values[i] + minus) + vs[i] * (plus - minus)


def build_report(protocol):
    a = protocol["a"]
    b = protocol["b"]
    h0 = protocol["h0"]
    x0 = protocol["x0"]

    dd = _d(x0, a)
    vv = _v(x0, b)
    sx = dd * ((x0 + h0) - 2 * x0 + (x0 - h0)) + vv * ((x0 + h0) - (x0 - h0))
    mu1 = 2 * h0 * vv
    sx2 = dd * ((x0 + h0) ** 2 - 2 * x0 ** 2 + (x0 - h0) ** 2) + vv * ((x0 + h0) ** 2 - (x0 - h0) ** 2)
    pred_x2 = mu1 * 2 * x0 + (2 * h0 * h0 * dd)
    exact = {"S_x": _round(sx), "mu1": _round(mu1), "S_x2": _round(sx2), "pred_x2": _round(pred_x2),
             "match": abs(sx - mu1) < 1e-12 and abs(sx2 - pred_x2) < 1e-12}

    rows = []
    for m in protocol["grid"]:
        h = 1.0 / m
        xs = [i * h for i in range(m)]
        fvals = [math.sin(2 * math.pi * x) for x in xs]
        ds = [_d(x, a) for x in xs]
        vs = [_v(x, b) for x in xs]
        left = []
        right = []
        for i in range(m):
            left.append(_site(fvals, ds, vs, i, m))
            m1, m2 = _moments(xs[i], h, a, b)
            fp = 2 * math.pi * math.cos(2 * math.pi * xs[i])
            fpp = -4 * math.pi * math.pi * math.sin(2 * math.pi * xs[i])
            right.append(m1 * fp + 0.5 * m2 * fpp)
        scale = max(abs(p) for p in right)
        errs = [abs(left[i] - right[i]) for i in range(m)]
        rows.append({"m": m, "h": _round(h), "rel_error": _round(max(errs) / scale)})

    log_h = [math.log(r["h"]) for r in rows]
    log_e = [math.log(r["rel_error"]) for r in rows]
    n = len(rows)
    mh = sum(log_h) / n
    me = sum(log_e) / n
    num = 0.0
    den = 0.0
    for k in range(n):
        num += (log_h[k] - mh) * (log_e[k] - me)
        den += (log_h[k] - mh) ** 2
    slope = num / den

    samples = []
    for x in protocol["sample_xs"]:
        m1, m2 = _moments(x, h0, a, b)
        samples.append({"x": _round(x), "mu1": _round(m1), "mu2": _round(m2),
                        "diffusion": _round(_d(x, a)), "drift": _round(_v(x, b))})

    variable = [_moments(k / 8.0, h0, a, b)[1] for k in range(8)]
    variation = max(variable) - min(variable)
    control = {"constant_variation": _round(0.0), "variable_variation": _round(variation),
               "coefficients_vary": variation > 1e-6 and _moments(0.25, h0, a, 0.0)[1] > 0}

    return {
        "schema": SCHEMA,
        "exact": exact,
        "convergence": rows,
        "convergence_exponent": _round(slope),
        "coefficient_samples": samples,
        "negative_control": control,
    }
