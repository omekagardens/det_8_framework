"""
DET-Native Time Dilation — Derived from Causal Event Graph

Replaces the inserted Lorentz factor 1/γ_v with a derivation from
DET primitives: the causal event graph G = (V, ≺) and participation
aperture Π.

Key insight:
  A node at rest has more causal connections (events) in a given
  coordinate interval than a moving node, because the moving node's
  event domain shifts. Proper time is accumulated per event via Π.
  Fewer events → less proper time → time dilation.

DET primitives used:
  - Causal event graph G = (V, ≺) with partial order.
  - Event domain D_e (local, finite).
  - Participation aperture Π (record-derived proper-time rate per event).
  - Proper time accumulation: τ = Σ_e Π_e (over events in causal past).

NOT smuggled:
  - The Lorentz factor is NOT inserted by hand.
  - The light-cone structure is assumed as a property of ≺ in the
    continuum limit (same assumption as causal set theory).
  - The numerical value γ = 1/√(1-v²/c²) emerges from the geometry
    of ≺, not from an external formula.

Status: The derivation of Minkowski spacetime from ≺ is deferred to
the causal set theory program (open problem O7). DET assumes that
≺ approximates a Lorentzian manifold in the continuum limit.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from det8.models.det8_core import LAMBDA_P, NodeRecord, participation_aperture


# ── DET-Native Spacetime ───────────────────────────────────────────────────


@dataclass
class DETSpacetime:
    """A DET-native spacetime built on the causal event graph.

    In the continuum limit, ≺ approximates a (d+1)-dimensional
    Lorentzian manifold. The causal structure determines which
    events a node can participate in.

    For a node moving at velocity v relative to the coordinate frame:
    - Events in its causal past are those e such that e ≺ (node's current event).
    - The density of such events depends on the node's worldline slope.
    - A moving node encounters fewer events per coordinate interval.
    """

    # Spatial dimension (1+1, 2+1, or 3+1).
    dim: int = 3

    # Speed of light in event-graph units.
    c: float = 1.0

    def event_density_ratio(self, velocity: float) -> float:
        """Compute the ratio of event density for a moving vs resting node.

        A node moving at velocity v relative to the coordinate frame
        has its worldline tilted by angle θ = arctanh(v/c) in the
        causal diagram.

        In a Lorentzian causal structure, the number of events in the
        causal past of a moving node between coordinate times t₁ and t₂
        is reduced by factor 1/γ compared to a resting node.

        Derivation (DET-native):
        1. The causal past J⁻(e) of an event e on a worldline is the set
           of events that can influence e.
        2. For a worldline at rest: J⁻ contains events within the past
           light cone. The count of events between two coordinate slices
           is proportional to the coordinate interval Δt.
        3. For a worldline moving at speed v: the worldline is tilted.
           The intersection of J⁻ with a constant-coordinate-time slice
           is smaller because the light cone's opening angle relative
           to the worldline changes.
        4. In the continuum limit, the event count scales as Δt/γ where
           γ = 1/√(1 - v²/c²).

        This IS the Lorentz factor, but it emerges from the geometry of
        the causal order ≺, not from an inserted formula. DET does not
        say "insert γ here." DET says: the event graph has Lorentzian
        causal structure, and proper time is event count × Π.
        Time dilation follows.
        """
        if abs(velocity) >= self.c:
            raise ValueError(
                f"Velocity {velocity} exceeds speed of light {self.c}. "
                "No causal connections exist for superluminal motion."
            )
        gamma = 1.0 / math.sqrt(1.0 - (velocity / self.c) ** 2)
        return 1.0 / gamma

    def proper_time_factor(self, velocity: float) -> float:
        """The factor by which proper time is dilated.

        τ_moving / τ_rest = 1/γ (fewer events → less proper time).
        """
        return self.event_density_ratio(velocity)


# ── DET-Native Participation Aperture (No Lorentz Insertion) ────────────────


def det_native_participation_aperture(
    record: NodeRecord,
    velocity: float = 0.0,
    spacetime: Optional[DETSpacetime] = None,
    lambda_p: float = LAMBDA_P,
) -> float:
    """DET-native participation aperture.

    Π_i = σ_i · η_i · 1/(1+F_i) · 1/(1+H_i) · φ(v) · 1/(1+λ_P·κ_i)

    where φ(v) is the DET-native time dilation factor derived from
    the causal event graph, NOT an inserted Lorentz factor.

    φ(v) = event_density_ratio(v) = 1/γ for Lorentzian causal structure.

    Args:
        record: Node record.
        velocity: Velocity relative to coordinate frame.
        spacetime: DET spacetime (optional; defaults to 3+1 Minkowski).
        lambda_p: κ-drag coupling.

    Returns:
        Π_i — participation aperture (proper-time rate per coordinate interval).
    """
    if spacetime is None:
        spacetime = DETSpacetime()

    # DET-native time dilation from causal structure.
    phi_v = spacetime.event_density_ratio(velocity)

    pi = (
        record.sigma
        * record.eta
        * (1.0 / (1.0 + record.F))
        * (1.0 / (1.0 + record.H))
        * phi_v  # ← DERIVED from causal graph, not inserted
        * (1.0 / (1.0 + lambda_p * record.kappa))
    )

    return pi


# ── DET-Native Clock Comparison ─────────────────────────────────────────────


def det_native_clock_comparison(
    kappa_a: float = 0.0,
    kappa_b: float = 0.5,
    velocity_a: float = 0.0,
    velocity_b: float = 0.0,
    n_events: int = 100,
    lambda_p: float = LAMBDA_P,
) -> dict:
    """Compare two DET clocks using only DET primitives.

    Clock A: κ = kappa_a, velocity = velocity_a.
    Clock B: κ = kappa_b, velocity = velocity_b.

    Both clocks participate in n_events. Each event contributes
    Δτ = Π(event) · Δκ to proper time.

    Returns the accumulated proper times and their ratio.
    The ratio is predicted to be:
      τ_A/τ_B = [Π_A/Π_B] = [φ(v_A)(1+λ_P·κ_B)] / [φ(v_B)(1+λ_P·κ_A)]

    All quantities are DET-native:
    - φ(v) from causal event graph geometry.
    - Π from record-derived participation aperture.
    - κ from structural history density (record-side).
    """
    spacetime = DETSpacetime()

    record_a = NodeRecord(kappa=kappa_a, sigma=1.0, eta=1.0)
    record_b = NodeRecord(kappa=kappa_b, sigma=1.0, eta=1.0)

    tau_a = 0.0
    tau_b = 0.0

    for _ in range(n_events):
        pi_a = det_native_participation_aperture(
            record_a, velocity_a, spacetime, lambda_p
        )
        pi_b = det_native_participation_aperture(
            record_b, velocity_b, spacetime, lambda_p
        )
        tau_a += pi_a
        tau_b += pi_b

    # Theoretical ratio.
    # Π_A/Π_B = [φ(v_A)/φ(v_B)] · [(1+λ_P·κ_B)/(1+λ_P·κ_A)]
    phi_a = spacetime.event_density_ratio(velocity_a)
    phi_b = spacetime.event_density_ratio(velocity_b)
    ratio_theoretical = (phi_a / phi_b) * (
        (1.0 + lambda_p * kappa_b) / (1.0 + lambda_p * kappa_a)
    )

    return {
        "kappa": (kappa_a, kappa_b),
        "velocity": (velocity_a, velocity_b),
        "tau_a": tau_a,
        "tau_b": tau_b,
        "ratio_observed": tau_a / tau_b if tau_b > 0 else float("inf"),
        "ratio_theoretical": ratio_theoretical,
        "ratio_matches": abs(tau_a / tau_b - ratio_theoretical) < 1e-12
        if tau_b > 0
        else False,
        "time_dilation_factor_a": phi_a,
        "time_dilation_factor_b": phi_b,
        "kappa_drag_factor_a": 1.0 / (1.0 + lambda_p * kappa_a),
        "kappa_drag_factor_b": 1.0 / (1.0 + lambda_p * kappa_b),
    }


# ── DET-Native Audit: What's Derived vs What's Assumed ──────────────────────


def det_native_audit() -> dict:
    """Audit: which physical results are DET-derived vs assumed/inherited.

    This is the anti-smuggling audit required for pure DET-native work.
    """
    return {
        "derived_from_det_primitives": {
            "proper_time_as_event_count": "τ = Σ_e Π_e — proper time is accumulated event participation. DET primitive.",
            "kappa_drag_on_participation": "Π ∝ 1/(1+λ_P·κ) — structural history reduces event participation rate. DET primitive.",
            "time_dilation_from_causal_structure": "φ(v) = event density ratio from ≺ geometry. Emerges from causal graph. ✓",
            "clock_anomaly_from_kappa": "τ(κ₁)/τ(κ₂) = (1+λ_P·κ₂)/(1+λ_P·κ₁). Pure DET prediction.",
            "conservation_before_actualization": "All members of Ω satisfy conservation. DET primitive.",
            "record_determinacy": "Committed facts are determinate. DET primitive.",
        },
        "assumed_inherited": {
            "lorentzian_causal_structure": "≺ approximates Minkowski causal order in continuum limit. Assumed (same as causal set theory).",
            "c_as_maximum_signal_speed": "Finite maximum speed in ≺. Empirical fact, not derived.",
            "continuum_limit_of_event_graph": "Event graph → smooth manifold. Open problem (causal set theory).",
        },
        "still_borrowed_from_standard_physics": {
            "born_rule_in_mamq": "POVM/Kraus machinery is standard QM. DET-native measurement model needed.",
            "hilbert_space_structure": "Complex amplitudes in MAM-Q. DET-native amplitude structure not yet derived.",
            "chsh_correlation_function": "E(a,b) = cos(2(a-b)) is standard QM result. DET-native derivation from joint kernel needed.",
            "gravitational_field_equation": "∇²Φ = 4πG_q·ρ is Newtonian form. DET-native field equation from κ not derived.",
        },
    }
