"""DET — Born-rule consistency under L2 normalization (p = 2), honestly stated.

`born_derivation.py` derives P = |c|² from kernel-root composition but leaves
"why squared, not |c|⁴ or |c|¹" in its *still-assumed* list.  This module shows
a *consistency* result, not a derivation from first principles:

    Among power rules P(c) = |c|^p, p = 2 is the unique rule that conserves
    total probability under an **L2-normalized** symmetric split
    (c_i = 1/√n):  Σ_i |c_i|^p = n·(1/√n)^p = n^(1 − p/2) = 1 only for p = 2.

**The circularity (red-team R2-2), stated plainly:** the split c_i = 1/√n is
itself the L2 (Born) normalization.  Under the matching Lp-normalized split
c_i = 1/n^(1/p), total probability is Σ_i |c_i|^p = n·(1/n) = 1 for **every**
p.  So conservation singles out p = 2 only *conditional on the L2 convention* —
the premise already encodes the Born rule for the uniform case.

This is therefore a **consistency check**: the Born rule is self-consistent
with L2 amplitude composition.  The genuine open questions — why L2 rather than
Lp, and why amplitudes compose linearly at all — are NOT addressed here.
"""

from __future__ import annotations

import math


def power_rule_probability(magnitude: float, p: float) -> float:
    """P(c) = |c|^p for a kernel root of the given magnitude."""

    if magnitude < 0.0:
        raise ValueError("magnitude cannot be negative")
    return magnitude**p


def symmetric_split_total_probability(p: float, n: int) -> float:
    """Σ_i |c_i|^p for an **L2-normalized** n-way split (c_i = 1/√n)."""

    if n < 1:
        raise ValueError("split count must be positive")
    return n * (1.0 / math.sqrt(n)) ** p


def lp_normalized_split_total_probability(p: float, n: int) -> float:
    """Σ_i |c_i|^p for an **Lp-normalized** n-way split (c_i = 1/n^(1/p)).

    This is the counter-argument to the p = 2 "uniqueness": with the matching
    Lp normalization, probability is conserved for every p.
    """

    if n < 1 or p <= 0.0:
        raise ValueError("split count must be positive and p positive")
    return n * (1.0 / n ** (1.0 / p)) ** p


def conservation_residual(p: float, n: int) -> float:
    """|n^(1 − p/2) − 1| under L2-normalized splits."""

    return abs(symmetric_split_total_probability(p, n) - 1.0)


def uniqueness_scan() -> dict:
    """Scan power rules under L2-normalized splits; p = 2 is the sole match.

    This is a CONSISTENCY check, not a derivation: the L2 split is the Born
    convention, so the scan demonstrates self-consistency, not uniqueness.
    """

    candidates = (1.0, 2.0, 3.0, 4.0)
    residuals = {
        p: max(conservation_residual(p, n) for n in (2, 3, 4))
        for p in candidates
    }
    conserving = [p for p, residual in residuals.items() if residual < 1e-12]
    lp_conserved_for_all = [
        p
        for p in candidates
        if abs(lp_normalized_split_total_probability(p, 3) - 1.0) < 1e-12
    ]
    return {
        "candidate_powers": candidates,
        "max_conservation_residual_L2_split": residuals,
        "conserving_under_L2_split": conserving,
        "lp_split_conserves_for_all_p": lp_conserved_for_all == list(candidates),
        "interpretation": (
            "p = 2 is the unique power rule conserving probability under the "
            "L2-normalized split, and Lp-normalized splits conserve for every p. "
            "So the 'uniqueness' is conditional on the L2 convention — a "
            "consistency check, not a derivation."
        ),
    }


def born_rule_uniqueness_theorem() -> dict:
    """Statement of the consistency result, with the circularity flagged."""

    return {
        "result": (
            "p = 2 is the unique power rule consistent with L2-normalized "
            "amplitude composition (c_i = 1/√n)."
        ),
        "argument": (
            "Σ_i |c_i|^p = n·(1/√n)^p = n^(1 − p/2); conservation ⇒ p = 2."
        ),
        "circularity": (
            "the L2-normalized split c_i = 1/√n already assumes the Born rule for "
            "the uniform case. Under Lp-normalized splits, conservation holds for "
            "every p (Σ_i |1/n^(1/p)|^p = n·(1/n) = 1)."
        ),
        "honest_classification": (
            "CONSISTENCY CHECK, not a derivation. It does not force L2 over Lp, "
            "nor linear amplitude composition."
        ),
        "provenance": {
            "conservation under L2 split": "MATH — arithmetic",
            "Lp split conserves for all p": "MATH — arithmetic",
            "L2 normalization is the Born convention": "MATH — definition",
        },
        "what_this_closes": (
            "born_derivation.py 'still-assumed' item, WEAKLY: only that the Born "
            "rule is self-consistent with L2 composition — not why L2."
        ),
        "what_remains_open": [
            "why L2 rather than Lp (this is the real 'why squared' question)",
            "linear root composition (assumed to follow from sequential-measurement consistency)",
            "unitary vs orthogonal basis change (why_complex.py handles the complex part)",
        ],
    }


def grade2_born_connection() -> dict:
    """Tie the L2-consistency result to grade-2 and the three-slit null.

    Note: this connection does NOT rescue the "uniqueness" — grade-2 selects the
    L2 structure empirically (three-slit I₃ = 0), so the Born rule's L2 form is
    empirically anchored to grade-2, but the *norm convention* is still assumed,
    not derived.
    """

    return {
        "claim": "p = 2 is the L2 form, which is the grade-2 (Sorkin) measure.",
        "reason": (
            "a grade-2 measure is bi-additive in kernel roots (I₃ = 0); the "
            "squared magnitude |Σ c_i|² is precisely that bi-additive form."
        ),
        "empirical_anchor": (
            "the three-slit experiments bound I₃ ≈ 0 (κ_Sorkin ≲ 10⁻⁴), confirming "
            "grade-2; so the L2 (Born) form is the empirically selected grade-2 "
            "measure — but the norm convention (L2 vs Lp) is still assumed, not derived."
        ),
        "links": {
            "born_derivation.py": "kernel-root composition",
            "dkappa_decoherence.py": "I₃ = κ·w₃ and the grade-2 theorem",
            "why_complex.py": "ℂ forced by reversibility (complements this)",
        },
    }
