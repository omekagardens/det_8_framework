"""
DET v8.0 — Falsification Ladder & Data Guardrail (Option B)

DET is a participation/measurement theory with ONE falsifiable prediction:
the κ-Π clock anomaly (Δν/ν = λ_P·κ / (1 + λ_P·κ)). This module defines:

1. The FALSIFICATION LADDER — the ordered, DET-native experiments that test
   (and can falsify) the claim, with explicit decision rules.
2. The DATA GUARDRAIL — every external dataset was built under a DIFFERENT
   theory (GR, ΛCDM, materials science), so only its theory-independent
   OBSERVED quantity is admissible; its theory-dependent interpretation is
   quarantined.
3. The DECISION LOGIC — given lab results, classify the outcome as
   falsified / bounded / consistent / confirmed.

Gravity-emergence note: gravity is NOT a current DET claim, but the door is
left open. "Does κ source or modify gravity?" is an OPEN research frontier,
not a rejected hypothesis; the retired gravity modules are archived so the
question can be revisited if a DET-native mechanism ever emerges.

Operational layer: SI conversion is via det_units (clock Δν/ν ↔ λ_P, proxy
R/R₀ ↔ κ). The fractional quantities used here are dimensionless and
anchor-free.
"""

from __future__ import annotations

import math


# ── Falsification ladder ────────────────────────────────────────────────────


def falsification_ladder() -> list[dict]:
    """The ordered, DET-native experiments that test the clock-anomaly claim.

    Each step names the question, the measurement, and the explicit
    falsification / confirmation conditions.
    """
    return [
        {
            "step": 1,
            "name": "κ-vs-defect-density discriminator (F9)",
            "question": "Is κ anything beyond ordinary material history?",
            "measurement": "recovery timescale τ_rec across temperature T",
            "falsifies_if": (
                "τ_rec tracks the Arrhenius annealing law τ_anneal = τ_0·exp(E_a/k_B T) "
                "⇒ κ = defect density ⇒ the κ-as-independent-field reading collapses "
                "(the record-kernel ontology is unaffected)"
            ),
            "confirms_if": (
                "τ_rec is T-independent (distinct from thermal annealing) "
                "⇒ κ is a distinct field"
            ),
            "module": "kappa_discriminator.py",
        },
        {
            "step": 2,
            "name": "Structural-proxy calibration",
            "question": "Can κ be measured independently of the clock?",
            "measurement": (
                "residual after regressing probe response against all known "
                "material variables (density, defect density, stress, …)"
            ),
            "falsifies_if": (
                "residual = 0 after the known-physics regression ⇒ κ = ordinary "
                "materials science ⇒ no independent κ"
            ),
            "confirms_if": "nonzero residual, cross-validated, reproducible",
            "module": "structural_proxy.py",
        },
        {
            "step": 3,
            "name": "Clock comparison",
            "question": "Does κ change the clock rate?",
            "measurement": (
                "fractional frequency difference Δν/ν between two κ-prepared "
                "clocks (κ_A = 0 reference, κ_B = κ)"
            ),
            "falsifies_if": (
                "null at precision σ ⇒ λ_P·κ < σ (λ_P bounded from above; "
                "the prediction is null at that precision)"
            ),
            "confirms_if": "Δν/ν = λ_P·κ/(1+λ_P·κ) at ≥5σ with the correct sign",
            "module": "clock_experiment.py",
        },
    ]


# ── Data guardrail ──────────────────────────────────────────────────────────


DATA_PROVENANCE = {
    "atomic_clock_comparison": {
        "origin_theory": "GR + quantum metrology",
        "observed_quantity": "fractional frequency ratio Δν/ν (theory-independent)",
        "derived_quantity": "gravitational redshift / relativistic corrections (GR-dependent)",
        "safe_use": "constrain λ_P·κ via Δν/ν = λ_P·κ/(1+λ_P·κ)",
    },
    "material_response": {
        "origin_theory": "materials science (elasticity, defect theory)",
        "observed_quantity": "probe response R (hardness, resistivity, …) (theory-independent)",
        "derived_quantity": "dislocation density / residual stress (materials-science-dependent)",
        "safe_use": "structural-proxy input: κ = 1 − (R/R₀)^(1/p)",
    },
    "sparc_rotation_curves": {
        "origin_theory": "ΛCDM (dark-matter halos)",
        "observed_quantity": "velocity field v(r) (theory-independent)",
        "derived_quantity": "dark-matter halo profile (ΛCDM-dependent)",
        "safe_use": "N/A under Option B (gravity program retired) — archived",
    },
    "eotvos_eta": {
        "origin_theory": "GR / equivalence principle",
        "observed_quantity": "Eötvös ratio η (theory-independent)",
        "derived_quantity": "bound on a fifth force (model-dependent)",
        "safe_use": "N/A under Option B (no fifth force in DET) — informational",
    },
}


def data_guardrail(dataset_key: str) -> dict:
    """Return the provenance + safe-use label for an external dataset.

    The guardrail is: only the OBSERVED quantity is admissible; the DERIVED
    quantity (valid only under the originating theory) is quarantined.
    """
    if dataset_key not in DATA_PROVENANCE:
        raise KeyError(f"unknown dataset: {dataset_key}")
    entry = dict(DATA_PROVENANCE[dataset_key])
    entry["dataset"] = dataset_key
    entry["rule"] = (
        "Use ONLY the observed_quantity. The derived_quantity is valid only "
        "under the origin_theory, not under DET."
    )
    return entry


# ── Decision logic ──────────────────────────────────────────────────────────


def classify_clock_result(
    measured_shift: float,
    sigma: float = 1e-18,
    required_sigma: float = 5.0,
) -> dict:
    """Classify a clock-comparison result (the sole prediction).

    measured_shift = Δν/ν (dimensionless, SI-observed ratio).
    sigma = measurement precision (fractional).
    """
    if sigma <= 0.0:
        raise ValueError("sigma must be > 0")
    significance = abs(measured_shift) / sigma

    if significance < 1.0:
        verdict = "null"
        detail = (
            f"|Δν/ν| = {measured_shift:.2e} < σ = {sigma:.0e} ⇒ λ_P·κ < σ. "
            f"The prediction is not confirmed at this precision; λ_P is bounded."
        )
    elif significance >= required_sigma and measured_shift > 0.0:
        verdict = "consistent"
        detail = (
            f"Δν/ν = {measured_shift:.2e} at {significance:.1f}σ with the correct "
            f"sign ⇒ consistent with Δν/ν = λ_P·κ/(1+λ_P·κ)."
        )
    else:
        verdict = "anomalous"
        detail = (
            f"|Δν/ν| = {measured_shift:.2e} at {significance:.1f}σ but wrong sign "
            f"or below {required_sigma:.0f}σ ⇒ not the predicted signal."
        )

    return {
        "measured_shift": measured_shift,
        "sigma": sigma,
        "significance": significance,
        "verdict": verdict,
        "detail": detail,
    }


def classify_discriminator_result(
    recovery_ratio: float,
    arrhenius_expected: float,
    tolerance: float = 0.1,
) -> dict:
    """Classify the F9 discriminator result.

    recovery_ratio = measured τ_rec(T_high)/τ_rec(T_low).
    arrhenius_expected = the ratio predicted by thermal annealing.
    κ is distinct iff recovery_ratio ≈ 1 (T-independent); it is defect density
    iff recovery_ratio ≈ arrhenius_expected (tracks the Arrhenius law).
    """
    tracks_arrhenius = abs(recovery_ratio - arrhenius_expected) <= tolerance * abs(arrhenius_expected)
    t_independent = abs(recovery_ratio - 1.0) <= tolerance

    if tracks_arrhenius and not t_independent:
        verdict = "falsified"
        detail = (
            f"recovery ratio {recovery_ratio:.2e} tracks the Arrhenius law "
            f"({arrhenius_expected:.2e}) ⇒ κ = defect density ⇒ DET is a relabeling."
        )
    elif t_independent and not tracks_arrhenius:
        verdict = "distinct"
        detail = (
            f"recovery ratio ≈ 1 (T-independent) ⇒ κ is distinct from thermal "
            f"annealing ⇒ proceed to proxy calibration."
        )
    else:
        verdict = "inconclusive"
        detail = "recovery ratio is ambiguous between the two hypotheses."

    return {
        "recovery_ratio": recovery_ratio,
        "arrhenius_expected": arrhenius_expected,
        "verdict": verdict,
        "detail": detail,
    }


# ── Gravity-emergence note ──────────────────────────────────────────────────


def gravity_emergence_note() -> dict:
    """Record that gravity is not a current claim but the door is open."""
    return {
        "status": "OPEN research frontier (not a rejected hypothesis)",
        "current_position": (
            "Option B (Round 6): κ couples only to participation; gravity is "
            "standard GR and dark matter is standard."
        ),
        "revisit_condition": (
            "A DET-native mechanism that sources or modifies gravity may be "
            "revisited IF and only if it is DERIVED from DET primitives and "
            "survives the same falsification discipline (equivalence principle, "
            "Eötvös, rotation curves) — not imported from a non-DET theory."
        ),
        "archived_modules": (
            "gravity_v2.py, sparc_analysis.py, cluster_dynamics.py, "
            "post_newtonian.py, kappa_derivation.py, det_gravity.py, "
            "gravity_experiment.py — retained for audit, not active claims."
        ),
    }


# ── Claim register (Option B) ───────────────────────────────────────────────


def claim_register() -> dict:
    """The active DET claims under Option B, with status labels."""
    return {
        "clock_anomaly": {
            "claim": "Δν/ν = λ_P·κ/(1+λ_P·κ) — two κ-prepared clocks tick at different rates.",
            "status": "PR (pre-registered, falsifiable)",
            "falsifies": "null at precision σ ⇒ λ_P·κ < σ",
        },
        "structural_proxy": {
            "claim": "κ can be measured independently via a calibrated probe response R(κ) = R₀(1−κ)^p.",
            "status": "P (proposed; gated on F9 discriminator)",
            "falsifies": "zero residual after known-physics regression",
        },
        "kappa_distinct_field": {
            "claim": "κ is a distinct field, not ordinary defect density.",
            "status": "P (proposed; gated on temporal signature)",
            "falsifies": "τ_rec tracks thermal annealing",
        },
        "gravity_emergence": {
            "claim": "κ does NOT source or modify gravity (current).",
            "status": "OPEN frontier (not claimed)",
            "falsifies": "N/A — no gravity claim is made",
        },
    }


# ── Ontology-first framing ──────────────────────────────────────────────────


def ontology_first_note() -> dict:
    """The framing: the ontology is primary; the probes are optional.

    This is Team A's rebuttal to the red-team's "F9 falsified ⇒ DET is a
    relabeling" framing — which conflated the PROBE with the ONTOLOGY.
    """
    return {
        "ontology": (
            "Relational record-kernel unification: event graph ≺ → record R → "
            "law map L → commit kernel K → participation aperture Π."
        ),
        "primary_content": (
            "The ontology resolves the four deadlocks (time, quantum, agency, "
            "history) in one framework. This is DET's primary content."
        ),
        "probe_status": (
            "The clock anomaly is an OPTIONAL empirical probe of ONE physical "
            "realization (κ as an independent field). It is not the point, and "
            "DET's value does not depend on λ_P ≠ 0."
        ),
        "what_falsification_means": (
            "A 'falsified' probe result collapses only the κ-as-independent-field "
            "reading; the ontology stands. Even 'κ = defect density' is an "
            "ontological RESULT: structural history = material history."
        ),
    }


def ontology_claim_register() -> dict:
    """The ontology's own epistemic status (R7-D).

    The ontology is not empirically falsifiable, so it needs its own evaluation
    criteria. For each of the four deadlocks, mark whether the resolution is
    DERIVED from DET primitives, ADOPTED from an existing proposal, a SKETCH, or
    a RELABELING of standard physics. This is the ontological analogue of the
    MODEL_CARD §6 physics claim register.
    """
    return {
        "evaluation_criteria": [
            "internal coherence — no contradictions (partially checked by tests)",
            "genuine unification — must do explanatory work, not relabel",
            "non-trivial deadlock resolution — derived vs adopted vs relabeled",
        ],
        "time": {
            "deadlock": "growing block vs relativity of simultaneity",
            "resolution": "the record grows at J^-(e); the 'Crystallizing Block'",
            "status": "ADOPTED (Ellis 2014) — borrowed, not DET-native",
        },
        "quantum": {
            "deadlock": "where do continuous complex amplitudes come from?",
            "resolution": "emergent statistics of discrete-sign kernel roots",
            "status": "SKETCH (not a proof; U(1) emergence is an open program)",
        },
        "agency": {
            "deadlock": "open becoming vs primitive stochasticity (F8-OPEN)",
            "resolution": "commit kernel K + Status M quarantine",
            "status": "QUARANTINED (the ontological gloss is M, not resolved)",
        },
        "history": {
            "deadlock": "κ-recovery vs the Second Law",
            "resolution": "free energy ψ = ψ₀ + ½K(κ−κ_eq)² drives recovery",
            "status": "RELABELED (standard internal-variable free energy)",
        },
        "honest_summary": (
            "None of the four deadlock resolutions is a DET-native derivation: "
            "one is ADOPTED (time), one is a SKETCH (quantum), one is "
            "QUARANTINED (agency), one is RELABELED (history). This is not "
            "disqualifying — a coherent SYNTHESIS of existing proposals is "
            "itself a contribution — but the framework should say so rather "
            "than 'four deadlocks resolved'."
        ),
    }


def run_full_ladder(
    proxy_true_kappa: float = 0.5,
    clock_lambda_p: float = 1e-12,
    clock_kappa: float = 0.5,
    seed: int = 42,
) -> dict:
    """End-to-end run of the three probes, framed ontology-first.

    Exercises the full testing path — F9 discriminator (temporal signature),
    structural-proxy ontology test, clock sensitivity — and reports it with the
    ontology-first framing: the probes test ONLY the κ-as-independent-field
    reading; the record-kernel ontology is never at stake.
    """
    from det8.models.kappa_discriminator import discriminator_signature, f9_specification
    from det8.models.structural_proxy import proxy_calibration_protocol
    from det8.models.clock_experiment import clock_sensitivity_table

    # Probe 1: F9 discriminator (temporal signature).
    sig = discriminator_signature()
    spec = f9_specification()

    # Probe 2: structural-proxy ontology test.
    proxy = proxy_calibration_protocol(true_kappa=proxy_true_kappa, seed=seed)

    # Probe 3: clock sensitivity.
    table = clock_sensitivity_table()

    return {
        "ontology_first": ontology_first_note(),
        "probe_1_discriminator": {
            "temporal_signature": sig["verdict"],
            "power": spec["power"]["detectable_5sigma"],
        },
        "probe_2_proxy": {
            "ontology_verdict": proxy["ontology_test"]["verdict"],
            "kappa_inferred": proxy["kappa_inferred_from_residual"],
        },
        "probe_3_clock": {
            "noise_floor": table["noise_floor"],
            "interpretation": table["interpretation"],
        },
        "overall": (
            "The three probes test ONLY the κ-as-independent-field reading. "
            "Whatever their outcomes, the record-kernel ontology stands — "
            "the probes are optional, the ontology is primary."
        ),
    }


# ── Parameter sweep: where do the probes bite? ──────────────────────────────


def probe_bites(
    tau_rec_s: float = 1e4,
    E_a_eV: float = 1.0,
    noise_std: float = 0.01,
    lambda_p: float = 1e-12,
    kappa: float = 0.5,
    T_low_K: float = 300.0,
    T_high_K: float = 900.0,
    tau0_s: float = 1e-13,
) -> dict:
    """Which probes are DECISIVE for a given parameter setting.

    probe 1 (discriminator): decisive iff the Arrhenius log-ratio over the
        temperature sweep is resolvable at 5σ (N=10, σ_logτ=0.5).
    probe 2 (proxy): decisive iff the κ residual (~κ of the response) exceeds
        3σ of the probe noise.
    probe 3 (clock): decisive iff λ_P·κ/(1+λ_P·κ) exceeds 5× the noise floor.
    """
    from det8.models.kappa_discriminator import annealing_timescale
    from det8.models.clock_experiment import ClockNoiseModel, EnvironmentalNoise

    # Probe 1: Arrhenius separation resolvable?
    tau_low = annealing_timescale(T_low_K, E_a_eV, tau0_s)
    tau_high = annealing_timescale(T_high_K, E_a_eV, tau0_s)
    log_ratio = math.log(tau_low / tau_high) if tau_high > 0 else float("inf")
    se = 0.5 / math.sqrt(10.0)
    probe1 = (log_ratio / se) >= 5.0 if se > 0 else False

    # Probe 2: κ residual > 3σ (κ signal ≈ κ · R₀).
    probe2 = (kappa * 1.0) > 3.0 * noise_std

    # Probe 3: λ_P·κ > 5× noise floor.
    cm = ClockNoiseModel()
    en = EnvironmentalNoise()
    noise_floor = math.sqrt(cm.sigma_F**2 + en.total_environmental()**2)
    y = lambda_p * kappa / (1.0 + lambda_p * kappa)
    probe3 = abs(y) > 5.0 * noise_floor

    return {
        "tau_rec_s": tau_rec_s,
        "E_a_eV": E_a_eV,
        "noise_std": noise_std,
        "lambda_p": lambda_p,
        "probe_1_discriminator": probe1,
        "probe_2_proxy": probe2,
        "probe_3_clock": probe3,
        "probe1_log_ratio": log_ratio,
        "probe2_signal_to_noise": kappa / noise_std if noise_std > 0 else float("inf"),
        "probe3_signal": y,
        "probe3_noise_floor": noise_floor,
    }


def sweep_probes(
    E_a_values: tuple[float, ...] = (0.5, 1.0, 2.0),
    noise_values: tuple[float, ...] = (0.001, 0.01, 0.05, 0.2),
    lambda_p_values: tuple[float, ...] = (1e-18, 1e-16, 1e-14),
) -> dict:
    """Map where each probe bites across the key parameter knobs.

    Sweeps E_a (discriminator), noise (proxy), and λ_P (clock) and reports,
    for each combination, which probes are decisive. The summary states the
    approximate threshold at which each probe transitions from decisive to
    inconclusive.
    """
    rows = []
    for E_a in E_a_values:
        for noise in noise_values:
            for lp in lambda_p_values:
                b = probe_bites(E_a_eV=E_a, noise_std=noise, lambda_p=lp)
                rows.append(
                    {
                        "E_a_eV": E_a,
                        "noise_std": noise,
                        "lambda_p": lp,
                        "p1_discriminator": b["probe_1_discriminator"],
                        "p2_proxy": b["probe_2_proxy"],
                        "p3_clock": b["probe_3_clock"],
                    }
                )

    # Thresholds (analytic):
    #   p1: log_ratio ≥ 5·(0.5/√10) ≈ 0.79  ⇒  E_a ≳ 0.03 eV always decisive.
    #   p2: noise ≤ κ/3 ≈ 0.167.
    #   p3: λ_P·κ/(1+λ_P·κ) ≥ 5·noise_floor ≈ 8.7e-18  ⇒  λ_P ≳ 2e-17 (κ=0.5).
    e_a_threshold = 0.79 * (8.617333262e-5) / (1.0 / 300.0 - 1.0 / 900.0)
    noise_threshold = 0.5 / 3.0
    lambda_p_threshold = 5.0 * probe_bites(lambda_p=1e-12)["probe3_noise_floor"] * 2.0

    return {
        "rows": rows,
        "n_combinations": len(rows),
        "thresholds": {
            "p1_discriminator": f"always decisive for E_a ≳ {e_a_threshold:.3f} eV (Arrhenius separation is huge)",
            "p2_proxy": f"decisive iff probe noise ≤ κ/3 ≈ {noise_threshold:.3f}",
            "p3_clock": f"decisive iff λ_P·κ/(1+λ_P·κ) ≥ 5×noise_floor (λ_P ≳ 2e-17 for κ=0.5)",
        },
        "interpretation": (
            f"Across {len(rows)} settings, the probes bite in complementary "
            f"regimes: the discriminator is decisive for essentially all E_a "
            f"(Arrhenius separation is enormous), the proxy bites when noise ≤ "
            f"{noise_threshold:.3f}, and the clock bites when λ_P·κ exceeds the "
            f"~10⁻¹⁷ noise floor. The clock is the hardest probe: it needs both "
            f"a κ measurement AND a large enough λ_P."
        ),
    }
