"""
CHSH Correspondence Harness — Standard Quantum Mechanics

Implements the standard CHSH inequality test using quantum mechanical
predictions. This is a correspondence model: it reproduces the expected
QM result |S| = 2√2 for a maximally entangled Bell state with optimal
measurement settings. It does NOT attempt a DET-native derivation.

The CHSH inequality:
    S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
where |S| ≤ 2 for any local hidden variable theory.

Quantum mechanics with a Bell state and optimal angles:
    a=0°, a'=45°, b=22.5°, b'=67.5°
yields S = 2√2 ≈ 2.828.

Purpose: Establish quantum compatibility baseline before any DET-native
derivation attempt (per P0.4r1.1 execution order: step 7 before step 8).
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Optional


# ── Bell State ─────────────────────────────────────────────────────────────


@dataclass
class BellState:
    """The Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2."""

    def correlation(self, angle_a: float, angle_b: float) -> float:
        """Quantum correlation E(a,b) = ⟨Φ⁺| (σ_a ⊗ σ_b) |Φ⁺⟩.

        For the Bell state |Φ⁺⟩, E(a,b) = cos(2(a - b)).
        (Note: this uses the standard convention where σ_a = cos(2a)σ_z + sin(2a)σ_x,
        so that the optimal CHSH angles are 0°, 45°, 22.5°, 67.5°.)

        Actually, the standard convention uses the angle directly:
        E(a,b) = -cos(2(a-b)) for the singlet state |Ψ⁻⟩.
        For |Φ⁺⟩ with σ_z ⊗ σ_z measurement at angle 0, we get E = cos(2(a-b))... 

        Let me use the standard result: for any maximally entangled state,
        with appropriately chosen measurement bases, E(a,b) = -cos(2(a-b))
        for the singlet, or E(a,b) = cos(2(a-b)) for |Φ⁺⟩ when using
        σ_θ = cos(2θ)σ_z + sin(2θ)σ_x.

        For CHSH with |Φ⁺⟩: optimal angles are a=0, a'=π/4, b=π/8, b'=3π/8,
        giving S = 2√2.

        Actually let me use the simpler convention:
        Measurement at angle θ measures σ_θ = cos(θ)σ_z + sin(θ)σ_x.
        Then for |Φ⁺⟩: E(a,b) = cos(a-b) for the specific measurement implementation.
        
        Let me just compute it directly from the state.
        """
        # For |Φ⁺⟩ and measurements σ_a ⊗ σ_b where σ_θ = cos(θ)σ_z + sin(θ)σ_x,
        # E(a,b) = cos(a)cos(b) + sin(a)sin(b) = cos(a-b) when the state is |Φ⁺⟩.
        # (The exact form depends on convention; what matters is that the
        # optimal CHSH value is 2√2.)
        return math.cos(2 * (angle_a - angle_b))

    def joint_probability(
        self, angle_a: float, angle_b: float, outcome_a: int, outcome_b: int
    ) -> float:
        """P(A=a, B=b | angles) for a ∈ {+1,-1}, b ∈ {+1,-1}.

        P(a,b) = (1 + a·b·E(a,b)) / 4 where a,b ∈ {+1,-1}.

        Wait, the correct formula for the singlet is:
        P(a,b) = (1 - a·b·cos(2(α-β))) / 4.
        For |Φ⁺⟩ it would be:
        P(a,b) = (1 + a·b·cos(2(α-β))) / 4.

        Actually, let me just use the standard QM formula:
        P(a,b) = (1 + a·b·E(a,b)) / 4, where E = correlation.

        For the specific measurement implementation used here:
        """
        E = self.correlation(angle_a, angle_b)
        return (1 + outcome_a * outcome_b * E) / 4.0


# ── CHSH Calculation ───────────────────────────────────────────────────────


def compute_chsh_S(
    a: float, a_prime: float, b: float, b_prime: float
) -> dict:
    """Compute the CHSH S value for a Bell state with given angles.

    S = E(a,b) - E(a,b') + E(a',b) + E(a',b')

    Returns the S value and whether it violates the CHSH inequality (|S| > 2).
    """
    bell = BellState()

    E_ab = bell.correlation(a, b)
    E_abp = bell.correlation(a, b_prime)
    E_apb = bell.correlation(a_prime, b)
    E_apbp = bell.correlation(a_prime, b_prime)

    S = E_ab - E_abp + E_apb + E_apbp

    return {
        "angles": {"a": a, "a'": a_prime, "b": b, "b'": b_prime},
        "correlations": {
            "E(a,b)": E_ab,
            "E(a,b')": E_abp,
            "E(a',b)": E_apb,
            "E(a',b')": E_apbp,
        },
        "S": S,
        "CHSH_bound": 2.0,
        "QM_maximum": 2 * math.sqrt(2),
        "violates_CHSH": abs(S) > 2.0,
        "close_to_QM_max": abs(abs(S) - 2 * math.sqrt(2)) < 1e-10,
    }


def optimal_chsh() -> dict:
    """Compute CHSH with optimal angles for maximal violation.

    For |Φ⁺⟩ with σ_θ = cos(2θ)σ_z + sin(2θ)σ_x:
    Optimal: a=0, a'=π/4, b=π/8, b'=3π/8
    (These are doubled from the usual singlet angles because of the state convention.)
    
    Actually, for the correlation function E(a,b) = cos(2(a-b)),
    the optimal angles satisfy:
    a=0, a'=π/4, b=π/8, b'=3π/8
    E(0,π/8) = cos(-π/4) = 1/√2
    E(0,3π/8) = cos(-3π/4) = -1/√2
    E(π/4,π/8) = cos(π/4) = 1/√2
    E(π/4,3π/8) = cos(-π/4) = 1/√2
    S = 1/√2 - (-1/√2) + 1/√2 + 1/√2 = 4/√2 = 2√2 ≈ 2.828.
    
    Wait, let me recompute:
    E(0,π/8) = cos(-π/4) = 1/√2
    E(0,3π/8) = cos(-3π/4) = -1/√2
    E(π/4,π/8) = cos(π/4) = 1/√2
    E(π/4,3π/8) = cos(-π/4) = 1/√2
    S = 1/√2 + 1/√2 + 1/√2 + 1/√2 = 4/√2 = 2√2. ✓
    """
    a = 0.0
    a_prime = math.pi / 4
    b = math.pi / 8
    b_prime = 3 * math.pi / 8

    return compute_chsh_S(a, a_prime, b, b_prime)


# ── Monte Carlo CHSH Simulation ─────────────────────────────────────────────


def simulate_chsh(
    n_trials: int = 10000,
    seed: int = 42,
    a: float = 0.0,
    a_prime: float = math.pi / 4,
    b: float = math.pi / 8,
    b_prime: float = 3 * math.pi / 8,
) -> dict:
    """Monte Carlo simulation of CHSH experiment.

    For each trial, randomly choose one of the four measurement settings
    and sample outcomes according to QM probabilities.
    """
    rng = random.Random(seed)
    bell = BellState()

    # We need to estimate E(a,b) from counts.
    # E(a,b) = P(++|ab) + P(--|ab) - P(+-|ab) - P(-+|ab)
    settings = [
        ("E(a,b)", a, b),
        ("E(a,b')", a, b_prime),
        ("E(a',b)", a_prime, b),
        ("E(a',b')", a_prime, b_prime),
    ]

    counts: dict[str, dict[str, int]] = {}
    for name, _, _ in settings:
        counts[name] = {"++": 0, "+-": 0, "-+": 0, "--": 0}

    for _ in range(n_trials):
        for name, angle_a, angle_b in settings:
            # Sample outcomes from the joint distribution.
            p_pp = bell.joint_probability(angle_a, angle_b, +1, +1)
            p_pm = bell.joint_probability(angle_a, angle_b, +1, -1)
            p_mp = bell.joint_probability(angle_a, angle_b, -1, +1)
            p_mm = bell.joint_probability(angle_a, angle_b, -1, -1)

            r = rng.random()
            if r < p_pp:
                counts[name]["++"] += 1
            elif r < p_pp + p_pm:
                counts[name]["+-"] += 1
            elif r < p_pp + p_pm + p_mp:
                counts[name]["-+"] += 1
            else:
                counts[name]["--"] += 1

    # Compute correlations from counts.
    correlations = {}
    for name, _, _ in settings:
        c = counts[name]
        total = sum(c.values())
        if total > 0:
            correlations[name] = (c["++"] + c["--"] - c["+-"] - c["-+"]) / total
        else:
            correlations[name] = 0.0

    S_sim = (
        correlations["E(a,b)"]
        - correlations["E(a,b')"]
        + correlations["E(a',b)"]
        + correlations["E(a',b')"]
    )

    S_theory = optimal_chsh()["S"]

    return {
        "n_trials": n_trials,
        "S_simulated": S_sim,
        "S_theoretical": S_theory,
        "delta": abs(S_sim - S_theory),
        "correlations_simulated": correlations,
        "violates_CHSH": abs(S_sim) > 2.0,
    }


# ── Local Hidden Variable Bound ─────────────────────────────────────────────


def chsh_lhv_bound() -> dict:
    """Compute the CHSH bound for local hidden variable theories.

    Returns the theoretical bound |S| ≤ 2.
    """
    return {
        "bound": 2.0,
        "meaning": "Any local hidden variable theory must satisfy |S| ≤ 2.",
        "QM_prediction": 2 * math.sqrt(2),
        "QM_exceeds_bound": 2 * math.sqrt(2) > 2.0,
    }
