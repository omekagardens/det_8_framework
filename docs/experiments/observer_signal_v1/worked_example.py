"""Small deterministic signal experiment; generated traces stay outside checkout."""

import argparse
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
CHECKOUT = BUNDLE.parents[2]
sys.path.insert(0, str(BUNDLE))

from kinematics import Geometry, QTime, StaticTime
from local_records import canonical_json
from observer import infer, pulse_spacing
from sim import EmissionSpec, ObserverConfig, simulate


def fixtures():
    """Named supplied generators, not descriptions granted to either observer."""
    cases = []
    definitions = (
        ("static", 0, F(1, 2), StaticTime(0), StaticTime(1)),
        ("expanding", 1, F(1, 2), QTime(1), QTime(F(1, 4))),
        ("contracting", -1, F(1, 2), QTime(1), QTime(2)),
        ("horizon", 1, F(1), QTime(1), QTime(F(1, 4))),
        ("beyond_horizon", 1, F(3, 2), QTime(1), QTime(F(1, 4))),
        ("before_arrival_cutoff", 1, F(1, 2), QTime(1), QTime(F(3, 4))),
        ("colocated", 1, F(0), QTime(1), QTime(1)),
        ("reverse", 1, F(1, 2), QTime(1), QTime(F(1, 4))),
        ("same_redshift_different_delay", 2, F(1, 4), QTime(1), QTime(F(1, 4))),
    )
    for name, h, ell, emitted, cutoff in definitions:
        emitter, target = ("B", "A") if name == "reverse" else ("A", "B")
        observers = (ObserverConfig("A", 0, 7), ObserverConfig("B", ell, -3))
        emissions = (EmissionSpec("signal-1", emitter, target, emitted, crest_id="crest-1"),)
        cases.append((name, Geometry(H=h), observers, emissions, cutoff))
    cases.append(
        (
            "finite_pulses",
            Geometry(H=1),
            (ObserverConfig("A", 0, 7), ObserverConfig("B", F(1, 2), -3)),
            (
                EmissionSpec("pulse-1", "A", "B", QTime(1), crest_id="crest-1"),
                EmissionSpec("pulse-2", "A", "B", QTime(F(3, 4)), crest_id="crest-2"),
            ),
            QTime(F(1, 4)),
        )
    )
    return tuple(cases)


def _output_directory(output):
    output = Path(output).resolve()
    if output == CHECKOUT or CHECKOUT in output.parents:
        raise ValueError("generated signal traces must be outside checkout")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("use a new or empty directory; no existing traces overwritten")
    output.mkdir(parents=True, exist_ok=True)
    return output


def _write_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(canonical_json(value) + "\n")


def run(output):
    output = _output_directory(output)
    reports = []
    for name, geometry, observers, emissions, cutoff in fixtures():
        directory = output / name
        directory.mkdir()
        # Preannounced identities only: no times, separations, H or forecasts.
        plans = {
            o.observer_id: tuple(e.signal_id for e in emissions if e.target_id == o.observer_id)
            for o in observers
        }
        _write_json(
            directory / "observer_plan.json",
            {
                name: {"expected_signals": list(ids), "calibration_id": "ideal-v1"}
                for name, ids in plans.items()
            },
        )
        result = simulate(geometry, observers, emissions, cutoff)
        interpretations = {}
        for observer_id, rows in result.histories:
            with (directory / (observer_id + ".jsonl")).open("x", encoding="utf-8") as stream:
                for row in rows:
                    stream.write(canonical_json(row.to_dict()) + "\n")
            interpretations[observer_id] = infer(observer_id, rows, plans[observer_id], "ideal-v1")
        _write_json(directory / "observer_reports.json", interpretations)
        # Producer audit is exported only as a separate artifact, never passed
        # to infer(). Reinterpreting it cannot change already retained records.
        _write_json(directory / "model_audit.json", result.audit)
        pulse = None
        if name == "finite_pulses":
            receipts = tuple(r for r in result.history("B") if r.kind == "reception")
            pulse = pulse_spacing(*receipts)
            _write_json(directory / "finite_spacing.json", pulse)
        reports.append(
            {
                "fixture": name,
                "emissions": sum(
                    r.kind == "emission" for _, rows in result.histories for r in rows
                ),
                "receptions": sum(
                    r.kind == "reception" for _, rows in result.histories for r in rows
                ),
                "observer_reports": interpretations,
                "separate_model_forecasts": [
                    {
                        "signal_id": f["signal_id"],
                        "forecast": f["forecast"],
                        "receipt_inside_cutoff": f["receipt_inside_cutoff"],
                    }
                    for f in result.audit["forecast"]
                ],
                "finite_spacing": pulse,
            }
        )
    summary = {
        "status": "supplied_geometry_model_not_actualization_derivation_or_measurement",
        "clock_display": "rational_grid_plus_proved_log_and_rounding_error",
        "fixture_count": len(reports),
        "results": reports,
        "actualization_to_geometry_rule": None,
        "instantaneous_vs_finite_example": {
            "exact_spacing_ratio": "ln(2)/ln(4/3)",
            "strict_rational_power_certificate": ["16/9 < 2", "2 < 64/27"],
            "endpoint_instantaneous_stretches": ["2", "3"],
        },
    }
    _write_json(output / "summary.json", summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="new/empty directory outside checkout")
    args = parser.parse_args()
    output = (
        args.output
        if args.output is not None
        else Path(tempfile.mkdtemp(prefix="observer_signal_v1-"))
    )
    summary = run(output)
    print(canonical_json({"output_directory": str(output.resolve()), "summary": summary}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
