"""Explicit simulation truth, never imported by the inference module.

The simulator adopts ideal projective qubit preparations/measurements. A binary
read precedes possibly outcome-dependent erasure. It is not experimental data.
"""

from fractions import Fraction as F
from random import Random
from types import MappingProxyType

from qubit import Bloch, ModelMismatch, plus_probability, selective_update
from records import ERASURE_MODEL, Command, TrialRecord, fresh_identity, validate_sequence

DEFAULT_TRUTH = MappingProxyType(
    {
        "phase_plus": Bloch((0, F(3, 5), 0)),
        "phase_minus": Bloch((0, -F(3, 5), 0)),
        "mixed": Bloch((F(1, 3), -F(2, 5), F(1, 4))),
    }
)


def _probability(value):
    if type(value) is int:
        value = F(value)
    if type(value) is not F or not 0 <= value <= 1:
        raise ValueError("simulation probabilities must be exact and in [0,1]")
    return value


def _draw(rng, probability):
    probability = _probability(probability)
    return rng.randrange(probability.denominator) < probability.numerator


def _rng(seed):
    if type(seed) is not int:
        raise ValueError("simulation seed must be a built-in integer")
    return Random(seed)


def simulate_fresh(
    plan, split, truth=None, seed=20260914, erasure_plus=F(1, 20), erasure_minus=F(1, 10)
):
    """Return observable attempts only; no true vector, latent outcome or RNG.

    Each setting uses a distinct successful preparation. The recipe is a label,
    not its truth vector. The estimator receives only the returned records.
    """
    if split not in ("training", "heldout"):
        raise ValueError("fresh simulation has training and heldout splits only")
    truth = DEFAULT_TRUTH if truth is None else truth
    if set(truth) != set(plan.recipe_ids) or any(type(s) is not Bloch for s in truth.values()):
        raise ValueError("supply a physical truth state for every planned recipe")
    ep, em = _probability(erasure_plus), _probability(erasure_minus)
    rng = _rng(seed)
    rows = []
    for recipe in plan.recipe_ids:
        state = truth[recipe]
        for setting in ("X", "Y", "Z") if split == "training" else ("W",):
            for index in range(plan.shots):
                trial, prep, record_id = fresh_identity(
                    plan.session_id, recipe, split, setting, index
                )
                command = Command(trial + "/command/0", "prepare:" + prep, setting)
                outcome = 1 if _draw(rng, plus_probability(state, setting)) else -1
                missing = _draw(rng, ep if outcome == 1 else em)
                rows.append(
                    TrialRecord(
                        record_id,
                        trial,
                        prep,
                        recipe,
                        plan.session_id,
                        split,
                        0,
                        "prepare:" + prep,
                        (command,),
                        setting,
                        plan.frame_id,
                        plan.calibration_id,
                        plan.provenance,
                        ERASURE_MODEL,
                        "successful",
                        "missing" if missing else "detected",
                        True,
                        None if missing else outcome,
                        "outcome_erased" if missing else None,
                    )
                )
    return tuple(rows)


def simulate_sequence(
    plan, initial, settings, seed=20260914, erase_at=None, sequence_id="serial-control"
):
    """One serial preparation; stop at the first erased result, without update.

    The intended settings list may be longer than the actual retained prefix.
    No record is created for an unattempted continuation.
    """
    if (
        type(settings) is not tuple
        or not settings
        or any(s not in ("X", "Y", "Z", "W") for s in settings)
    ):
        raise ValueError("supply a nonempty ordered setting tuple")
    if type(initial) is not Bloch:
        raise TypeError("supply a physical initial model")
    if (
        type(sequence_id) is not str
        or not sequence_id
        or len(sequence_id) > 48
        or any(not (c.isascii() and (c.isalnum() or c in "_.-")) for c in sequence_id)
    ):
        raise ValueError("sequence_id must be a canonical nominal acquisition label")
    if erase_at is not None and (type(erase_at) is not int or not 0 <= erase_at < len(settings)):
        raise ValueError("erase_at must name an actual planned step")
    rng, state = _rng(seed), initial
    trial = plan.session_id + "/sequential/" + sequence_id
    prep = "prep:" + trial
    commands, rows = [], []
    for step, setting in enumerate(settings):
        command_precursor = commands[-1].command_id if commands else "prepare:" + prep
        commands.append(Command(trial + f"/command/{step}", command_precursor, setting))
        outcome = 1 if _draw(rng, plus_probability(state, setting)) else -1
        missing = step == erase_at
        row = TrialRecord(
            "record:" + trial + f"/{step}",
            trial,
            prep,
            "serial-control",
            plan.session_id,
            "sequential",
            step,
            rows[-1].record_id if rows else "prepare:" + prep,
            tuple(commands),
            setting,
            plan.frame_id,
            plan.calibration_id,
            plan.provenance,
            ERASURE_MODEL,
            "successful",
            "missing" if missing else "detected",
            True,
            None if missing else outcome,
            "outcome_erased" if missing else None,
        )
        rows.append(row)
        if missing:
            break
        state = selective_update(state, setting, outcome)
    return validate_sequence(tuple(rows))


def replay_sequence(records, initial):
    """Interpret retained records against a supplied model, never repair them.

    Missing or failed acquisitions have no selected branch here. A zero-model-
    probability observed outcome remains in the records and is a mismatch.
    """
    rows = validate_sequence(records)
    if type(initial) is not Bloch:
        raise TypeError("supply a physical initial model")
    state = initial
    result = {
        "status": "resolved",
        "retained_record_ids": tuple(r.record_id for r in rows),
        "residual": None,
        "mismatch_record_id": None,
    }
    for row in rows:
        if (
            row.preparation_status != "successful"
            or row.status != "detected"
            or row.acquisition_model != ERASURE_MODEL
        ):
            result["status"] = "unresolved_no_selected_update"
            return result
        try:
            state = selective_update(state, row.setting, row.outcome)
        except ModelMismatch:
            result["status"] = "model_mismatch_zero_probability"
            result["mismatch_record_id"] = row.record_id
            return result
    result["residual"] = state.r
    return result
