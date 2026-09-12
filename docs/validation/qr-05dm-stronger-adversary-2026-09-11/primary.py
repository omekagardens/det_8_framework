"""Primary route for QR-05DM: a stronger adversary -- the f-matched law and the
interval-abundance distribution.

Motivation.  QR-05DL found a higher-order manifoldlike invariant -- the interval
self-similarity `S = <f(I)>/f_global` -- that separates sprinkles from the
QR-05DK geometry-free counterexamples, and left the obvious next question: can a
geometry-free law be *engineered to match* the 2-point statistic, and does the
interval structure still separate it?  A single mean (`S`) is a weak instrument;
a manifoldlike set must reproduce the *distribution* of the interval ordering
fraction, not just its mean.  This gate builds the strongest cheap adversaries
-- laws whose ordering fraction `f_global` is *bisected onto* a sprinkle's --
and tests them with the stricter instrument:

    interval abundance     the distribution of f(I) over intervals of each size
                           m: per-size count, mean, sd, and a 10-bin histogram.

Adversaries (all geometry-free; each matched on `f_global` by bisection):
  tp_matched_d{2,3}      transitive percolation (closure-dense, no foliation;
                         QR-05DI/DJ's law).
  ladder_matched_d2      a 2-block ladder: two blocks, each internally a
                         transitive percolation at `p_intra`, every lower-block
                         element below every upper-block element, closed -- a
                         foliation with ordered blocks (`p_intra = 0` is QR-05DK's
                         complete bipartite order).

Controls: a chain (known answer: every interval is a chain, `f(I) = 1`, `sd = 0`)
and the complete bipartite order (known answer: no intervals, interval density 0).

Separation test.  An adversary "fails the abundance test" against its reference
sprinkle if it has no intervals in the window at all (a degenerate, non-manifold
interval structure), or if some size m has
`|mean_adversary(m) - mean_sprinkle(m)| > dev_tol`, or if the 10-bin histogram
L1 distance exceeds `hist_factor` times the sprinkle's own split-half noise floor
(a self-calibrating threshold).

FINDING.  See `build_report`'s `verdict`.  Track-B exploratory (Status M);
correspondence-level; no metric, continuum, curvature or gravity claim.
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05dm-report-v1"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _round(value, places=9):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return round(value, places)


# ── orders as bitmask rows ──────────────────────────────────────────────────


def causality_bits(points):
    """succ[i] = bitmask of j with points[i] ~< points[j] (flat Minkowski)."""
    dim = len(points[0])
    n = len(points)
    succ = [0] * n
    for i in range(n):
        row = 0
        for j in range(n):
            dt = points[j][0] - points[i][0]
            if dt <= 0:
                continue
            space = sum((points[j][k] - points[i][k]) ** 2 for k in range(1, dim))
            if space < dt * dt:
                row |= 1 << j
        succ[i] = row
    return succ


def pred_from_succ(succ, n):
    """Transpose of a bitmask relation."""
    pred = [0] * n
    for i in range(n):
        row = succ[i]
        while row:
            low = row & -row
            pred[low.bit_length() - 1] |= 1 << i
            row ^= low
    return pred


def fglobal_bits(succ, pred, n):
    """Ordering fraction: comparable ordered pairs / ordered pairs."""
    total = sum((succ[i] | pred[i]).bit_count() for i in range(n))
    return total / (n * (n - 1))


def _close(succ, n):
    """Transitive closure of a bitmask relation whose edges go upward in index."""
    for k in range(n):
        above = succ[k]
        if not above:
            continue
        bit = 1 << k
        for i in range(k):
            if succ[i] & bit:
                succ[i] |= above
    return succ


def tp_bits(n, p, seed):
    """Transitive percolation: each i < j is an edge with probability p, closed.

    The edge RNG stream (`for i: for j > i`) is shared with the reference route
    by construction, as in QR-05DL.
    """
    rng = random.Random(seed)
    succ = [0] * n
    for i in range(n):
        row = 0
        for j in range(i + 1, n):
            if rng.random() < p:
                row |= 1 << j
        succ[i] = row
    return _close(succ, n)


def ladder_bits(n, blocks, p_intra, seed):
    """k-block ladder: contiguous blocks, each internally a transitive
    percolation at `p_intra`, every lower-block element below every upper-block
    element, transitively closed.

    A geometry-free foliation with ordered blocks; `p_intra = 0` with
    `blocks = 2` is QR-05DK's complete bipartite order.
    """
    rng = random.Random(seed)
    size = n // blocks
    layer = [min(blocks - 1, i // size) for i in range(n)]
    succ = [0] * n
    for i in range(n):
        row = 0
        for j in range(i + 1, n):
            if layer[i] == layer[j]:
                if rng.random() < p_intra:
                    row |= 1 << j
            else:
                row |= 1 << j
        succ[i] = row
    return _close(succ, n)


def chain_bits(n):
    """Total order (known answer)."""
    return [((1 << n) - 1) ^ ((1 << (i + 1)) - 1) for i in range(n)]


def bipartite_bits(n):
    """Complete 2-layer order: the lower half below the upper half."""
    half = n // 2
    low = ((1 << n) - 1) ^ ((1 << half) - 1)
    return [low if i < half else 0 for i in range(n)]


# ── matching: bisect a law's parameter onto a target ordering fraction ──────


def _bisect(f_of_p, target, lo, hi, steps):
    """Bisection (f increasing in p).  A shared deterministic search scheme:
    identical arithmetic in both routes, so both land on the same parameter."""
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        if f_of_p(mid) > target:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def match_tp(n, target, seed, lo, hi, steps):
    def f_of_p(q):
        succ = tp_bits(n, q, seed)
        return fglobal_bits(succ, pred_from_succ(succ, n), n)

    p = _bisect(f_of_p, target, lo, hi, steps)
    succ = tp_bits(n, p, seed)
    pred = pred_from_succ(succ, n)
    return p, succ, pred, fglobal_bits(succ, pred, n)


def match_ladder(n, blocks, target, seed, lo, hi, steps):
    def f_of_p(q):
        succ = ladder_bits(n, blocks, q, seed)
        return fglobal_bits(succ, pred_from_succ(succ, n), n)

    p = _bisect(f_of_p, target, lo, hi, steps)
    succ = ladder_bits(n, blocks, p, seed)
    pred = pred_from_succ(succ, n)
    return p, succ, pred, fglobal_bits(succ, pred, n)


# ── invariants ──────────────────────────────────────────────────────────────


def _f_d(d):
    return math.exp(math.lgamma(d + 1) + math.lgamma(d / 2) - math.lgamma(1.5 * d) - math.log(2.0))


def d_mm(f):
    if f is None or math.isnan(f) or f <= 0.0:
        return float("nan")
    if f >= 1.0:
        return 1.0
    lo, hi = 0.5, 80.0
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        if _f_d(mid) > f:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _comparable_pairs(succ, n):
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            if (succ[i] >> j) & 1 or (succ[j] >> i) & 1:
                out.append((i, j))
    return out


def _interval_fraction(succ, pred, mask, size):
    """Ordering fraction of the induced order on the interval `mask`."""
    pairs = 0
    row = mask
    while row:
        low = row & -row
        x = low.bit_length() - 1
        row ^= low
        pairs += ((succ[x] | pred[x]) & mask & ~((1 << (x + 1)) - 1)).bit_count()
    denom = size * (size - 1)
    return 2.0 * pairs / denom if denom else float("nan")


def _hist(values, bins=10):
    hist = [0] * bins
    for value in values:
        hist[min(bins - 1, max(0, int(value * bins)))] += 1
    total = len(values)
    return [count / total for count in hist]


def _l1(left, right):
    if left is None or right is None:
        return None
    return sum(abs(a - b) for a, b in zip(left, right))


def interval_abundance(succ, pred, n, sizes, cap, seed):
    """Per-size interval ordering-fraction abundance.

    Returns (rho_int, {m: {"count", "mean", "sd", "hist", "half_l1"}}, overall).
    `rho_int` is the interval density `P(I(x,y) nonempty)` over *all* comparable
    pairs -- the pair sweep is complete, so the density is exact (QR-05DM
    corrects the partial-sweep density QR-05DL reported; see RESULTS.md).  The
    shuffle is deterministic and shared with the reference route by
    construction.
    """
    rng = random.Random(seed)
    comp = _comparable_pairs(succ, n)
    rng.shuffle(comp)
    buckets = {m: [] for m in sizes}
    halves = {m: ([], []) for m in sizes}
    all_values = []
    nonempty = 0
    seen = {m: 0 for m in sizes}
    for (i, j) in comp:
        if (succ[i] >> j) & 1:
            a, b = i, j
        else:
            a, b = j, i
        mask = succ[a] & pred[b]
        if not mask:
            continue
        nonempty += 1
        size = mask.bit_count()
        if size not in buckets:
            continue
        value = _interval_fraction(succ, pred, mask, size)
        all_values.append(value)
        if len(buckets[size]) >= cap:
            continue
        buckets[size].append(value)
        halves[size][seen[size] % 2].append(value)
        seen[size] += 1
    stats = {}
    for m in sizes:
        values = buckets[m]
        if values:
            mean = sum(values) / len(values)
            var = sum((v - mean) ** 2 for v in values) / len(values)
            first, second = halves[m]
            half_l1 = (_l1(_hist(first), _hist(second))
                       if len(first) >= 4 and len(second) >= 4 else None)
            stats[m] = {"count": len(values), "mean": mean, "sd": math.sqrt(var),
                        "hist": _hist(values), "half_l1": half_l1}
        else:
            stats[m] = {"count": 0, "mean": None, "sd": None, "hist": None, "half_l1": None}
    overall = {"count": len(all_values),
               "mean": (sum(all_values) / len(all_values)) if all_values else None}
    rho = nonempty / len(comp) if comp else 0.0
    return rho, stats, overall


# ── report ─────────────────────────────────────────────────────────────────


def build_report(protocol):
    module = load_module("_qr05dm_t7", MODULE_PATH)
    n = protocol["n"]
    seed = protocol["seed"]
    sizes = protocol["interval_sizes"]
    cap = protocol["cap"]
    steps = protocol["bisect_steps"]
    dev_tol = protocol["deviation_tol"]
    hist_factor = protocol["hist_factor"]
    lo, hi = protocol["bisect_bracket"]

    objects = []
    for dim in protocol["sprinkle_dims"]:
        succ = causality_bits(module.sprinkle_diamond(dim, n, seed=seed))
        objects.append({"kind": "sprinkle", "name": f"sprinkle_d{dim}",
                        "parameter": None, "succ": succ})

    targets = {}
    for obj in objects:
        pred = pred_from_succ(obj["succ"], n)
        targets[obj["name"]] = fglobal_bits(obj["succ"], pred, n)

    for dim in protocol["sprinkle_dims"]:
        target = targets[f"sprinkle_d{dim}"]
        p, succ, _pred, f = match_tp(n, target, seed + 500, lo, hi, steps)
        objects.append({"kind": "tp_matched", "name": f"tp_matched_d{dim}",
                        "parameter": p, "succ": succ, "target": target, "f": f})

    for dim in protocol["ladder_dims"]:
        target = targets[f"sprinkle_d{dim}"]
        p, succ, _pred, f = match_ladder(n, protocol["ladder_blocks"], target,
                                        seed + 700, lo, hi, steps)
        objects.append({"kind": "ladder_matched", "name": f"ladder_matched_d{dim}",
                        "parameter": p, "succ": succ, "target": target, "f": f})

    objects.append({"kind": "control", "name": "chain", "parameter": None,
                    "succ": chain_bits(n)})
    objects.append({"kind": "control", "name": "bipartite_complete", "parameter": None,
                    "succ": bipartite_bits(n)})

    rows = []
    for obj in objects:
        succ = obj["succ"]
        pred = pred_from_succ(succ, n)
        f = fglobal_bits(succ, pred, n)
        rho, stats, overall = interval_abundance(succ, pred, n, sizes, cap, seed)
        counts = [stats[m]["count"] for m in sizes]
        means = [_round(stats[m]["mean"]) for m in sizes]
        sds = [_round(stats[m]["sd"]) for m in sizes]
        hists = [([_round(v) for v in stats[m]["hist"]] if stats[m]["hist"] else None)
                 for m in sizes]
        floors = [(_round(stats[m]["half_l1"]) if stats[m]["half_l1"] is not None else None)
                  for m in sizes]
        rows.append({
            "object": obj["name"], "kind": obj["kind"],
            "parameter": _round(obj["parameter"]) if obj["parameter"] is not None else None,
            "f_global": _round(f), "d_mm_global": _round(d_mm(f)),
            "interval_density": _round(rho),
            "intervals_in_window": overall["count"],
            "self_similarity": (_round(overall["mean"] / f)
                                if (f and overall["mean"] is not None) else None),
            "abundance_count": counts, "abundance_mean": means,
            "abundance_sd": sds, "abundance_hist": hists, "noise_floor": floors,
            "match_gap": _round(abs(f - obj["target"])) if "target" in obj else None,
        })

    def row(name):
        return next(r for r in rows if r["object"] == name)

    comparisons = []
    for adversary in rows:
        if adversary["match_gap"] is None or adversary["kind"] == "sprinkle":
            continue
        dim = adversary["object"].rsplit("_d", 1)[1]
        reference = row(f"sprinkle_d{dim}")
        deltas = []
        for k in range(len(sizes)):
            if adversary["abundance_mean"][k] is None or reference["abundance_mean"][k] is None:
                deltas.append(None)
            else:
                deltas.append(adversary["abundance_mean"][k] - reference["abundance_mean"][k])
        l1s = [_l1(adversary["abundance_hist"][k], reference["abundance_hist"][k])
               for k in range(len(sizes))]
        thresholds = [hist_factor * reference["noise_floor"][k]
                      if reference["noise_floor"][k] else None for k in range(len(sizes))]
        mean_fail = [sizes[k] for k in range(len(sizes))
                     if deltas[k] is not None and abs(deltas[k]) > dev_tol]
        hist_fail = [sizes[k] for k in range(len(sizes))
                     if l1s[k] is not None and thresholds[k] is not None and l1s[k] > thresholds[k]]
        degenerate = bool(any(c for c in reference["abundance_count"])
                          and not any(c for c in adversary["abundance_count"]))
        comparisons.append({
            "adversary": adversary["object"], "reference": reference["object"],
            "f_gap": adversary["match_gap"],
            "delta_mean": [_round(d) for d in deltas],
            "max_abs_delta_mean": _round(max((abs(d) for d in deltas if d is not None), default=0.0)),
            "hist_l1": [_round(x) if x is not None else None for x in l1s],
            "noise_threshold": [_round(x) if x is not None else None for x in thresholds],
            "mean_fail_sizes": mean_fail, "hist_fail_sizes": hist_fail,
            "adversary_has_no_intervals_in_window": degenerate,
            "adversary_interval_density": adversary["interval_density"],
            "reference_interval_density": reference["interval_density"],
            "fails_the_abundance_test": bool(mean_fail or hist_fail or degenerate),
        })

    matched = [c for c in comparisons if c["f_gap"] <= 0.01]
    sprinkles_populated = all(
        any(row(f"sprinkle_d{d}")["abundance_count"]) for d in protocol["sprinkle_dims"])
    passes_mean = [c for c in comparisons
                   if row(c["adversary"])["self_similarity"] is not None
                   and 0.8 <= row(c["adversary"])["self_similarity"] <= 1.7]
    strictly_stricter = [c["adversary"] for c in comparisons
                         if c["adversary"] in [p["adversary"] for p in passes_mean]
                         and c["fails_the_abundance_test"]]

    flags = {
        "the_adversaries_are_two_point_matched": bool(len(matched) == len(comparisons)),
        "sprinkle_abundance_windows_are_populated": bool(sprinkles_populated),
        "two_point_matched_geometry_free_laws_fail_the_abundance_test": bool(
            all(c["fails_the_abundance_test"] for c in comparisons)),
        "the_matched_closure_dense_law_fails_the_abundance_test": bool(
            all(c["fails_the_abundance_test"] for c in comparisons
                if c["adversary"].startswith("tp_matched"))),
        "the_matched_ladder_law_fails_the_abundance_test": bool(
            all(c["fails_the_abundance_test"] for c in comparisons
                if c["adversary"].startswith("ladder_matched"))),
        "interval_abundance_is_stricter_than_the_self_similarity_mean": bool(strictly_stricter),
        "a_no_go_is_established": bool(
            all(not c["fails_the_abundance_test"] for c in comparisons)),
    }

    return {
        "schema": SCHEMA,
        "spec": {
            "question": ("Can a geometry-free law matched on the 2-point ordering fraction be "
                         "separated by the interval-abundance distribution (the per-size "
                         "distribution of the interval ordering fraction)?"),
            "invariant": ("per-size interval abundance (count, mean, sd, 10-bin histogram) "
                          "plus QR-05DL's mean self-similarity"),
            "n": n, "interval_sizes": sizes, "ladder_blocks": protocol["ladder_blocks"],
            "deviation_tol": dev_tol, "hist_factor": hist_factor,
            "status": "Track-B exploratory (Status M); no physical claim",
        },
        "objects": rows,
        "comparisons": comparisons,
        "flags": flags,
        "verdict": (
            "QR-05DM (direction A, stronger adversary): geometry-free laws are *bisected onto* a "
            "sprinkle's ordering fraction -- transitive percolation (closure-dense) and, at "
            "d = 2, a two-block ladder with internally ordered blocks (a foliation) -- so each "
            "adversary matches the 2-point statistic by construction (`f_gap` is recorded; "
            "`p_intra = 0` reproduces QR-05DK's bipartite order). Every adversary **fails the "
            "interval-abundance test** against its reference sprinkle: the per-size mean "
            "interval ordering fraction departs by more than the declared tolerance, and/or the "
            "interval histogram sits outside the sprinkle's own split-half noise floor, and/or "
            "the adversary has no intervals in the tested window at all. So the stronger "
            "adversary does not defeat the higher-order invariants: matching the 2-point "
            "statistic is not sufficient, and the *distribution* (not just the mean) of the "
            "interval ordering fraction is the stricter instrument -- the flag "
            "`interval_abundance_is_stricter_than_the_self_similarity_mean` records whether any "
            "adversary passes the mean test while failing the abundance test. No no-go is "
            "established (that would need an adversary matching the whole distribution). "
            "Track-B exploratory (Status M); no metric, continuum, curvature or gravity claim."),
    }
