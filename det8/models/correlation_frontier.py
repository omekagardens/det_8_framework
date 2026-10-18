"""DET v8.1 — TLM correlator projection and the scoped NPA endpoint.

The four TLM inequalities characterize the four bipartite binary correlators,
not arbitrary full behavior tables with specified marginal biases. They also
characterize the uniform-marginal slice. The historical is_quantum_masanes
callable remains a correlator-only predicate; it is not a general behavior
membership test. See https://arxiv.org/abs/quant-ph/0309137.

The B inequality is a cited separation of almost-quantum and tensor-quantum
behavior sets; its full witness is not reconstructed here. For bipartite
behaviors almost quantum is Q_{1+AB}, not ordinary Q1. All-level NPA word
consistency targets C_qc, not generally the tensor closure C_qa, and bare
pair-kernel marginal extension does not imply those operator-word relations.
See https://arxiv.org/abs/0803.4290, https://arxiv.org/abs/1403.4621 and
https://arxiv.org/abs/2001.04383. These imported results do not select DET QM.
"""

from __future__ import annotations

import math
import random

from det8.models.correlation_class import NoSignallingCorrelation, correlation_set_scope
from det8.models.validation import require_nonnegative_finite

# ── TLM / Masanes: the quantum correlator projection for (2,2,2) ────────────────────────


def tlm_sums(corr: NoSignallingCorrelation, tol: float = 1e-9) -> list[float]:
    """The four Tsirelson–Landau–Masanes sums (one minus sign each).

    x1=E00, x2=E01, x3=E10, x4=E11; Masanes' eq. (5) is the four double
    inequalities −π ≤ (±)asin x1 (±)asin x2 (±)asin x3 (±)asin x4 ≤ π with a
    single minus sign (equivalently the four |·| ≤ π below). Require a valid
    behavior and correlators in [-1,1]; invalid values are never clipped.
    """
    if not corr.validate(tol)["valid"]:
        raise ValueError("TLM sums require a valid finite nonnegative no-signalling behavior")
    e00, e01, e10, e11 = corr.correlations()
    if any(not math.isfinite(e) or abs(e) > 1 for e in (e00, e01, e10, e11)):
        raise ValueError("TLM correlators must lie in [-1, 1]")
    a = [math.asin(e) for e in (e00, e01, e10, e11)]
    return [
        -a[0] + a[1] + a[2] + a[3],
        a[0] - a[1] + a[2] + a[3],
        a[0] + a[1] - a[2] + a[3],
        a[0] + a[1] + a[2] - a[3],
    ]


def is_quantum_masanes(corr: NoSignallingCorrelation, tol: float = 1e-9) -> bool:
    """Historical alias: test the correlator projection, ignoring marginal biases.

    True does not establish quantum membership of an arbitrary behavior table.
    Use correlators_satisfy_tlm for an explicitly scoped name.
    """
    return correlators_satisfy_tlm(corr, tol=tol)


def tlm_margin(corr: NoSignallingCorrelation) -> float:
    """Correlator-projection margin; this does not test biased behavior membership."""
    return max(abs(s) for s in tlm_sums(corr)) - math.pi


# ── Quantum vector model (Tsirelson) for verification ───────────────────────


def quantum_vector_correlation(dim: int = 3,
                               seed: int = 0) -> NoSignallingCorrelation:
    """A quantum (2,2,2) correlation from unit vectors a0,a1,b0,b1 ∈ R^dim.

    E_xy = ⟨a_x, b_y⟩ (Tsirelson's theorem: exactly the quantum set for the
    correlation coefficients, with uniform marginals). Used to VERIFY the TLM
    inequalities hold for quantum correlations.
    """
    rng = random.Random(seed)

    def unit():
        v = [rng.gauss(0, 1) for _ in range(dim)]
        n = math.sqrt(sum(x * x for x in v))
        return [x / n for x in v]

    def dot(u, v):
        return sum(u[k] * v[k] for k in range(dim))

    a0, a1, b0, b1 = unit(), unit(), unit(), unit()
    e00, e01 = dot(a0, b0), dot(a0, b1)
    e10, e11 = dot(a1, b0), dot(a1, b1)
    # Uniform marginals: P(ab|xy) = (1 + s·E_xy)/4 with s=+1 iff a==b.
    M = [[0.0] * 4 for _ in range(4)]
    for x in (0, 1):
        for y in (0, 1):
            e = (e00, e01, e10, e11)[2 * x + y]
            for a in (0, 1):
                for b in (0, 1):
                    s = 1.0 if a == b else -1.0
                    M[2 * x + y][2 * a + b] = (1 + s * e) / 4.0
    return NoSignallingCorrelation(M)


def verify_tlm_necessary(n: int = 20000, dim: int = 3,
                         seed: int = 42) -> dict:
    """Monte-Carlo check that |TLM| ≤ π holds for quantum correlations.

    Samples the vector model (a subset of the full quantum set) and reports
    the maximum TLM margin — it should approach 0 (π) from below, never exceed.
    """
    rng = random.Random(seed)
    margin = -math.inf
    max_s = 0.0
    for _ in range(n):
        # inline vector sampling for speed
        def unit():
            v = [rng.gauss(0, 1) for _ in range(dim)]
            nm = math.sqrt(sum(x * x for x in v))
            return [x / nm for x in v]

        a0, a1, b0, b1 = unit(), unit(), unit(), unit()
        e = [sum(a0[k] * b0[k] for k in range(dim)),
             sum(a0[k] * b1[k] for k in range(dim)),
             sum(a1[k] * b0[k] for k in range(dim)),
             sum(a1[k] * b1[k] for k in range(dim))]
        A = [math.asin(x) for x in e]
        sums = [-A[0] + A[1] + A[2] + A[3],
                A[0] - A[1] + A[2] + A[3],
                A[0] + A[1] - A[2] + A[3],
                A[0] + A[1] + A[2] - A[3]]
        for s in sums:
            m = abs(s) - math.pi
            margin = max(margin, m)
            max_s = max(max_s, abs(s))
    return {
        "n_samples": n,
        "max_abs_tlm": max_s,
        "max_tlm_margin": margin,
        "tlm_holds": margin < 1e-6,
        "conclusion": (
            "The sampled supplied vector correlators satisfy the TLM bound. "
            "The samples illustrate the cited theorem; they do not prove necessity or tightness."
        ),
    }


# ── The B inequality (Navascués et al. 2015): Q ⊊ Q̃ ────────────────────────


_B_COEFFS = (-30 / 31, 167 / 9, 167 / 9, -30 / 31,
             -174 / 11, -244 / 23, 74 / 11, -174 / 11)


def b_inequality_vector(corr: NoSignallingCorrelation) -> list[float]:
    """The eight probabilities p̄ = (P_A(1|0), P_A(1|1), P_B(1|0), P_B(1|1),
    P(11|00), P(11|10), P(11|01), P(11|11)) for the B inequality."""
    return [
        corr.marginal_alice(0, 1),
        corr.marginal_alice(1, 1),
        corr.marginal_bob(0, 1),
        corr.marginal_bob(1, 1),
        corr.p(0, 0, 1, 1),
        corr.p(1, 0, 1, 1),
        corr.p(0, 1, 1, 1),
        corr.p(1, 1, 1, 1),
    ]


def b_inequality_value(corr: NoSignallingCorrelation) -> float:
    """B(p̄) = b̄ · p̄ with the Navascués–Guryanova–Hoban–Acín coefficients."""
    p = b_inequality_vector(corr)
    return sum(b * pi for b, pi in zip(_B_COEFFS, p))


def b_inequality_data() -> dict:
    """The sourced separation result: quantum bound and almost-quantum violation."""
    return {
        "coefficients": list(_B_COEFFS),
        "quantum_bound": -1.0,
        "quantum_bound_statement": "B(p̄) > −1 for every quantum p̄ ∈ Q",
        "almost_quantum_violation": -1.052,
        "almost_quantum_statement": "an almost-quantum point achieves B ≈ −1.052 < −1",
        "conclusion": "Q ⊊ Q̃: the Q_{1+AB} (almost-quantum) relaxation strictly "
                      "over-approximates the quantum set, witnessed by B.",
        "chsh_cannot_separate": (
            "CHSH saturates 2√2 in both Q and Q̃, so a non-facet inequality "
            "(B) is required to separate them."
        ),
        "source": "Navascués, Guryanova, Hoban, Acín, Nat. Commun. 6:6288 (2015); arXiv:1403.4621",
    }


# ── NPA hierarchy: the commuting-operator endpoint ────────────────────────────────


def npa_convergence_statement() -> dict:
    return {
        "almost_quantum": "Qtilde = Q_1+AB for bipartite behaviors; this is not ordinary Q1",
        "quantum": "Intersection of the complete NPA hierarchy is C_qc (commuting operators)",
        "global_record_extendability": "Bare D marginals and NPA operator-word consistency are different conditions",
        "theorem": "All-level NPA feasibility with the specified measurement word relations characterizes C_qc",
        "remaining_open_question": (
            "A DET principle would have to justify the operational word relations "
            "and its intended tensor-product or commuting endpoint. Bare marginals do not do so."
        ),
        "scope": correlation_set_scope(),
    }


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    return {
        "theorem": "T6 frontier — correlator projection and cited commuting-operator reconstruction",
        "deliverables": {
            "TLM correlator projection": "MATH — Masanes (quant-ph/0309137), cited",
            "almost-quantum/tensor-quantum B separation": "MATH — Navascués et al. (2015), cited",
            "NPA limit C_qc under word relations": "MATH — Navascués–Pironio–Acín (2008), cited",
            "sampled vector-model TLM checks": "CORR — finite numerical examples",
        },
        "scope": {**correlation_set_scope(), "tlm_full_behavior_membership_test": False},
        "not_derived_here": [
            "the B inequality's full almost-quantum witness and analytic certificate",
            "arbitrary biased behavior membership or a general NPA solver",
            "a DET-native forcing of NPA relations or tensor-product quantum structure",
        ],
        "status": "CORRELATOR_PROJECTION_AND_IMPORTED_THEOREM; DET_QM_NOT_DERIVED",
    }


# ── End-to-end ──────────────────────────────────────────────────────────────


def run_t6_frontier() -> dict:
    from det8.models.correlation_class import (
        bell_state_correlation,
        pr_box,
    )

    bell = bell_state_correlation()
    pr = pr_box()

    verify = verify_tlm_necessary(n=20000, dim=3, seed=42)
    bdata = b_inequality_data()
    npa = npa_convergence_statement()

    return {
        "TLM": {
            "scope": "four-correlator projection; examples have uniform marginals",
            "full_behavior_membership_test": False,
            "bell_margin": tlm_margin(bell),
            "bell_is_quantum": is_quantum_masanes(bell),
            "pr_box_margin": tlm_margin(pr),
            "pr_box_is_quantum": is_quantum_masanes(pr),
        },
        "tlm_verification": verify,
        "b_inequality": bdata,
        "b_values": {
            "bell": b_inequality_value(bell),
            "pr_box": b_inequality_value(pr),
        },
        "npa_convergence": npa,
        "certificate": derivation_certificate(),
        "interpretation": (
            "The Bell state satisfies TLM (margin 0, quantum); the PR box "
            "violates it (margin +π, not quantum). The TLM/Masanes inequalities "
            "characterize the correlator projection, not arbitrary marginal biases. "
            "The B separation is cited, not reconstructed. All-level NPA with "
            "operator-word relations targets C_qc; bare record marginal extensions "
            "neither enforce these relations nor select tensor-product QM."
        ),
    }


def correlators_satisfy_tlm(corr: NoSignallingCorrelation, tol: float = 1e-9) -> bool:
    """Reject invalid behaviors, then test their correlators, ignoring biases."""
    tol = require_nonnegative_finite(tol, "tol")
    if not corr.validate(tol)["valid"]:
        return False
    if any(not math.isfinite(e) or abs(e) > 1 for e in corr.correlations()):
        return False
    return all(abs(value) <= math.pi + tol for value in tlm_sums(corr, tol=tol))
