"""
CHSH Correlation and Amplitude Emergence from DET Primitives

Derives E(a,b) = cos(2(a-b)) for the Bell state from DET's:
  1. Nonfactorizable joint kernel roots c_ij.
  2. Linear root transformation under basis change (Born derivation).
  3. Born rule: K(i,j) = |c_ij|².

No QM borrowing — the correlation function is a theorem about how
kernel roots compose under rotation for a specific nonfactorizable
record (the Bell state).

Also formalizes amplitude emergence: complex numbers arise from the
need to represent continuous interference in kernel root composition.
"""

from __future__ import annotations

import math
import cmath
from dataclasses import dataclass, field
from typing import Optional


# ── Kernel Roots for Two-Qubit System ──────────────────────────────────────


@dataclass
class TwoQubitRoots:
    """Kernel roots c_ij for a two-qubit relational record.

    K(i,j) = |c_ij|² for i,j ∈ {0,1}.

    These are DET primitives, NOT QM amplitudes. They are the
    square roots of the commit kernel values, carrying phase
    information needed for nonfactorizable composition.
    """

    c00: complex
    c01: complex
    c10: complex
    c11: complex

    def __post_init__(self):
        norm = (
            abs(self.c00) ** 2
            + abs(self.c01) ** 2
            + abs(self.c10) ** 2
            + abs(self.c11) ** 2
        )
        if abs(norm - 1.0) > 1e-12 and norm > 1e-15:
            inv = 1.0 / math.sqrt(norm)
            self.c00 *= inv
            self.c01 *= inv
            self.c10 *= inv
            self.c11 *= inv

    def kernel(self, i: int, j: int) -> float:
        """Born rule: K(i,j) = |c_ij|²."""
        c = [self.c00, self.c01, self.c10, self.c11][i * 2 + j]
        return abs(c) ** 2

    @staticmethod
    def bell_phi_plus() -> "TwoQubitRoots":
        """Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2.

        Roots: c_00 = c_11 = 1/√2, c_01 = c_10 = 0.
        """
        inv2 = 1.0 / math.sqrt(2)
        return TwoQubitRoots(c00=inv2, c01=0, c10=0, c11=inv2)


# ── Basis Rotation ──────────────────────────────────────────────────────────


def rotation_matrix(angle: float) -> list[list[complex]]:
    """Single-qubit rotation matrix for measurement at angle θ.

    U(θ) = [[cos(θ), sin(θ)], [-sin(θ), cos(θ)]]

    For complex amplitudes, this generalizes to:
    U(θ) = [[cos(θ), sin(θ)], [-sin(θ), cos(θ)]]
    with real entries (same form for real and complex roots).

    This is the DET-native basis change operation: kernel roots
    transform linearly under this matrix (from Born derivation §5).
    """
    cos_t = math.cos(angle)
    sin_t = math.sin(angle)
    return [[cos_t, sin_t], [-sin_t, cos_t]]


def transform_roots(
    roots: TwoQubitRoots,
    angle_a: float,
    angle_b: float,
) -> TwoQubitRoots:
    """Transform two-qubit roots under rotation by angles a and b.

    c'_ij = Σ_{k,l} U(a)_{ik} · U(b)_{jl} · c_kl

    This is the tensor product of single-qubit rotations.
    Derived from: roots transform linearly (Born derivation §5),
    and independent systems compose via tensor product.
    """
    Ua = rotation_matrix(angle_a)
    Ub = rotation_matrix(angle_b)

    c = [[roots.c00, roots.c01], [roots.c10, roots.c11]]
    c_new = [[0j, 0j], [0j, 0j]]

    for i in range(2):
        for j in range(2):
            total = 0j
            for k in range(2):
                for l in range(2):
                    total += Ua[i][k] * Ub[j][l] * c[k][l]
            c_new[i][j] = total

    return TwoQubitRoots(
        c00=c_new[0][0],
        c01=c_new[0][1],
        c10=c_new[1][0],
        c11=c_new[1][1],
    )


# ── Correlation Function ────────────────────────────────────────────────────


def correlation(roots: TwoQubitRoots) -> float:
    """Compute correlation E = Σ_{i,j} (+1 for i=j, -1 for i≠j) · K(i,j).

    For outcomes mapped to {+1,-1}: A = 1-2i, B = 1-2j.
    E = Σ_{i,j} A·B · K(i,j).

    DET-native: uses Born rule K(i,j) = |c_ij|².
    """
    e = 0.0
    for i in (0, 1):
        for j in (0, 1):
            a_val = 1 - 2 * i  # +1 for 0, -1 for 1
            b_val = 1 - 2 * j
            e += a_val * b_val * roots.kernel(i, j)
    return e


def correlation_function_derived(angle_a: float, angle_b: float) -> dict:
    """Derive the CHSH correlation function for the Bell state.

    E(a,b) = cos(2(a-b))

    This is a DET theorem, not borrowed from QM:
      1. Bell state roots: c_00=c_11=1/√2, c_01=c_10=0.
      2. Transform by U(a)⊗U(b).
      3. Apply Born rule: K(i,j) = |c'_ij|².
      4. Compute E = Σ A·B·K.
      5. Result: E(a,b) = cos(2(a-b)).
    """
    bell = TwoQubitRoots.bell_phi_plus()
    transformed = transform_roots(bell, angle_a, angle_b)
    E = correlation(transformed)

    expected = math.cos(2 * (angle_a - angle_b))

    return {
        "angles": (angle_a, angle_b),
        "E_computed": E,
        "E_expected": expected,
        "E_formula": "cos(2(a-b))",
        "match": abs(E - expected) < 1e-12,
    }


def verify_chsh_complete() -> dict:
    """Verify full CHSH: S = E(a,b) - E(a,b') + E(a',b) + E(a',b')."""
    a = 0.0
    a_prime = math.pi / 4
    b = math.pi / 8
    b_prime = 3 * math.pi / 8

    results = {}
    for name, (ang_a, ang_b) in [
        ("E(a,b)", (a, b)),
        ("E(a,b')", (a, b_prime)),
        ("E(a',b)", (a_prime, b)),
        ("E(a',b')", (a_prime, b_prime)),
    ]:
        r = correlation_function_derived(ang_a, ang_b)
        results[name] = r["E_computed"]

    S = results["E(a,b)"] - results["E(a,b')"] + results["E(a',b)"] + results["E(a',b')"]
    S_target = 2 * math.sqrt(2)

    return {
        "correlations": results,
        "S": S,
        "S_target": S_target,
        "S_matches": abs(S - S_target) < 1e-12,
        "violates_CHSH": abs(S) > 2.0,
        "derived_from": [
            "Bell state kernel roots (nonfactorizable record)",
            "Linear root transformation (Born derivation §5)",
            "Born rule K(i,j)=|c_ij|²",
            "Correlation definition E=Σ A·B·K",
        ],
    }


# ── Amplitude Emergence ────────────────────────────────────────────────────


def amplitude_emergence() -> dict:
    """Formalize how complex amplitudes emerge from DET kernel roots.

    DET starts with: commit kernel K(i) ∈ [0,1].
    Kernel roots: c_i with K(i) = |c_i|² (Born derivation).

    Why COMPLEX numbers rather than just real ± signs?

    Real signs (±) give only two phases: constructive (+) and
    destructive (-) interference. This produces:
      |c_0 + c_1|² = K(0) + K(1) ± 2√(K(0)K(1))

    Complex phases e^{iφ} give continuous interference:
      |c_0 + e^{iφ}c_1|² = K(0) + K(1) + 2√(K(0)K(1))·cos(φ)

    The continuous phase is REQUIRED to reproduce:
    1. Mach-Zehnder interferometer: continuous fringe visibility.
    2. Bell inequality violations: continuous angle dependence.
    3. Any system where relative phase varies continuously.

    The complex numbers are NOT fundamental. They are the MINIMAL
    mathematical structure that allows kernel roots to compose
    correctly for all nonfactorizable records. If real signs
    sufficed, we would use them. They don't — continuous
    interference forces complex phases.

    Theorem: The set of kernel roots {c_i} for a system with N
    distinguishable outcomes forms a vector space over ℂ of
    dimension N, equipped with the inner product ⟨c,d⟩ = Σ c_i* d_i
    and norm ‖c‖² = Σ |c_i|² = 1.
    """
    return {
        "starting_point": "Commit kernel K(i) ∈ [0,1] (DET primitive)",
        "step_1": "Kernel roots c_i with K(i)=|c_i|² (Born derivation)",
        "step_2": "Real signs (±) sufficient for factorizable records",
        "step_3": "Nonfactorizable records FORCE phase information",
        "step_4": "Continuous interference FORCES complex phases e^{iφ}",
        "result": "Hilbert space emerges as the space of kernel roots",
        "what_is_derived": [
            "Complex vector space structure (from root composition)",
            "Inner product ⟨c,d⟩ = Σ c_i* d_i (from probability conservation)",
            "Norm ‖c‖² = 1 (from kernel normalization)",
            "Unitary transformations U (from basis-change consistency)",
        ],
        "what_is_fundamental": [
            "K (commit kernel) — the probabilities",
            "Composition rule for nonfactorizable records — forces phases",
        ],
        "what_is_not_assumed": [
            "Hilbert space as primitive — it emerges",
            "Wavefunction as primitive — it is the vector of roots",
            "Complex numbers as primitive — forced by interference",
        ],
    }
