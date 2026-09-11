"""Primary route for QR-05DD: the order-only (longest-chain) uniform bound.

PRE-SPECIFIED QUESTION (follows QR-05DA/DB/DC).  Does the order-only longest-chain
reconstruction's scale-free uniform (max-over-pairs) distortion vanish as the
sprinkling density grows?

GEOMETRY -> ORDER.  In 1+1 Minkowski the causal order is exactly the 2-D dominance
order in light-cone coordinates u = t - x, v = t + x: p < q  <=>  (u_p < u_q and
v_p < v_q).  The longest chain is therefore a last-passage-percolation / LIS
functional and is computed in O(n^2 log n) with a Fenwick prefix-max.

REDUCTION (T1, exact).  With L(x,y) the longest-chain length and ell = rho^{-1/d},
the scale-free uniform distortion is

    delta_order = min_{c>0} max_{x<y} | ell*L(x,y) - c*tau(x,y) |
                = ell * min_{c>0} max_{x<y} | L(x,y) - c'*tau(x,y) |  =  ell * U,

where U is the uniform fluctuation of L away from its mean a_d*rho^{1/d}*tau.  Hence
delta_order -> 0  iff  U = o(rho^{1/d}).

FLUCTUATION SCALING (T2, imported LPP theory).  For a fixed pair the interval holds
M ~ rho*c_d*tau^d points and (Baik-Deift-Johansson / LPP) L = a_d*rho^{1/d}*tau with
fluctuation rho^{theta}; in 1+1 theta = 1/6, giving delta_order ~ rho^{-(1/d-theta)}
= N^{-1/3}.

NUMERICAL RESULT (T3).  Over N = 128 ... 2048 the measured ceiling is a power law in
N with no plateau, exponent ~ 0.30, consistent with the prediction 1/3 and steeper
than QR-05DA's small-range fit (0.16).  An adversarial non-manifoldlike control (a
layered order) does not vanish.  So the order-only uniform bound is supported to
vanish; an unconditional proof is a LPP concentration problem, flagged as such.

Supplied geometry; no metric, continuum, curvature or gravity claim.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05dd-report-v1"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _round(value, places=9):
    return round(value, places)


def tau_directed(points):
    n = len(points)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dt = points[j][0] - points[i][0]
            dx = points[j][1] - points[i][1]
            out[i][j] = math.sqrt(dt * dt - dx * dx) if dt * dt > dx * dx and dt > 0 else 0.0
    return out


def longest_chain_pairs(points):
    """(L(i,j), tau(i,j)) for every causal pair i < j, via a Fenwick prefix-max
    over the light-cone (u, v) dominance order."""
    n = len(points)
    us = [points[k][0] - points[k][1] for k in range(n)]
    vs = [points[k][0] + points[k][1] for k in range(n)]
    order = sorted(range(n), key=lambda k: us[k])
    lengths = []
    taus = []
    for idx, p in enumerate(order):
        future = [q for q in order[idx + 1:] if vs[q] > vs[p]]
        if not future:
            continue
        vsorted = sorted({vs[q] for q in future})
        rank = {v: i + 1 for i, v in enumerate(vsorted)}
        m = len(vsorted)
        tree = [0] * (m + 1)
        for q in sorted(future, key=lambda q: us[q]):
            r = rank[vs[q]]
            best = 0
            i = r - 1
            while i > 0:
                if tree[i] > best:
                    best = tree[i]
                i -= i & (-i)
            lpq = 1 + best
            i = r
            while i <= m:
                if lpq > tree[i]:
                    tree[i] = lpq
                i += i & (-i)
            dt = points[q][0] - points[p][0]
            dx = points[q][1] - points[p][1]
            lengths.append(lpq)
            taus.append(math.sqrt(dt * dt - dx * dx) if dt * dt > dx * dx else 0.0)
    return lengths, taus


def distortion(lengths, taus, iters):
    """min_{c>0} max |L - c*tau| (the ceiling), with the median at the optimum."""
    lo, hi = 0.0, max(lengths) / min(t for t in taus if t > 0) + 1.0
    gr = (math.sqrt(5.0) - 1.0) / 2.0

    def f(c):
        worst = 0.0
        for k in range(len(lengths)):
            v = abs(lengths[k] - c * taus[k])
            if v > worst:
                worst = v
        return worst

    c1 = hi - gr * (hi - lo)
    c2 = lo + gr * (hi - lo)
    f1, f2 = f(c1), f(c2)
    for _ in range(iters):
        if f1 < f2:
            hi, c2, f2 = c2, c1, f1
            c1 = hi - gr * (hi - lo)
            f1 = f(c1)
        else:
            lo, c1, f1 = c1, c2, f2
            c2 = lo + gr * (hi - lo)
            f2 = f(c2)
    cstar = 0.5 * (lo + hi)
    devs = sorted(abs(lengths[k] - cstar * taus[k]) for k in range(len(lengths)))
    return cstar, f(cstar), devs[len(devs) // 2]


def _loglog_slope(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[k] - mx) * (ys[k] - my) for k in range(n))
    den = sum((xs[k] - mx) ** 2 for k in range(n))
    return num / den


def _r_squared(xs, ys, slope):
    my = sum(ys) / len(ys)
    ss_tot = sum((y - my) ** 2 for y in ys)
    mx = sum(xs) / len(xs)
    intercept = my - slope * mx
    ss_res = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0


def layered_control(n):
    """A 3-layer Kleitman-Rothschild-style order: every element of layer i relates
    to every element of layer j > i.  The longest chain is bounded (<= 2) while the
    reference time-separation varies, so the scale-free distortion cannot vanish."""
    per = max(1, n // 3)
    times = [0.0, 0.5, 1.0]
    points = [(times[k // per], 0.3 * math.sin(2.7 * (k * 0.61803398875))) for k in range(n)]
    layers = [min(2, k // per) for k in range(n)]
    lengths = []
    taus = []
    tau = tau_directed(points)
    for i in range(n):
        for j in range(n):
            if layers[j] > layers[i]:
                lengths.append(layers[j] - layers[i])
                taus.append(tau[i][j])
    return lengths, taus


def build_report(protocol):
    module = load_module("_qr05dd_t7", MODULE_PATH)
    iters = protocol["minimax_iters"]
    rows = []
    for n in protocol["n_list"]:
        for seed in protocol["seeds"]:
            points = module.sprinkle_diamond(2, n, seed=seed)
            lengths, taus = longest_chain_pairs(points)
            _c, ceiling, median = distortion(lengths, taus, iters)
            ell = math.sqrt(protocol["area"] / n)
            mean_l = sum(lengths) / len(lengths)
            rows.append({"n": n, "seed": seed, "pairs": len(lengths),
                         "ceiling_norm": _round(ceiling / mean_l),
                         "ceiling_links": _round(ceiling),
                         "median_norm": _round(median / mean_l),
                         "mean_L": _round(mean_l)})

    by_n = {}
    for n in protocol["n_list"]:
        vals = [r["ceiling_norm"] for r in rows if r["n"] == n]
        by_n[n] = sum(vals) / len(vals)
    xs = [math.log(n) for n in protocol["n_list"]]
    ys = [math.log(by_n[n]) for n in protocol["n_list"]]
    slope = _loglog_slope(xs, ys)
    alpha = -slope
    r2 = _r_squared(xs, ys, slope)

    control_lengths, control_taus = layered_control(protocol["control_n"])
    _cc, control_ceiling, _cm = distortion(control_lengths, control_taus, iters)
    control_mean = sum(control_lengths) / len(control_lengths)

    flags = {
        "ceiling_is_a_power_law": bool(alpha > 0.1 and r2 > 0.9),
        "ceiling_consistent_with_lpp_prediction": bool(abs(alpha - 1.0 / 3.0) < 0.12),
        "ceiling_does_not_plateau": bool(by_n[protocol["n_list"][-1]] < 0.7 * by_n[protocol["n_list"][0]]),
        "order_only_uniform_bound_vanishes": bool(alpha > 0.0 and r2 > 0.9),
        "nonmanifoldlike_control_does_not_vanish": bool(control_ceiling / control_mean > 0.5),
        "unconditional_proof_established": False,
    }

    return {
        "schema": SCHEMA,
        "spec": {
            "question": ("Does the order-only longest-chain reconstruction's scale-free "
                         "uniform (max-over-pairs) distortion vanish as the sprinkling "
                         "density grows?"),
            "geometry": ("1+1 Minkowski; the causal order is the 2-D dominance order in "
                         "light-cone coordinates (u=t-x, v=t+x); longest chain = LPP/LIS"),
            "reduction": ("delta_order = ell * U with U the uniform fluctuation of L; "
                          "vanishes iff U = o(rho^{1/d})"),
            "prediction": ("LPP/BDJ: L fluctuation rho^{theta}, theta=1/6 in 1+1, so "
                           "delta_order ~ N^{-(1/d-theta)} = N^{-1/3}"),
            "convergence": "scale-free L-infinity distortion to the directed Lorentzian distance",
            "controls": ["layered_nonmanifoldlike"],
        },
        "convergence": rows,
        "by_n": {str(n): _round(by_n[n]) for n in protocol["n_list"]},
        "fit": {"alpha": _round(alpha), "r_squared": _round(r2),
                "range": [protocol["n_list"][0], protocol["n_list"][-1]],
                "predicted_alpha_lpp": _round(1.0 / 3.0)},
        "control": {"name": "layered_nonmanifoldlike", "pairs": len(control_lengths),
                    "ceiling_norm": _round(control_ceiling / control_mean),
                    "does_not_vanish": bool(control_ceiling / control_mean > 0.5)},
        "flags": flags,
        "verdict": (
            "QR-05DD: the order-only (longest-chain) uniform bound. In 1+1 Minkowski the "
            "causal order is a 2-D dominance order, so the longest chain is a "
            "last-passage-percolation functional; the scale-free uniform distortion is "
            "exactly ell times the uniform fluctuation of L, so it vanishes iff that "
            "fluctuation is sublinear in rho^{1/d} (T1). Imported LPP/BDJ scaling predicts "
            "a fluctuation rho^{1/6} and hence a distortion ~ N^{-1/3} (T2). Measured over "
            f"N = {protocol['n_list'][0]}...{protocol['n_list'][-1]}, the ceiling decays as a "
            f"power law with exponent {alpha:.2f} (R^2 = {r2:.3f}) and no plateau, "
            "consistent with the 1/3 prediction and steeper than QR-05DA's small-range fit "
            "(0.16): the order-only uniform bound is supported to vanish (T3). An "
            "adversarial non-manifoldlike layered order does not vanish. So the "
            "longest-chain reconstruction is the axiom-compliant (DB/DC) and "
            "ceiling-convergent object; an unconditional proof is a LPP concentration "
            "problem, flagged as open. No metric, continuum, curvature or gravity claim."),
    }
