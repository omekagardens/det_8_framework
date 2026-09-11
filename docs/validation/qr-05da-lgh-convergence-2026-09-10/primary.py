"""Primary route for QR-05DA: scale-free LGH convergence and the estimator split.

QR-05CZ corrected QR-05CW/CX (the continuum counterpart had to be the *directed*
Lorentzian distance) and *reopened* the scale-free convergence question: the
certified lower bound decayed but the natural-correspondence upper bound was
noisy and did not visibly decay, so the infimum stayed bracketed.

This gate attacks the reopened question. It (1) extends the trend to N = 512 and
fits the decay law of the certified lower bound and of the natural-correspondence
ceiling; (2) localizes the ceiling in proper time, showing it is dominated by
large-proper-time pairs and is the finite-size fluctuation of the longest-chain
estimator rather than a support or convention defect; and (3) puts a *count-based*
reconstruction of the discrete time-separation on the same scale-free footing.

Two discrete reconstructions of the time-separation between i and j are compared,
both built from the same (prec) and the same mean spacing ell = sqrt(area/N):

  order-only (QR-05CW..CZ):      d_chain(i,j) = (longest chain i -> j) * ell
  order+count (T7-native):       d_count(i,j) = ell * sqrt(1 + m_ij),
                                 m_ij = #{k : i < k < j} (points strictly between)

The unit offset keeps links positive so the count support matches the directed
Lorentzian distance; the raw m form has a support defect (m = 0 on links), which
is reported. Both are compared to the directed Lorentzian distance under a global
homothety:  inf over c > 0 of min over bijections sigma of
max over pairs |d_X(i,j) - c d_Y(sigma i, sigma j)|, each matrix mean-normalized.

Supplied geometry; no metric, continuum, curvature or gravity claim.
"""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
import statistics
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
    """Longest-chain length i -> j (the order-only time-separation, in links)."""
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


def interval_counts(prec, order):
    """m_ij = #{k : i < k < j}, the number of points strictly between i and j."""
    n = len(prec)
    desc = [set() for _ in range(n)]
    for src in reversed(order):
        acc = set()
        for k in range(n):
            if prec[src][k]:
                acc.add(k)
                acc |= desc[k]
        desc[src] = acc
    anc = [set() for _ in range(n)]
    for src in order:
        acc = set()
        for k in range(n):
            if prec[k][src]:
                acc.add(k)
                acc |= anc[k]
        anc[src] = acc
    return [[len(desc[i] & anc[j]) if prec[i][j] else 0 for j in range(n)] for i in range(n)]


def count_separation(prec, counts, ell):
    """Order+count time-separation (T7-native): ``ell * sqrt(1 + m_ij)``.

    This is a *distance estimator*, not a Lorentzian metric. On a three-event
    chain ``a ≺ b ≺ c`` it gives ``d(a,c) = ell*sqrt(2)`` while
    ``d(a,b) + d(b,c) = 2*ell``, so it violates the Lorentzian reverse-triangle
    inequality ``d(a,c) >= d(a,b) + d(b,c)``; see ``test_qr05da`` and
    SUPERSEDED.md.
    """
    n = len(prec)
    return [[ell * math.sqrt(counts[i][j] + 1) if prec[i][j] else 0.0
             for j in range(n)] for i in range(n)]


def tau_directed(points):
    """Lorentzian distance: positive only for earlier -> later (LMS axiom A3)."""
    n = len(points)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dt = points[j][0] - points[i][0]
            spatial = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, len(points[i])))
            out[i][j] = math.sqrt(dt * dt - spatial) if (dt > 0 and dt * dt > spatial) else 0.0
    return out


def tau_symmetric(points):
    """The CW/CX counterpart (|dt|^2): retained only to re-exhibit the defect."""
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


def pairs_of(a, b):
    n = len(a)
    return [(a[i][j], b[i][j]) for i in range(n) for j in range(n)]


def permute(b, perm):
    n = len(b)
    return [[b[perm[i]][perm[j]] for j in range(n)] for i in range(n)]


def distortion(a, b, perm):
    n = len(a)
    return max(abs(a[i][j] - b[perm[i]][perm[j]]) for i in range(n) for j in range(n))


def minimax_scale(pairs, iters):
    """min over c > 0 of max |p - c q| (a convex 1-D problem)."""
    const = max((abs(p) for p, q in pairs if q == 0.0), default=0.0)

    def f(c):
        worst = const
        for p, q in pairs:
            if q != 0.0:
                value = abs(p - c * q)
                if value > worst:
                    worst = value
        return worst

    lo, hi = 1e-9, 32.0
    gr = (math.sqrt(5.0) - 1.0) / 2.0
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
    return cstar, f(cstar)


def sorted_lists(a, b):
    n = len(a)
    left = sorted(a[i][j] for i in range(n) for j in range(n) if i != j)
    right = sorted(b[i][j] for i in range(n) for j in range(n) if i != j)
    return left, right


def lower_bound_scale(a, b, iters):
    """Certified lower bound: scale-optimized sorted-multiset matching bound."""
    left, right = sorted_lists(a, b)
    return minimax_scale(list(zip(left, right)), iters)[1]


def exact_scale_free_infimum(a, b, iters):
    n = len(a)
    best, best_perm = None, None
    for perm in itertools.permutations(range(n)):
        _c, value = minimax_scale(pairs_of(a, permute(b, perm)), iters)
        if best is None or value < best:
            best, best_perm = value, perm
    return best, best_perm


def _bucket(ratio):
    """Proper-time bucket label for tau/ell = ratio."""
    k = int(math.floor(math.log2(ratio)))
    if k < -4:
        return "lt_2^-4"
    if k >= 6:
        return "ge_2^6"
    return f"2^{k}..2^{k+1}"


def _support_mismatch(a, b):
    n = len(a)
    return sum(1 for i in range(n) for j in range(n) if (a[i][j] > 0) != (b[i][j] > 0))


def _quantile(values, q):
    """Nearest-rank quantile: the smallest sample with P(X <= v) >= q.

    The DA statistics are distortion magnitudes, so the 99th percentile is
    ``_quantile(values, 0.99)`` at index ``ceil(0.99 n) - 1`` (nearest rank).
    The first DA capture used index ``int(0.01 n)`` -- the *1st* percentile --
    and was mislabelled ``p99``; see SUPERSEDED.md.
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
    prec = causality(points)
    ell = math.sqrt(area / n)
    chain_raw = chain_matrix(prec, order)
    counts = interval_counts(prec, order)
    tau_raw = tau_directed(points)
    raw_count = [[ell * math.sqrt(counts[i][j]) if counts[i][j] > 0 else 0.0 for j in range(n)] for i in range(n)]
    count_time = count_separation(prec, counts, ell)
    return {
        "n": n,
        "ell": ell,
        "chain_raw": chain_raw,
        "counts": counts,
        "tau_raw": tau_raw,
        "chain": normalize(chain_raw),
        "tau": normalize(tau_raw),
        "tau_symmetric": normalize(tau_symmetric(points)),
        "count": normalize(count_time),
        "raw_count": raw_count,
    }


def _loglog_slope(xs, ys):
    """Least-squares slope of log y against log x (y ~ x^slope)."""
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    num = sum((a - mx) * (b - my) for a, b in zip(lx, ly))
    den = sum((a - mx) ** 2 for a in lx)
    return num / den


def build_report(protocol):
    module = load_module("_qr05da_t7", MODULE_PATH)
    iters = protocol["minimax_iters"]
    area = protocol["area"]
    seed = protocol["seed"]

    # 1. Retained convention checks (chain vs directed support must match; the
    #    symmetric counterpart must be detected as a defect; the raw count form
    #    is zero on links, which motivates the unit offset).
    convention = {"n_checked": list(protocol["convention_n"]),
                  "chain_vs_directed": {}, "chain_vs_symmetric": {},
                  "count_offset_vs_directed": {}, "count_raw_vs_directed": {}}
    for n in protocol["convention_n"]:
        bundle = _bundle(module, n, seed, area)
        convention["chain_vs_directed"][str(n)] = _support_mismatch(bundle["chain"], bundle["tau"])
        convention["chain_vs_symmetric"][str(n)] = _support_mismatch(bundle["chain"], bundle["tau_symmetric"])
        convention["count_offset_vs_directed"][str(n)] = _support_mismatch(bundle["count"], bundle["tau"])
        convention["count_raw_vs_directed"][str(n)] = _support_mismatch(bundle["raw_count"], bundle["tau"])

    # 2. Trend + localization, one pass over N x seeds.
    scale_cache = {}
    trend = []
    for n in protocol["n_scale"]:
        chain_upper, chain_lower, chain_p99, chain_median = [], [], [], []
        count_upper, count_p99, count_median = [], [], []
        for s in protocol["seeds"]:
            bundle = _bundle(module, n, s, area)
            chain, tau, count = bundle["chain"], bundle["tau"], bundle["count"]
            c_chain, chain_upper_value = minimax_scale(pairs_of(chain, tau), iters)
            scale_cache[(n, s)] = c_chain
            chain_upper.append(chain_upper_value)
            chain_lower.append(lower_bound_scale(chain, tau, iters))
            chain_distortion = [abs(chain[i][j] - c_chain * tau[i][j])
                                for i in range(n) for j in range(n) if tau[i][j] > 0]
            chain_p99.append(_p99(chain_distortion))
            chain_median.append(_median(chain_distortion))
            c_count, count_upper_value = minimax_scale(pairs_of(count, tau), iters)
            count_upper.append(count_upper_value)
            count_distortion = [abs(count[i][j] - c_count * tau[i][j])
                                for i in range(n) for j in range(n) if tau[i][j] > 0]
            count_p99.append(_p99(count_distortion))
            count_median.append(_median(count_distortion))
        ell = math.sqrt(area / n)
        cu = statistics.fmean(chain_upper)
        cl = statistics.fmean(chain_lower)
        cp = statistics.fmean(chain_p99)
        cm = statistics.fmean(chain_median)
        xu = statistics.fmean(count_upper)
        xp = statistics.fmean(count_p99)
        xm = statistics.fmean(count_median)
        trend.append({
            "n": n, "ell": _round(ell), "seeds": len(protocol["seeds"]),
            "chain_upper_mean": _round(cu), "chain_upper_sd": _round(statistics.pstdev(chain_upper)),
            "chain_lower_mean": _round(cl),
            "chain_median_mean": _round(cm), "chain_p99_mean": _round(cp),
            "count_upper_mean": _round(xu), "count_upper_sd": _round(statistics.pstdev(count_upper)),
            "count_median_mean": _round(xm), "count_p99_mean": _round(xp),
            "chain_upper_over_ell": _round(cu / ell), "chain_lower_over_ell": _round(cl / ell),
            "count_upper_over_ell": _round(xu / ell)})

    # Asymptotic decay fits use N >= fit_n_min only: the smallest sizes carry a
    # chain-length transient (few points, coarse integer chains) that does not
    # describe the asymptotic rate.
    fitted = [r for r in trend if r["n"] >= protocol["fit_n_min"]]
    fitted_n = [r["n"] for r in fitted]
    decay = {
        "fit_n_min": protocol["fit_n_min"],
        "chain_lower": _round(-_loglog_slope(fitted_n, [r["chain_lower_mean"] for r in fitted])),
        "chain_median": _round(-_loglog_slope(fitted_n, [r["chain_median_mean"] for r in fitted])),
        "chain_upper": _round(-_loglog_slope(fitted_n, [r["chain_upper_mean"] for r in fitted])),
        "chain_p99": _round(-_loglog_slope(fitted_n, [r["chain_p99_mean"] for r in fitted])),
        "count_median": _round(-_loglog_slope(fitted_n, [r["count_median_mean"] for r in fitted])),
        "count_upper": _round(-_loglog_slope(fitted_n, [r["count_upper_mean"] for r in fitted])),
        "count_p99": _round(-_loglog_slope(fitted_n, [r["count_p99_mean"] for r in fitted])),
    }
    for key in ("chain_lower", "chain_median", "chain_upper", "chain_p99",
                "count_median", "count_upper", "count_p99"):
        decay[f"ell_exponent_{key}"] = _round(2.0 * decay[key])

    # Proper-time localization of the chain ceiling, at the largest size only.
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
        localization.append({
            "bucket": label, "n": data["n"],
            "max_abs": _round(max(data["abs"])),
            "mean_abs": _round(statistics.fmean(data["abs"])),
            "ratio_mean": _round(statistics.fmean(data["ratio"])),
            "ratio_sd": _round(statistics.pstdev(data["ratio"]))})

    # 3. Exact-grid identity optimality for the chain reconstruction (retained).
    exact = []
    for n in protocol["n_exact"]:
        bundle = _bundle(module, n, protocol["exact_seed"], area)
        value, perm = exact_scale_free_infimum(bundle["chain"], bundle["tau"], iters)
        c_identity, identity = minimax_scale(pairs_of(bundle["chain"], bundle["tau"]), iters)
        exact.append({"n": n, "scale_free_identity": _round(identity),
                      "exact_scale_free_infimum": _round(value),
                      "relative_scale": _round(c_identity),
                      "identity_optimal": bool(perm == tuple(range(n)))})

    # 4. Random-correspondence control at a single size.
    control_n = protocol["control_n"]
    bundle = _bundle(module, control_n, protocol["exact_seed"], area)
    rng = random.Random(protocol["control_seed"])
    shuffled = list(range(control_n))
    rng.shuffle(shuffled)
    control = {
        "n": control_n,
        "identity": _round(minimax_scale(pairs_of(bundle["chain"], bundle["tau"]), iters)[1]),
        "random": _round(minimax_scale(pairs_of(bundle["chain"], permute(bundle["tau"], tuple(shuffled))), iters)[1]),
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
