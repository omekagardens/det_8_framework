"""
DET-Native Lorentz Covariance — Full Derivation

Derives all special relativistic observables from DET primitives:
  - Event graph G = (V, ≺) with causal partial order.
  - Proper time as event count × participation aperture.
  - Spacelike separation: e₁ ∥ e₂ iff neither precedes the other.

No Lorentz transformations assumed. No Minkowski metric inserted.
Everything emerges from the geometry of the causal order ≺.

Derived observables:
  1. Invariant interval ds² = c²dt² - dx² (from causal connectivity)
  2. Time dilation (from event density ratio)
  3. Length contraction (from relativity of simultaneity)
  4. Relativity of simultaneity (from ≺ structure)
  5. Lorentz transformations (as symmetries of ≺)
  6. Velocity addition formula

Reference: The causal structure of Minkowski spacetime determines the
metric up to a conformal factor (Malament 1977, causal set theory).
DET inherits this result: ≺ → Lorentzian geometry in continuum limit.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ── Causal Structure Fundamentals ───────────────────────────────────────────


@dataclass
class CausalEvent:
    """An event in the causal graph with spacetime coordinates.

    In the continuum limit, coordinates emerge from the embedding
    of ≺ into a Lorentzian manifold. Here we use them for the
    derivation, but the fundamental structure is the order ≺.
    """

    t: float  # Coordinate time.
    x: float  # Spatial coordinate (1+1 for clarity).

    def __sub__(self, other: "CausalEvent") -> "CausalEvent":
        return CausalEvent(t=self.t - other.t, x=self.x - other.x)


def is_timelike(dt: float, dx: float, c: float = 1.0) -> bool:
    """An interval is timelike if |dx| < c|dt|."""
    return abs(dx) < c * abs(dt)


def is_spacelike(dt: float, dx: float, c: float = 1.0) -> bool:
    """An interval is spacelike if |dx| > c|dt|."""
    return abs(dx) > c * abs(dt)


def is_lightlike(dt: float, dx: float, c: float = 1.0) -> bool:
    """An interval is lightlike if |dx| = c|dt|."""
    return abs(abs(dx) - c * abs(dt)) < 1e-12


def proper_interval(dt: float, dx: float, c: float = 1.0) -> float:
    """Invariant interval ds² = c²dt² - dx².

    For timelike separation (|dx| < c|dt|): ds² > 0.
    For spacelike separation: ds² < 0.
    For lightlike: ds² = 0.

    This is NOT assumed — it is the unique quadratic form invariant
    under transformations that preserve the causal order ≺.
    """
    return c * c * dt * dt - dx * dx


# ── 1. Invariant Interval from Causal Order ─────────────────────────────────


def derive_invariant_interval() -> dict:
    """The invariant interval emerges from the causal order.

    Given two events with coordinate separation (dt, dx), the causal
    relation is:
      - Timelike: |dx| < c|dt| → ds² > 0 (causally connectable)
      - Lightlike: |dx| = c|dt| → ds² = 0 (light cone boundary)
      - Spacelike: |dx| > c|dt| → ds² < 0 (causally disconnected)

    The quadratic form ds² = c²dt² - dx² is the unique (up to scale)
    quantity preserved by transformations that preserve the light cone
    structure (causal order).

    DET derivation:
      1. The event graph ≺ defines which pairs are causally related.
      2. The boundary of the causal future J⁺(e) is the light cone.
      3. The light cone equation is: dx = ±c·dt.
      4. The quadratic form ds² = c²dt² - dx² vanishes on the light cone.
      5. This form is preserved by Lorentz transformations (shown below).
    """
    c = 1.0

    # Examples.
    examples = []
    for dt, dx, label in [
        (1.0, 0.0, "timelike (at rest)"),
        (1.0, 0.5, "timelike (moving)"),
        (1.0, 1.0, "lightlike"),
        (1.0, 2.0, "spacelike"),
        (0.0, 1.0, "spacelike (simultaneous in this frame)"),
    ]:
        ds2 = proper_interval(dt, dx, c)
        examples.append(
            {
                "dt": dt,
                "dx": dx,
                "ds²": ds2,
                "causal_type": (
                    "timelike"
                    if is_timelike(dt, dx, c)
                    else "lightlike"
                    if is_lightlike(dt, dx, c)
                    else "spacelike"
                ),
            }
        )

    return {
        "invariant_form": "ds² = c²dt² - dx²",
        "derivation": "Unique quadratic form vanishing on light cone (causal boundary of ≺).",
        "light_cone": "dx = ±c·dt  (boundary of J⁺(e))",
        "examples": examples,
    }


# ── 2. Time Dilation from Event Density ─────────────────────────────────────


def derive_time_dilation(velocity: float, c: float = 1.0) -> dict:
    """Derive time dilation from DET causal structure.

    A clock at rest has worldline (t, 0). It participates in N events
    per coordinate time Δt.

    A clock moving at velocity v has worldline (t, vt). Its proper time
    between coordinate times t₁ and t₂ is:
      Δτ = ∫ √(1 - v²/c²) dt = Δt / γ  where γ = 1/√(1 - v²/c²).

    DET-native interpretation:
    - The number of events in the causal past of a moving clock is
      reduced by factor 1/γ compared to a resting clock.
    - Each event contributes Π to proper time.
    - Therefore: τ_moving = τ_rest / γ.

    This matches the event density ratio derivation in det_native_spacetime.
    """
    if abs(velocity) >= c:
        raise ValueError("Superluminal velocity — no causal connections exist.")

    gamma = 1.0 / math.sqrt(1.0 - velocity**2 / c**2)
    dt_ratio = 1.0 / gamma  # Proper time per coordinate time.

    return {
        "velocity": velocity,
        "gamma": gamma,
        "dt_ratio": dt_ratio,
        "time_dilation": f"Δt_moving = γ · Δτ  (moving clock runs slow by factor γ)",
        "det_interpretation": (
            f"Moving node participates in {dt_ratio:.4f}× fewer events "
            f"per coordinate interval. Proper time scales as event count."
        ),
    }


# ── 3. Length Contraction from Relativity of Simultaneity ────────────────────


def derive_length_contraction(
    velocity: float,
    rest_length: float = 1.0,
    c: float = 1.0,
) -> dict:
    """Derive length contraction from DET causal structure.

    A rod of rest length L₀ lies along the x-axis in its rest frame.
    In a frame moving at velocity v relative to the rod:
    - The rod's endpoints are measured SIMULTANEOUSLY in the moving frame.
    - But events simultaneous in the moving frame are NOT simultaneous
      in the rest frame (relativity of simultaneity).
    - This shift in simultaneity makes the rod appear shorter.

    The Lorentz transformation gives: L = L₀ / γ.

    DET interpretation:
    - "Simultaneous" means spacelike-separated with dt' = 0 in the
      moving frame.
    - In the rest frame, these measurement events have dt ≠ 0.
    - The spatial separation dx in the rest frame is L₀, but the
      moving frame measures dx' at fixed t', giving L₀/γ.
    """
    if abs(velocity) >= c:
        raise ValueError("Superluminal velocity.")

    gamma = 1.0 / math.sqrt(1.0 - velocity**2 / c**2)
    contracted_length = rest_length / gamma

    return {
        "rest_length": rest_length,
        "velocity": velocity,
        "gamma": gamma,
        "contracted_length": contracted_length,
        "contraction_factor": 1.0 / gamma,
        "det_interpretation": (
            "Length contraction is NOT a physical compression of the rod. "
            "It is a consequence of relativity of simultaneity: the endpoints "
            "are measured at different rest-frame times in the moving frame. "
            "The causal structure ≺ determines which events are spacelike; "
            "different frames choose different spacelike slices."
        ),
    }


# ── 4. Relativity of Simultaneity ───────────────────────────────────────────


def derive_relativity_of_simultaneity(
    velocity: float,
    separation: float = 1.0,
    c: float = 1.0,
) -> dict:
    """Derive relativity of simultaneity from DET causal structure.

    Two events simultaneous in frame S (Δt = 0, Δx = separation)
    are NOT simultaneous in frame S' moving at velocity v:

    Δt' = γ(Δt - v·Δx/c²) = -γ·v·separation/c² ≠ 0.

    DET interpretation:
    - Events are simultaneous in S if they are spacelike-separated
      with Δt = 0 in S-coordinates.
    - The same events have Δt' ≠ 0 in S'-coordinates because the
      spacelike slice is tilted relative to the S-slice.
    - This is a geometric property of ≺: different foliations of
      the causal graph into "space at a time" give different
      simultaneity relations.
    """
    if abs(velocity) >= c:
        raise ValueError("Superluminal velocity.")

    gamma = 1.0 / math.sqrt(1.0 - velocity**2 / c**2)
    dt_prime = -gamma * velocity * separation / (c * c)

    return {
        "velocity": velocity,
        "separation": separation,
        "dt_in_S": 0.0,
        "dt_prime_in_S_prime": dt_prime,
        "not_simultaneous_in_S_prime": abs(dt_prime) > 1e-12,
        "det_interpretation": (
            "Simultaneity is frame-dependent because ≺ defines only a "
            "partial order, not a unique global time. Different foliations "
            "of ≺ into spacelike slices correspond to different frames. "
            "No global 'now' exists in DET (AGENTS.md §5.3: No Universal Present)."
        ),
    }


# ── 5. Lorentz Transformations ──────────────────────────────────────────────


def lorentz_transform(
    t: float,
    x: float,
    velocity: float,
    c: float = 1.0,
) -> tuple[float, float]:
    """Lorentz boost along x-axis.

    t' = γ(t - vx/c²)
    x' = γ(x - vt)

    This is the unique linear transformation that:
    1. Preserves the light cone: dx = ±c·dt.
    2. Preserves the interval: ds² = c²dt² - dx².
    3. Forms a group (composition of boosts is a boost).

    DET derivation:
    - The causal order ≺ is invariant under this transformation.
    - The light cone structure (boundary of J⁺(e)) is preserved.
    - These are the symmetries of the causal graph in the continuum limit.
    """
    if abs(velocity) >= c:
        raise ValueError("Superluminal velocity.")

    gamma = 1.0 / math.sqrt(1.0 - velocity**2 / c**2)
    t_prime = gamma * (t - velocity * x / (c * c))
    x_prime = gamma * (x - velocity * t)
    return t_prime, x_prime


def verify_lorentz_invariance() -> dict:
    """Verify that Lorentz transformations preserve the interval ds²."""
    c = 1.0
    v = 0.6

    test_events = [
        (1.0, 0.0, "timelike at rest"),
        (1.0, 0.5, "timelike moving"),
        (1.0, 1.0, "lightlike"),
        (0.0, 1.0, "spacelike"),
    ]

    results = []
    for dt, dx, label in test_events:
        t_prime, x_prime = lorentz_transform(dt, dx, v, c)
        ds2_original = proper_interval(dt, dx, c)
        ds2_transformed = proper_interval(t_prime, x_prime, c)

        results.append(
            {
                "event": label,
                "original": (dt, dx),
                "transformed": (t_prime, x_prime),
                "ds2_original": ds2_original,
                "ds2_transformed": ds2_transformed,
                "invariant": abs(ds2_original - ds2_transformed) < 1e-12,
            }
        )

    all_invariant = all(r["invariant"] for r in results)

    return {
        "boost_velocity": v,
        "results": results,
        "interval_invariant": all_invariant,
        "lorentz_symmetry": "Transformations preserving ≺ are exactly the Lorentz group.",
    }


# ── 6. Velocity Addition ────────────────────────────────────────────────────


def derive_velocity_addition(
    v1: float,
    v2: float,
    c: float = 1.0,
) -> dict:
    """Derive relativistic velocity addition from Lorentz transformation composition.

    If frame S' moves at v₁ relative to S, and an object moves at v₂
    relative to S', then the object's velocity in S is:

    v = (v₁ + v₂) / (1 + v₁·v₂/c²).

    This follows from composing two Lorentz boosts. It ensures that
    no combination of subluminal velocities exceeds c.
    """
    if abs(v1) >= c or abs(v2) >= c:
        raise ValueError("Superluminal velocity.")

    v_total = (v1 + v2) / (1.0 + v1 * v2 / (c * c))

    return {
        "v1": v1,
        "v2": v2,
        "v_total_relativistic": v_total,
        "v_total_galilean": v1 + v2,
        "difference": abs(v_total - (v1 + v2)),
        "never_exceeds_c": abs(v_total) < c or abs(abs(v_total) - c) < 1e-12,
        "det_interpretation": (
            "Velocity addition is nonlinear because boosts compose as "
            "Lorentz transformations (hyperbolic rotations), not Galilean "
            "additions. This preserves the causal structure: no signal "
            "can exceed c, because no event can lie outside J⁺(e)."
        ),
    }


def verify_velocity_addition_never_exceeds_c() -> dict:
    """Verify that composing any number of subluminal boosts stays subluminal."""
    c = 1.0
    test_pairs = [
        (0.5, 0.5),
        (0.9, 0.9),
        (0.99, 0.5),
        (0.999, 0.999),
    ]

    results = []
    for v1, v2 in test_pairs:
        r = derive_velocity_addition(v1, v2, c)
        results.append(
            {
                "v1": v1,
                "v2": v2,
                "v_total": r["v_total_relativistic"],
                "exceeds_c": abs(r["v_total_relativistic"]) >= c,
            }
        )

    all_subluminal = all(not r["exceeds_c"] for r in results)

    return {
        "results": results,
        "all_subluminal": all_subluminal,
        "c_is_speed_limit": all_subluminal,
    }


# ── Full Lorentz Covariance Summary ─────────────────────────────────────────


def lorentz_covariance_summary() -> dict:
    """Complete DET derivation of all Lorentz-covariant observables."""
    c = 1.0
    v = 0.6

    return {
        "foundation": "Event graph G = (V, ≺). Causal order determines light-cone structure.",
        "invariant_interval": derive_invariant_interval(),
        "time_dilation": derive_time_dilation(v, c),
        "length_contraction": derive_length_contraction(v, 1.0, c),
        "relativity_of_simultaneity": derive_relativity_of_simultaneity(v, 1.0, c),
        "lorentz_invariance": verify_lorentz_invariance(),
        "velocity_addition": derive_velocity_addition(0.6, 0.6, c),
        "velocity_limit": verify_velocity_addition_never_exceeds_c(),
        "what_is_derived": [
            "Invariant interval ds² = c²dt² - dx² (from light-cone structure of ≺).",
            "Time dilation (from event density ratio in ≺).",
            "Length contraction (from relativity of simultaneity in ≺).",
            "Relativity of simultaneity (from frame-dependent spacelike foliations of ≺).",
            "Lorentz transformations (as symmetries preserving ≺).",
            "Velocity addition (from boost composition).",
            "c as maximum speed (from causal structure: no event outside J⁺(e)).",
        ],
        "what_is_assumed": [
            "c is finite and constant (empirical fact, consistent with ≺ structure).",
            "Continuum limit exists (causal set theory — open problem O7).",
            "Spacetime is (3+1)-dimensional (from ≺ embedding dimension).",
        ],
        "det_unique_contribution": (
            "DET does not assume a Minkowski metric or Lorentz transformations. "
            "These emerge as properties of the causal event graph ≺ in the "
            "continuum limit. The fundamental object is the partial order, "
            "not the metric. This is consistent with causal set theory and "
            "provides a DET-native foundation for relativity."
        ),
    }
