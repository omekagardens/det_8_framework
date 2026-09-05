"""Capture/replay QR-03 exact predictive-history equivalence and its controls."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import sys
import time
from fractions import Fraction
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import predictive
import reference_qr03

ex = predictive.ex
SOURCES = (
    "README.md",
    "predictive.py",
    "reference_qr03.py",
    "study.py",
    "test_qr03.py",
    "../qr-01-quantum-records-2026-09-05/exact.py",
    "../qr-01-quantum-records-2026-09-05/reference.py",
)
PRIORS = {
    "qr-01-quantum-records-2026-09-05": "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b",
    "qr-02-record-coarse-graining-2026-09-05": "b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c",
}
RESULT = ROOT / "results.json"
RESEARCH_BASE_COMMIT = "e3c891e8db844ee31ebcffad1f25aa3a02558b4f"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matrix(rows):
    return tuple(tuple(x if isinstance(x, ex.C) else ex.q(x) for x in row) for row in rows)


I = ex.identity(2)
P0, P1 = matrix([[1, 0], [0, 0]]), matrix([[0, 0], [0, 1]])
X, Y, Z = (
    matrix([[0, 1], [1, 0]]),
    matrix([[0, ex.q(0, -1)], [ex.q(0, 1), 0]]),
    matrix([[1, 0], [0, -1]]),
)
H = Fraction(1, 2)


def instrument(outcomes):
    return {
        "support": [0],
        "outcomes": [
            {"label": label, "kraus": [ex.matrix_wire(k) for k in operators]}
            for label, operators in outcomes
        ],
    }


def measurement(pauli):
    return instrument(
        [
            ("+", (ex.scale(ex.add(I, pauli), ex.q(H)),)),
            ("-", (ex.scale(ex.add(I, ex.scale(pauli, ex.q(-1))), ex.q(H)),)),
        ]
    )


def event(name, record, inst):
    return {"event_id": name, "record_id": record, **inst}


def problem(events, settings, last_record=None):
    schedule = [e["event_id"] for e in events]
    source = {
        "schema_version": "det8-qr01-problem-v1",
        "qubits": 1,
        "events": events,
        "precedence": [[schedule[0], schedule[1]]] if len(schedule) == 2 else [],
    }
    records = sorted(
        tuple(
            sorted(
                (event["record_id"], outcome["label"])
                for event, outcome in zip(events, choice, strict=True)
            )
        )
        for choice in product(*(event["outcomes"] for event in events))
    )
    return {
        "schema_version": "det8-qr03-problem-v1",
        "source": source,
        "schedule": schedule,
        "futures": [
            {"setting": setting, "instrument": measurement({"X": X, "Y": Y, "Z": Z}[setting])}
            for setting in settings
        ],
        "summary": [
            {
                "record": [list(pair) for pair in record],
                "label": "all" if last_record is None else "last_" + dict(record)[last_record],
            }
            for record in records
        ],
    }


def fixtures():
    amp3, amp4 = ex.q(Fraction(3, 5)), ex.q(Fraction(4, 5))
    coin = instrument([("a", (ex.scale(I, amp3),)), ("b", (ex.scale(I, amp4),))])
    phase = instrument([("a", (ex.scale(I, amp3),)), ("b", (ex.scale(Z, amp4),))])
    mz = instrument([("0", (P0,)), ("1", (P1,))])
    zero = instrument([("alive", (I,)), ("dead", (ex.zeros(2),))])
    tomography = ("X", "Y", "Z")
    return [
        ("coin_tomography", problem([event("coin", "coin", coin)], tomography), 1, 0, True),
        ("phase_z_only", problem([event("phase", "phase", phase)], ("Z",)), 1, 0, True),
        ("phase_tomography", problem([event("phase", "phase", phase)], tomography), 2, 0, False),
        ("projective_z_x_only", problem([event("Z", "z", mz)], ("X",)), 1, 0, True),
        ("projective_z_tomography", problem([event("Z", "z", mz)], tomography), 2, 0, False),
        (
            "two_stage_zx",
            problem([event("Z", "z", mz), event("X", "x", measurement(X))], tomography, "x"),
            2,
            0,
            True,
        ),
        (
            "repeated_z_zeros",
            problem([event("Z0", "firstZ", mz), event("Z1", "lastZ", mz)], tomography, "lastZ"),
            2,
            2,
            True,
        ),
        ("zero_branch_control", problem([event("zero", "zero", zero)], ("Z",)), 1, 1, True),
    ]


def record_key(record):
    return tuple(tuple(pair) for pair in record)


def conditional(row, coordinates):
    denominator = sum(
        (Fraction(v) * t for v, t in zip(row["denominator"], coordinates, strict=True)), Fraction(0)
    )
    require(denominator >= 0, "negative probability on a physical control input")
    predictions = []
    for question in row["numerators"]:
        numerator = sum(
            (Fraction(v) * t for v, t in zip(question["coefficients"], coordinates, strict=True)),
            Fraction(0),
        )
        require(0 <= numerator <= denominator, "invalid numerator on a physical control input")
        predictions.append(
            {
                "setting": question["setting"],
                "outcome": question["outcome"],
                "probability": None if denominator == 0 else str(numerator / denominator),
            }
        )
    return {
        "record": row["record"],
        "history_probability": str(denominator),
        "possible_on_input": denominator > 0,
        "predictions": predictions,
    }


def partitions_refine(fine, coarse):
    fine_sets = [set(map(record_key, group)) for group in fine]
    coarse_sets = [set(map(record_key, group)) for group in coarse]
    return set.union(*fine_sets) == set.union(*coarse_sets) and all(
        any(group <= prior for prior in coarse_sets) for group in fine_sets
    )


def controls(cases):
    by_name = {case["name"]: case for case in cases}
    refinements = []
    for small, large in (
        ("phase_z_only", "phase_tomography"),
        ("projective_z_x_only", "projective_z_tomography"),
    ):
        before, after = by_name[small], by_name[large]
        require(
            before["problem"]["source"] == after["problem"]["source"],
            "refinement changed the source",
        )
        require(
            all(future in after["problem"]["futures"] for future in before["problem"]["futures"]),
            "future family is not actually an extension",
        )
        require(
            partitions_refine(after["analysis"]["classes"], before["analysis"]["classes"])
            and len(after["analysis"]["classes"]) > len(before["analysis"]["classes"]),
            "expected strict future-family refinement failed",
        )
        refinements.append(
            {"smaller_family": small, "expanded_family": large, "strict_refinement": True}
        )

    mixed = (H, H, Fraction(0), Fraction(0))
    phase = by_name["phase_tomography"]["analysis"]
    mixed_predictions = [conditional(row, mixed) for row in phase["histories"]]
    require(
        mixed_predictions[0]["predictions"] == mixed_predictions[1]["predictions"],
        "maximally mixed control must hide the phase difference",
    )
    require(
        not phase["pairs"][0]["equal"] and phase["pairs"][0]["witness"] is not None,
        "all-state test missed hidden phase distinction",
    )

    last = by_name["two_stage_zx"]["analysis"]
    group = next(group for group in last["classes"] if dict(group[0])["x"] == "+")
    group_keys = set(map(record_key, group))
    group_rows = [row for row in last["histories"] if record_key(row["record"]) in group_keys]
    unequal_history = [
        conditional(row, (Fraction(3, 4), Fraction(1, 4), Fraction(0), Fraction(0)))
        for row in group_rows
    ]
    require(
        {row["history_probability"] for row in unequal_history} == {"3/8", "1/8"},
        "two-stage histories must retain distinct occurrence probabilities",
    )
    require(
        unequal_history[0]["predictions"] == unequal_history[1]["predictions"],
        "last-X summary failed on the explanatory input",
    )

    projective = by_name["projective_z_x_only"]
    pure_predictions = [
        conditional(row, (Fraction(1), Fraction(0), Fraction(0), Fraction(0)))
        for row in projective["analysis"]["histories"]
    ]
    require(
        all(row["status"] == "POSSIBLE" for row in projective["analysis"]["histories"])
        and [row["possible_on_input"] for row in pure_predictions] == [True, False],
        "input-specific impossibility was confused with zero history",
    )
    require(
        all(p["probability"] is None for p in pure_predictions[1]["predictions"]),
        "impossible input-specific history acquired a conditional distribution",
    )
    source = ex.parse_problem(projective["problem"]["source"])
    raw_states = ex.execute_operator(
        source, tuple(projective["problem"]["schedule"]), ex.scale(I, ex.q(H))
    )
    normalized = {
        record: ex.scale(state, ex.q(1 / ex.trace(state).real))
        for record, state in raw_states.items()
    }
    require(
        set(normalized.values()) == {P0, P1},
        "X-equivalent histories must still have different quantum states",
    )
    return {
        "family_refinements": refinements,
        "maximally_mixed_false_merge": {
            "predictions": mixed_predictions,
            "all_state_failure_witness": phase["pairs"][0]["witness"],
        },
        "same_last_x_distinct_history_weights": unequal_history,
        "input_specific_impossibility": pure_predictions,
        "predictive_not_full_state_equivalence": [
            {"record": [list(pair) for pair in record], "normalized_state": ex.matrix_wire(state)}
            for record, state in normalized.items()
        ],
    }


def retained_bits(analysis):
    tokens = []
    for history in analysis["histories"]:
        tokens.extend(history["denominator"])
        for row in history["numerators"]:
            tokens.extend(row["coefficients"])
    for pair in analysis["pairs"]:
        for row in pair["questions"]:
            tokens.extend(row["coefficients"])
        witness = pair["witness"]
        if witness is not None:
            tokens.extend(witness["bloch"])
            for row in witness["density"]:
                for cell in row:
                    tokens.extend(cell)
            tokens.extend(
                witness[key]
                for key in (
                    "left_history_probability",
                    "right_history_probability",
                    "left_conditional",
                    "right_conditional",
                    "delta",
                )
            )
    values = [Fraction(token) for token in tokens]
    return max(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) for value in values
    )


def run_suite():
    cases = []
    for name, wire, classes, zeros, valid in fixtures():
        actual = predictive.analyze(wire)
        require(actual == reference_qr03.analyze(wire), f"independent reference mismatch: {name}")
        require(
            len(actual["classes"]) == classes
            and len(actual["never_possible"]) == zeros
            and actual["candidate_valid"] == valid,
            f"unexpected fixture classification: {name}",
        )
        cases.append(
            {
                "name": name,
                "problem": wire,
                "expected_classes": classes,
                "expected_never_possible": zeros,
                "expected_candidate_valid": valid,
                "max_retained_coefficient_witness_bits": retained_bits(actual),
                "analysis": actual,
            }
        )
    return {
        "classification": "EXACT_FINITE_RESEARCH_NOT_EMPIRICAL",
        "cases": cases,
        "analytical_controls": controls(cases),
        "new_physical_laws": False,
        "ret_integration_tested": False,
        "research_base_commit": RESEARCH_BASE_COMMIT,
        "bounds": {
            "qubits": 1,
            "source_events": 2,
            "source_histories": 4,
            "future_settings": 3,
            "input_component_bits": 64,
            "coefficient_guard_bits": 4096,
            "hermitian_basis_dimension": 4,
            "quadratic_monomials": 10,
            "full_rank_witness_probes": 10,
            "general_adaptive_graph": False,
        },
        "totals": {
            "fixtures": len(cases),
            "initial_hermitian_basis_evaluations": 4 * len(cases),
            "future_basis_image_evaluations": sum(
                4 * len(c["analysis"]["histories"]) * len(c["problem"]["futures"]) for c in cases
            ),
            "history_rows": sum(len(c["analysis"]["histories"]) for c in cases),
            "never_possible_histories": sum(len(c["analysis"]["never_possible"]) for c in cases),
            "live_pairs": sum(len(c["analysis"]["pairs"]) for c in cases),
            "question_polynomials": sum(
                len(p["questions"]) for c in cases for p in c["analysis"]["pairs"]
            ),
            "physical_failure_witnesses": sum(
                not p["equal"] for c in cases for p in c["analysis"]["pairs"]
            ),
            "valid_candidate_fixtures": sum(c["analysis"]["candidate_valid"] for c in cases),
            "invalid_candidate_fixtures": sum(not c["analysis"]["candidate_valid"] for c in cases),
            "additional_direct_source_state_executions": 1,
            "additional_history_conditional_evaluations": 6,
            "additional_future_probability_entries": 28,
            "additional_input_impossible_probability_entries": 2,
        },
    }


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def source_ledger():
    ledger = {}
    for name in SOURCES:
        path = ROOT / name
        require(path.is_file() and not path.is_symlink(), f"missing/plain-source violation: {name}")
        raw = path.read_bytes()
        ledger[name] = {"bytes": len(raw), "sha256": digest(raw)}
    return ledger


def prior_identity():
    ledger = {}
    for name, expected in PRIORS.items():
        path = ROOT.parent / name / "results.json"
        require(path.is_file() and not path.is_symlink(), "prior artifact must be a plain file")
        raw = path.read_bytes()
        require(digest(raw) == expected, "prior evidence identity changed")
        ledger[name] = {"bytes": len(raw), "sha256": digest(raw)}
    return ledger


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="fresh read-only exact replay")
    args = parser.parse_args()
    require(bool(sys.flags.isolated), "run with python -I")
    require(sys.pycache_prefix is not None, "set an external -X pycache_prefix")
    cache = Path(sys.pycache_prefix).resolve()
    require(not cache.is_relative_to(ROOT.parents[2]), "bytecode cache must be outside checkout")
    if not args.verify and RESULT.exists():
        raise FileExistsError("results.json already exists; use --verify (never overwrite)")
    frozen, prior = source_ledger(), prior_identity()
    original_bytes, existing = None, None
    if args.verify:
        require(RESULT.is_file() and not RESULT.is_symlink(), "missing/plain-result violation")
        original_bytes = RESULT.read_bytes()
        existing = json.loads(original_bytes)
        require(existing["schema_version"] == "det8-qr03-results-v1", "wrong results schema")
        require(
            existing["source_ledger"] == frozen and existing["prior_artifacts"] == prior,
            "source/prior ledger differs from capture",
        )
    started = time.perf_counter()
    suite = run_suite()
    elapsed = time.perf_counter() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require(
        source_ledger() == frozen and prior_identity() == prior,
        "source/prior changed during execution",
    )
    if args.verify:
        require(existing["suite"] == json.loads(canonical(suite)), "exact replay differs")
        require(RESULT.read_bytes() == original_bytes, "result changed during replay")
        print(
            json.dumps(
                {
                    "status": "VERIFIED_EXACT_REPLAY",
                    "seconds": elapsed,
                    "result_sha256": digest(original_bytes),
                    "totals": suite["totals"],
                }
            )
        )
        return
    report = {
        "schema_version": "det8-qr03-results-v1",
        "source_ledger": frozen,
        "prior_artifacts": prior,
        "suite": suite,
        "runtime": {
            "python": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
            "isolated": bool(sys.flags.isolated),
            "optimized": sys.flags.optimize,
            "bytecode_cache": str(cache),
            "suite_seconds": elapsed,
            "rss_high_water_at_suite_end": rss,
            "rss_units": "bytes" if sys.platform == "darwin" else "KiB",
            "accounting_scope": "exact suite; excludes serialization and later comparison overhead",
            "dependencies": "Python standard library and pinned QR-01 sources; no RET imports",
        },
    }
    raw = canonical(report)
    with RESULT.open("xb") as output:
        output.write(raw)
    require(RESULT.read_bytes() == raw, "result readback differs")
    print(
        json.dumps(
            {
                "status": "CREATED_EXACT_FINITE_RESULT",
                "path": str(RESULT),
                "sha256": digest(raw),
                "seconds": elapsed,
                "totals": suite["totals"],
            }
        )
    )


if __name__ == "__main__":
    main()
