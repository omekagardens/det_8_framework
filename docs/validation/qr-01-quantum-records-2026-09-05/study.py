"""Create or independently replay the bounded QR-01 exact finite study."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import exact as ex
import reference as ref

SOURCES = ("README.md", "exact.py", "reference.py", "study.py", "test_qr01.py")
RESULT = ROOT / "results.json"


def require(condition, message):
    """Study checks must remain active under python -O."""
    if not condition:
        raise ValueError(message)


def matrix(rows):
    return tuple(tuple(x if isinstance(x, ex.C) else ex.q(x) for x in row) for row in rows)


I = ex.identity(2)
P0 = matrix([[1, 0], [0, 0]])
P1 = matrix([[0, 0], [0, 1]])
H = Fraction(1, 2)
PX = (matrix([[H, H], [H, H]]), matrix([[H, -H], [-H, H]]))
PY = (matrix([[H, ex.q(0, -H)], [ex.q(0, H), H]]), matrix([[H, ex.q(0, H)], [ex.q(0, -H), H]]))
Z = matrix([[1, 0], [0, -1]])
S = matrix([[1, 0], [0, ex.q(0, 1)]])
DAMP = (matrix([[1, 0], [0, Fraction(4, 5)]]), matrix([[0, Fraction(3, 5)], [0, 0]]))


def event(eid, support, outcomes, record_id=None):
    return {
        "event_id": eid,
        "record_id": record_id or eid,
        "support": list(support),
        "outcomes": [
            {"label": label, "kraus": [ex.matrix_wire(m) for m in kraus]}
            for label, kraus in outcomes
        ],
    }


def local(eid, qubit, outcomes):
    embedded = [
        (label, tuple(ex.tensor(m, I) if qubit == 0 else ex.tensor(I, m) for m in kraus))
        for label, kraus in outcomes
    ]
    return event(eid, [qubit], embedded)


def problem(qubits, events, precedence=()):
    return {
        "schema_version": "det8-qr01-problem-v1",
        "qubits": qubits,
        "events": events,
        "precedence": [list(edge) for edge in precedence],
    }


def fixtures():
    z_outcomes = [("0", (P0,)), ("1", (P1,))]
    x_outcomes = [("+", (PX[0],)), ("-", (PX[1],))]
    y_outcomes = [("+", (PY[0],)), ("-", (PY[1],))]
    za, zb = local("ZA", 0, z_outcomes), local("ZB", 1, z_outcomes)
    ya, yb = local("YA", 0, y_outcomes), local("YB", 1, y_outcomes)
    xb = local("XB", 1, x_outcomes)
    damping = local("DA", 0, [("kept", DAMP)])
    cnot = matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    parity = (
        matrix([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]]),
        matrix([[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0]]),
    )
    diamond = problem(
        2,
        [
            event("start", [0, 1], [("unitary", (cnot,))]),
            za,
            yb,
            event("finish", [0, 1], [("even", (parity[0],)), ("odd", (parity[1],))]),
        ],
        [("start", "ZA"), ("start", "YB"), ("ZA", "finish"), ("YB", "finish")],
    )
    antichain = problem(
        2,
        [
            local(name, support, [("unitary", (op,))])
            for name, support, op in (("ZA", 0, Z), ("ZB", 1, Z), ("SA", 0, S), ("SB", 1, S))
        ],
    )
    z, x = event("Z", [0], z_outcomes), event("X", [0], x_outcomes)
    return [
        ("disjoint_z", problem(2, [za, zb]), True, "nontrivial_commutation"),
        ("complex_disjoint", problem(2, [ya, zb]), True, "nontrivial_commutation"),
        ("damping_disjoint", problem(2, [damping, xb]), True, "nontrivial_commutation"),
        ("four_event_diamond", diamond, True, "nontrivial_commutation"),
        ("four_event_antichain", antichain, True, "nontrivial_commutation"),
        ("ordered_zx", problem(1, [z, x], [("Z", "X")]), True, "ordered_control"),
        ("unordered_zx", problem(1, [z, x]), False, "expected_counterexample"),
        (
            "zero_outcome",
            problem(1, [event("zero", [], [("impossible", (ex.zeros(2),)), ("surviving", (I,))])]),
            True,
            "zero_branch_control",
        ),
    ]


def checked_map(wire, order):
    parsed = ex.parse_problem(wire)
    observed = ex.operator_maps(parsed, order)
    independent = ref.reference_schedule(wire, order)
    converted = {
        key: tuple(tuple(ex.C(*v) for v in row) for row in block)
        for key, block in independent.items()
    }
    require(
        ex.difference(observed, converted) is None,
        f"independent reference disagreement for {order}",
    )
    return observed


def max_retained_bits(blocks):
    return max(
        max(abs(v.numerator).bit_length(), v.denominator.bit_length())
        for block in blocks.values()
        for row in block
        for c in row
        for v in (c.real, c.imag)
    )


def case_result(name, wire, expected_equal, classification):
    parsed = ex.parse_problem(wire)
    orders = ex.schedules(parsed)
    by_order = {order: checked_map(wire, order) for order in orders}
    baseline = by_order[orders[0]]
    schedule_checks = [
        {
            "schedule": list(order),
            "difference_from_first": ex.difference(baseline, maps),
            "maps": ex.maps_wire(maps),
        }
        for order, maps in by_order.items()
    ]
    all_equal = all(item["difference_from_first"] is None for item in schedule_checks)
    require(all_equal == expected_equal, f"unexpected schedule classification: {name}")
    pair_checks = []
    for a, b in ex.incomparable_pairs(parsed):
        pair_wire = problem(parsed.qubits, [e for e in wire["events"] if e["event_id"] in (a, b)])
        left, right = checked_map(pair_wire, (a, b)), checked_map(pair_wire, (b, a))
        witness = ex.difference(left, right)
        pair_checks.append(
            {
                "events": [a, b],
                "equal": witness is None,
                "difference": witness,
                "problem": pair_wire,
                "maps_first_then_second": ex.maps_wire(left),
                "maps_second_then_first": ex.maps_wire(right),
            }
        )
    pairs_equal = all(item["equal"] for item in pair_checks)
    require(pairs_equal == expected_equal, f"unexpected pair classification: {name}")
    require(not pairs_equal or all_equal, "sufficient-condition implication failed")
    return {
        "name": name,
        "classification": classification,
        "problem": wire,
        "expected_schedule_equality": expected_equal,
        "all_schedules_equal": all_equal,
        "nontrivial_schedule_comparison": len(orders) > 1,
        "pair_condition_vacuous": not pair_checks,
        "schedule_count": len(orders),
        "basis_elements_per_map": parsed.dimension**2,
        "record_blocks_per_schedule": len(baseline),
        "pair_checks": pair_checks,
        "schedule_checks": schedule_checks,
        "max_retained_schedule_map_rational_bits": max(map(max_retained_bits, by_order.values())),
    }


def branches_wire(blocks):
    return [
        {
            "record": list(key),
            "probability": ex.trace(value).wire(),
            "unnormalized_state": ex.matrix_wire(value),
        }
        for key, value in blocks.items()
    ]


def analytic_controls(cases):
    bell = matrix([[H, 0, 0, H], [0, 0, 0, 0], [0, 0, 0, 0], [H, 0, 0, H]])
    bell_problem = ex.parse_problem(cases["disjoint_z"][0])
    bell_branches = ex.execute_operator(bell_problem, ("ZA", "ZB"), bell)
    for key, state in bell_branches.items():
        expected = H if key[0][1] == key[1][1] else 0
        require(ex.trace(state) == ex.q(expected), "Bell record regression")
    zx_problem = ex.parse_problem(cases["unordered_zx"][0])
    zero_first = ex.execute_operator(zx_problem, ("Z", "X"), P0)
    zero_reverse = ex.execute_operator(zx_problem, ("X", "Z"), P0)
    for key, state in zero_first.items():
        require(
            ex.trace(state) == ex.q(H if dict(key)["Z"] == "0" else 0),
            "Z-first |0> analytic probability mismatch",
        )
    require(
        all(ex.trace(s) == ex.q(Fraction(1, 4)) for s in zero_reverse.values()),
        "X-first |0> analytic probability mismatch",
    )
    mixed = ex.scale(I, ex.q(H))
    mixed_first = ex.execute_operator(zx_problem, ("Z", "X"), mixed)
    mixed_reverse = ex.execute_operator(zx_problem, ("X", "Z"), mixed)
    require(
        all(
            ex.trace(s) == ex.q(Fraction(1, 4))
            for s in (*mixed_first.values(), *mixed_reverse.values())
        ),
        "mixed-state joint probability mismatch",
    )
    mixed_difference = ex.difference(mixed_first, mixed_reverse)
    require(mixed_difference is not None, "missed equal-probability branch-state conflict")
    discarded = [
        ex.total_map(checked_map(cases["unordered_zx"][0], order))
        for order in (("Z", "X"), ("X", "Z"))
    ]
    depolarizer = tuple(
        tuple(ex.q(H if i in (0, 3) and j in (0, 3) else 0) for j in range(4)) for i in range(4)
    )
    require(
        discarded[0] == discarded[1] == depolarizer,
        "outcome-discarded maps must both be trace(.) I/2",
    )
    zero_wire = cases["zero_outcome"][0]
    zero_maps = checked_map(zero_wire, ("zero",))
    require(
        len(zero_maps) == 2 and zero_maps[(("zero", "impossible"),)] == ex.zeros(4),
        "identically zero outcome was pruned",
    )
    return {
        "bell_local_z": branches_wire(bell_branches),
        "zx_from_zero": {
            "Z_then_X": branches_wire(zero_first),
            "X_then_Z": branches_wire(zero_reverse),
        },
        "zx_from_maximally_mixed": {
            "Z_then_X": branches_wire(mixed_first),
            "X_then_Z": branches_wire(mixed_reverse),
            "branch_state_difference": mixed_difference,
        },
        "zx_discarded_maps_equal_exact_depolarizer": True,
        "identically_zero_outcome_retained": True,
    }


def no_signalling_controls():
    checks = []
    for name, outcomes in (
        ("remote_z", [("0", (P0,)), ("1", (P1,))]),
        ("remote_damping", [("kept", DAMP)]),
    ):
        wire = problem(2, [local(name, 1, outcomes)])
        blocks = checked_map(wire, (name,))
        total = ex.total_map(blocks)
        for k in range(4):
            for l in range(4):
                for a in range(2):
                    for c in range(2):
                        reduced = sum(
                            (total[(2 * a + b) * 4 + 2 * c + b][4 * k + l] for b in range(2)),
                            ex.ZERO,
                        )
                        expected = ex.q(int(a == k // 2 and c == l // 2 and k % 2 == l % 2))
                        require(reduced == expected, "unconditional remote marginal changed")
        checks.append(
            {
                "name": name,
                "problem": wire,
                "maps": ex.maps_wire(blocks),
                "basis_count": 16,
                "partial_trace_equal_for_every_basis_unit": True,
            }
        )
    return checks


def run_suite():
    inventory = fixtures()
    results = [case_result(*item) for item in inventory]
    controls = analytic_controls(
        {name: (wire, expected, kind) for name, wire, expected, kind in inventory}
    )
    no_signalling = no_signalling_controls()
    return {
        "classification": "EXACT_FINITE_RESEARCH_NOT_EMPIRICAL",
        "new_physical_laws_proposed": False,
        "ret_integration_tested": False,
        "gate_advancement_authorized": False,
        "bounds": {
            "qubits": 2,
            "events": 4,
            "outcomes_per_event": 2,
            "kraus_per_outcome": 2,
            "input_rational_bits": 64,
            "internal_rational_component_guard_bits": ex.MAX_BITS,
            "adaptive_settings": False,
            "sampling": False,
        },
        "cases": results,
        "analytic_controls": controls,
        "unconditional_remote_marginal_controls": no_signalling,
        "totals": {
            "fixtures": len(results),
            "main_schedules": sum(r["schedule_count"] for r in results),
            "main_schedule_matrix_unit_executions": sum(
                r["schedule_count"] * r["basis_elements_per_map"] for r in results
            ),
            "incomparable_pairs": sum(len(r["pair_checks"]) for r in results),
            "positive_nontrivial_fixtures": sum(
                r["classification"] == "nontrivial_commutation" for r in results
            ),
            "expected_counterexample_fixtures": sum(
                r["classification"] == "expected_counterexample" for r in results
            ),
            "vacuous_pair_control_fixtures": sum(r["pair_condition_vacuous"] for r in results),
            "additional_pair_schedules": 2 * sum(len(r["pair_checks"]) for r in results),
            "additional_pair_matrix_unit_executions": sum(
                2 * len(r["pair_checks"]) * r["basis_elements_per_map"] for r in results
            ),
            "additional_analytic_map_schedules": 3,
            "additional_analytic_map_matrix_unit_executions": 12,
            "additional_analytic_direct_state_executions": 5,
            "additional_remote_marginal_schedules": len(no_signalling),
            "additional_remote_marginal_matrix_unit_executions": sum(
                r["basis_count"] for r in no_signalling
            ),
        },
    }


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_ledger():
    ledger = {}
    for name in SOURCES:
        path = ROOT / name
        require(path.is_file() and not path.is_symlink(), f"missing/plain-source violation: {name}")
        raw = path.read_bytes()
        ledger[name] = {"bytes": len(raw), "sha256": digest(raw)}
    return ledger


def canonical(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify", action="store_true", help="read-only exact replay of results.json"
    )
    args = parser.parse_args()
    require(bool(sys.flags.isolated), "run with python -I")
    require(sys.pycache_prefix is not None, "set an external -X pycache_prefix")
    cache = Path(sys.pycache_prefix).resolve()
    require(not cache.is_relative_to(ROOT.parents[2]), "bytecode cache must be outside checkout")
    if not args.verify and RESULT.exists():
        raise FileExistsError("results.json already exists; use --verify (never overwrite)")
    frozen = source_ledger()
    existing = None
    original_result_bytes = None
    if args.verify:
        require(RESULT.is_file() and not RESULT.is_symlink(), "missing/plain-result violation")
        original_result_bytes = RESULT.read_bytes()
        existing = json.loads(original_result_bytes)
        require(existing["schema_version"] == "det8-qr01-results-v1", "wrong results schema")
        require(existing["source_ledger"] == frozen, "source ledger changed since capture")
    start = time.perf_counter()
    suite = run_suite()
    elapsed = time.perf_counter() - start
    require(source_ledger() == frozen, "source changed during execution")
    if args.verify:
        require(existing["suite"] == json.loads(canonical(suite)), "exact replay differs")
        require(RESULT.read_bytes() == original_result_bytes, "result changed during replay")
        print(
            json.dumps(
                {
                    "status": "VERIFIED_EXACT_REPLAY",
                    "seconds": elapsed,
                    "result_sha256": digest(original_result_bytes),
                    "totals": suite["totals"],
                }
            )
        )
        return
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    report = {
        "schema_version": "det8-qr01-results-v1",
        "source_ledger": frozen,
        "suite": suite,
        "runtime": {
            "python": sys.version,
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
            "platform": platform.platform(),
            "isolated": bool(sys.flags.isolated),
            "optimized": sys.flags.optimize,
            "bytecode_cache": str(cache),
            "elapsed_seconds": elapsed,
            "process_peak_rss_raw": peak_rss,
            "process_peak_rss_units": "bytes" if sys.platform == "darwin" else "KiB",
            "memory_scope": "process high-water RSS, not an isolated allocation delta",
            "dependencies": "Python standard library only; no det8 imports",
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
