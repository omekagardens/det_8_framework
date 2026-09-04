"""
DET v8.1 — Order-and-Count Geometry (T7)

Kinematic reconstruction of a stable manifoldlike Lorentzian geometry from the
causal order ≺ and the counting measure # alone. Gravity is OUT OF SCOPE.

    (≺, #)  ⟶  Lorentzian geometry (dimension, null/conformal structure,
                                 conformal factor, manifoldlike limit)

THE HONEST SEPARATION (the point of this theorem). Two things are routinely
conflated in "causal set → spacetime" programs; T7 keeps them apart:

  1. ESTIMATOR VERIFICATION (what this module does). Given a KNOWN Lorentzian
     manifold, sprinkle events and check that order+count *recover* its
     dimension, null structure, and conformal factor. This is CORR — it proves
     the estimators work on known data, not that the primitives force geometry.

  2. GENUINE EMERGENCE (open). Proving that a bare discrete order+count
     structure is *manifoldlike* — i.e. approximately embeds, and embeds
     essentially uniquely, into a Lorentzian manifold — is the manifoldlikeness
     problem, OPEN in causal set theory. DET's primitives (≺, #, L, 𝔇) do not
     resolve it; they inherit it. Claiming "DET derives spacetime" would be
     smuggling. This module states the boundary explicitly.

What is implemented (pure stdlib):

  - fixed-count iid sampling in a causal diamond (equivalent to a Poisson
    sprinkling conditioned on N = n) of d-dimensional Minkowski spacetime
    (d = 2, 3, 4).
  - causal order generated from the imported flat metric.
  - ORDER → null/conformal diagnostic: under the hypotheses of the imported
    Malament / Hawking–King–McCarthy results, causal structure fixes conformal
    structure. This module does not prove that theorem. It checks only that a
    finite-density link-nullness diagnostic improves on selected generated data.
  - COUNT → conformal-factor diagnostic: in the generating model the counting
    density is ρ·Ω^d at fixed known ρ; a non-uniform
    conformal sprinkling in 1+1 has its conformal factor recovered from counts
    while its causal order stays flat (conformal invariance of order).
  - ORDER+COUNT → dimension: the ordering fraction r = R/C(N,2) in a diamond
    is a dimension-dependent function (Myrheim–Meyer); dimension is recovered
    by comparison to the analytic reference. Independent Monte-Carlo estimates
    are retained as implementation diagnostics.

DERIVATION CERTIFICATE (honest provenance):

  order ⇒ conformal class        MATH — Malament (1977); Hawking–King–McCarthy
                                          (1976); cited.
  count ⇒ conformal factor       MATH — causal set "order + number = geometry"
                                          (Sorkin et al.); cited.
  ordering fraction ⇒ dimension  MATH — Myrheim (1978); Meyer (1988); cited.
  estimator verification         synthetic CORR — on generated Minkowski
                                          sprinklings; no empirical interface.
  manifoldlike emergence         OPEN — not derived here; inherited from causal
                                          set theory (not resolved by DET).

  NOT claimed: gravity, curvature from κ, or any Π/κ conformal factor. The
  retired κ-gravity conformal factor Ω = Π/c is superseded by count.
"""

from __future__ import annotations

import math
import random


# ── Geometry helpers ────────────────────────────────────────────────────────


def _spatial_dist(p: tuple, q: tuple) -> float:
    """Euclidean distance in the spatial (d−1) coordinates."""
    return math.sqrt(sum((p[k] - q[k]) ** 2 for k in range(1, len(p))))


def causally_related(p: tuple, q: tuple) -> bool:
    """p ≺ q in flat Minkowski: t_q > t_p and ‖x_q − x_p‖ < t_q − t_p (c=1)."""
    return q[0] > p[0] and _spatial_dist(p, q) < q[0] - p[0]


def _in_diamond(p: tuple) -> bool:
    """Is p inside the unit causal diamond {0 < t < 1, |x| < min(t, 1−t)}?"""
    t = p[0]
    r = _spatial_dist(p, (0,) + (0,) * (len(p) - 1))
    return 0.0 < t < 1.0 and r < min(t, 1.0 - t)


# ── Sprinkling ──────────────────────────────────────────────────────────────


def sprinkle_diamond(dim: int, n: int, seed: int = 42,
                     weight=None, weight_max: float = 1.0) -> list[tuple]:
    """Rejection-sample n events in the d-dimensional unit causal diamond.

    `weight` optionally biases the density (used for the conformal-factor
    demonstration); it must be a callable p -> non-negative float bounded by
    `weight_max`. The proposal box is [0,1] × [−1/2,1/2]^(d−1), which
    contains the full diamond rather than only one spatial orthant.
    """
    if dim < 2:
        raise ValueError("dim must be at least 2")
    if n < 0:
        raise ValueError("n must be non-negative")
    if not math.isfinite(weight_max) or weight_max <= 0:
        raise ValueError("weight_max must be finite and positive")

    rng = random.Random(seed)
    points: list[tuple] = []
    while len(points) < n:
        p = (rng.random(),) + tuple(
            rng.random() - 0.5 for _ in range(dim - 1)
        )
        if not _in_diamond(p):
            continue
        if weight is not None:
            w = weight(p)
            if not math.isfinite(w) or w < 0 or w > weight_max:
                raise ValueError("weight must be finite and lie in [0, weight_max]")
            if rng.random() > w / weight_max:
                continue
        points.append(p)
    return points


def build_causality(points: list[tuple]) -> list[list[bool]]:
    """prec[i][j] = (points[i] ≺ points[j]) under the flat Minkowski order."""
    n = len(points)
    prec = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and causally_related(points[i], points[j]):
                prec[i][j] = True
    return prec


# ── ORDER → conformal (null) structure via links ────────────────────────────


def links(prec: list[list[bool]]) -> list[list[int]]:
    """links[i] = {j : i ≺ j with no k such that i ≺ k ≺ j}.

    For the generated manifoldlike samples, link separations provide a
    finite-density null-cone diagnostic. This is not the Malament/HKM theorem
    and does not establish continuum or physical manifoldlikeness.
    """
    n = len(prec)
    L = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if not prec[i][j]:
                continue
            is_link = True
            for k in range(n):
                if prec[i][k] and prec[k][j]:
                    is_link = False
                    break
            if is_link:
                L[i].append(j)
    return L


def link_nullness(points: list[tuple], prec: list[list[bool]]) -> dict:
    """Mean null separation δ = Δt − ‖Δx‖ over links vs over all comparable pairs.

    In the selected generated samples, links should be nearer null (δ ≈ 0)
    than generic comparable pairs.
    """
    L = links(prec)
    link_deltas = []
    all_deltas = []
    for i in range(len(points)):
        for j in range(len(points)):
            if not prec[i][j]:
                continue
            dt = points[j][0] - points[i][0]
            dx = _spatial_dist(points[i], points[j])
            d = dt - dx
            all_deltas.append(d)
            if j in L[i]:
                link_deltas.append(d)
    mean = lambda xs: sum(xs) / len(xs) if xs else 0.0
    return {
        "mean_link_nullness": mean(link_deltas),
        "mean_comparable_nullness": mean(all_deltas),
        "n_links": len(link_deltas),
        "n_comparable": len(all_deltas),
    }


# ── ORDER + COUNT → dimension (Myrheim–Meyer ordering fraction) ─────────────


def ordering_fraction(points: list[tuple]) -> float:
    """r = R / C(N,2), where R = # comparable ordered pairs.

    In a causal diamond this is shape-independent and a monotone decreasing
    function of the spacetime dimension d (Myrheim 1978; Meyer 1988).
    """
    prec = build_causality(points)
    n = len(points)
    R = sum(1 for i in range(n) for j in range(n) if prec[i][j])
    denom = n * (n - 1) / 2
    return R / denom if denom else 0.0


def myrheim_meyer_ordering_fraction(dim: int) -> float:
    """Analytic ordering fraction for a Minkowski Alexandrov interval.

    r(d) = Γ(d+1) Γ(d/2) / [2 Γ(3d/2)].
    This is imported causal-set mathematics, not a DET-derived law.
    """
    if dim < 2:
        raise ValueError("dim must be at least 2")
    return (
        math.gamma(dim + 1) * math.gamma(dim / 2)
        / (2 * math.gamma(3 * dim / 2))
    )


def reference_ordering_fractions(dims: list[int], n: int = 400,
                                 trials: int = 5, seed: int = 42) -> dict:
    """Independent Monte-Carlo estimates of r(d), for implementation checks."""
    ref = {}
    for d in dims:
        rs = []
        for t in range(trials):
            pts = sprinkle_diamond(d, n, seed=seed + t)
            rs.append(ordering_fraction(pts))
        ref[d] = sum(rs) / len(rs)
    return ref


def estimate_dimension(points: list[tuple], reference: dict) -> int:
    """Recover the spacetime dimension by nearest reference ordering fraction."""
    r = ordering_fraction(points)
    return min(reference, key=lambda d: abs(reference[d] - r))


# ── COUNT → conformal factor ────────────────────────────────────────────────


def conformal_invariance_of_order() -> dict:
    """The causal order is invariant under a conformal factor Ω² > 0.

    A conformal rescaling g → Ω² g multiplies the spacetime interval by Ω² > 0,
    which preserves its sign. Hence two events are causally related under g iff
    they are under Ω² g. This is the exact (pointwise) form of "order is blind
    to the conformal factor": the order alone can determine the metric only up
    to Ω. The constant-factor sign calculation below is only an arithmetic
    sanity check; it does not verify the general theorem.
    """
    pairs = {
        "timelike": ((0.0, 0.0), (1.0, 0.4)),
        "null": ((0.0, 0.0), (1.0, 1.0)),
        "spacelike": ((0.0, 0.0), (1.0, 1.4)),
    }

    def interval_squared(pair):
        p, q = pair
        return (q[0] - p[0]) ** 2 - _spatial_dist(p, q) ** 2

    def sign(x):
        return (x > 0) - (x < 0)

    flat_signs = {kind: sign(interval_squared(pair))
                  for kind, pair in pairs.items()}
    omega_values = (0.5, 1.0, 3.0, 100.0)
    same_for_all_omega = all(
        sign(omega2 * interval_squared(pair)) == flat_signs[kind]
        for omega2 in omega_values
        for kind, pair in pairs.items()
    )
    return {
        "statement": "g → Ω²·g preserves the causal order for every Ω² > 0 (Malament/HKM).",
        "toy_pairs": pairs,
        "flat_interval_signs": flat_signs,
        "tested_constant_factors": omega_values,
        "invariant": same_for_all_omega,
    }


def conformal_sprinkle_1d(n: int, b: float = 1.0, seed: int = 42) -> tuple:
    """1+1 box [0,1]×[0,1] sprinkle with conformal factor Ω(x)² = 1 + b·x.

    The metric is Ω² (−dt² + dx²), conformally flat, so the CAUSAL ORDER is
    identical to flat Minkowski. Only the volume density (and hence the count)
    sees Ω: the count density is ∝ Ω². Returns (points, weight_function).
    """
    weight = lambda p: 1.0 + b * p[1]  # Ω(x)² = 1 + b·x
    rng = random.Random(seed)
    points = []
    while len(points) < n:
        p = (rng.random(), rng.random())  # (t, x)
        if rng.random() > weight(p) / (1.0 + b):
            continue
        points.append(p)
    return points, weight


def recover_conformal_factor(points: list[tuple], weight, b: float = 1.0,
                             n_bins: int = 10) -> dict:
    """Recover Ω(x)² from binned counts of a conformal 1+1 sprinkling.

    The count density ∝ Ω², so the normalized per-bin count should reproduce
    the normalized weight. Compares the recovered profile to the truth by
    mean squared error.
    """
    bins = [0] * n_bins
    for p in points:
        idx = min(int(p[1] * n_bins), n_bins - 1)
        bins[idx] += 1
    mean_count = sum(bins) / n_bins
    recovered = [c / mean_count for c in bins]  # normalized density profile.
    xs = [(k + 0.5) / n_bins for k in range(n_bins)]
    truth = [weight((0.0, x)) for x in xs]
    mean_truth = sum(truth) / n_bins
    truth_norm = [w / mean_truth for w in truth]
    mse = sum((recovered[k] - truth_norm[k]) ** 2 for k in range(n_bins)) / n_bins
    return {
        "recovered": recovered,
        "truth": truth_norm,
        "mse": mse,
        "x_centers": xs,
    }


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    return {
        "theorem": "T7 — Order-and-Count Geometry",
        "deliverables": {
            "causal order ⇒ conformal (null) structure": "MATH — Malament (1977); Hawking–King–McCarthy (1976); cited",
            "counting measure ⇒ conformal factor": "MATH — causal-set 'order + number = geometry' (Sorkin et al.); cited",
            "ordering fraction ⇒ dimension": "MATH — Myrheim (1978); Meyer (1988); cited",
            "finite-density link-nullness diagnostic": "synthetic CORR — checked on generated Minkowski sprinklings",
            "normalized conformal profile from counts": "synthetic CORR — checked with known density and generating profile",
            "dimension recovery (estimator check)": "synthetic CORR — verified against the analytic Myrheim–Meyer reference",
        },
        "empirical_interface": (
            "None. Inputs are pseudo-random points generated from known "
            "Minkowski or conformally flat geometries."
        ),
        "physical_inference_barrier": (
            "Passing these checks validates code behavior conditional on the "
            "generating models; it supplies no evidence that physical events "
            "are causal-set elements or that a metric is an actualized record."
        ),
        "not_derived_here": [
            "manifoldlike emergence — the claim that a bare (≺, #) structure embeds uniquely into a Lorentzian manifold; OPEN in causal set theory, inherited by DET",
            "gravity or curvature — out of scope for T7 (kinematic only)",
            "the Π/κ conformal factor — retired; count supersedes it",
        ],
        "status": (
            "Synthetic estimator verification complete (CORR). Genuine emergence is the "
            "open manifoldlikeness problem, stated explicitly rather than "
            "claimed. DET does NOT derive spacetime from primitives; it checks "
            "selected estimators against known generated Lorentzian geometries."
        ),
    }


# ── End-to-end T7 ───────────────────────────────────────────────────────────


def run_t7() -> dict:
    """Synthetic T7 diagnostics for nullness, density profile, and dimension."""
    # 1. Finite-density link-nullness diagnostic in 1+1.
    pts_small = sprinkle_diamond(2, 60, seed=1)
    pts_large = sprinkle_diamond(2, 240, seed=1)
    prec_small = build_causality(pts_small)
    prec_large = build_causality(pts_large)
    null_small = link_nullness(pts_small, prec_small)
    null_large = link_nullness(pts_large, prec_large)

    # 2. Counts → normalized generating-density profile in 1+1.
    pts_conf, weight = conformal_sprinkle_1d(4000, b=1.0, seed=7)
    conf = recover_conformal_factor(pts_conf, weight, b=1.0, n_bins=10)
    order_inv = conformal_invariance_of_order()

    # 3. Order+count → dimension.
    analytic_ref = {
        d: myrheim_meyer_ordering_fraction(d) for d in (2, 3, 4)
    }
    monte_carlo_ref = reference_ordering_fractions(
        [2, 3, 4], n=400, trials=5, seed=42
    )
    est_dims = {}
    for d in (2, 3, 4):
        pts = sprinkle_diamond(d, 400, seed=100 + d)
        est_dims[d] = estimate_dimension(pts, analytic_ref)

    return {
        "links_nullness_small": null_small,
        "links_nullness_large": null_large,
        "links_more_null_at_higher_density":
            null_large["mean_link_nullness"] < null_small["mean_link_nullness"],
        "conformal_recovery": conf,
        "order_conformal_invariance": order_inv,
        "reference_ordering_fractions": analytic_ref,
        "monte_carlo_ordering_fractions": monte_carlo_ref,
        "monte_carlo_reference_errors": {
            d: monte_carlo_ref[d] - analytic_ref[d] for d in analytic_ref
        },
        "estimated_dimensions": est_dims,
        "certificate": derivation_certificate(),
        "interpretation": (
            "On generated samples, the link-nullness diagnostic improves with "
            "density, a positive constant conformal rescaling preserves interval "
            "sign in a toy check, a known normalized density profile is recovered "
            "from counts, and analytic ordering fractions recover the generating "
            "dimensions. These are synthetic checks conditional on imported "
            "geometries and causal-set mathematics; manifoldlike emergence remains the open "
            "causal-set problem DET inherits."
        ),
    }
