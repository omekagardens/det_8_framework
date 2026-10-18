"""Create-only exact research capture; --verify performs a read-only replay."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import platform
import re
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
RESULT_SCHEMA = "det8-qr05a-results-v1"
BASE_COMMIT = "1fac1352ffe14dbbd6227dd1806bd8f6432ba0e4"
SOURCES = (
    "README.md",
    "growth.py",
    "reference_qr05a.py",
    "study.py",
    "test_qr05a.py",
    "test_capture.py",
    "../qr-01-quantum-records-2026-09-05/exact.py",
    "../qr-01-quantum-records-2026-09-05/reference.py",
)
PRIORS = (
    "qr-01-quantum-records-2026-09-05",
    "qr-02-record-coarse-graining-2026-09-05",
    "qr-03-predictive-histories-2026-09-05",
    "qr-04-adaptive-causal-records-2026-09-05",
)
PRIOR_HASHES = (
    "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b",
    "b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c",
    "2b92b7bd42aa9cde29722269c1a31f339e37b217d1256e50d8ea0ee34d8188c2",
    "a5dc5f5e96a189ae8fd5648334e630fd4c24f6cee2fa805a45d32522bc0bcd70",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name, filename):
    require(name not in sys.modules, "private study module name collision")
    path = HERE / filename
    require(path.is_file() and not path.is_symlink(), "source must be a plain file")
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "cannot load source")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)  # noqa: S102
    return module


def fixtures():
    cases = (
        ("weak_phase", "weak_phase", "2/5", (True, True, True)),
        ("grouped_dephase", "weak_dephase", "2/5", (True, True, True)),
        ("zero_link_boundary", "weak_phase", "0", (True, True, True)),
        ("chain_boundary", "weak_phase", "1", (True, True, True)),
        ("past_local_noncommutation", "parity_zx", "2/5", (False, False, False)),
        ("zero_weight_hidden_conflict", "parity_zx", "0", (False, True, True)),
        ("ambient_stage_artifact", "stage_zx", "2/5", (False, False, False)),
        ("normalized_noncovariant_growth", "weak_phase", None, (True, False, False)),
    )
    return [
        {
            "id": name,
            "input": {
                "schema_version": "det8-qr05a-problem-v1",
                "births": 3,
                "growth": {"kind": "percolation", "p": p}
                if p is not None
                else {"kind": "uniform_ideals"},
                "instrument": rule,
            },
            "expected": dict(
                zip(
                    (
                        "unweighted_diamonds_equal",
                        "weighted_diamonds_equal",
                        "terminal_relabeling_equal",
                    ),
                    expected,
                    strict=True,
                )
            ),
        }
        for name, rule, p, expected in cases
    ]


def invalid_fixtures():
    base = fixtures()[0]["input"]
    cases = []
    for name, key, value in (
        ("wrong_schema", "schema_version", "other"),
        ("boolean_birth", "births", True),
        ("too_many_births", "births", 4),
        ("zero_births", "births", 0),
        ("unknown_instrument", "instrument", "hidden_callback"),
    ):
        wire = copy.deepcopy(base)
        wire[key] = value
        cases.append((name, wire))
    for name, value in (
        ("float_probability", 0.4),
        ("boolean_probability", False),
        ("noncanonical_probability", "4/10"),
        ("negative_probability", "-1/5"),
        ("probability_above_one", "6/5"),
        ("oversized_probability", "1/18446744073709551617"),
        ("exponent_probability", "1e-1000000"),
    ):
        wire = copy.deepcopy(base)
        wire["growth"]["p"] = value
        cases.append((name, wire))
    wire = copy.deepcopy(base)
    wire["undeclared_read"] = [0]
    cases.append(("unknown_root_field", wire))
    wire = copy.deepcopy(base)
    wire["growth"]["kind"] = "record_feedback"
    cases.append(("unknown_growth", wire))
    wire = copy.deepcopy(base)
    wire["growth"] = {"kind": "uniform_ideals", "p": "1/2"}
    cases.append(("unused_growth_parameter", wire))
    wire = copy.deepcopy(base)
    del wire["growth"]["p"]
    cases.append(("missing_probability", wire))
    return cases


def zero_matrix(n):
    return [[["0", "0"] for _ in range(n)] for _ in range(n)]


def add_wire(a, b):
    return [
        [
            [str(F(x) + F(y)) for x, y in zip(ca, cb, strict=True)]
            for ca, cb in zip(ra, rb, strict=True)
        ]
        for ra, rb in zip(a, b, strict=True)
    ]


def scale_wire(a, scale):
    return [[[str(F(c) * scale) for c in cell] for cell in row] for row in a]


def apply_diagonal_input(superop, zero, one):
    return [
        [
            [
                str(F(superop[2 * i + j][0][part]) * zero + F(superop[2 * i + j][3][part]) * one)
                for part in (0, 1)
            ]
            for j in range(2)
        ]
        for i in range(2)
    ]


def independent_weight(growth, order):
    if growth["kind"] == "percolation":
        p = F(growth["p"])
        links = sum(sum(not any(i in order[j] for j in past) for i in past) for past in order)
        incomparables = len(order) * (len(order) - 1) // 2 - sum(map(len, order))
        return p**links * (1 - p) ** incomparables
    weight = F(1)
    for n in range(len(order)):
        subsets = [{i for i in range(n) if mask & (1 << i)} for mask in range(1 << n)]
        count = sum(all(set(order[j]) <= s for j in s) for s in subsets)
        weight /= count
    return weight


def closed_form(case, history):
    order, record = history["order"], history["outcomes"]
    weight = independent_weight(case["growth"], order)
    require(str(weight) == history["weight"], "independent classical path weight differs")
    n = len(record)
    n1 = sum(record)
    a = F(3, 5) ** (n - n1) * F(4, 5) ** n1
    b = F(4, 5) ** (n - n1) * F(3, 5) ** n1
    k = sum(sum(record[i] for i in past) % 2 for past in order)
    phase = ((1, 0), (0, 1), (-1, 0), (0, -1))[k % 4]
    coherence = F(-7, 25) ** n if case["instrument"] == "weak_dephase" else F(1)
    result = zero_matrix(4)
    result[0][0] = [str(weight * a * a), "0"]
    result[3][3] = [str(weight * b * b), "0"]
    real, imag = weight * a * b * coherence * phase[0], weight * a * b * coherence * phase[1]
    result[1][1] = [str(real), str(-imag)]
    result[2][2] = [str(real), str(imag)]
    return result


def find_history(analysis, order, record):
    for i, row in enumerate(analysis["levels"][-1]["histories"]):
        if row["order"] == order and row["outcomes"] == record:
            return i, row
    raise ValueError("missing physical-control history")


def controls(cases):
    by_id = {case["id"]: case["analysis"] for case in cases}
    p0 = [[["1", "0"], ["0", "0"]], [["0", "0"], ["0", "0"]]]
    items = []
    for name, left_order, left_record, right_order, right_record, input_bits, expected in (
        (
            "past_local_noncommutation",
            [[], [0], []],
            [1, 0, 0],
            [[], [], [0]],
            [1, 0, 0],
            (0, 1),
            (F(9, 250), F(0)),
        ),
        (
            "ambient_stage_artifact",
            [[], [], []],
            [0, 1, 0],
            [[], [], []],
            [1, 0, 0],
            (1, 0),
            (F(27, 500), F(0)),
        ),
        (
            "normalized_noncovariant_growth",
            [[], [0], []],
            [0, 0, 0],
            [[], [], [0]],
            [0, 0, 0],
            (1, 0),
            (F(243, 31250), F(729, 125000)),
        ),
    ):
        left_i, left = find_history(by_id[name], left_order, left_record)
        right_i, right = find_history(by_id[name], right_order, right_record)
        outputs = [apply_diagonal_input(row["superoperator"], *input_bits) for row in (left, right)]
        require(
            outputs == [scale_wire(p0, e) for e in expected], f"physical witness differs: {name}"
        )
        items.append(
            {
                "case": name,
                "histories": [left_i, right_i],
                "input_diagonal": list(input_bits),
                "outputs": outputs,
            }
        )
    stage = by_id["ambient_stage_artifact"]
    index, _ = find_history(stage, [[], [], []], [0, 0, 0])
    row = next(
        r for r in stage["relabelings"] if r["history"] == index and r["permutation"] == [1, 0, 2]
    )
    require(
        row["map_equal"] and not row["settings_equal"] and row["target"] == index,
        "setting-only automorphism witness missing",
    )
    items.append({"case": "setting_only_automorphism", "relabeling": row})
    phase = by_id["weak_phase"]
    fork_i, fork = find_history(phase, [[], [0], [0]], [0, 0, 0])
    join_i, join = find_history(phase, [[], [], [0, 1]], [0, 0, 0])
    require(fork["superoperator"] == join["superoperator"], "fork/join payload collision differs")
    require(
        sum(not s for s in fork["order"]) == 1 and sum(not s for s in join["order"]) == 2,
        "fork/join nonisomorphism witness differs",
    )
    require(fork["weight"] == join["weight"] == "12/125", "fork/join weight differs")
    items.append(
        {
            "case": "nonisomorphic_order_payload_collision",
            "histories": [fork_i, join_i],
            "orders": [fork["order"], join["order"]],
            "minimal_element_counts": [1, 2],
            "shared_weight": fork["weight"],
            "shared_superoperator": fork["superoperator"],
            "claim": "PAYLOAD_MAP_ALONE_DOES_NOT_IDENTIFY_THE_RETAINED_ORDER",
        }
    )
    return items


def retained_bits(value):
    best = 0
    if isinstance(value, dict):
        return max((retained_bits(v) for v in value.values()), default=0)
    if isinstance(value, list):
        return max((retained_bits(v) for v in value), default=0)
    if type(value) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value):
        number = F(value)
        best = max(abs(number.numerator).bit_length(), number.denominator.bit_length())
    return best


def run_suite():
    direct = load("qr05a_capture_direct", "growth.py")
    reference = load("qr05a_capture_reference", "reference_qr05a.py")
    cases, closed_maps = [], 0
    for case in fixtures():
        actual, other = direct.analyze(case["input"]), reference.analyze(case["input"])
        require(actual == other, f"independent full analysis differs: {case['id']}")
        require(actual["flags"]["normalized"], f"normalization failed: {case['id']}")
        for flag, expected in case["expected"].items():
            require(
                actual["flags"][flag] == expected, f"prespecified flag differs: {case['id']}/{flag}"
            )
        for level in actual["levels"]:
            for history in level["histories"]:
                require(
                    str(independent_weight(case["input"]["growth"], history["order"]))
                    == history["weight"],
                    "classical weight formula differs",
                )
                if case["input"]["instrument"] in ("weak_phase", "weak_dephase"):
                    require(
                        closed_form(case["input"], history) == history["superoperator"],
                        "closed-form full map differs",
                    )
                    closed_maps += 1
        grouped_sum = zero_matrix(4)
        members = []
        for cls in actual["classes"]:
            members.extend(cls["members"])
            summed = zero_matrix(4)
            for index in cls["members"]:
                summed = add_wire(summed, actual["levels"][-1]["histories"][index]["superoperator"])
            require(summed == cls["superoperator"], "class pushforward differs")
            grouped_sum = add_wire(grouped_sum, cls["superoperator"])
        require(sorted(members) == list(range(56)), "class membership loses path multiplicity")
        require(grouped_sum == actual["levels"][-1]["total_map"], "grouping changes total map")
        cases.append({**case, "analysis": actual, "retained_component_bits": retained_bits(actual)})
    rejected = []
    for name, wire in invalid_fixtures():
        results = []
        for implementation in (direct, reference):
            try:
                implementation.analyze(wire)
            except (ValueError, TypeError):
                results.append(True)
            else:
                raise ValueError(f"invalid fixture accepted: {name}")
        rejected.append({"id": name, "input": wire, "both_rejected": all(results)})
    return {
        "cases": cases,
        "rejections": rejected,
        "analytic_controls": controls(cases),
        "totals": {
            "fixtures": len(cases),
            "rejected_fixtures": len(rejected),
            "closed_form_maps": closed_maps,
            "history_maps": sum(sum(c["analysis"]["counts"]["level_histories"]) for c in cases),
            "terminal_maps": sum(c["analysis"]["counts"]["level_histories"][-1] for c in cases),
            "diamond_contexts": sum(c["analysis"]["counts"]["diamond_contexts"] for c in cases),
            "diamond_outcome_pairs": sum(
                c["analysis"]["counts"]["diamond_outcome_pairs"] for c in cases
            ),
            "terminal_relabelings": sum(
                c["analysis"]["counts"]["terminal_relabelings"] for c in cases
            ),
            "zero_terminal_maps": sum(c["analysis"]["counts"]["zero_terminal_maps"] for c in cases),
            "retained_component_bits": max(c["retained_component_bits"] for c in cases),
        },
        "research_base_commit": BASE_COMMIT,
        "claim": "EXACT_FINITE_CLASSICAL_ORDER_QUANTUM_PAYLOAD_CONSISTENCY",
        "empirical_data_used": False,
        "ret_integration_tested": False,
        "gravity_derived": False,
        "bounds": {
            "births": 3,
            "fixed_qubits": 1,
            "outcomes": 2,
            "kraus_per_outcome": 2,
            "input_bits": 64,
            "arithmetic_guard_bits": 4096,
        },
    }


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def ledger():
    result = {}
    for name in SOURCES:
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"source is not a plain file: {name}")
        raw = path.read_bytes()
        result[name] = {"bytes": len(raw), "sha256": digest(raw)}
    return result


def priors():
    result = {}
    for directory, expected in zip(PRIORS, PRIOR_HASHES, strict=True):
        path = HERE.parent / directory / "results.json"
        require(path.is_file() and not path.is_symlink(), "prior artifact is not a plain file")
        raw = path.read_bytes()
        require(digest(raw) == expected, "pinned prior artifact changed")
        result[directory] = {"bytes": len(raw), "sha256": digest(raw)}
    return result


def canonical(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="read-only exact replay")
    args = parser.parse_args()
    require(
        sys.flags.isolated and sys.pycache_prefix, "run isolated with an external bytecode cache"
    )
    cache = Path(sys.pycache_prefix).resolve()
    require(cache != Path(cache.anchor), "bytecode cache must not be a filesystem root")
    require(not cache.is_relative_to(ROOT), "bytecode cache must be outside checkout")
    if not args.verify and (RESULT.exists() or RESULT.is_symlink()):
        raise FileExistsError("results.json already exists; use --verify, never overwrite")
    frozen, previous = ledger(), priors()
    if args.verify:
        require(RESULT.is_file() and not RESULT.is_symlink(), "result must be a plain file")
        raw_before = RESULT.read_bytes()
        existing = json.loads(raw_before)
        require(
            type(existing) is dict and existing.get("schema_version") == RESULT_SCHEMA,
            "unrecognized result schema",
        )
        require(
            existing["source_ledger"] == frozen and existing["prior_artifacts"] == previous,
            "source/prior identity changed",
        )
    started = time.perf_counter()
    suite = run_suite()
    elapsed = time.perf_counter() - started
    require(ledger() == frozen and priors() == previous, "source/prior changed during execution")
    if args.verify:
        require(existing["suite"] == suite, "exact replay differs")
        require(RESULT.read_bytes() == raw_before, "result changed during replay")
        print(
            json.dumps(
                {
                    "status": "VERIFIED_EXACT_REPLAY",
                    "seconds": elapsed,
                    "sha256": digest(raw_before),
                    "totals": suite["totals"],
                }
            )
        )
        return
    report = {
        "schema_version": RESULT_SCHEMA,
        "source_ledger": frozen,
        "prior_artifacts": previous,
        "suite": suite,
        "runtime": {
            "python": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
            "isolated": bool(sys.flags.isolated),
            "optimized": sys.flags.optimize,
            "bytecode_cache": str(cache),
            "suite_seconds": elapsed,
            "rss_high_water_at_suite_end": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "rss_units": "bytes" if sys.platform == "darwin" else "KiB",
            "scope": "suite only; excludes serialization; no application performance claim",
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
                "seconds": elapsed,
                "sha256": digest(raw),
                "totals": suite["totals"],
            }
        )
    )


if __name__ == "__main__":
    main()
