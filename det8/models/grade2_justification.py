"""DET v8.1 — grade-two restriction and the separate strong-positivity premise.

An explicit nonnegative normalized grade-three set-function shows that
normalization, eventwise positivity and binary event notation do not force
grade two. No composition theorem follows without a specified composition
contract. Grade two gives I3=0 on disjoint events, but eventwise positivity
plus grade two does not imply strong positivity or a Hilbert representation.
On three atoms, μ(A)=|A|(|A|-1)/6 is a counterexample: singleton weights are
zero and pair weights are 1/3, impossible for a PSD Gram matrix.

The finite Gram theorem in pair_kernel.py requires an admitted Hermitian,
biadditive, strongly positive pair-kernel. These are additional premises.
The count-based statistic below checks one triple against a fixed tolerance;
it is neither a significance calculation nor evidence selecting the Born
rule, the complex field, or all quantum instruments. Existing synthetic
count generation and historical callable names are retained.
"""

from __future__ import annotations

import itertools
import math
import random

from det8.models.pair_kernel import PairKernel

# ── The grade / Möbius basis of a finite measure ────────────────────────────


class GradeMeasure:
    """A set-function μ on Ω = {0,…,n−1} in its grade (Möbius) basis.

    μ(A) = Σ_{S ⊆ A} w_S, with weights w_S ∈ ℝ for each nonempty S ⊆ Ω
    (w_∅ = 0 by convention). A measure is 'grade-k' iff every weight of
    size > k vanishes; then I_k on disjoint singletons equals the size-k weight.
    """

    def __init__(self, weights: dict, n: int):
        self.n = n
        self.weights = {frozenset(S): float(w) for S, w in weights.items()}
        # drop zero weights for a clean 'grade' computation
        self.weights = {S: w for S, w in self.weights.items() if abs(w) > 1e-12}

    @staticmethod
    def _as_set(event) -> frozenset:
        if isinstance(event, frozenset):
            return event
        return frozenset(event)

    def omega(self) -> frozenset:
        return frozenset(range(self.n))

    def mu(self, A) -> float:
        A = self._as_set(A)
        return sum(w for S, w in self.weights.items() if S <= A)

    def interference(self, *sets) -> float:
        """I_k(A_1,…,A_k) = Σ_{∅≠J⊆[k]} (−1)^{k−|J|} μ(∪_{j∈J} A_j)."""
        sets = [self._as_set(s) for s in sets]
        k = len(sets)
        total = 0.0
        for r in range(1, k + 1):
            sign = (-1) ** (k - r)
            for J in itertools.combinations(range(k), r):
                union = frozenset()
                for j in J:
                    union |= sets[j]
                total += sign * self.mu(union)
        return total

    def grade(self) -> int:
        """The largest subset size with a nonzero weight (∞ if none)."""
        if not self.weights:
            return 0
        return max(len(S) for S in self.weights)

    def is_grade(self, k: int, tol: float = 1e-9) -> bool:
        return all(len(S) <= k for S in self.weights)

    def is_normalized(self, tol: float = 1e-9) -> bool:
        return abs(self.mu(self.omega()) - 1.0) < tol

    def is_positive(self, tol: float = 1e-9) -> bool:
        """μ(A) ≥ 0 for every A ⊆ Ω (positive commitability)."""
        return all(self.mu(frozenset(i for i in range(self.n) if mask >> i & 1)) >= -tol
                   for mask in range(1 << self.n))


# ── Constructors for each grade ─────────────────────────────────────────────


def make_grade1_classical(n: int, seed: int = 42) -> GradeMeasure:
    """A classical (grade-1) measure: additive, weights only on singletons."""
    rng = random.Random(seed)
    p = [rng.random() for _ in range(n)]
    tot = sum(p)
    weights = {frozenset([i]): p[i] / tot for i in range(n)}
    return GradeMeasure(weights, n)


def grade_measure_from_pair_kernel(pk: PairKernel) -> GradeMeasure:
    """Extract the grade-2 (Möbius) weights of a pair-kernel 𝔇.

    w_i = μ({i}) = 𝔇({i},{i});  w_ij = I_2({i},{j}) = 2 Re 𝔇({i},{j});
    all higher weights are zero (grade-2). This is the T2a↔T2b bridge.
    """
    n = pk.n
    weights = {}
    for i in range(n):
        weights[frozenset([i])] = pk.mu({i})
    for i in range(n):
        for j in range(i + 1, n):
            weights[frozenset([i, j])] = 2.0 * pk.D_value({i}, {j}).real
    return GradeMeasure(weights, n)


def make_grade3_counterexample(delta: float = 0.25, n: int = 4) -> GradeMeasure:
    """An explicit normalized, POSITIVE grade-3 measure with I_3 = δ ≠ 0.

    Weights: singletons (1−δ)/n each; a single triple {0,1,2} with weight δ;
    all else zero. Then μ(Ω) = 1, μ(A) ≥ 0 for all A (for 0 < δ < 1), and
    I_3({0},{1},{2}) = w_{012} = δ ≠ 0, while I_4 = 0 (no 4-set weight).
    """
    from det8.models.validation import require_real_finite

    delta = require_real_finite(delta, "delta")
    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie strictly between 0 and 1")
    if isinstance(n, bool) or not isinstance(n, int) or n < 3:
        raise ValueError("n must be an integer of at least 3")
    weights = {frozenset([i]): (1.0 - delta) / n for i in range(n)}
    weights[frozenset([0, 1, 2])] = delta
    return GradeMeasure(weights, n)


# ── The negative result ─────────────────────────────────────────────────────


def negative_result() -> dict:
    """Grade-2 is not forced by normalization and eventwise positivity.

    Constructs the explicit grade-3 counterexample and verifies it is a
    legitimate normalized, positive measure with I_3 ≠ 0. Binary yes/no
    event notation alone does not constrain its degree. Additional axioms
    connecting a causal order to the measure are not tested here.
    """
    m = make_grade3_counterexample(delta=0.25, n=4)
    i3 = m.interference({0}, {1}, {2})
    i4 = m.interference({0}, {1}, {2}, {3})
    return {
        "normalized": m.is_normalized(),
        "positive": m.is_positive(),
        "grade": m.grade(),
        "I3": i3,
        "I4": i4,
        "conclusion": (
            "A normalized, positive grade-3 measure exists with I_3 = "
            f"{i3:.3f} ≠ 0. Positivity + normalization therefore do NOT force "
            "grade-2; the pairwise restriction is an independent assumption."
        ),
        "binary_events_note": (
            "Each subset of Ω = {0,1,2,3} defines a yes/no event, yet I3 is nonzero. "
            "Binary event notation alone does not force grade two; no extra "
            "causal-order/measure compatibility axioms are tested."
        ),
    }


# ── Honest enumeration of the a-priori forcing routes ───────────────────────


def a_priori_routes() -> dict:
    """Candidate a-priori justifications of grade-2, and their status."""
    return {
        "record_is_a_set_of_binary_facts": {
            "claim": "the record R is a set of binary (yes/no) committed facts, so the possibility measure is grade-2",
            "status": "CIRCULAR — 'grade-2' is precisely 'no irreducible higher-order relations'; asserting the record carries only pairwise relations IS the assumption",
        },
        "sequential_pairwise_commit": {
            "claim": "record growth is sequential, one commit at a time against the existing pairwise record, forcing grade-2",
            "status": "CIRCULAR — presupposes the existing record is pairwise (grade-2) at each step",
        },
        "binary_causal_order": {
            "claim": "≺ is a binary relation, so the induced measure must be grade-2",
            "status": "NOT IMPLIED BY BINARY NOTATION ALONE — the counterexample has yes/no events; additional order/measure compatibility axioms are untested",
        },
        "composition_closure": {
            "claim": "composition of alternatives forces grade-2",
            "status": "NOT ESTABLISHED HERE — no physical composition contract or closure theorem is supplied",
        },
        "verdict": (
            "No non-circular a-priori forcing of grade-2 is available from the "
            "current primitives. The honest discriminator is empirical (§7.2): "
            "measure I_2 and I_3 from raw counts."
        ),
    }


# ── §7.2 empirical discriminator ────────────────────────────────────────────


def estimate_mu_from_counts(counts: dict) -> dict:
    """Estimate μ(A) = N(A)/N(Ω) from raw alternative-combination counts.

    `counts` maps a frozenset (a set of alternatives) to its raw count.
    """
    counts = {GradeMeasure._as_set(A): float(c) for A, c in counts.items()}
    omega = frozenset().union(*counts.keys()) if counts else frozenset()
    total = counts.get(omega, sum(counts.values()))
    if total <= 0:
        raise ValueError("total count must be positive")
    return {A: c / total for A, c in counts.items()}


def interference_from_counts(counts: dict, *sets) -> float:
    """Estimate I_k from raw counts (the §7.2 discriminator statistic)."""
    mu = estimate_mu_from_counts(counts)
    sets = [GradeMeasure._as_set(s) for s in sets]
    k = len(sets)
    total = 0.0
    for r in range(1, k + 1):
        sign = (-1) ** (k - r)
        for J in itertools.combinations(range(k), r):
            union = frozenset()
            for j in J:
                union |= sets[j]
            total += sign * mu.get(union, 0.0)
    return total


def grade2_discriminator(counts: dict, tol: float = 0.05) -> dict:
    """§7.2: compare one counted triple's I3 with a fixed tolerance.

    Estimates I_2 (pairwise interference) and I_3 (3-way) from raw counts and
    compares |I_3| to a tolerance. Honest note: the significance of |I_3| > 0
    depends on the counting model (Poisson/multinomial); this returns the raw
    estimates and a coarse classification, not a formal p-value.
    """
    estimate_mu_from_counts(counts)  # Validate the reference normalization.
    omega = frozenset().union(*counts.keys())
    # I_2 on the first two singletons, I_3 on the first three.
    atoms = sorted(omega)[:3]
    a, b, c = frozenset([atoms[0]]), frozenset([atoms[1]]), frozenset([atoms[2]])
    i2 = interference_from_counts(counts, a, b)
    i3 = interference_from_counts(counts, a, b, c)
    return {
        "I2": i2,
        "I3": i3,
        "grade2": abs(i3) < tol,
        "scope": {"tested_triple": tuple(atoms), "significance_test": False,
                  "universal_grade2_established": False, "born_rule_selected": False},
        "interpretation": (
            f"I_2 = {i2:+.4f} (pairwise interference), I_3 = {i3:+.4f} "
            f"(3-way). " + ("Consistent with grade-2 (I_3 ≈ 0)."
                            if abs(i3) < tol else
                            "Outside the stated tolerance on this triple; counting and apparatus errors require separate analysis.")
        ),
    }


def simulate_counts(measure: GradeMeasure, n_trials: int,
                    seed: int = 42) -> dict:
    """Draw raw alternative-combination counts from a measure (multi-slit).

    §7.2 measures the *event intensity* μ(A) for each open alternative-set A
    (the multi-slit analogue): a separate run for each A counts arrivals
    N(A) ∝ μ(A), with μ(Ω) = N(Ω) the reference total. Each N(A) is drawn
    Poisson(mean n_trials·μ(A)) via a normal approximation. Crucially, this
    exposes I_2 and I_3 (single-outcome sampling would erase them).
    """
    rng = random.Random(seed)
    atoms = list(range(measure.n))
    counts = {}
    for mask in range(1, 1 << measure.n):
        A = frozenset(i for i in atoms if mask >> i & 1)
        lam = n_trials * measure.mu(A)
        n = max(0, round(rng.gauss(lam, math.sqrt(max(lam, 1e-9)))))
        counts[A] = n
    return counts


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    return {
        "theorem": "T2a — non-entailment of grade two and strong positivity",
        "deliverables": {
            "grade-two set-functions have I3=0 on disjoint events": "MATH — finite interference identity",
            "strongly positive Hermitian biadditive D has a finite Gram representation": "MATH — conditional Gram theorem",
            "normalization and eventwise positivity do not force grade two": "MATH — grade-three counterexample",
            "nonnegative grade two does not force strong positivity": "MATH — zero-singleton, positive-pair counterexample",
            "count-based I2 and I3 statistic": "CORR — fixed-tolerance descriptive calculation",
        },
        "scope": {
            "grade2_implies_strong_positivity": False,
            "gram_requires_strong_positivity": True,
            "composition_closure_established": False,
            "empirical_born_selection": False,
        },
        "not_derived_here": [
            "a forcing of grade two or strong positivity from the record/order primitives",
            "composition closure without a specified composition law",
            "a universal interference law or Born rule from finite noisy counts",
        ],
        "status": "COUNTEREXAMPLES_AND_CONDITIONAL_GRAM_THEOREM; FULL_QM_NOT_DERIVED",
    }


# ── End-to-end ──────────────────────────────────────────────────────────────


def run_t2a() -> dict:
    from det8.models.pair_kernel import make_pair_kernel

    # 1. The negative result.
    neg = negative_result()

    # 2. The supplied pair-kernel has I_3 = 0, I_2 ≠ 0.
    pk = make_pair_kernel(4, seed=42, coherent=True)
    g2 = grade_measure_from_pair_kernel(pk)
    g2_i2 = g2.interference({0}, {1})
    g2_i3 = g2.interference({0}, {1}, {2})

    # 3. Empirical discriminator on simulated grade-2 vs grade-3 data.
    counts_g2 = simulate_counts(g2, n_trials=20000, seed=1)
    counts_g3 = simulate_counts(make_grade3_counterexample(0.25, 4),
                                n_trials=20000, seed=2)
    disc_g2 = grade2_discriminator(counts_g2)
    disc_g3 = grade2_discriminator(counts_g3)

    return {
        "negative_result": neg,
        "grade2_pair_kernel": {"I2": g2_i2, "I3": g2_i3,
                               "grade": g2.grade(),
                               "I3_vanishes": abs(g2_i3) < 1e-9},
        "discriminator_grade2_data": disc_g2,
        "discriminator_grade3_data": disc_g3,
        "a_priori_routes": a_priori_routes(),
        "certificate": derivation_certificate(),
        "interpretation": (
            "A normalized positive grade-3 measure exists (I_3 = "
            f"{neg['I3']:.3f} ≠ 0), so grade-2 is not forced a priori. The "
            "grade-2 pair-kernel has I_3 = 0 (grade 2) with I_2 ≠ 0. The §7.2 "
            f"discriminator reads grade-2 data as I_3 ≈ {disc_g2['I3']:+.4f} "
            f"(grade-2: {disc_g2['grade2']}) and grade-3 data as I_3 ≈ "
            f"{disc_g3['I3']:+.4f} (grade-2: {disc_g3['grade2']}). Grade-2 is "
            "a separately proposed restriction; these synthetic counts do not establish it universally or select a Born rule."
        ),
    }


def strong_positivity_counterexample() -> dict:
    """A nonnegative normalized grade-two measure with no strongly positive D."""
    measure = GradeMeasure({frozenset(pair): 1 / 3
                            for pair in itertools.combinations(range(3), 2)}, n=3)
    return {
        "measure": measure,
        "singleton_weights": [measure.mu({i}) for i in range(3)],
        "pair_weights": [measure.mu(pair) for pair in itertools.combinations(range(3), 2)],
        "normalized": measure.is_normalized(),
        "eventwise_positive": measure.is_positive(),
        "grade": measure.grade(),
        "strong_positive_representation_exists": False,
        "proof": "PSD Cauchy-Schwarz makes every off-diagonal entry vanish when all diagonals vanish, contradicting the positive pair weights.",
    }
