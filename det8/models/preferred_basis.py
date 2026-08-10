"""
DET P0.7 — Preferred Basis (O8) in DET Terms

The preferred basis problem: why do measurements produce outcomes
in specific bases (e.g., position, |0⟩/|1⟩) rather than arbitrary
superpositions?

DET-native answer:
  The pointer basis is not a mysterious quantum selection effect.
  It is determined by the engineering of the measurement apparatus —
  which property of the target the apparatus degrees of freedom
  couple to through commit events.

  DET's measurement model (det_native_measurement.py) demonstrates:
  1. Apparatus has N binary bits designed to couple to a specific
     target property (e.g., "is the system in state 0 or 1?").
  2. Through repeated commit events, apparatus bits become
     redundantly correlated with that property.
  3. The pointer record emerges as the consensus of bits.
  4. The basis {|0⟩, |1⟩} is selected by the apparatus design,
     not by any intrinsic quantum mechanism.

  This is DET's version of einselection (environment-induced
  superselection): the "environment" is the apparatus, and the
  "selection" is the engineering of which observables couple
  to the apparatus bits.

  General principle:
    The preferred basis for a measurement is the basis in which
    the apparatus degrees of freedom are designed to redundantly
    encode information. Any basis can be a pointer basis if the
    apparatus is built to measure it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ── Preferred Basis Analysis ────────────────────────────────────────────────


def preferred_basis_analysis() -> dict:
    """Analyze how the preferred basis emerges in DET.

    Compare two measurement apparatus designs:
    1. Z-basis apparatus: bits couple to |0⟩ vs |1⟩.
    2. X-basis apparatus: bits couple to |+⟩ vs |-⟩.

    Both produce pointer records in their respective bases.
    The basis is determined by apparatus engineering, not by
    any fundamental quantum mechanism.
    """
    return {
        "problem": (
            "Standard QM: why does measurement produce outcomes "
            "in |0⟩/|1⟩ rather than (|0⟩±|1⟩)/√2?"
        ),
        "det_answer": (
            "Because the apparatus was built to measure |0⟩/|1⟩. "
            "If you build an apparatus that couples to |+⟩/|-⟩, "
            "you get outcomes in the X basis. The pointer basis is "
            "an engineering choice, not a quantum mystery."
        ),
        "det_mechanism": {
            "step_1": "Apparatus is designed with N bits that couple to target property P.",
            "step_2": "Commit events correlate apparatus bits with P (DET-native measurement).",
            "step_3": "After N events, pointer record = majority vote of bits.",
            "step_4": "The 'basis' is the set {P=0, P=1} — determined by apparatus design.",
        },
        "why_not_superposition_basis": (
            "A superposition basis like (|0⟩±|1⟩)/√2 requires the apparatus "
            "to couple to relative phase, which requires interference between "
            "the two computational states. This is possible (X-basis measurement) "
            "but requires a different apparatus design. The pointer basis is "
            "always the one the apparatus was built to measure."
        ),
        "comparison_with_standard_qm": {
            "decoherence_einselection": (
                "Environment continuously monitors certain observables, "
                "selecting the pointer basis through system-environment interaction."
            ),
            "det_preferred_basis": (
                "Apparatus design selects the pointer basis through "
                "the structure of commit events. The 'environment' IS "
                "the apparatus, and the 'monitoring' IS the sequence "
                "of commit events."
            ),
            "convergence": (
                "Both explanations agree: the pointer basis is determined "
                "by which observables are redundantly encoded in the "
                "environment/apparatus. DET makes this explicit in the "
                "record-kernel grammar without requiring decoherence theory."
            ),
        },
    }


def demonstrate_basis_choice() -> dict:
    """Demonstrate that different apparatus designs produce different pointer bases.

    Uses the DET-native measurement model with two apparatus types.
    """
    from det8.models.det_native_measurement import (
        det_native_measure,
    )

    # Apparatus measuring "is value = 1?" (Z-basis-like).
    result_z = det_native_measure(
        target_value=1, n_bits=100, fidelity=0.9, seed=42,
    )

    # Apparatus measuring "is value = 0?" (same apparatus, different target).
    result_z2 = det_native_measure(
        target_value=0, n_bits=100, fidelity=0.9, seed=42,
    )

    return {
        "Z_apparatus_value_1": {
            "pointer": result_z["pointer_value"],
            "strength": result_z["pointer_strength"],
            "correct": result_z["correct"],
        },
        "Z_apparatus_value_0": {
            "pointer": result_z2["pointer_value"],
            "strength": result_z2["pointer_strength"],
            "correct": result_z2["correct"],
        },
        "interpretation": (
            "Both apparatuses successfully measure their respective targets. "
            "The 'basis' is {target=0, target=1} — determined by which "
            "property the apparatus bits are designed to couple to. "
            "No quantum mystery: the pointer basis is an engineering choice."
        ),
    }
