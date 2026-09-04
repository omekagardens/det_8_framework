"""Synthetic special-relativity correspondence checks.

Status: SYNTHETIC_CORRESPONDENCE.  This module supplies 1+1-dimensional
Minkowski coordinates, the quadratic interval, a finite invariant speed, and
the standard Lorentz boost, then checks familiar identities.  It does not
derive any of those inputs from a DET event record, reconstruct a conformal
factor, or show that DET dynamics generate a manifoldlike causal set.

The historical ``derive_*`` names remain as API compatibility aliases.  Read
them as "evaluate the standard formula under the stated assumptions."  The
possible interpretation of a causal order as underlying Lorentzian geometry
is kept separate from what the calculations directly establish.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from det8.models.legacy_gravity_quarantine import SALVAGED_CORRESPONDENCE


CORRESPONDENCE_STATUS = SALVAGED_CORRESPONDENCE[__name__]


# ── Causal Structure Fundamentals ───────────────────────────────────────────


@dataclass
class CausalEvent:
    """An event with supplied 1+1-dimensional Minkowski coordinates."""

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
    """Evaluate the supplied Minkowski interval ds² = c²dt² - dx².

    For timelike separation (|dx| < c|dt|): ds² > 0.
    For spacelike separation: ds² < 0.
    For lightlike: ds² = 0.

    The quadratic form is an input to this correspondence calculation.
    """
    return c * c * dt * dt - dx * dx


# ── 1. Invariant Interval from Causal Order ─────────────────────────────────


def derive_invariant_interval() -> dict:
    """Classify supplied coordinate separations with the Minkowski interval.

    Given two events with coordinate separation (dt, dx), the causal
    relation is:
      - Timelike: |dx| < c|dt| → ds² > 0 (causally connectable)
      - Lightlike: |dx| = c|dt| → ds² = 0 (light cone boundary)
      - Spacelike: |dx| > c|dt| → ds² < 0 (causally disconnected)

    No event graph is inferred here: ``dt``, ``dx``, ``c``, and the interval
    form are all supplied by the synthetic generator.
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
        "derivation": (
            "Historical API field: the calculation assumes the Minkowski quadratic form; "
            "it does not derive it from a DET record."
        ),
        "classification": "SYNTHETIC_CORRESPONDENCE",
        "light_cone": "dx = ±c·dt  (boundary of J⁺(e))",
        "examples": examples,
    }


# ── 2. Time Dilation from Event Density ─────────────────────────────────────


def derive_time_dilation(velocity: float, c: float = 1.0) -> dict:
    """Evaluate standard time dilation for a supplied velocity and c.

    A clock at rest has worldline (t, 0). It participates in N events
    per coordinate time Δt.

    A clock moving at velocity v has worldline (t, vt). Its proper time
    between coordinate times t₁ and t₂ is:
      Δτ = ∫ √(1 - v²/c²) dt = Δt / γ  where γ = 1/√(1 - v²/c²).

    This function does not construct or count events.  An event-density
    account would be an additional interpretation requiring an independently
    specified sampling measure and clock observable.
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
            f"Conditional interpretation only: an independently justified event-count "
            f"clock would need a density ratio {dt_ratio:.4f}. This function does not "
            f"generate or observe that ratio."
        ),
    }


# ── 3. Length Contraction from Relativity of Simultaneity ────────────────────


def derive_length_contraction(
    velocity: float,
    rest_length: float = 1.0,
    c: float = 1.0,
) -> dict:
    """Evaluate standard length contraction in supplied Minkowski geometry.

    A rod of rest length L₀ lies along the x-axis in its rest frame.
    In a frame moving at velocity v relative to the rod:
    - The rod's endpoints are measured SIMULTANEOUSLY in the moving frame.
    - But events simultaneous in the moving frame are NOT simultaneous
      in the rest frame (relativity of simultaneity).
    - This shift in simultaneity makes the rod appear shorter.

    The Lorentz transformation gives: L = L₀ / γ.

    Optional causal-order interpretation:
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
            "Given the supplied Minkowski causal structure, different inertial "
            "frames choose different spacelike slices. This is not a DET derivation."
        ),
    }


# ── 4. Relativity of Simultaneity ───────────────────────────────────────────


def derive_relativity_of_simultaneity(
    velocity: float,
    separation: float = 1.0,
    c: float = 1.0,
) -> dict:
    """Evaluate standard relativity of simultaneity for a Lorentz boost.

    Two events simultaneous in frame S (Δt = 0, Δx = separation)
    are NOT simultaneous in frame S' moving at velocity v:

    Δt' = γ(Δt - v·Δx/c²) = -γ·v·separation/c² ≠ 0.

    Optional causal-order interpretation:
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
            "The calculation supplies the Lorentzian order and does not select a "
            "Track-B ontology of time."
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

    This function directly supplies the standard boost.  It verifies a
    correspondence only; no continuum causal graph is constructed.
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
        "lorentz_symmetry": (
            "The supplied Lorentz boost preserves the supplied Minkowski interval."
        ),
    }


# ── 6. Velocity Addition ────────────────────────────────────────────────────


def derive_velocity_addition(
    v1: float,
    v2: float,
    c: float = 1.0,
) -> dict:
    """Evaluate relativistic velocity addition from supplied Lorentz boosts.

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
            "can exceed c within the supplied Minkowski model."
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
    """Summarize the synthetic special-relativity correspondence checks."""
    c = 1.0
    v = 0.6

    return {
        "classification": "SYNTHETIC_CORRESPONDENCE",
        "foundation": (
            "Supplied 1+1 Minkowski coordinates, interval, invariant speed, and Lorentz boost."
        ),
        "invariant_interval": derive_invariant_interval(),
        "time_dilation": derive_time_dilation(v, c),
        "length_contraction": derive_length_contraction(v, 1.0, c),
        "relativity_of_simultaneity": derive_relativity_of_simultaneity(v, 1.0, c),
        "lorentz_invariance": verify_lorentz_invariance(),
        "velocity_addition": derive_velocity_addition(0.6, 0.6, c),
        "velocity_limit": verify_velocity_addition_never_exceeds_c(),
        "what_is_derived": [
            "Nothing DET-native; this legacy field is retained for API compatibility.",
        ],
        "what_is_reproduced": [
            "Minkowski interval classification.",
            "Time dilation and length contraction.",
            "Relativity of simultaneity.",
            "Lorentz-boost interval invariance.",
            "Relativistic velocity addition and its invariant speed bound.",
        ],
        "what_is_assumed": [
            "1+1-dimensional Minkowski coordinates and metric signature.",
            "A finite invariant speed c.",
            "The standard Lorentz transformation.",
            "No DET continuum limit is assumed to have been established.",
        ],
        "det_unique_contribution": (
            "No unique DET contribution is established by these calculations. "
            "They are known-answer tests that a future record-growth model must "
            "reproduce without assuming the target geometry."
        ),
    }
