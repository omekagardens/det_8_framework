"""DET — the Quantum deadlock resolution (SKETCH → ADOPTED).

The Quantum deadlock: Everett reifies unactualized possibilities into parallel
universes; Copenhagen refuses to discuss the interval; Bohm hides outcomes in
inaccessible pilot waves. DET resolves it as:

    A quantum superposition is an actual, phase-bearing relational constraint
    on future possibilities — a real, open relation that does not contain its
    own outcome.

This module assembles the four pieces that move the resolution from SKETCH to
ADOPTED, each with an honest status:

  1. COMPLEX — ℂ is forced by (Ω ≠ 0, empirically) + (reversibility ⇒ U(m)).
     `why_complex.py`.  Status: MATH + empirical.
  2. GRADE-2 — the single-time measure has no third-order interference (I₃ = 0),
     empirically confirmed by three-slit.  `dkappa_decoherence.py`.
     Status: MATH + empirical.
  3. BORN (p = 2) — the squared magnitude is the UNIQUE power rule conserving
     probability under basis splits.  `born_rule_uniqueness.py`.  Status: MATH.
  4. OPEN — the constraint does not contain its own outcome (no fact register;
     NPF-C code-auditable).  The "no fact exists" reading is Status M (F8-OPEN).

Almost-quantum (the user's framing, stated precisely): the STATIC level is
real/almost-quantum (Tsirelson), while ℂ is DYNAMICAL — so static experiments
probe the real (grade-2) level and the complex structure is a dynamical
feature. No super-quantum correlation has ever been observed.
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
    |Σ c_i|² is bi-additive.  This ties p = 2 (born_rule_uniqueness) to the
    grade-2 structure (dkappa_decoherence, three-slit I₃ = 0).
    """

    c = list(amplitudes)

    def P(*idx):
        return abs(sum(c[i] for i in idx)) ** 2

    i3 = P(0, 1, 2) - P(0, 1) - P(0, 2) - P(1, 2) + P(0) + P(1) + P(2)
    return {
        "I3": i3,
        "born_rule_is_grade2": abs(i3) < 1e-12,
        "note": "|Σ c_i|² is bi-additive, so I₃ = 0: the Born rule is the grade-2 measure.",
    }


def pillars() -> dict:
    """The four pillars of the resolution, each with an honest status."""

    return {
        "complex": {
            "claim": "amplitudes are complex (phase-bearing)",
            "status": "MATH + empirical",
            "source": (
                "ℂ is forced by Ω ≠ 0 (empirically, Renou 2021 rules out real QM) "
                "plus reversibility (O ∩ Sp = U(m), a complex structure J = G⁻¹Ω)."
            ),
        },
        "grade2": {
            "claim": "the single-time measure is grade-2 (I₃ = 0)",
            "status": "MATH + empirical",
            "source": "three-slit bounds κ_Sorkin ≲ 10⁻⁴; the Born rule is bi-additive.",
        },
        "born": {
            "claim": "the probability rule is P = |c|² (L2, grade-2)",
            "status": "MATH — consistency check (conditional on L2 normalization)",
            "source": (
                "p = 2 is the unique power rule consistent with L2-normalized "
                "splits; Lp-normalized splits conserve for every p, so this is "
                "self-consistency, not a derivation (red-team R2-2)."
            ),
        },
        "open": {
            "claim": "the constraint does not contain its own outcome",
            "status": "Status M (F8-OPEN); NPF-C code-auditable",
            "source": (
                "no fact register exists in toy models (NPF-C); whether 'no fact "
                "about the outcome EXISTS' has no unique discriminator (F8-OPEN)."
            ),
        },
    }


def coherence_check() -> dict:
    """Verify the four pillars are mutually consistent (not just individually true).

    The two load-bearing consistencies:
      (a) Born (p = 2) IS the grade-2 structure — the squared magnitude is
          bi-additive, so its third-order interference vanishes;
      (b) ℂ is DYNAMICAL while the static level is REAL (almost-quantum) — the
          three-slit/Bell static level does not require the complex structure,
          so the grade-2 (static) and complex (dynamical) pillars do not collide.
    """

    born_grade2 = born_rule_is_grade2()
    born_unique = uniqueness_scan()
    observation = connection_to_observation()
    real_qm = real_part_gives_real_qm()

    born_p2_conserves_L2 = born_unique["conserving_under_L2_split"] == [2.0]
    return {
        "born_rule_is_grade2": born_grade2["born_rule_is_grade2"],
        "I3_from_born_rule": born_grade2["I3"],
        "born_p2_conserves_L2": born_p2_conserves_L2,
        "lp_split_conserves_for_all_p": born_unique["lp_split_conserves_for_all_p"],
        "static_level_is_real": "real-realizable" in observation["kinematics_are_real"],
        "complex_is_dynamical": "DYNAMICS" in observation["complex_is_dynamical"]
        or "dynamical" in observation["complex_is_dynamical"].lower(),
        "real_qm_not_classical": real_qm["real_QM_not_classical"],
        "coherent": (
            born_grade2["born_rule_is_grade2"]
            and born_p2_conserves_L2
            and real_qm["real_QM_not_classical"]
        ),
    }


def quantum_resolution() -> dict:
    """The full resolution: four pillars + coherence + the almost-quantum framing."""

    return {
        "deadlock": "Quantum (Many-Worlds / Copenhagen / Bohm)",
        "resolution": (
            "a superposition is an actual, phase-bearing relational constraint on "
            "future possibilities — a real, open relation that does not contain "
            "its own outcome"
        ),
        "pillars": pillars(),
        "coherence": coherence_check(),
        "almost_quantum": {
            "static_level": (
                "real / almost-quantum — Tsirelson: real unit vectors realize the "
                "(2,2,2) correlation set, so the static level that Bell and "
                "three-slit probe is real."
            ),
            "complex_is_dynamical": (
                "ℂ is forced by reversible dynamics (U(m)), a dynamical structure, "
                "not a static correlation."
            ),
            "precise_claim": connection_to_observation()["verdict"],
        },
        "provenance": {
            "complex": "MATH + empirical — why_complex.py (Renou 2021, O∩Sp=U(m))",
            "grade2": "MATH + empirical — dkappa_decoherence.py (three-slit null)",
            "born": "MATH — born_rule_uniqueness.py (p = 2 unique)",
            "open": "Status M — F8-OPEN (no unique discriminator); NPF-C code-auditable",
        },
        "honest_boundary": (
            "ADOPTED as a coherent account of the real, complex, grade-2, Born "
            "constraint; the 'open outcome' pillar remains Status M, not adopted — "
            "it is the interpretation of what the constraint lacks, and F8-OPEN "
            "shows no unique discriminator."
        ),
    }
