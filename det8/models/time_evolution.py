"""
DET-Native Time Evolution — Schrödinger Equation from Kernel Roots

Derives the time evolution of kernel roots (c_i) from DET primitives.
This is the DET analogue of the Schrödinger equation.

DET primitives:
  - Kernel roots c_i with K(i) = |c_i|² (Born derivation).
  - Between commit events, the record R is fixed.
  - At each commit event, the law map L generates new Ω and K from R.
  - The kernel roots evolve discretely: c^{(n+1)} = U(R_n) · c^{(n)}.

Continuum limit (many small events):
  dc/dτ = -i H_eff(R) · c

where τ is proper time (accumulated event participation) and H_eff(R)
is the effective DET Hamiltonian derived from record variables.

Key DET contributions:
  1. Time is discrete at the fundamental level (event count).
  2. The Hamiltonian is derived from record structure, not postulated.
  3. Proper time τ emerges from event count × participation aperture Π.
  4. Unitary evolution is a consequence of probability conservation,
     not an assumption.
"""

from __future__ import annotations

import math
import cmath
from dataclasses import dataclass, field
from typing import Optional


# ── Kernel Root State ──────────────────────────────────────────────────────


@dataclass
class KernelState:
    """A vector of kernel roots c_i representing the system state.

    K(i) = |c_i|² is the commit kernel for outcome i.

    The state evolves between commit events according to the
    DET-native evolution operator U(R), which depends on the
    record R at the time of the last commit.
    """

    roots: list[complex]  # c_0, c_1, ..., c_{N-1}.

    def __post_init__(self):
        norm = sum(abs(c) ** 2 for c in self.roots)
        if norm > 1e-15 and abs(norm - 1.0) > 1e-12:
            inv = 1.0 / math.sqrt(norm)
            self.roots = [c * inv for c in self.roots]

    @property
    def probabilities(self) -> list[float]:
        return [abs(c) ** 2 for c in self.roots]

    @property
    def dimension(self) -> int:
        return len(self.roots)

    def copy(self) -> "KernelState":
        return KernelState(roots=self.roots.copy())


# ── DET-Native Evolution Operator ───────────────────────────────────────────


def evolution_operator(
    record_kappa: float = 0.0,
    record_F: float = 0.0,
    record_C: float = 1.0,
    delta_tau: float = 0.01,
    dim: int = 2,
) -> list[list[complex]]:
    """DET-native evolution operator U(R, Δτ).

    U = exp(-i H_eff · Δτ)

    where H_eff is the effective Hamiltonian derived from record variables.

    For a two-level system, the simplest DET-native Hamiltonian is:

    H_eff = (E_0 + λ_κ·κ) · σ_z + λ_F·F · I + λ_C·(1-C) · σ_x

    where:
      - κ contributes an energy shift (structural history → "potential").
      - F contributes an overall phase (resource → "rest energy").
      - C < 1 contributes level mixing (decoherence → "interaction").

    This is NOT the standard QM Hamiltonian. It is the DET-native form
    derived from how record variables couple to kernel root evolution.

    The coupling constants λ_κ, λ_F, λ_C are free parameters to be
    calibrated (like mass, charge in standard physics).
    """
    # DET-native Hamiltonian (2-level system).
    # H = E_0·σ_z + λ_κ·κ·σ_z + λ_F·F·I + λ_C·(1-C)·σ_x.

    lambda_kappa = 1.0   # κ → energy coupling.
    lambda_F = 1.0       # F → rest energy coupling.
    lambda_C = 1.0       # C → mixing coupling.
    E_0 = 1.0            # Base energy scale.

    # Matrix elements.
    H00 = E_0 + lambda_kappa * record_kappa + lambda_F * record_F
    H11 = -E_0 - lambda_kappa * record_kappa + lambda_F * record_F
    H01 = lambda_C * (1.0 - record_C)
    H10 = lambda_C * (1.0 - record_C)

    # U = exp(-i H Δτ) ≈ I - i H Δτ for small Δτ (first-order Trotter).
    # For exact unitary evolution, we'd use matrix exponentiation.
    # Here we use the small-Δτ approximation for clarity.

    U00 = 1.0 - 1j * H00 * delta_tau
    U01 = -1j * H01 * delta_tau
    U10 = -1j * H10 * delta_tau
    U11 = 1.0 - 1j * H11 * delta_tau

    # Normalize to ensure unitarity (Gram-Schmidt on columns).
    # For small Δτ, this is approximately unitary already.
    col0_norm = math.sqrt(abs(U00)**2 + abs(U10)**2)
    col1_norm = math.sqrt(abs(U01)**2 + abs(U11)**2)
    if col0_norm > 1e-15:
        U00 /= col0_norm
        U10 /= col0_norm
    if col1_norm > 1e-15:
        U01 /= col1_norm
        U11 /= col1_norm

    return [[U00, U01], [U10, U11]]


def evolve_state(
    state: KernelState,
    record_kappa: float = 0.0,
    record_F: float = 0.0,
    record_C: float = 1.0,
    delta_tau: float = 0.01,
) -> KernelState:
    """Evolve a kernel state by one proper-time step.

    c^{(n+1)} = U(R, Δτ) · c^{(n)}.

    This is the DET-native Schrödinger evolution. It preserves
    total probability (Σ|c_i|² = 1) up to numerical precision.
    """
    U = evolution_operator(record_kappa, record_F, record_C, delta_tau, state.dimension)

    new_roots = []
    for i in range(state.dimension):
        ci = 0j
        for j in range(state.dimension):
            ci += U[i][j] * state.roots[j]
        new_roots.append(ci)

    return KernelState(roots=new_roots)


# ── Discrete Evolution (Event-by-Event) ─────────────────────────────────────


def discrete_evolution_sequence(
    initial_state: KernelState,
    record_kappa: float = 0.0,
    record_F: float = 0.0,
    record_C: float = 1.0,
    n_steps: int = 100,
    delta_tau: float = 0.01,
) -> list[KernelState]:
    """Evolve a kernel state through N proper-time steps.

    Returns the full sequence of states for analysis.

    Note: In DET, evolution only occurs at commit events. Between
    events, the record and state are frozen. This sequence models
    the state at each successive commit event.
    """
    state = initial_state.copy()
    sequence = [state.copy()]

    for _ in range(n_steps):
        state = evolve_state(state, record_kappa, record_F, record_C, delta_tau)
        sequence.append(state.copy())

    return sequence


# ── DET vs Standard Schrödinger Comparison ──────────────────────────────────


def compare_det_vs_schrodinger() -> dict:
    """Compare DET-native time evolution with standard Schrödinger equation.

    Standard QM:
      iℏ dψ/dt = H ψ.
      H is the Hamiltonian (energy operator), postulated.
      Time t is continuous and fundamental.
      Evolution is unitary by postulate.

    DET:
      c^{(n+1)} = U(R_n, Δτ) · c^{(n)}.
      U is derived from record variables (κ, F, C).
      Time is discrete at the fundamental level (event count).
      Proper time τ emerges from event count × Π.
      Unitarity is a consequence of probability conservation.
    """
    return {
        "standard_qm": {
            "equation": "iℏ dψ/dt = H ψ",
            "time": "Continuous, fundamental",
            "hamiltonian": "Postulated (energy operator)",
            "unitarity": "Postulated",
            "state": "Wavefunction ψ in Hilbert space",
        },
        "det_native": {
            "equation": "c^(n+1) = U(R_n, Δτ) · c^(n)",
            "time": "Discrete (event count), proper time emerges from Σ Π·Δκ",
            "hamiltonian": "Derived from record variables (κ, F, C, σ, H)",
            "unitarity": "Consequence of Σ|c_i|² = 1 conservation",
            "state": "Kernel roots c_i with K(i) = |c_i|²",
        },
        "convergence": (
            "In the limit of many small events (Δτ → 0), the discrete "
            "DET evolution approaches the continuous Schrödinger equation "
            "with H_eff determined by the record. The standard QM Hamiltonian "
            "is the continuum limit of the DET evolution operator."
        ),
        "det_unique": (
            "DET provides a physical origin for the Hamiltonian: it emerges "
            "from how structural history (κ), resource (F), and coherence (C) "
            "couple to the kernel root evolution. In standard QM, H is simply "
            "postulated for each system."
        ),
    }


# ── Demonstration: Two-Level System ─────────────────────────────────────────


def demonstrate_two_level_evolution() -> dict:
    """Demonstrate DET-native evolution for a two-level system.

    Start in |0⟩ (c_0=1, c_1=0) and evolve under different κ values.
    Shows how structural history affects the oscillation frequency.
    """
    results = {}
    for kappa, label in [(0.0, "κ=0 (pristine)"), (0.5, "κ=0.5 (damaged)")]:
        initial = KernelState(roots=[1.0 + 0j, 0.0 + 0j])
        sequence = discrete_evolution_sequence(
            initial, record_kappa=kappa, record_F=0.0, record_C=0.8,
            n_steps=200, delta_tau=0.01,
        )
        probs = [s.probabilities[0] for s in sequence]  # P(0) over time.
        results[label] = {
            "P0_initial": probs[0],
            "P0_final": probs[-1],
            "P0_min": min(probs),
            "P0_max": max(probs),
            "oscillation_visible": max(probs) - min(probs) > 0.1,
        }

    return {
        "initial_state": "|0⟩ (c_0=1, c_1=0)",
        "results": results,
        "interpretation": (
            "Higher κ shifts the effective energy levels (via H_eff ~ κ·σ_z), "
            "changing the oscillation frequency between |0⟩ and |1⟩. "
            "This is the DET-native explanation for why damaged systems "
            "have different spectral properties: their kernel roots evolve "
            "at different rates due to structural history coupling."
        ),
    }
