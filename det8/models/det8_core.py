"""
DET v8.0 Physical Core — Record, Participation Aperture, and Proper Time

Implements the DET 8 record structure with all physical variables,
the participation aperture Π, proper-time accumulation, and
mutable-q dynamics. This is the DET 8-native physics layer,
independent of DET 7.

Key variables (from P0.1 §6.1, revised per D3r1, M0 fix):
  F_i     : local resource/field participation
  kappa_i : structural history density [0, 1]  (was: q_i)
  N_i     : local event count (monotone, non-decreasing) — SEPARATE from κ
  sigma_i : conductivity / processing factor > 0
  H_i     : local coordination load ≥ 0
  C_i     : coherence
  r_i     : pointer/record strength
  theta_i : phase (when active)
  eta_i   : structural viability / actuation-readiness [0, 1]

Derived (D3r1):
  gamma_i = lambda_gamma * kappa_i  — gravitational source charge
  Pi_i    : participation aperture (proper-time rate per event)
  Delta_tau_i : proper-time increment = Π_i · ΔN_i
  psi_i   : free energy (structural + baseline)

M0 fix (mathematical review, Aug 2026):
  Δτ_i = Π_i · ΔN_i  (NOT Δτ_i = Π_i · Δκ_i).
  N is a monotone event counter. κ is mutable structural history.
  Previously conflated — κ was used for both, creating inconsistency
  when κ decreased (recovery would imply negative proper time).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ── Physical Constants ─────────────────────────────────────────────────────

# Coupling constant for κ-drag on participation aperture.
# Must be calibrated empirically: λ_P = Π(0)/Π(1) - 1.
LAMBDA_P = 1.0

# Gravitational coupling: γ = λ_γ · κ.
LAMBDA_GAMMA = 1.0

# Structural stiffness (energy cost per unit κ² deviation).
K_STRUCTURAL = 1.0

# Equilibrium structural history (κ relaxes toward this).
KAPPA_EQ = 0.0

# Recovery time scale.
TAU_REC = 10.0

# Damage coefficient per event.
ALPHA_DAMAGE = 0.01

# Baseline for gravity sourcing ρ = γ - γ_b.
GAMMA_B = 0.0


# ── Node Record ─────────────────────────────────────────────────────────────


@dataclass
class NodeRecord:
    """Complete DET 8 record at a single node.

    Modal annotation: A (actual committed facts).

    All variables are record-side — they are committed facts,
    not metaphysical primitives. None is agency.
    """

    # ── Core physical variables ──
    F: float = 0.0      # local resource/field (≥ 0)
    kappa: float = 0.0  # structural history density [0, 1]  (D3r1: was 'q')
    N: float = 0.0      # local event count (monotone, non-decreasing). M0 fix.
    sigma: float = 1.0   # conductivity (positive)
    H: float = 0.0      # coordination load (non-negative)
    C: float = 1.0      # coherence
    r: float = 0.0      # pointer/record strength
    theta: float = 0.0  # phase [0, 2π)
    eta: float = 1.0    # structural viability [0, 1]

    # ── Derived / cached ──
    _proper_time: float = field(default=0.0, repr=False)

    def __post_init__(self):
        # Clamp values to valid ranges.
        self.kappa = max(0.0, min(1.0, self.kappa))
        self.sigma = max(1e-12, self.sigma)
        self.H = max(0.0, self.H)
        self.eta = max(0.0, min(1.0, self.eta))
        self.F = max(0.0, self.F)

    @property
    def gamma(self) -> float:
        """Gravitational source charge γ = λ_γ · κ."""
        return LAMBDA_GAMMA * self.kappa

    def copy(self) -> "NodeRecord":
        return NodeRecord(
            F=self.F,
            kappa=self.kappa,
            sigma=self.sigma,
            H=self.H,
            C=self.C,
            r=self.r,
            theta=self.theta,
            eta=self.eta,
            N=self.N,
            _proper_time=self._proper_time,
        )


# ── Participation Aperture ──────────────────────────────────────────────────


def participation_aperture(
    record: NodeRecord,
    velocity_fraction: float = 0.0,
    lambda_p: float = LAMBDA_P,
) -> float:
    """Compute the participation aperture Π_i.

    Π_i = σ_i · η_i · 1/(1+F_i) · 1/(1+H_i) · 1/γ_v · 1/(1+λ_P·κ_i)

    κ_i enters as drag: higher κ → lower Π → slower proper time.

    Modal annotation: P (proposed physical — clock ansatz).
    """
    if velocity_fraction >= 1.0:
        raise ValueError("Velocity fraction must be < 1.0")

    # Lorentz factor.
    if velocity_fraction > 0.0:
        gamma = 1.0 / math.sqrt(1.0 - velocity_fraction**2)
    else:
        gamma = 1.0

    # Participation aperture.
    pi = (
        record.sigma
        * record.eta
        * (1.0 / (1.0 + record.F))
        * (1.0 / (1.0 + record.H))
        * (1.0 / gamma)
        * (1.0 / (1.0 + lambda_p * record.kappa))
    )

    return pi


def proper_time_increment(
    record: NodeRecord,
    delta_N: float = 1.0,
    velocity_fraction: float = 0.0,
    lambda_p: float = LAMBDA_P,
) -> float:
    """Compute the proper-time increment Δτ_i = Π_i · ΔN_i.

    M0 fix: ΔN is event-count increment, NOT Δκ (structural history change).
    N is monotone, non-decreasing. κ can decrease with recovery.
    """
    pi = participation_aperture(record, velocity_fraction, lambda_p)
    return pi * delta_N


def accumulate_proper_time(
    record: NodeRecord,
    delta_N: float = 1.0,
    velocity_fraction: float = 0.0,
    lambda_p: float = LAMBDA_P,
) -> float:
    """Accumulate proper time: Δτ = Π · ΔN.

    M0 fix: increments record.N by delta_N (monotone event count).
    Updates record._proper_time by Π · ΔN.
    """
    delta_tau = proper_time_increment(record, delta_N, velocity_fraction, lambda_p)
    record.N += delta_N  # Monotone event count.
    record._proper_time += delta_tau
    return delta_tau


# ── Mutable-q Dynamics ──────────────────────────────────────────────────────


def apply_q_damage(
    record: NodeRecord,
    damage: float,
) -> float:
    """Apply structural damage: increase q.

    q represents accumulated structural constraint.
    Damage increases q, which reduces Π.

    Args:
        record: The node record (mutated in place).
        damage: Amount of q to add [0, 1].

    Returns:
        The new q value.
    """
    record.kappa = min(1.0, record.kappa + damage)
    return record.kappa


def apply_q_recovery(
    record: NodeRecord,
    recovery: float,
) -> float:
    """Apply natural recovery: decrease q.

    Recovery reduces structural constraint.
    This is record-side dynamics, not Boundary Jubilee (which is M/H).

    Args:
        record: The node record (mutated in place).
        recovery: Amount of q to remove [0, 1].

    Returns:
        The new q value.
    """
    record.kappa = max(0.0, record.kappa - recovery)
    return record.kappa


def apply_q_jubilee(
    record: NodeRecord,
    amount: float,
) -> float:
    """Apply Boundary-mediated q-reduction (Jubilee).

    Modal annotation: M/H (metaphysical/hypothetical).
    Outside the minimal physical core.

    This is separated from natural recovery because Jubilee may
    operate without the usual energy/entropy accounting.

    Args:
        record: The node record (mutated in place).
        amount: Amount of q to remove [0, 1].

    Returns:
        The new q value.
    """
    record.kappa = max(0.0, record.kappa - amount)
    return record.kappa


# ── q-Dependent Observables ─────────────────────────────────────────────────


def effective_gravity_source(
    record: NodeRecord,
    baseline: float = GAMMA_B,
) -> float:
    """Compute the gravitational source contrast ρ = q - b.

    Modal annotation: P (proposed physical; inherited from DET 7 concept).
    The mapping from ρ to metric curvature is unresolved.

    Args:
        record: The node record.
        baseline: The baseline b (cosmic average or zero).

    Returns:
        ρ = q - b, the gravitational source contrast.
    """
    return record.kappa - baseline


def clock_ratio(
    record_a: NodeRecord,
    record_b: NodeRecord,
    lambda_p: float = LAMBDA_P,
) -> float:
    """Compute the clock rate ratio between two nodes.

    Π_A / Π_B = how much faster A's proper time flows relative to B's,
    assuming equal σ, η, F, H, γ_v and differing only in q.

    This is the basis for the q-Π clock anomaly prediction (D3 §7.3):
    two identical clocks with different q should tick at different rates.

    Args:
        record_a: First node record.
        record_b: Second node record.
        lambda_p: q-drag coupling.

    Returns:
        Π_A / Π_B.
    """
    # Only compare the q-dependent part if other factors are equal.
    # Full comparison uses the complete Π formula.
    pi_a = participation_aperture(record_a, lambda_p=lambda_p)
    pi_b = participation_aperture(record_b, lambda_p=lambda_p)
    return pi_a / pi_b if pi_b > 0 else float("inf")


# ── Multi-Node System ──────────────────────────────────────────────────────


@dataclass
class DetSystem:
    """A multi-node DET 8 system.

    Tracks records, proper time, and event history.
    """

    nodes: dict[int, NodeRecord] = field(default_factory=dict)
    event_count: int = 0
    total_proper_time: float = 0.0

    def add_node(self, node_id: int, record: Optional[NodeRecord] = None) -> None:
        if record is None:
            record = NodeRecord()
        self.nodes[node_id] = record

    def step(
        self,
        delta_N: float = 1.0,
        velocity_fractions: Optional[dict[int, float]] = None,
        lambda_p: float = LAMBDA_P,
    ) -> dict[int, float]:
        """Advance all nodes by ΔN events. Returns proper-time increments."""
        increments: dict[int, float] = {}
        vf = velocity_fractions or {}

        for node_id, record in self.nodes.items():
            v = vf.get(node_id, 0.0)
            dtau = accumulate_proper_time(record, delta_N, v, lambda_p)
            increments[node_id] = dtau
            self.total_proper_time += dtau

        self.event_count += 1
        return increments

    def q_damage_event(
        self,
        node_id: int,
        damage: float,
        delta_kappa: float = 1.0,
        lambda_p: float = LAMBDA_P,
    ) -> dict:
        """Apply damage to a node and record the effect on Π.

        Returns before/after comparison.
        """
        record = self.nodes[node_id]
        pi_before = participation_aperture(record, lambda_p=lambda_p)
        kappa_before = record.kappa

        apply_q_damage(record, damage)

        pi_after = participation_aperture(record, lambda_p=lambda_p)
        kappa_after = record.kappa

        return {
            "node": node_id,
            "kappa_before": kappa_before,
            "kappa_after": kappa_after,
            "pi_before": pi_before,
            "pi_after": pi_after,
            "pi_ratio": pi_after / pi_before if pi_before > 0 else 0.0,
            "delta_kappa": damage,
        }

    def q_recovery_event(
        self,
        node_id: int,
        recovery: float,
        delta_kappa: float = 1.0,
        lambda_p: float = LAMBDA_P,
    ) -> dict:
        """Apply recovery to a node and record the effect on Π."""
        record = self.nodes[node_id]
        pi_before = participation_aperture(record, lambda_p=lambda_p)
        kappa_before = record.kappa

        apply_q_recovery(record, recovery)

        pi_after = participation_aperture(record, lambda_p=lambda_p)
        kappa_after = record.kappa

        return {
            "node": node_id,
            "kappa_before": kappa_before,
            "kappa_after": kappa_after,
            "pi_before": pi_before,
            "pi_after": pi_after,
            "pi_ratio": pi_after / pi_before if pi_before > 0 else float("inf"),
            "delta_kappa": -recovery,
        }


# ── q-Π Clock Anomaly Test ─────────────────────────────────────────────────


def q_clock_anomaly_test(
    duration_kappa: float = 100.0,
    q_damaged: float = 0.5,
    lambda_p: float = LAMBDA_P,
) -> dict:
    """Test the q-Π clock anomaly prediction.

    Two identical clocks (same σ, η, F, H, γ_v):
    - Clock A: q = 0 (pristine, fully recovered).
    - Clock B: q = q_damaged (damaged, constrained).

    After duration_kappa coordinate intervals, compare accumulated
    proper time. DET predicts Clock B accumulates LESS proper time.
    """
    system = DetSystem()
    system.add_node(0, NodeRecord(kappa=0.0, sigma=1.0))       # Pristine
    system.add_node(1, NodeRecord(kappa=q_damaged, sigma=1.0))  # Damaged

    tau_0 = 0.0
    tau_1 = 0.0

    for _ in range(int(duration_kappa)):
        increments = system.step(delta_N=1.0, lambda_p=lambda_p)
        tau_0 += increments[0]
        tau_1 += increments[1]

    ratio = tau_0 / tau_1 if tau_1 > 0 else float("inf")

    # Theoretical ratio: Π_0 / Π_1 = (1 + λ_P·q_damaged) / 1
    theoretical_ratio = 1.0 + lambda_p * q_damaged

    return {
        "duration_kappa": duration_kappa,
        "q_damaged": q_damaged,
        "lambda_p": lambda_p,
        "tau_pristine": tau_0,
        "tau_damaged": tau_1,
        "ratio_observed": ratio,
        "ratio_theoretical": theoretical_ratio,
        "anomaly_confirmed": abs(ratio - theoretical_ratio) < 1e-12,
        "damaged_clock_slower": tau_1 < tau_0,
    }
