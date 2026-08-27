"""Neutron-lifetime counting adapter over the likelihood-agnostic evidence core.

The Gaussian RET core ingests published *aggregate* lifetimes. This adapter
exercises the evidence layer's Binomial and Poisson families on the
physically-natural raw observables instead: a bottle method counts surviving
neutrons, and a beam method counts decay products. It is a synthetic
demonstration (no collaboration raw data is ingested); its purpose is to show
that the raw counting likelihoods reproduce the same proton-pipeline
conclusion as the aggregate Gaussian core.
"""

from __future__ import annotations

import json
import math

from det8.models.relational_evidence import (
    BetaBinomial,
    Binomial,
    EvidenceHypothesis,
    EvidenceQuestion,
    EvidenceRecord,
    NegativeBinomial,
    Poisson,
    evidence_payload_digest,
    evidence_question_probabilities,
    initialize_evidence_posterior,
    update_evidence_posterior,
)

REFERENCE_LIFETIME_S = 877.75
BOTTLE_TRIALS = 1_000_000
BOTTLE_STORAGE_S = 1_000.0
# Detected beam decays when the lifetime equals the reference value. This scale
# is chosen so the ~1% beam/bottle discrepancy is many Poisson sigmas, matching
# the real measurements' relative precision.
BEAM_REFERENCE_COUNTS = 160_000.0
BEAM_SCALE = BEAM_REFERENCE_COUNTS * REFERENCE_LIFETIME_S


def _survival_probability(lifetime_s: float, storage_s: float) -> float:
    return math.exp(-storage_s / lifetime_s)


def _poisson_rate(lifetime_s: float) -> float:
    return BEAM_SCALE / lifetime_s


def _lifetime_hypothesis(
    name: str,
    lifetime_bottle: float,
    lifetime_proton_beam: float,
    lifetime_electron_beam: float,
    complexity: float,
) -> EvidenceHypothesis:
    """A point-predictive hypothesis carrying a lifetime per measurement class.

    Dark decay lengthens the beam beta-partial lifetime and shortens the bottle
    survival lifetime; a proton-readout systematic lengthens only the proton
    beam. The hypothesis states encode those signatures directly.
    """

    state = {
        "bottle": lifetime_bottle,
        "proton_beam": lifetime_proton_beam,
        "electron_beam": lifetime_electron_beam,
    }

    def predictive(action, state):
        if action.family == "bottle_survival":
            probability = _survival_probability(
                state["bottle"], float(action.coordinate)
            )
            return Binomial(BOTTLE_TRIALS, probability)
        if action.family == "proton_beam_decay":
            return Poisson(_poisson_rate(state["proton_beam"]))
        if action.family == "electron_beam_decay":
            return Poisson(_poisson_rate(state["electron_beam"]))
        raise ValueError("unknown counting action family: %s" % action.family)

    return EvidenceHypothesis(
        name=name,
        family="lifetime_counting",
        predictive=predictive,
        complexity=complexity,
        initial_state=state,
    )


def _robust_bottom() -> EvidenceHypothesis:
    """Broad reference that absorbs counts outside every declared lifetime."""

    def predictive(action, state):
        if action.family == "bottle_survival":
            return BetaBinomial(BOTTLE_TRIALS, 1.0, 1.0)
        return NegativeBinomial(1.0, 1.0e-5)

    return EvidenceHypothesis(
        name="M_bottom",
        family="lifetime_counting",
        predictive=predictive,
        complexity=0.0,
        robust=True,
    )


def run_neutron_counting_evidence() -> dict[str, object]:
    hypotheses = [
        _lifetime_hypothesis("common_lifetime", 877.75, 877.75, 877.75, 0.0),
        _lifetime_hypothesis("proton_pipeline", 877.75, 887.7, 877.75, 1.0),
        _lifetime_hypothesis("dark_decay", 867.75, 887.75, 887.75, 3.0),
    ]
    posterior = initialize_evidence_posterior(
        hypotheses,
        _robust_bottom(),
        complexity_penalty=0.8,
        open_prior=0.03,
    )

    bottle_observation = round(
        BOTTLE_TRIALS * _survival_probability(REFERENCE_LIFETIME_S, BOTTLE_STORAGE_S)
    )
    proton_observation = round(_poisson_rate(887.7))
    electron_observation = round(_poisson_rate(877.2))

    records = [
        EvidenceRecord(
            record_id="ucntau_bottle_survival",
            source_ids=("ucntau_survival",),
            action="bottle_survival_count",
            coordinate=BOTTLE_STORAGE_S,
            digest=evidence_payload_digest(bottle_observation),
            family="bottle_survival",
            scope="statistical",
            observation=bottle_observation,
        ),
        EvidenceRecord(
            record_id="nist_proton_beam_decay",
            source_ids=("nist_bl1_proton",),
            action="proton_beam_decay_count",
            coordinate=None,
            digest=evidence_payload_digest(proton_observation),
            family="proton_beam_decay",
            scope="statistical",
            observation=proton_observation,
        ),
        EvidenceRecord(
            record_id="jparc_electron_beam_decay",
            source_ids=("jparc_electron",),
            action="electron_beam_decay_count",
            coordinate=None,
            digest=evidence_payload_digest(electron_observation),
            family="electron_beam_decay",
            scope="statistical",
            observation=electron_observation,
        ),
    ]

    trace = []
    for record in records:
        posterior = update_evidence_posterior(posterior, record)
        trace.append(
            {
                "record": record.record_id,
                "observation": record.observation,
                "weights": dict(posterior.weights),
            }
        )

    question = EvidenceQuestion(
        "discrepancy_source",
        {
            "common_lifetime": "common_lifetime",
            "proton_pipeline": "proton_pipeline",
            "dark_decay": "dark_decay",
        },
    )
    return {
        "fixture": "neutron lifetime raw-count evidence",
        "reference_lifetime_s": REFERENCE_LIFETIME_S,
        "observed_counts": {
            "bottle_survivors": bottle_observation,
            "nist_proton_decays": proton_observation,
            "jparc_electron_decays": electron_observation,
        },
        "assimilation_trace": trace,
        "final_weights": dict(posterior.weights),
        "question_probabilities": evidence_question_probabilities(
            posterior, question
        ),
        "prequential_log_scores": {
            name: float(value)
            for name, value in posterior.cumulative_log_scores.items()
        },
        "warning": (
            "Counts are synthetic roundings of the published lifetimes; "
            "no collaboration raw data is ingested."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_neutron_counting_evidence(), indent=2))
