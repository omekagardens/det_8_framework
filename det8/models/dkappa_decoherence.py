"""DET — κ-dependent decoherence functional D_κ (the first "push").

The lens's first concrete novelty target: deform Sorkin's grade-2 decoherence
functional 𝔇 by a history-carrying record term of strength κ (the
structural-history coordinate).  On a finite alternative space Ω,

    μ_κ(A) = (1 − κ) · μ₂(A) + κ · μ₃(A),

where μ₂(A) = 𝔇(A,A) is a grade-2 pair-kernel (third-order interference
I₃ = 0) and μ₃ is a normalized grade-3 "record" measure carrying a single
nonzero triple weight r.  Because I₃ is linear in the measure and vanishes on
the grade-2 part,

    I₃(μ_κ) = κ · r   (for the record triple),

so the three-slit bound |I₃| < ε is a direct bound κ < ε/r.  This is the
anchor: a κ ≠ 0 coupling would show up as grade-3 three-slit interference.

Well-definedness (from the grade hierarchy): both μ₂ and μ₃ are non-negative
and normalized, so μ_κ is non-negative and normalized for every κ ∈ [0,1].

Provenance:
  grade-2 pair-kernel μ₂       MATH — Sorkin decoherence functional (credited).
  grade-3 record measure μ₃    MATH — Sorkin grade-3 measure (credited).
  the κ-weighted coupling      TH-DET — the DET-specific hypothesis (novel).
  I₃(μ_κ) = κ·r                MATH — linearity of I₃ in the measure.

This module registers a *mechanism*, not a novel effect: the existing
three-slit null (I₃ ≈ 0) already bounds κ, and does not falsify the lens.
"""

from __future__ import annotations

from dataclasses import dataclass

from det8.models.pair_kernel import PairKernel, make_pair_kernel


def _as_frozenset(event) -> frozenset:
    if isinstance(event, frozenset):
        return event
    return frozenset(event)


@dataclass(frozen=True)
class Dkappa:
    """κ-deformed decoherence functional μ_κ = (1−κ)μ₂ + κμ₃.

    ``pair_kernel`` supplies the grade-2 part μ₂ = 𝔇(·,·); ``record_triple``
    names the three events that carry the grade-3 record weight
    ``triple_weight`` = r; ``kappa`` is the coupling strength.
    """

    pair_kernel: PairKernel
    record_triple: frozenset
    triple_weight: float
    kappa: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.kappa <= 1.0:
            raise ValueError("kappa must lie in [0,1]")
        if not 0.0 <= self.triple_weight <= 1.0:
            raise ValueError("triple weight must lie in [0,1]")
        if len(self.record_triple) != 3:
            raise ValueError("record triple must contain exactly three events")
        if not self.record_triple <= self.pair_kernel.omega():
            raise ValueError("record triple must lie within the alternative space")

    def grade2_mu(self, A) -> float:
        return self.pair_kernel.mu(A)

    def grade3_mu(self, A) -> float:
        """Normalized grade-3 record measure: singles + one triple weight r."""
        A = _as_frozenset(A)
        n = self.pair_kernel.n
        r = self.triple_weight
        return len(A) * (1.0 - r) / n + (r if self.record_triple <= A else 0.0)

    def mu(self, A) -> float:
        return (1.0 - self.kappa) * self.grade2_mu(A) + self.kappa * self.grade3_mu(A)

    def interference_I3(self, A, B, C) -> float:
        A, B, C = map(_as_frozenset, (A, B, C))
        return (
            self.mu(A | B | C) - self.mu(A | B) - self.mu(A | C)
            - self.mu(B | C) + self.mu(A) + self.mu(B) + self.mu(C)
        )

    def normalize_check(self, tol: float = 1e-9) -> bool:
        return abs(self.mu(self.pair_kernel.omega()) - 1.0) < tol

    def positivity_check(self, tol: float = 1e-9) -> dict:
        minimum = 0.0
        for mask in range(1 << self.pair_kernel.n):
            event = frozenset(
                i for i in range(self.pair_kernel.n) if mask >> i & 1
            )
            minimum = min(minimum, self.mu(event))
        return {"min_mu": minimum, "positive": minimum >= -tol}


def record_interference_I3(dk: Dkappa) -> float:
    """I₃({a},{b},{c}) for the record triple — equals κ · triple_weight."""

    a, b, c = sorted(dk.record_triple)
    return dk.interference_I3({a}, {b}, {c})


def three_slit_kappa_bound(epsilon: float, triple_weight: float) -> float:
    """Given a measured |I₃| < ε, the implied κ bound is ε / r."""

    if not epsilon > 0.0:
        raise ValueError("epsilon must be positive")
    if not triple_weight > 0.0:
        raise ValueError("triple weight must be positive")
    return epsilon / triple_weight


def make_dkappa(
    kappa: float, n: int = 4, triple_weight: float = 0.1, seed: int = 42
) -> Dkappa:
    """Build a κ-deformed functional on the record triple (0, 1, 2)."""

    if n < 3:
        raise ValueError("need at least three events for a record triple")
    pair = make_pair_kernel(n, seed=seed, coherent=True)
    return Dkappa(pair, frozenset((0, 1, 2)), triple_weight, kappa)


def derivation_certificate() -> dict:
    """Provenance of each D_κ deliverable (honest classification)."""

    return {
        "theorem": "D_κ — κ-dependent decoherence functional (the first push)",
        "deliverables": {
            "grade-2 pair-kernel μ₂": "MATH — Sorkin decoherence functional / quantum measure theory (credited)",
            "grade-3 record measure μ₃": "MATH — Sorkin grade-3 measure (credited)",
            "κ-weighted coupling μ_κ = (1−κ)μ₂ + κμ₃": "TH-DET — the DET-specific hypothesis (novel)",
            "I₃(μ_κ) = κ·r": "MATH — linearity of third-order interference in the measure",
            "positivity + normalization of μ_κ": "MATH — convex combination of normalized non-negative measures",
            "three-slit anchor |I₃| < ε ⇒ κ < ε/r": "MATH — direct inversion of the bound",
        },
        "not_derived_here": [
            "that κ ≠ 0 — the coupling is a hypothesis, not a derivation",
            "that the record term is grade-3 (not another form) — a modeling choice",
            "the sign or shape of the history-carrying term — one concrete ansatz",
        ],
        "status": (
            "formalized mechanism; the existing three-slit null already bounds κ. "
            "Registered in the Novelty Ledger."
        ),
    }


def run_dkappa(
    kappa: float = 0.1, n: int = 4, triple_weight: float = 0.1, seed: int = 42
) -> dict:
    """Demonstrate D_κ: I₃ = κ·r, the κ=0 limit, and the three-slit κ bound."""

    dk = make_dkappa(kappa, n, triple_weight, seed)
    dk_zero = make_dkappa(0.0, n, triple_weight, seed)
    i3 = record_interference_I3(dk)
    i3_zero = record_interference_I3(dk_zero)
    epsilon = 0.01  # illustrative three-slit precision on I₃
    bound = three_slit_kappa_bound(epsilon, triple_weight)

    return {
        "kappa": kappa,
        "triple_weight": triple_weight,
        "record_triple": sorted(dk.record_triple),
        "normalized": dk.normalize_check(),
        "positivity": dk.positivity_check(),
        "I3_at_kappa": i3,
        "I3_at_kappa_zero": i3_zero,
        "I3_equals_kappa_times_r": abs(i3 - kappa * triple_weight) < 1e-12,
        "three_slit_epsilon": epsilon,
        "kappa_bound_from_three_slit": bound,
        "certificate": derivation_certificate(),
        "interpretation": (
            f"I₃ = {i3:.6f} at κ = {kappa} (grade-3), "
            f"I₃ = {i3_zero:.1e} at κ = 0 (grade-2). "
            f"A three-slit null |I₃| < {epsilon} bounds κ < {bound:.4f}."
        ),
    }
