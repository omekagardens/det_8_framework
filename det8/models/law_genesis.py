"""DET — F10 Law Genesis (fixed vs emergent law map L).

The question: is the law map L (R⁻ → (Ω, Σ, K, C)) a FIXED object that is
discovered, or an EMERGENT description — the minimal predictive compression of
the record — that can change as the record grows?

DET's κ is already defined as the minimal predictive compression of the causal
record (Fisher–Rao distance; the scalar κ is the rank-one special case). So DET
commits to the EMERGENT reading: the law is the compressed regularity, not a
fixed external object.  ONTOLOGY.md §2 states this explicitly ("Lawfulness is
not assumed … F10").

This module formalizes the dichotomy, the DET commitment, and the observable
anchor: law *stability* — whether the compressed regularity changes as the
record grows — which ties F10 to the RET longitudinal / change-point machinery.
"""

from __future__ import annotations

import math

from det8.models.relational_tomography import (
    GaussianParameterState,
    RelationalAction,
    change_point_mixture,
    change_probability,
    collapse_mixture,
    update_mixture_state,
)


def law_map_dichotomy() -> dict:
    """The two readings of L, stated cleanly."""

    return {
        "fixed": {
            "reading": "L is a single unchanging function R⁻ → (Ω, Σ, K, C).",
            "consequence": "laws are DISCOVERED; the compressed regularity never changes.",
        },
        "emergent": {
            "reading": "L is the minimal predictive compression of the record.",
            "consequence": "laws are COMPRESSED REGULARITIES; they can change as the record grows.",
        },
    }


def det_commitment() -> dict:
    """DET's κ-as-compression already commits to the emergent reading."""

    return {
        "kappa_definition": (
            "κ is the minimal predictive compression of the causal record "
            "(Fisher–Rao distance; the scalar is the rank-one special case)."
        ),
        "implication": (
            "if the law map L is the compressed regularity, and κ is its "
            "compression coordinate, then L is EMERGENT — a description, not a "
            "fixed external object. This is the 'novelty is the description' "
            "thesis applied to law itself."
        ),
        "commitment": "EMERGENT (compressed regularity)",
    }


def law_stability_probe(
    compression_values=(0.0, 0.0, 0.0, 0.0, 0.0, 2.5, 2.5, 2.5, 2.5, 2.5),
    *,
    drift_standard_deviation=2.5,
    change_prior=0.1,
    noise=0.2,
) -> dict:
    """The observable anchor: does the compressed regularity change?

    Treat the compression coordinate as a scalar record measured over time, and
    run the change-point detector (from relational_tomography). A fixed law shows
    no change-point; an emergent law shows one when the compression shifts.
    """

    probe = RelationalAction("compress", "science", (0.0,), {"kappa": (1.0,)})
    state = GaussianParameterState(("kappa",), (0.0,), ((1.0,),))
    trace = []
    for value in compression_values:
        updated = update_mixture_state(
            change_point_mixture(state, {"kappa": drift_standard_deviation}, change_prior),
            probe,
            (value,),
            noise,
        )
        probability = 1.0 if len(updated.components) == 1 else change_probability(updated)
        state = collapse_mixture(updated)
        trace.append(probability)

    peak = max(range(len(trace)), key=lambda i: trace[i])
    return {
        "compression_trace": compression_values,
        "change_probability_trace": trace,
        "change_peak_index": peak,
        "change_detected": max(trace) > 0.5,
        "interpretation": (
            f"the compressed regularity changes at index {peak} (change posterior "
            f"peaks at {max(trace):.3f}). A fixed law would show no peak; an "
            f"emergent law shows one when the compression shifts."
        ),
    }


def f10_resolution() -> dict:
    """The F10 account: DET commits to emergent L, and stability is observable."""

    probe = law_stability_probe()
    return {
        "question": "is the law map L fixed (discovered) or emergent (compressed)?",
        "dichotomy": law_map_dichotomy(),
        "det_commitment": det_commitment(),
        "observable_anchor": {
            "probe": "law stability — a change-point on the compressed regularity",
            "result": probe,
            "ties_to": "RET longitudinal / change-point machinery (relational_tomography)",
        },
        "resolution": (
            "DET resolves F10 in the EMERGENT direction: L is the compressed "
            "regularity (κ is its coordinate), not a fixed external object. The "
            "residual question is why the compression is *stable* (does not drift "
            "arbitrarily), which is the redundant-record stability question."
        ),
        "honest_boundary": (
            "this is a commitment + an observable anchor, not a derivation that "
            "L must be emergent. The 'fixed law' reading remains logically "
            "possible; DET rules it out by choice (κ is defined as compression)."
        ),
    }
