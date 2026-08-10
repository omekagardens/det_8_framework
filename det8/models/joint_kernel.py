"""
DET 8 Nonfactorizable Joint Kernel — Bell Correlation Sketch

Implements a DET-native approach to Bell correlations using a
nonfactorizable joint relational kernel. This is a SKETCH, not a
completed model — it demonstrates the architecture, not the derivation.

Key DET claims:
1. The entangled pair is a single relational record spanning both nodes.
2. The law map generates Ω_AB (joint outcomes) from the complete
   relational record, not from separate local records.
3. The joint kernel K((A,B) | R, a, b) is NOT factorizable into
   K_A(A|R,a) · K_B(B|R,b).
4. No-signalling is preserved: marginals don't depend on remote settings.
5. Measurement Independence is preserved: settings a,b are free inputs
   to the law map, not correlated with any hidden λ.

This sketch uses standard QM correlations as the "target" that a
DET-native kernel must reproduce. The actual DET-native derivation
(why K takes this specific form) remains an open problem (O4).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable


# ── Relational Record ──────────────────────────────────────────────────────


@dataclass
class RelationalRecord:
    """A relational record spanning two spacelike-separated nodes.

    This is NOT two independent local records. It is a single
    nonfactorizable object that constrains joint outcomes.

    For the Bell state |Φ⁺⟩, the record encodes:
    - Perfect correlation in the Z basis.
    - Anticorrelation in the X basis? No, for |Φ⁺⟩:
      ⟨Φ⁺|σ_x⊗σ_x|Φ⁺⟩ = +1 (correlated in X too for this state).
    """

    # For a two-qubit system, the relational record contains the
    # state amplitudes or equivalent constraint structure.
    # Here we use a simple parameterization.
    correlation_strength: float = 1.0  # 1.0 = maximally entangled.


# ── Joint Kernel ────────────────────────────────────────────────────────────


def nonfactorizable_joint_kernel(
    record: RelationalRecord,
    angle_a: float,
    angle_b: float,
    outcome_a: int,
    outcome_b: int,
) -> float:
    """DET joint kernel: K((A,B) | R, a, b).

    This kernel CANNOT be decomposed into K_A(A|R,a) · K_B(B|R,b).
    It is fundamentally a joint distribution over the outcome pair.

    For this sketch, we use the standard QM correlation function
    as a placeholder for the DET-native law map.

    K(A,B | a,b) = (1 + A·B·E(a,b)) / 4
    where E(a,b) = cos(2(a-b)) for |Φ⁺⟩.

    This satisfies:
    - Σ_{A,B} K(A,B) = 1 (normalization).
    - K(A,B) ≥ 0 (non-negativity).
    - Σ_B K(A,B) = 1/2 for each A (correct marginals, no-signalling).
    - NOT factorizable: K(A,B) ≠ K_A(A) · K_B(B) when E ≠ 0.
    """
    E = record.correlation_strength * math.cos(2 * (angle_a - angle_b))
    return (1 + outcome_a * outcome_b * E) / 4.0


def joint_kernel_marginal_a(
    record: RelationalRecord,
    angle_a: float,
    angle_b: float,
    outcome_a: int,
) -> float:
    """Marginal probability P(A|a,b) = Σ_B K(A,B|a,b).

    For the nonfactorizable kernel with E(a,b) = cos(2(a-b)):
    P(A=+1|a,b) = K(+1,+1) + K(+1,-1) = 1/2.
    P(A=-1|a,b) = 1/2.

    The marginal is independent of b (no-signalling).
    """
    return sum(
        nonfactorizable_joint_kernel(record, angle_a, angle_b, outcome_a, b_outcome)
        for b_outcome in [+1, -1]
    )


# ── Factorizability Check ──────────────────────────────────────────────────


def check_factorizability(
    record: RelationalRecord,
    angle_a: float,
    angle_b: float,
) -> dict:
    """Check whether the joint kernel factorizes for given settings.

    Factorizability requires: K(A,B) = K_A(A) · K_B(B) for all A,B.

    Returns the maximum deviation from factorizability.
    """
    max_deviation = 0.0
    failures = []

    for a_out in [+1, -1]:
        p_a = joint_kernel_marginal_a(record, angle_a, angle_b, a_out)

        for b_out in [+1, -1]:
            # Compute P(B|a,b) = Σ_A K(A,B|a,b).
            p_b = sum(
                nonfactorizable_joint_kernel(record, angle_a, angle_b, a_in, b_out)
                for a_in in [+1, -1]
            )

            joint = nonfactorizable_joint_kernel(
                record, angle_a, angle_b, a_out, b_out
            )
            product = p_a * p_b
            deviation = abs(joint - product)

            if deviation > max_deviation:
                max_deviation = deviation

            if deviation > 1e-12:
                failures.append(
                    {
                        "outcomes": (a_out, b_out),
                        "joint": joint,
                        "product": product,
                        "deviation": deviation,
                    }
                )

    return {
        "factorizable": max_deviation < 1e-12,
        "max_deviation": max_deviation,
        "n_failures": len(failures),
        "sample_failure": failures[0] if failures else None,
    }


# ── No-Signalling Verification ──────────────────────────────────────────────


def verify_no_signalling(
    record: RelationalRecord,
    angle_a: float,
    angle_b1: float,
    angle_b2: float,
) -> dict:
    """Verify that P(A|a,b1) = P(A|a,b2) for all A.

    This is the operational no-signalling condition: Bob's setting
    does not affect Alice's marginal distribution.
    """
    results = {}
    for a_out in [+1, -1]:
        p_b1 = joint_kernel_marginal_a(record, angle_a, angle_b1, a_out)
        p_b2 = joint_kernel_marginal_a(record, angle_a, angle_b2, a_out)

        results[a_out] = {
            "P(A|b1)": p_b1,
            "P(A|b2)": p_b2,
            "equal": abs(p_b1 - p_b2) < 1e-12,
        }

    return {
        "no_signalling": all(r["equal"] for r in results.values()),
        "details": results,
    }


# ── CHSH from Joint Kernel ─────────────────────────────────────────────────


def chsh_from_joint_kernel(
    record: RelationalRecord,
    a: float = 0.0,
    a_prime: float = math.pi / 4,
    b: float = math.pi / 8,
    b_prime: float = 3 * math.pi / 8,
) -> dict:
    """Compute CHSH S from the nonfactorizable joint kernel.

    E(a,b) = Σ_{A,B} A·B·K(A,B|a,b).

    Then S = E(a,b) - E(a,b') + E(a',b) + E(a',b').
    """
    def correlation(angle_a: float, angle_b: float) -> float:
        e = 0.0
        for a_out in [+1, -1]:
            for b_out in [+1, -1]:
                k = nonfactorizable_joint_kernel(
                    record, angle_a, angle_b, a_out, b_out
                )
                e += a_out * b_out * k
        return e

    E_ab = correlation(a, b)
    E_abp = correlation(a, b_prime)
    E_apb = correlation(a_prime, b)
    E_apbp = correlation(a_prime, b_prime)

    S = E_ab - E_abp + E_apb + E_apbp

    return {
        "E(a,b)": E_ab,
        "E(a,b')": E_abp,
        "E(a',b)": E_apb,
        "E(a',b')": E_apbp,
        "S": S,
        "S_target": 2 * math.sqrt(2),
        "violates_CHSH": abs(S) > 2.0,
        "close_to_target": abs(abs(S) - 2 * math.sqrt(2)) < 1e-10,
    }


# ── DET-Native Architecture (Not Just QM Borrowing) ─────────────────────────


def det_native_joint_kernel_sketch() -> dict:
    """Describe the DET-native architecture for the joint kernel.

    This documents what a DET-native derivation would need to supply,
    as opposed to the current QM-borrowed placeholder.
    """
    return {
        "architecture": {
            "step_1": "Law map L generates joint Ω_AB from relational record R_AB.",
            "step_2": "Ω_AB contains (A,B) pairs satisfying relational constraints.",
            "step_3": "K((A,B)|R_AB,a,b) is normalized over Ω_AB.",
            "step_4": "K is NOT factorizable: it is a primitive joint distribution.",
            "step_5": "No-signalling: marginals don't depend on remote settings (structural).",
            "step_6": "CHSH violation emerges from nonfactorizability + relational constraints.",
        },
        "what_is_borrowed": [
            "The specific functional form E(a,b) = cos(2(a-b)) is standard QM.",
            "The Born rule conversion from amplitudes to probabilities.",
            "The Hilbert space structure underlying the Bell state.",
        ],
        "what_det_must_supply": [
            "A DET-native law map that generates the joint Ω_AB from record structure.",
            "A DET-native kernel K that does not presuppose QM amplitudes.",
            "A derivation of the specific correlation function from relational constraints.",
            "A demonstration that the joint kernel is primitive (not composed from local kernels).",
            "A proof that no-signalling is structural, not fine-tuned.",
        ],
        "open_blocker": "O4: Formal nonfactorizable joint kernel compatible with no-signalling, MI, and covariance.",
    }
