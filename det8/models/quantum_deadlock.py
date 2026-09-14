"""DET — a Status-M quantum interpretation with conditional formal checks.

The adopted interpretation reads a quantum superposition as a present,
phase-bearing relational constraint on future possibilities. This ontology
has no unique empirical discriminator. The formal examples do not establish
it, derive a physical complex field, or select a complete quantum theory.

Compatible complex structure is assumed; squared-norm composition yields
grade-two interference; the L2 split check is conditional on its normalization.
A finite three-slit null does not remove the extra strong-positivity or
operational premises. Real correlator coordinates, real operational QM and
almost-quantum behavior sets are distinct. The no-outcome-register property
is a scoped software statement (NPF-C), not proof of ontological openness.
Historical callable names are retained for compatibility.
"""

from __future__ import annotations

from det8.models.born_rule_uniqueness import uniqueness_scan
from det8.models.why_complex import (
    connection_to_observation,
    real_part_gives_real_qm,
)


def born_rule_is_grade2(amplitudes=(1.0, 1.0, 1.0)) -> dict:
    """The Born rule P = |Σ c_i|² is grade-2: its third-order interference vanishes.

    For three path amplitudes, the Born probabilities satisfy
    I₃ = P_012 − P_01 − P_02 − P_12 + P_0 + P_1 + P_2 = 0 exactly, because
    the squared norm expands into singleton and pair terms. Its associated
    pair kernel is biadditive; the set-function itself is quadratic. This is
    a conditional example, not uniqueness of the Born rule among grade-two measures.
    """

    c = list(amplitudes)

    def P(*idx):
        return abs(sum(c[i] for i in idx)) ** 2

    i3 = P(0, 1, 2) - P(0, 1) - P(0, 2) - P(1, 2) + P(0) + P(1) + P(2)
    return {
        "I3": i3,
        "born_rule_is_grade2": abs(i3) < 1e-12,
        "note": "The squared-norm set-function has only singleton and pair terms, so I3=0. This conditional grade-two example does not establish a converse or uniqueness.",
    }


def pillars() -> dict:
    """Keep formal premises and the adopted Status-M interpretation separate."""
    return {
        "complex": {
            "claim": "the chosen amplitude formalism uses complex scalars",
            "status": "CONDITIONAL_MATH; FIELD_SELECTION_OPEN",
            "source": "why_complex.py checks compatible forms and a counterexample to reversibility implying compatibility",
            "complex_field_selected": False,
        },
        "grade2": {
            "claim": "squared-norm composition gives I3=0 on disjoint alternatives",
            "status": "CONDITIONAL_MATH; PHYSICAL_RESTRICTION_SEPARATE",
            "source": "A pair-kernel requires strong positivity separately; finite interference bounds do not derive all QM",
            "strong_positivity_derived": False,
        },
        "born": {
            "claim": "p=2 conserves probability for an L2-normalized split",
            "status": "MATH — consistency check conditional on L2 normalization",
            "source": "Matching Lp-normalized splits conserve for every p; this does not select L2",
            "born_rule_derived": False,
        },
        "open": {
            "claim": "the interpreted constraint does not contain its own outcome",
            "status": "Status M; scoped NPF-C software property is separate",
            "source": "No stored outcome register in a toy model does not establish absence of an ontological future fact",
        },
    }


def coherence_check() -> dict:
    """Two compatible algebraic examples, not a proof of the ontology or full QM."""
    born_grade2 = born_rule_is_grade2()
    born_unique = uniqueness_scan()
    real_kernel = real_part_gives_real_qm()
    born_p2_conserves_L2 = born_unique["conserving_under_L2_split"] == [2.0]
    return {
        "born_rule_is_grade2": born_grade2["born_rule_is_grade2"],
        "I3_from_born_rule": born_grade2["I3"],
        "born_p2_conserves_L2": born_p2_conserves_L2,
        "lp_split_conserves_for_all_p": born_unique["lp_split_conserves_for_all_p"],
        "static_level_is_real": False,  # No blanket identification of physical static theory.
        "complex_is_dynamical": False,  # No scalar-field selection by dynamics alone.
        "real_qm_not_classical": real_kernel["real_QM_not_classical"],
        "coherent": (born_grade2["born_rule_is_grade2"] and born_p2_conserves_L2
                     and real_kernel["real_QM_not_classical"]),
        "scope": {"algebraic_examples_only": True, "ontology_validated": False,
                  "complex_field_selected": False, "full_qm_derived": False},
    }


def quantum_resolution() -> dict:
    """Assemble the adopted interpretation without promoting its formal premises."""
    return {
        "deadlock": "Quantum (Many-Worlds / Copenhagen / Bohm)",
        "resolution": "a superposition is interpreted as an actual, open relational constraint on future possibilities",
        "pillars": pillars(),
        "coherence": coherence_check(),
        "almost_quantum": {
            "static_level": "Static correlator projections do not identify real operational QM with almost-quantum behavior sets",
            "complex_is_dynamical": "Compatible forms give a conditional dynamical representation, not a scalar-field selection theorem",
            "precise_claim": connection_to_observation()["verdict"],
            "real_correlators_equal_almost_quantum": False,
        },
        "provenance": {
            "complex": "conditional compatible-form mathematics",
            "grade2": "conditional squared-norm identity; physical restriction separate",
            "born": "L2-normalization consistency check",
            "open": "Status M; scoped NPF-C code audit is separate",
        },
        "honest_boundary": "The adopted open-relational reading remains Status M. These algebraic checks neither validate the ontology nor derive full QM.",
        "full_qm_derived": False,
    }
