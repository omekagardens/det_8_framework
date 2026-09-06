"""Create-only capture and fresh replay of the QR-04 adaptive record study."""

from __future__ import annotations

import argparse
import copy
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

import adaptive
import reference_qr04

ex = adaptive.ex
SOURCES = (
    "README.md",
    "adaptive.py",
    "reference_qr04.py",
    "study.py",
    "test_qr04.py",
    "../qr-01-quantum-records-2026-09-05/exact.py",
    "../qr-01-quantum-records-2026-09-05/reference.py",
)
PRIORS = {
    "qr-01-quantum-records-2026-09-05": "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b",
    "qr-02-record-coarse-graining-2026-09-05": "b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c",
    "qr-03-predictive-histories-2026-09-05": "2b92b7bd42aa9cde29722269c1a31f339e37b217d1256e50d8ea0ee34d8188c2",
}
RESEARCH_BASE_COMMIT = "80258ec5191b33a5159e6af53b372c409702f89e"
RESULT = ROOT / "results.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matrix(rows):
    return tuple(tuple(v if isinstance(v, ex.C) else ex.q(v) for v in row) for row in rows)


I = ex.identity(2)
P0, P1 = matrix([[1, 0], [0, 0]]), matrix([[0, 0], [0, 1]])
X, Y, Z = (
    matrix([[0, 1], [1, 0]]),
    matrix([[0, ex.q(0, -1)], [ex.q(0, 1), 0]]),
    matrix([[1, 0], [0, -1]]),
)
S = matrix([[1, 0], [0, ex.q(0, 1)]])
RESET = (P0, matrix([[0, 1], [0, 0]]))
HALF = Fraction(1, 2)


def outcomes(rows):
    return [
        {"label": label, "kraus": [ex.matrix_wire(k) for k in operators]}
        for label, operators in rows
    ]


def measurement(pauli):
    return outcomes(
        [
            ("0", (ex.scale(ex.add(I, pauli), ex.q(HALF)),)),
            ("1", (ex.scale(ex.add(I, ex.scale(pauli, ex.q(-1))), ex.q(HALF)),)),
        ]
    )


def unitary(operator):
    return outcomes([("done", (operator,))])


def coin(dimension=2, zero=False):
    return outcomes(
        [
            (
                "0",
                (
                    ex.identity(dimension)
                    if zero
                    else ex.scale(ex.identity(dimension), ex.q(Fraction(3, 5))),
                ),
            ),
            (
                "1",
                (
                    ex.zeros(dimension)
                    if zero
                    else ex.scale(ex.identity(dimension), ex.q(Fraction(4, 5))),
                ),
            ),
        ]
    )


def embed(rows, target):
    result = copy.deepcopy(rows)
    for row in result:
        row["kraus"] = [
            ex.matrix_wire(
                ex.tensor(ex.decode_matrix(k, 2), I)
                if target == 0
                else ex.tensor(I, ex.decode_matrix(k, 2))
            )
            for k in row["kraus"]
        ]
    return result


def damping(a, b, grouped=False):
    stay = matrix([[1, 0], [0, Fraction(a, 5)]])
    decay = matrix([[0, Fraction(b, 5)], [0, 0]])
    return (
        outcomes([("done", (stay, decay))])
        if grouped
        else outcomes([("0", (stay,)), ("1", (decay,))])
    )


def event(eid, rid, support, settings, reads=(), rule=None, available=None):
    reads = tuple(sorted(reads))
    contexts = [
        tuple(zip(reads, labels, strict=True)) for labels in product(("0", "1"), repeat=len(reads))
    ]
    return {
        "event_id": eid,
        "record_id": rid,
        "support": support,
        "available_records": list(reads if available is None else available),
        "read_records": list(reads),
        "settings": [{"setting": sid, "outcomes": rows} for sid, rows in settings],
        "policy": [
            {
                "when": [list(pair) for pair in context],
                "setting": settings[0][0] if rule is None else rule(dict(context)),
            }
            for context in contexts
        ],
    }


def problem(events, edges=(), qubits=1):
    return {
        "schema_version": "det8-qr04-problem-v1",
        "qubits": qubits,
        "events": events,
        "precedence": [list(pair) for pair in edges],
    }


def fixtures():
    selector = event("C", "c", [], [("coin", coin())])
    same = [("Z", measurement(Z)), ("X", measurement(X))]
    select_axis = lambda r: "Z" if r["c"] == "0" else "X"
    shared = problem(
        [
            selector,
            event("A", "a", [0], same, ("c",), select_axis),
            event("B", "b", [0], same, ("c",), select_axis),
        ],
        (("C", "A"), ("C", "B")),
    )
    independent = problem(
        [
            event("C", "c", [], [("coin", coin())]),
            event("D", "d", [], [("coin", coin())]),
            event("A", "a", [0], same, ("c",), select_axis),
            event("B", "b", [0], same, ("d",), lambda r: "Z" if r["d"] == "0" else "X"),
        ],
        (("C", "A"), ("D", "B")),
    )
    ordered = problem(
        [
            event("C", "c", [0], [("Z", measurement(Z))]),
            event(
                "A",
                "a",
                [0],
                [("I", unitary(I)), ("X", unitary(X))],
                ("c",),
                lambda r: "I" if r["c"] == "0" else "X",
            ),
        ],
        (("C", "A"),),
    )
    two_read = problem(
        [
            event("C", "c", [], [("coin", coin())]),
            event("D", "d", [], [("coin", coin())]),
            event(
                "A",
                "a",
                [0],
                [("I", unitary(I)), ("S", unitary(S))],
                ("c", "d"),
                lambda r: "I" if r["c"] == r["d"] else "S",
            ),
        ],
        (("C", "A"), ("D", "A")),
    )
    disjoint = problem(
        [
            event("C", "c", [], [("coin", coin(4))]),
            event(
                "A",
                "a",
                [0],
                [("Y", embed(measurement(Y), 0)), ("Z", embed(measurement(Z), 0))],
                ("c",),
                lambda r: "Y" if r["c"] == "0" else "Z",
            ),
            event(
                "B",
                "b",
                [1],
                [("X", embed(measurement(X), 1)), ("Z", embed(measurement(Z), 1))],
                ("c",),
                lambda r: "X" if r["c"] == "0" else "Z",
            ),
        ],
        (("C", "A"), ("C", "B")),
        2,
    )
    multi = problem(
        [
            event("C", "c", [], [("coin", coin(4))]),
            event(
                "A",
                "a",
                [0],
                [
                    ("damp", embed(damping(3, 4, True), 0)),
                    ("reset", embed(outcomes([("done", RESET)]), 0)),
                ],
                ("c",),
                lambda r: "damp" if r["c"] == "0" else "reset",
            ),
            event("B", "b", [1], [("Y", embed(measurement(Y), 1))]),
        ],
        (("C", "A"), ("C", "B")),
        2,
    )
    restricted = problem(
        [
            event(
                "C",
                "c",
                [0],
                [("measure_reset", outcomes([("0", (RESET[0],)), ("1", (RESET[1],))]))],
            ),
            event("A", "a", [0], [("Z", measurement(Z))]),
            event(
                "B",
                "b",
                [0],
                [("damp34", damping(3, 4)), ("damp43", damping(4, 3))],
                ("c",),
                lambda r: "damp34" if r["c"] == "0" else "damp43",
            ),
        ],
        (("C", "A"), ("C", "B")),
    )
    unreachable = problem(
        [
            event("C", "c", [], [("identity_zero", coin(zero=True))]),
            event(
                "A",
                "a",
                [0],
                [("I", unitary(I)), ("S", unitary(S))],
                ("c",),
                lambda r: "I" if r["c"] == "0" else "S",
            ),
            event("B", "b", [0], [("X", unitary(X))]),
        ],
        (("C", "A"), ("C", "B")),
    )
    return [
        ("ordered_adaptive_reset", ordered, True, True),
        ("shared_selector_overlap", shared, True, True),
        ("independent_selectors_conflict", independent, False, False),
        ("two_read_xor_policy", two_read, True, True),
        ("disjoint_adaptive_complex", disjoint, True, True),
        ("disjoint_adaptive_multikraus", multi, True, True),
        ("source_range_restriction", restricted, True, False),
        ("unreachable_policy_context", unreachable, True, False),
    ]


def invalid_fixtures():
    base = fixtures()[1][1]
    result = []

    def add(name, mutate):
        wire = copy.deepcopy(base)
        mutate(wire)
        result.append((name, wire))

    add("ancestor_not_available", lambda w: w["events"][1].update(available_records=[]))
    add("incomparable_availability", lambda w: w["events"][1].update(available_records=["b", "c"]))
    add("self_availability", lambda w: w["events"][1].update(available_records=["a", "c"]))
    add("unknown_availability", lambda w: w["events"][1].update(available_records=["c", "unknown"]))
    add("policy_missing_row", lambda w: w["events"][1]["policy"].pop())
    add(
        "policy_duplicate_row",
        lambda w: w["events"][1]["policy"].__setitem__(
            1, copy.deepcopy(w["events"][1]["policy"][0])
        ),
    )
    add("policy_unknown_setting", lambda w: w["events"][1]["policy"][0].update(setting="missing"))
    add("hidden_scheduler_field", lambda w: w["events"][1].update(scheduler_index=1))
    add("record_overwrite", lambda w: w["events"][1].update(record_id="c"))
    add("cyclic_dependencies", lambda w: w["precedence"].append(["A", "C"]))
    add(
        "different_setting_domains",
        lambda w: w["events"][1]["settings"][1]["outcomes"][0].update(label="other"),
    )
    zero = copy.deepcopy(fixtures()[-1][1])
    zero["events"][1]["policy"][1]["when"] = [["b", "done"]]
    result.append(("forbidden_read_in_impossible_context", zero))
    return result


def apply_map(wire, state):
    d = len(state)
    superoperator = ex.decode_matrix(wire, d * d)
    vector = tuple(x for row in state for x in row)
    output = tuple(
        sum((entry * v for entry, v in zip(row, vector, strict=True)), ex.ZERO)
        for row in superoperator
    )
    return tuple(tuple(output[i * d + j] for j in range(d)) for i in range(d))


def state_outputs(maps, state):
    rows = []
    for block in maps:
        output = apply_map(block["superoperator"], state)
        weight = ex.trace(output)
        require(weight.imag == 0 and 0 <= weight.real <= 1, "invalid physical branch probability")
        rows.append(
            {
                "record": block["record"],
                "state": ex.matrix_wire(output),
                "probability": str(weight.real),
            }
        )
    require(
        sum((Fraction(row["probability"]) for row in rows), Fraction(0)) == 1,
        "physical branch probabilities not normalized",
    )
    return rows


def controls(cases):
    by_name = {case["name"]: case for case in cases}
    reset = by_name["ordered_adaptive_reset"]["analysis"]
    reset_rows = state_outputs(reset["schedules"][0]["maps"], ex.scale(I, ex.q(HALF)))
    require(
        all(row["state"] == ex.matrix_wire(ex.scale(P0, ex.q(HALF))) for row in reset_rows),
        "adaptive reset control failed",
    )

    bell = matrix([[HALF, 0, 0, HALF], [0, 0, 0, 0], [0, 0, 0, 0], [HALF, 0, 0, HALF]])
    disjoint = by_name["disjoint_adaptive_complex"]["analysis"]
    bell_rows = state_outputs(disjoint["schedules"][0]["maps"], bell)
    for row in bell_rows:
        record = {rid: (setting, outcome) for rid, setting, outcome in row["record"]}
        expected = (
            Fraction(9, 100)
            if record["c"][1] == "0"
            else Fraction(8, 25)
            if record["a"][1] == record["b"][1]
            else Fraction(0)
        )
        require(
            Fraction(row["probability"]) == expected, "adaptive Bell correlation control failed"
        )

    restricted = by_name["source_range_restriction"]["analysis"]
    restricted_rows = state_outputs(restricted["schedules"][0]["maps"], ex.scale(I, ex.q(HALF)))
    require(
        restricted["schedule_equal"] and not restricted["universal_pair_equal"],
        "source restriction distinction missing",
    )
    pair = restricted["pairs"][0]
    witnesses = []
    for context in pair["contexts"]:
        outputs = []
        for direction in ("forward", "reverse"):
            block = next(
                b
                for b in context[direction]
                if {rid: x for rid, _, x in b["record"]} == {"a": "1", "b": "1"}
            )
            outputs.append(apply_map(block["superoperator"], P1))
        expected = Fraction(16, 25) if context["read_context"][0][1] == "0" else Fraction(9, 25)
        require(
            outputs == [ex.scale(P0, ex.q(expected)), ex.zeros(2)],
            "unreachable-intermediate-state witness failed",
        )
        witnesses.append(
            {
                "read_context": context["read_context"],
                "input": ex.matrix_wire(P1),
                "input_reachable_after_source": False,
                "forward": ex.matrix_wire(outputs[0]),
                "reverse": ex.matrix_wire(outputs[1]),
            }
        )

    impossible = by_name["unreachable_policy_context"]["analysis"]
    require(
        [c["equal"] for c in impossible["pairs"][0]["contexts"]] == [True, False],
        "impossible-context distinction failed",
    )
    require(
        impossible["counts"]["zero_schedule_blocks"] == 2, "impossible output records were pruned"
    )

    conflict = by_name["independent_selectors_conflict"]["analysis"]
    ab_pair = next(p for p in conflict["pairs"] if p["events"] == ["A", "B"])
    require(
        [c["equal"] for c in ab_pair["contexts"]] == [True, False, False, True],
        "independent-selector mixed-context conflict missing",
    )
    conflict_record = [["a", "Z", "0"], ["b", "X", "0"], ["c", "coin", "0"], ["d", "coin", "1"]]
    conflict_outputs = []
    expected_states = (
        ex.scale(ex.add(I, X), ex.q(Fraction(36, 625))),
        ex.scale(P0, ex.q(Fraction(36, 625))),
    )
    for order, expected in zip(
        (["C", "A", "D", "B"], ["C", "D", "B", "A"]), expected_states, strict=True
    ):
        schedule = next(row for row in conflict["schedules"] if row["order"] == order)
        block = next(row for row in schedule["maps"] if row["record"] == conflict_record)
        output = apply_map(block["superoperator"], P0)
        require(output == expected, "physical full-schedule conflict witness failed")
        conflict_outputs.append(
            {
                "order": order,
                "state": ex.matrix_wire(output),
                "probability": str(ex.trace(output).real),
            }
        )
    return {
        "adaptive_reset_mixed_input": reset_rows,
        "adaptive_disjoint_bell_input": ex.matrix_wire(bell),
        "adaptive_disjoint_bell_outputs": bell_rows,
        "source_restricted_mixed_outputs": restricted_rows,
        "unreachable_intermediate_state_witnesses": witnesses,
        "unreachable_context_flags": [c["equal"] for c in impossible["pairs"][0]["contexts"]],
        "independent_selector_context_flags": [c["equal"] for c in ab_pair["contexts"]],
        "physical_full_schedule_conflict": {
            "input": ex.matrix_wire(P0),
            "record": conflict_record,
            "outputs": conflict_outputs,
        },
        "accounting": {
            "full_output_blocks_applied_to_physical_inputs": len(reset_rows)
            + len(bell_rows)
            + len(restricted_rows)
            + len(conflict_outputs),
            "additional_pair_blocks_applied": 2 * len(witnesses),
            "new_matrix_unit_executions": 0,
        },
    }


def retained_bits(analysis):
    bits = 0
    bundles = [s["maps"] for s in analysis["schedules"]]
    bundles += [
        c[direction]
        for p in analysis["pairs"]
        for c in p["contexts"]
        for direction in ("forward", "reverse")
    ]
    for bundle in bundles:
        for block in bundle:
            for row in block["superoperator"]:
                for cell in row:
                    for token in cell:
                        value = Fraction(token)
                        bits = max(
                            bits, abs(value.numerator).bit_length(), value.denominator.bit_length()
                        )
    return bits


def run_suite():
    cases = []
    for name, wire, schedule_expected, pair_expected in fixtures():
        actual = adaptive.analyze(wire)
        require(actual == reference_qr04.analyze(wire), f"independent reference differs: {name}")
        require(
            actual["schedule_equal"] == schedule_expected
            and actual["universal_pair_equal"] == pair_expected,
            f"prespecified expectation differs: {name}",
        )
        cases.append(
            {
                "name": name,
                "problem": wire,
                "analysis": actual,
                "reference_equal": True,
                "retained_map_component_bits": retained_bits(actual),
            }
        )
    rejections = []
    for name, wire in invalid_fixtures():
        flags = []
        for analyze in (adaptive.analyze, reference_qr04.analyze):
            try:
                analyze(wire)
            except ValueError:
                flags.append(True)
            else:
                flags.append(False)
        require(all(flags), f"invalid input accepted: {name}")
        rejections.append(
            {
                "name": name,
                "problem": wire,
                "executor_rejected": flags[0],
                "reference_rejected": flags[1],
            }
        )
    totals = {
        key: sum(case["analysis"]["counts"][key] for case in cases)
        for key in cases[0]["analysis"]["counts"]
    }
    totals.update(
        {
            "fixtures": len(cases),
            "rejected_fixtures": len(rejections),
            "schedule_equal_fixtures": sum(c["analysis"]["schedule_equal"] for c in cases),
            "universal_pair_equal_fixtures": sum(
                c["analysis"]["universal_pair_equal"] for c in cases
            ),
            "nontrivial_schedule_equal_fixtures": sum(
                c["analysis"]["schedule_equal"] and c["analysis"]["nontrivial_schedule_comparison"]
                for c in cases
            ),
            "source_only_equal_fixtures": sum(
                c["analysis"]["schedule_equal"] and not c["analysis"]["universal_pair_equal"]
                for c in cases
            ),
            "failing_pair_contexts": sum(
                not ctx["equal"]
                for c in cases
                for p in c["analysis"]["pairs"]
                for ctx in p["contexts"]
            ),
            "retained_map_component_bits": max(c["retained_map_component_bits"] for c in cases),
        }
    )
    return {
        "cases": cases,
        "rejections": rejections,
        "controls": controls(cases),
        "totals": totals,
        "research_base_commit": RESEARCH_BASE_COMMIT,
        "empirical_data_used": False,
        "ret_integration_tested": False,
        "claim": "EXACT_FINITE_ADAPTIVE_RECORD_COMPOSITION",
        "bounds": {
            "qubits": 2,
            "events": 4,
            "settings_per_event": 2,
            "outcomes_per_setting": 2,
            "kraus_per_outcome": 2,
            "read_records_per_event": 2,
            "policy_rows_per_event": 4,
            "schedules_per_fixture": 24,
            "input_component_bits": 64,
            "arithmetic_guard_bits": 4096,
        },
    }


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def source_ledger():
    ledger = {}
    for name in SOURCES:
        path = ROOT / name
        require(path.is_file() and not path.is_symlink(), f"source must be a plain file: {name}")
        raw = path.read_bytes()
        ledger[name] = {"bytes": len(raw), "sha256": digest(raw)}
    return ledger


def prior_identity():
    ledger = {}
    for name, expected in PRIORS.items():
        path = ROOT.parent / name / "results.json"
        require(path.is_file() and not path.is_symlink(), "prior must be a plain file")
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
    require(sys.pycache_prefix is not None, "set external -X pycache_prefix")
    cache = Path(sys.pycache_prefix).resolve()
    require(not cache.is_relative_to(ROOT.parents[2]), "bytecode cache must be outside checkout")
    if not args.verify and (RESULT.exists() or RESULT.is_symlink()):
        raise FileExistsError("results.json already exists; use --verify (never overwrite)")
    frozen, prior = source_ledger(), prior_identity()
    original_bytes, existing = None, None
    if args.verify:
        require(RESULT.is_file() and not RESULT.is_symlink(), "result must be a plain file")
        original_bytes = RESULT.read_bytes()
        existing = json.loads(original_bytes)
        require(existing["schema_version"] == "det8-qr04-results-v1", "wrong results schema")
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
        "schema_version": "det8-qr04-results-v1",
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
