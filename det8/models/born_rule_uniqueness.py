"""DET — Born-rule uniqueness (why the squared magnitude, not another power).

`born_derivation.py` derives P = |c|² from kernel-root composition but leaves
"why squared, not |c|⁴ or |c|¹" in its *still-assumed* list.  This module closes
that gap: among scale-free rules P(c) = |c|^p, only **p = 2** conserves total
probability under the linear basis transformations that correctly compose
nonfactorizable records.

Theorem (MATH): start from a single kernel root c = 1 and split it symmetrically
into n roots c_i = 1/√n.  Total probability under P(c) = |c|^p is

    Σ_i |c_i|^p = n · (1/√n)^p = n^(1 − p/2).

Conservation (total must stay 1) forces 1 − p/2 = 0, i.e. **p = 2**, for every
n ≥ 2.  So the squared magnitude is the *unique* power rule consistent with a
probability assignment that is conserved under basis change.

Synthesis: p = 2 is exactly the grade-2 (Sorkin) measure — the class with no
third-order interference.  The three-slit null (I₃ = 0) empirically confirms
grade-2, so the Born rule is the *empirically anchored* unique grade-2
probability rule, tying this result to the D_κ program.

Honest boundary: uniqueness holds within the power-law class and the grade-2
class.  It does not yet force *linear* root composition or *unitary* (rather
than orthogonal) transformations; those remain the open front (the latter is
`why_complex.py`).
"""

from __future__ import annotations

import math


def power_rule_probability(magnitude: float, p: float) -> float:
    """P(c) = |c|^p for a kernel root of the given magnitude."""

    if magnitude < 0.0:
        raise ValueError("magnitude cannot be negative")
    return magnitude**p


def symmetric_split_total_probability(p: float, n: int) -> float:
    """Σ_i |c_i|^p for an n-way symmetric split of a unit root."""

    if n < 1:
        raise ValueError("split count must be positive")
    return n * (1.0 / math.sqrt(n)) ** p


def conservation_residual(p: float, n: int) -> float:
    """|n^(1 − p/2) − 1| — how far the power rule misses conservation."""

    return abs(symmetric_split_total_probability(p, n) - 1.0)


def uniqueness_scan() -> dict:
    """Scan candidate power rules and show only p = 2 conserves probability."""

    candidates = (1.0, 2.0, 3.0, 4.0)
    residuals = {
        p: max(conservation_residual(p, n) for n in (2, 3, 4))
        for p in candidates
    }
    conserving = [p for p, residual in residuals.items() if residual < 1e-12]
    return {
        "candidate_powers": candidates,
        "max_conservation_residual": residuals,
        "conserving_powers": conserving,
        "p_equals_2_is_unique": conserving == [2.0],
    }


def born_rule_uniqueness_theorem() -> dict:
    """Statement of the uniqueness result with provenance."""

    return {
        "theorem": (
            "among P(c) = |c|^p, only p = 2 conserves total probability under "
            "symmetric basis splits, for every n ≥ 2"
        ),
        "argument": (
            "Σ_i |c_i|^p = n·(1/√n)^p = n^(1 − p/2); conservation ⇒ 1 − p/2 = 0 ⇒ p = 2"
        ),
        "provenance": {
            "symmetric-split conservation": "MATH — probability normalization",
            "P(c) = |c|^p power-law class": "MATH — scale-free rotation-invariant rules",
            "uniqueness within the class": "MATH — algebra",
        },
        "what_this_closes": (
            "born_derivation.py 'still-assumed' item: the squared-magnitude form "
            "is now unique, not assumed"
        ),
        "what_remains_open": [
            "linear root composition (assumed to follow from sequential-measurement consistency)",
            "unitary vs orthogonal basis change (why_complex.py handles the complex part)",
        ],
    }


def grade2_born_connection() -> dict:
    """Tie Born-rule uniqueness (p = 2) to grade-2 and the three-slit null."""

    return {
        "claim": "p = 2 is exactly the grade-2 (Sorkin) measure.",
        "reason": (
            "A grade-2 measure is bi-additive in kernel roots, i.e. its third-order "
            "interference I₃ vanishes; the squared magnitude |Σ c_i|² is precisely "
            "that bi-additive form."
        ),
        "empirical_anchor": (
            "the three-slit experiments bound I₃ ≈ 0 (κ_Sorkin ≲ 10⁻⁴), confirming "
            "grade-2; therefore the Born rule is the empirically anchored unique "
            "grade-2 probability rule."
        ),
        "links": {
            "born_derivation.py": "kernel-root composition",
            "dkappa_decoherence.py": "I₃ = κ·w₃ and the grade-2 theorem",
            "why_complex.py": "ℂ forced by reversibility (complements this)",
        },
    }
