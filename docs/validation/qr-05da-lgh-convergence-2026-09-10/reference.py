"""Independent reference route for QR-05DA.

Same report by different mechanics, so the two routes must agree before the gate
is published:

  - chains by a reverse (successor) dynamic program instead of the forward
    (predecessor) one;
  - interval counts by integer bitmasks and ``int.bit_count`` instead of set
    intersections;
  - the relative scale by bisecting the crossing of the upper and lower
    envelopes instead of golden-section minimisation;
  - the trend, decay fits, localization buckets and verdict recoded.
"""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05da-report-v2"
BUCKET_LABELS = ["lt_2^-4"] + [f"2^{k}..2^{k+1}" for k in range(-4, 6)] + ["ge_2^6"]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _round(value, places=9):
    return round(value, places)


def _spatial_sq(p, q):
    return sum((q[k] - p[k]) ** 2 for k in range(1, len(p)))


def _causality(points):
    n = len(points)
    out = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dt = points[j][0] - points[i][0]
                if dt > 0 and _spatial_sq(points[i], points[j]) < dt * dt:
                    out[i][j] = True
    return out


def _chains(prec, order):
    n = len(prec)
    ch = [[0] * n for _ in range(n)]
    for src in reversed(order):
        row = [0] * n
        for k in range(n):
            if prec[src][k]:
                if row[k] == 0:
                    row[k] = 1
                rk = ch[k]
                for j in range(n):
                    if rk[j] > 0:
                        v = rk[j] + 1
                        if v > row[j]:
                            row[j] = v
        ch[src] = row
    return ch


def _interval_counts(prec, order):
    n = len(prec)
    desc = [0] * n
    for src in reversed(order):
        mask = 0
        for k in range(n):
            if prec[src][k]:
                mask |= (1 << k) | desc[k]
        desc[src] = mask
    anc = [0] * n
    for src in order:
        mask = 0
        for k in range(n):
            if prec[k][src]:
                mask |= (1 << k) | anc[k]
        anc[src] = mask
    return [[(desc[i] & anc[j]).bit_count() if prec[i][j] else 0 for j in range(n)] for i in range(n)]


def _count_separation(prec, counts, ell):
    """Order+count time-separation estimator ``ell * sqrt(1 + m_ij)``.

    A distance estimator, not a metric: it violates the Lorentzian
    reverse-triangle inequality on a three-event chain a ≺ b ≺ c.
    """
    n = len(prec)
    return [[ell * math.sqrt(counts[i][j] + 1) if prec[i][j] else 0.0
             for j in range(n)] for i in range(n)]


def _tau(points, directed):
    n = len(points)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dt = points[j][0] - points[i][0]
            sq = _spatial_sq(points[i], points[j])
            if directed:
                out[i][j] = math.sqrt(dt * dt - sq) if (dt > 0 and dt * dt > sq) else 0.0
            else:
                out[i][j] = math.sqrt(dt * dt - sq) if dt * dt > sq else 0.0
    return out


def _norm(matrix):
    vals = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix)) if matrix[i][j] > 0]
    if not vals:
        return [[0.0] * len(matrix) for _ in matrix]
    m = sum(vals) / len(vals)
    return [[matrix[i][j] / m for j in range(len(matrix))] for i in range(len(matrix))]


def _pairs(a, b):
    n = len(a)
    return [(a[i][j], b[i][j]) for i in range(n) for j in range(n)]


def _permute(b, perm):
    n = len(b)
    return [[b[perm[i]][perm[j]] for j in range(n)] for i in range(n)]


def _minimax(pairs, iters):
    def upper(c):
        return max(p - c * q for p, q in pairs)

    def lower(c):
        return max(c * q - p for p, q in pairs)

    lo, hi = 0.0, 32.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if upper(mid) > lower(mid):
            lo = mid
        else:
            hi = mid
    c = 0.5 * (lo + hi)
    return c, max(upper(c), lower(c))


def _sorted_lists(a, b):
    n = len(a)
    left = sorted(a[i][j] for i in range(n) for j in range(n) if i != j)
    right = sorted(b[i][j] for i in range(n) for j in range(n) if i != j)
    return left, right


def _lb_scale(a, b, iters):
    left, right = _sorted_lists(a, b)
    return _minimax(list(zip(left, right)), iters)[1]


def _exact_sf(a, b, iters):
    n = len(a)
    best, best_perm = None, None
    for perm in itertools.permutations(range(n)):
        _c, value = _minimax(_pairs(a, _permute(b, perm)), iters)
        if best is None or value < best:
            best, best_perm = value, perm
    return best, best_perm


def _bucket(ratio):
    k = int(math.floor(math.log2(ratio)))
    if k < -4:
        return "lt_2^-4"
    if k >= 6:
        return "ge_2^6"
    return f"2^{k}..2^{k+1}"


def _mismatch(a, b):
    n = len(a)
    return sum(1 for i in range(n) for j in range(n) if (a[i][j] > 0) != (b[i][j] > 0))


def _quantile(values, q):
    """Nearest-rank quantile (index ``ceil(q n) - 1``); see the primary route.

    The first capture used index ``int(0.01 n)`` -- the 1st percentile -- for a
    statistic named ``p99``; the corrected form is the 99th percentile.
    """
    if not values:
        raise ValueError("quantile of an empty sequence")
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(q * len(ordered)) - 1))
    return ordered[index]


def _p99(values):
    return _quantile(values, 0.99)


def _median(values):
    return _quantile(values, 0.5)


def _bundle(module, n, seed, area):
    points = module.sprinkle_diamond(2, n, seed=seed)
    order = sorted(range(n), key=lambda i: points[i][0])
    prec = _causality(points)
    ell = math.sqrt(area / n)
    chain_raw = _chains(prec, order)
    counts = _interval_counts(prec, order)
    tau_raw = _tau(points, True)
    raw_count = [[ell * math.sqrt(counts[i][j]) if counts[i][j] > 0 else 0.0 for j in range(n)] for i in range(n)]
    count_time = _count_separation(prec, counts, ell)
    return {"n": n, "ell": ell, "chain_raw": chain_raw, "counts": counts, "tau_raw": tau_raw,
            "chain": _norm(chain_raw), "tau": _norm(tau_raw), "tau_symmetric": _norm(_tau(points, False)),
            "count": _norm(count_time), "raw_count": raw_count}


def _slope(xs, ys):
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    return sum((a - mx) * (b - my) for a, b in zip(lx, ly)) / sum((a - mx) ** 2 for a in lx)


def build_report(protocol):
    module = load_module("_qr05da_t7_ref", MODULE_PATH)
    iters = protocol["minimax_iters"]
    area = protocol["area"]
    seed = protocol["seed"]

    convention = {"n_checked": list(protocol["convention_n"]),
                  "chain_vs_directed": {}, "chain_vs_symmetric": {},
                  "count_offset_vs_directed": {}, "count_raw_vs_directed": {}}
    for n in protocol["convention_n"]:
        bundle = _bundle(module, n, seed, area)
        convention["chain_vs_directed"][str(n)] = _mismatch(bundle["chain"], bundle["tau"])
        convention["chain_vs_symmetric"][str(n)] = _mismatch(bundle["chain"], bundle["tau_symmetric"])
        convention["count_offset_vs_directed"][str(n)] = _mismatch(bundle["count"], bundle["tau"])
        convention["count_raw_vs_directed"][str(n)] = _mismatch(bundle["raw_count"], bundle["tau"])

    scale_cache = {}
    trend = []
    for n in protocol["n_scale"]:
        chain_upper, chain_lower, chain_p99, chain_median = [], [], [], []
        count_upper, count_p99, count_median = [], [], []
        for s in protocol["seeds"]:
            bundle = _bundle(module, n, s, area)
            chain, tau, count = bundle["chain"], bundle["tau"], bundle["count"]
            c_chain, chain_upper_value = _minimax(_pairs(chain, tau), iters)
            scale_cache[(n, s)] = c_chain
            chain_upper.append(chain_upper_value)
            chain_lower.append(_lb_scale(chain, tau, iters))
            chain_distortion = [abs(chain[i][j] - c_chain * tau[i][j])
                                for i in range(n) for j in range(n) if tau[i][j] > 0]
            chain_p99.append(_p99(chain_distortion))
            chain_median.append(_median(chain_distortion))
            c_count, count_upper_value = _minimax(_pairs(count, tau), iters)
            count_upper.append(count_upper_value)
            count_distortion = [abs(count[i][j] - c_count * tau[i][j])
                                for i in range(n) for j in range(n) if tau[i][j] > 0]
            count_p99.append(_p99(count_distortion))
            count_median.append(_median(count_distortion))
        ell = math.sqrt(area / n)
        cu = sum(chain_upper) / len(chain_upper)
        cl = sum(chain_lower) / len(chain_lower)
        cp = sum(chain_p99) / len(chain_p99)
        cm = sum(chain_median) / len(chain_median)
        xu = sum(count_upper) / len(count_upper)
        xp = sum(count_p99) / len(count_p99)
        xm = sum(count_median) / len(count_median)
        trend.append({
            "n": n, "ell": _round(ell), "seeds": len(protocol["seeds"]),
            "chain_upper_mean": _round(cu),
            "chain_upper_sd": _round(math.sqrt(sum((v - cu) ** 2 for v in chain_upper) / len(chain_upper))),
            "chain_lower_mean": _round(cl),
            "chain_median_mean": _round(cm), "chain_p99_mean": _round(cp),
            "count_upper_mean": _round(xu),
            "count_upper_sd": _round(math.sqrt(sum((v - xu) ** 2 for v in count_upper) / len(count_upper))),
            "count_median_mean": _round(xm), "count_p99_mean": _round(xp),
            "chain_upper_over_ell": _round(cu / ell), "chain_lower_over_ell": _round(cl / ell),
            "count_upper_over_ell": _round(xu / ell)})

    fitted = [r for r in trend if r["n"] >= protocol["fit_n_min"]]
    fitted_n = [r["n"] for r in fitted]
    decay = {
        "fit_n_min": protocol["fit_n_min"],
        "chain_lower": _round(-_slope(fitted_n, [r["chain_lower_mean"] for r in fitted])),
        "chain_median": _round(-_slope(fitted_n, [r["chain_median_mean"] for r in fitted])),
        "chain_upper": _round(-_slope(fitted_n, [r["chain_upper_mean"] for r in fitted])),
        "chain_p99": _round(-_slope(fitted_n, [r["chain_p99_mean"] for r in fitted])),
        "count_median": _round(-_slope(fitted_n, [r["count_median_mean"] for r in fitted])),
        "count_upper": _round(-_slope(fitted_n, [r["count_upper_mean"] for r in fitted])),
        "count_p99": _round(-_slope(fitted_n, [r["count_p99_mean"] for r in fitted])),
    }
    for key in ("chain_lower", "chain_median", "chain_upper", "chain_p99",
                "count_median", "count_upper", "count_p99"):
        decay[f"ell_exponent_{key}"] = _round(2.0 * decay[key])

    buckets = {label: {"n": 0, "abs": [], "ratio": []} for label in BUCKET_LABELS}
    localize_n = protocol["n_localize"]
    for s in protocol["seeds"]:
        bundle = _bundle(module, localize_n, s, area)
        chain, tau = bundle["chain"], bundle["tau"]
        c_chain = scale_cache[(localize_n, s)]
        for i in range(localize_n):
            for j in range(localize_n):
                if bundle["tau_raw"][i][j] > 0.0:
                    label = _bucket(bundle["tau_raw"][i][j] / bundle["ell"])
                    buckets[label]["n"] += 1
                    buckets[label]["abs"].append(abs(chain[i][j] - c_chain * tau[i][j]))
                    buckets[label]["ratio"].append(bundle["chain_raw"][i][j] / (bundle["tau_raw"][i][j] / bundle["ell"]))

    localization = []
    for label in BUCKET_LABELS:
        data = buckets[label]
        if data["n"] == 0:
            continue
        mean_abs = sum(data["abs"]) / len(data["abs"])
        ratio_mean = sum(data["ratio"]) / len(data["ratio"])
        localization.append({
            "bucket": label, "n": data["n"], "max_abs": _round(max(data["abs"])),
            "mean_abs": _round(mean_abs),
            "ratio_mean": _round(ratio_mean),
            "ratio_sd": _round(math.sqrt(sum((v - ratio_mean) ** 2 for v in data["ratio"]) / len(data["ratio"])))})

    exact = []
    for n in protocol["n_exact"]:
        bundle = _bundle(module, n, protocol["exact_seed"], area)
        value, perm = _exact_sf(bundle["chain"], bundle["tau"], iters)
        c_identity, identity = _minimax(_pairs(bundle["chain"], bundle["tau"]), iters)
        exact.append({"n": n, "scale_free_identity": _round(identity),
                      "exact_scale_free_infimum": _round(value), "relative_scale": _round(c_identity),
                      "identity_optimal": bool(perm == tuple(range(n)))})

    control_n = protocol["control_n"]
    bundle = _bundle(module, control_n, protocol["exact_seed"], area)
    rng = random.Random(protocol["control_seed"])
    shuffled = list(range(control_n))
    rng.shuffle(shuffled)
    control = {
        "n": control_n,
        "identity": _round(_minimax(_pairs(bundle["chain"], bundle["tau"]), iters)[1]),
        "random": _round(_minimax(_pairs(bundle["chain"], _permute(bundle["tau"], tuple(shuffled))), iters)[1]),
    }

    crossover = next((r["n"] for r in trend if r["count_upper_mean"] < r["chain_upper_mean"]), None)
    large_tau = ("2^2..2^3", "2^3..2^4", "2^4..2^5", "2^5..2^6", "ge_2^6")
    near_null = ("lt_2^-4", "2^-4..2^-3", "2^-3..2^-2")
    flags = {
        "chain_ceiling_decays_slowly": bool(decay["chain_upper"] > 0.0),
        "chain_median_decays_faster_than_chain_max": bool(decay["chain_median"] > decay["chain_upper"]),
        "chain_p99_decays_faster_than_chain_max": bool(decay["chain_p99"] > decay["chain_upper"]),
        "count_max_decays_faster_than_chain_max": bool(decay["count_upper"] > decay["chain_upper"]),
        "count_median_decays_faster_than_chain_median": bool(decay["count_median"] > decay["chain_median"]),
        "count_p99_decays_faster_than_chain_p99": bool(decay["count_p99"] > decay["chain_p99"]),
        "count_below_chain_from_n": crossover,
        "count_support_matches_directed": bool(all(v == 0 for v in convention["count_offset_vs_directed"].values())),
        "ceiling_is_at_large_proper_time": bool(
            max((row["mean_abs"] for row in localization if row["bucket"] in large_tau), default=0.0)
            > max((row["mean_abs"] for row in localization if row["bucket"] in near_null), default=0.0)),
        "exact_identity_optimal": bool(all(row["identity_optimal"] for row in exact)),
        "lgh_infimum_established": False,
    }

    return {
        "schema": SCHEMA,
        "convention": convention,
        "trend": trend,
        "decay": decay,
        "localization": localization,
        "exact": exact,
        "random_control": control,
        "flags": flags,
        "verdict": (
            "Scale-free LGH convergence re-examined. The certified lower bound for the "
            "order-only (longest-chain) time-separation decays steadily (exponent ~"
            f"{decay['chain_lower']:.2f} in N), but the natural-correspondence ceiling decays "
            f"only ~N^-{decay['chain_upper']:.2f} (much slower than ell) and is localized to "
            "large-proper-time pairs: it is the finite-size fluctuation of the longest-chain "
            "estimator, not a support or convention defect. The distortion is concentrated in "
            f"the upper tail: the typical (median) distortion is ~N^-{decay['chain_median']:.2f} "
            f"while the 99th percentile is ~N^-{decay['chain_p99']:.2f}, both far above the "
            "ceiling decay. The chain bracket therefore does NOT close and chain-based "
            "convergence is not established. The order+count (T7-native) reconstruction decays "
            f"faster on every statistic (ceiling ~N^-{decay['count_upper']:.2f}, median "
            f"~N^-{decay['count_median']:.2f}, 99th percentile ~N^-{decay['count_p99']:.2f}) and "
            f"falls below the chain ceiling from N={crossover}, but its 99th percentile is still "
            "O(0.1) at N=512, so it too is not verified to converge. The obstruction is "
            "therefore estimator-specific: the convergence question depends on which discrete "
            "time-separation reconstruction is used, not on the directed-distance convention "
            "(already corrected by QR-05CZ). The order+count form is a distance estimator, not a "
            "Lorentzian metric (it violates the Lorentzian reverse-triangle inequality on a "
            "three-event chain). No metric, continuum, curvature or gravity claim."),
    }
