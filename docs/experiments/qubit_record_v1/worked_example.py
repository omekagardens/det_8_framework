"""Reproducible synthetic experiment; full trial data must stay outside checkout."""

import argparse
import sys
import tempfile
from dataclasses import replace
from fractions import Fraction as F
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
CHECKOUT = BUNDLE.parents[2]
sys.path.insert(0, str(BUNDLE))

from inference import ExperimentPlan, encode, fit, score
from qubit import nonselective_update, plus_probability
from records import canonical_json
from simulator import (
    DEFAULT_TRUTH,
    replay_sequence,
    simulate_fresh,
    simulate_sequence,
)


def _output_directory(output):
    output = Path(output).resolve()
    if output == CHECKOUT or CHECKOUT in output.parents:
        raise ValueError("full generated trial datasets must be outside the checkout")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("use a new or empty output directory; no existing data is overwritten")
    output.mkdir(parents=True, exist_ok=True)
    return output


def _write_json(output, name, value):
    with (output / name).open("x", encoding="utf-8") as stream:
        stream.write(canonical_json(encode(value)) + "\n")


def _write_records(output, name, records):
    with (output / name).open("x", encoding="utf-8") as stream:
        for row in records:
            stream.write(canonical_json(row.to_dict()) + "\n")


def run(output, seed=20260914):
    """Freeze and persist a training-only prediction before generating W data.

    The output JSON is an audit export, not a signed prediction or fit-input API.
    The score consumes the exact immutable fit object made here. Truth auditing
    is separate and is performed only after prediction and evaluation.
    """
    if type(seed) is not int:
        raise ValueError("seed must be a built-in integer")
    output = _output_directory(output)
    plan = ExperimentPlan()
    _write_json(output, "plan.json", plan.to_dict())

    training = simulate_fresh(plan, "training", seed=seed)
    _write_records(output, "training.jsonl", training)
    frozen = fit(plan, training)
    before = frozen.fingerprint
    _write_json(output, "predictions.json", frozen.to_dict())
    partial = fit(plan, tuple(r for r in training if r.setting in ("X", "Z")), axes=("X", "Z"))
    _write_json(output, "partial_xz_prediction.json", partial.to_dict())

    # W is generated only after both frozen prediction exports exist.
    held = simulate_fresh(plan, "heldout", seed=seed + 1)
    _write_records(output, "heldout.jsonl", held)
    report = score(frozen, held)
    if frozen.fingerprint != before:
        raise RuntimeError("scoring changed the frozen training prediction")
    _write_json(output, "score.json", report)

    serial = simulate_sequence(
        plan,
        DEFAULT_TRUTH["phase_plus"],
        ("Y", "Y", "Z", "Y"),
        seed=seed + 2,
        sequence_id="resolved-control",
    )
    erased = simulate_sequence(
        plan,
        DEFAULT_TRUTH["phase_plus"],
        ("Y", "Y", "Z"),
        seed=seed + 3,
        erase_at=0,
        sequence_id="erased-control",
    )
    # Fault injection is explicitly separate from valid simulated acquisition:
    # invert the same-axis repeated outcome to demonstrate retained mismatch.
    bad = (*serial[:1], replace(serial[1], outcome=-serial[0].outcome))
    _write_records(output, "sequential_records.jsonl", serial)
    _write_records(output, "sequential_erased.jsonl", erased)
    _write_records(output, "fault_injection_records.jsonl", bad)
    serial_report = {
        "resolved": replay_sequence(serial, DEFAULT_TRUTH["phase_plus"]),
        "erased": replay_sequence(erased, DEFAULT_TRUTH["phase_plus"]),
        "fault_injection": replay_sequence(bad, DEFAULT_TRUTH["phase_plus"]),
        "same_axis_repeatable": serial[0].outcome == serial[1].outcome,
        "known_nonselective_Z_then_Y_plus": {
            recipe: plus_probability(nonselective_update(DEFAULT_TRUTH[recipe], "Z"), "Y")
            for recipe in ("phase_plus", "phase_minus")
        },
    }
    _write_json(output, "sequential_summary.json", serial_report)

    # Generator truth, seeds, and recipes are never part of the observable rows.
    truth = {
        "provenance": "simulation-only; not apparatus calibration or inferred state",
        "training_seed": seed,
        "heldout_seed": seed + 1,
        "resolved_sequence_seed": seed + 2,
        "erased_sequence_seed": seed + 3,
        "erasure_probability_plus": F(1, 20),
        "erasure_probability_minus": F(1, 10),
        "actual_calibration_error": 0,
        "actual_preparation_drift": 0,
        "states": {
            name: {
                "bloch": state.r,
                "plus_laws": {s: plus_probability(state, s) for s in ("X", "Y", "Z", "W")},
            }
            for name, state in DEFAULT_TRUTH.items()
        },
    }
    _write_json(output, "truth_audit.json", truth)
    summary = encode(
        {
            "schema_version": 1,
            "status": "synthetic_worked_example_not_physical_validation",
            "seed": seed,
            "shots_per_stratum": plan.shots,
            "training_attempts": len(training),
            "heldout_attempts": len(held),
            "training_missing": sum(r.status == "missing" for r in training),
            "heldout_missing": sum(r.status == "missing" for r in held),
            "plan_sha256": plan.fingerprint,
            "prediction_sha256": before,
            "frozen_prediction_unchanged": frozen.fingerprint == before,
            "pipeline_order": [
                "plan",
                "training",
                "frozen_prediction",
                "heldout",
                "score",
                "truth_audit",
            ],
            "results": [
                {
                    "recipe_id": r.recipe_id,
                    "status": r.status,
                    "point_estimate": r.point_estimate,
                    "point_W_plus": r.point_probability,
                    "ideal_W_interval": r.ideal_probability_interval,
                    "held_frequency_band": r.frozen_frequency_band,
                    "same_conventional_point": r.point_estimate == r.conventional_point,
                }
                for r in frozen.results
            ],
            "partial_XZ": [
                {
                    "recipe_id": r.recipe_id,
                    "status": r.status,
                    "point_estimate": r.point_estimate,
                    "unresolved_alternatives": r.unresolved_alternatives,
                    "ideal_W_interval": r.ideal_probability_interval,
                }
                for r in partial.results
            ],
            "heldout_scores": report["results"],
            "sequential": serial_report,
        }
    )
    _write_json(output, "summary.json", summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="new/empty directory outside checkout")
    parser.add_argument("--seed", type=int, default=20260914)
    args = parser.parse_args()
    output = (
        args.output
        if args.output is not None
        else Path(tempfile.mkdtemp(prefix="qubit_record_v1-"))
    )
    summary = run(output, args.seed)
    print(canonical_json({"output_directory": str(output.resolve()), "summary": summary}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
