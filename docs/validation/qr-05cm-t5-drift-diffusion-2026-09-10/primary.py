"""Primary route for the QR-05CM T5 drift-diffusion / variable-coefficient benchmark.

A local kernel whose moments vary with position generates a drift-diffusion
operator with position-dependent coefficients (record_kernel physics T5):
S f(x) -> mu1(x) f'(x) + (1/2) mu2(x) f''(x), with the local kernel moments
mu1(x) = sum_j K^x_j (jh), mu2(x) = sum_j K^x_j (jh)^2. Section A checks
quadratics exactly, B measures the h^2 convergence with varying coefficients,
C shows the coefficients are the local moments, D is the constant-kernel
control. Supplied geometry; no gravity claim.
"""

from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "qr05cm-report-v1"


def _round(value, places=9):
    return round(value, places)


def diffusion(x, a):
    return 1.0 + a * math.sin(2 * math.pi * x)


def drift(x, b):
    return b * math.cos(2 * math.pi * x)


def kernel_moments(x, h, a, b):
    # K^x = {+1: D+V, -1: D-V, 0: -2D}  ->  mu1 = 2hV, mu2 = 2h^2 D
    d = diffusion(x, a)
    v = drift(x, b)
    return 2 * h * v, 2 * h * h * d


def apply_site(values, ds, vs, i, m):
    ip = (i + 1) % m
    im = (i - 1) % m
    return ds[i] * (values[ip] - 2 * values[i] + values[im]) + vs[i] * (values[ip] - values[im])


def build_report(protocol):
    a = protocol["a"]
    b = protocol["b"]
    h0 = protocol["h0"]
    x0 = protocol["x0"]

    d0 = diffusion(x0, a)
    v0 = drift(x0, b)
    s_x = d0 * ((x0 + h0) - 2 * x0 + (x0 - h0)) + v0 * ((x0 + h0) - (x0 - h0))
    mu1 = 2 * h0 * v0
    s_x2 = d0 * ((x0 + h0) ** 2 - 2 * x0 ** 2 + (x0 - h0) ** 2) + v0 * ((x0 + h0) ** 2 - (x0 - h0) ** 2)
    pred_x2 = mu1 * (2 * x0) + 0.5 * (2 * h0 * h0 * d0) * 2
    exact = {"S_x": _round(s_x), "mu1": _round(mu1), "S_x2": _round(s_x2), "pred_x2": _round(pred_x2),
             "match": bool(abs(s_x - mu1) < 1e-12 and abs(s_x2 - pred_x2) < 1e-12)}

    rows = []
    for m in protocol["grid"]:
        h = 1.0 / m
        xs = [i * h for i in range(m)]
        values = [math.sin(2 * math.pi * x) for x in xs]
        ds = [diffusion(x, a) for x in xs]
        vs = [drift(x, b) for x in xs]
        sf = []
        pred = []
        for i in range(m):
            sf.append(apply_site(values, ds, vs, i, m))
            m1, m2 = kernel_moments(xs[i], h, a, b)
            fp = 2 * math.pi * math.cos(2 * math.pi * xs[i])
            fpp = -(2 * math.pi) ** 2 * math.sin(2 * math.pi * xs[i])
            pred.append(m1 * fp + 0.5 * m2 * fpp)
        scale = max(abs(p) for p in pred)
        rel = max(abs(sf[i] - pred[i]) for i in range(m)) / scale
        rows.append({"m": m, "h": _round(h), "rel_error": _round(rel)})

    xs = [math.log(r["h"]) for r in rows]
    ys = [math.log(r["rel_error"]) for r in rows]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    slope = sum((xs[i] - mx) * (ys[i] - my) for i in range(len(xs))) / sum((xs[i] - mx) ** 2 for i in range(len(xs)))

    samples = []
    for x in protocol["sample_xs"]:
        m1, m2 = kernel_moments(x, h0, a, b)
        samples.append({"x": _round(x), "mu1": _round(m1), "mu2": _round(m2),
                        "diffusion": _round(diffusion(x, a)), "drift": _round(drift(x, b))})

    constant_mu2 = kernel_moments(0.25, h0, a, 0.0)[1]
    variable_mu2 = [kernel_moments(x / 8.0, h0, a, b)[1] for x in range(8)]
    variation = max(variable_mu2) - min(variable_mu2)
    negative_control = {"constant_variation": _round(0.0),
                        "variable_variation": _round(variation),
                        "coefficients_vary": bool(variation > 1e-6 and constant_mu2 > 0)}

    return {
        "schema": SCHEMA,
        "exact": exact,
        "convergence": rows,
        "convergence_exponent": _round(slope),
        "coefficient_samples": samples,
        "negative_control": negative_control,
    }
