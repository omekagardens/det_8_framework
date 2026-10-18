"""Create or replay the exact QR-02 candidate and information-loss study."""

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

import coarse
import reference_qr02

ex = coarse.ex
SOURCES = (
    "README.md",
    "coarse.py",
    "reference_qr02.py",
    "study.py",
    "test_qr02.py",
    "../qr-01-quantum-records-2026-09-05/exact.py",
    "../qr-01-quantum-records-2026-09-05/reference.py",
)
RESULT = ROOT / "results.json"
PRIOR = ROOT.parent / "qr-01-quantum-records-2026-09-05" / "results.json"
PRIOR_SHA = "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matrix(rows):
    return tuple(tuple(x if isinstance(x, ex.C) else ex.q(x) for x in row) for row in rows)


I = ex.identity(2)
P0, P1 = matrix([[1, 0], [0, 0]]), matrix([[0, 0], [0, 1]])
X, Z = matrix([[0, 1], [1, 0]]), matrix([[1, 0], [0, -1]])
S = matrix([[1, 0], [0, ex.q(0, 1)]])
JUMP = matrix([[0, 1], [0, 0]])
H = Fraction(1, 2)
PX = (matrix([[H, H], [H, H]]), matrix([[H, -H], [-H, H]]))
PY = (matrix([[H, ex.q(0, -H)], [ex.q(0, H), H]]), matrix([[H, ex.q(0, H)], [ex.q(0, -H), H]]))


def instrument(outcomes, support=(0,)):
    return {
        "support": list(support),
        "outcomes": [
            {"label": label, "kraus": [ex.matrix_wire(m) for m in matrices]}
            for label, matrices in outcomes
        ],
    }


def unitary(operator):
    return instrument([("done", (operator,))])


def embed(inst, qubit):
    return instrument(
        [
            (
                o["label"],
                tuple(
                    ex.tensor(ex.decode_matrix(m, 2), I)
                    if qubit == 0
                    else ex.tensor(I, ex.decode_matrix(m, 2))
                    for m in o["kraus"]
                ),
            )
            for o in inst["outcomes"]
        ],
        (qubit,),
    )


def problem(source, fine, candidate, groups=None, qubits=1):
    if groups is None:
        groups = {o["label"]: "merged" for o in source["outcomes"]}
    return {
        "schema_version": "det8-qr02-problem-v1",
        "qubits": qubits,
        "source": source,
        "groups": [{"fine": x, "coarse": z} for x, z in groups.items()],
        "fine_future": [{"fine": x, "instrument": inst} for x, inst in fine.items()],
        "coarse_future": [{"coarse": z, "instrument": inst} for z, inst in candidate.items()],
    }


def fixtures():
    source_z = instrument([("0", (P0,)), ("1", (P1,))])
    x_measure = instrument([("+", (PX[0],)), ("-", (PX[1],))])
    y_measure = instrument([("+", (PY[0],)), ("-", (PY[1],))])
    ident, flip = unitary(I), unitary(X)
    controlled = {"0": ident, "1": flip}
    reset = instrument([("done", (P0, JUMP))])
    erasing = instrument([("0", (P0,)), ("1", (JUMP,))])
    amp3, amp4 = ex.q(Fraction(3, 5)), ex.q(Fraction(4, 5))
    coin = instrument([("0", (ex.scale(I, amp3),)), ("1", (ex.scale(I, amp4),))])
    mixture = instrument([("done", (ex.scale(I, amp3), ex.scale(S, amp4)))])
    dephase = instrument(
        [
            ("0", (ex.scale(P0, amp3), ex.scale(P1, amp3))),
            ("1", (ex.scale(P0, amp4), ex.scale(P1, amp4))),
        ]
    )
    zero = instrument([("0", (I,)), ("1", (ex.zeros(2),))])
    phase_error = instrument([("0", (ex.scale(I, amp3),)), ("1", (ex.scale(Z, amp4),))])
    return [
        (
            "independent_x_after_z",
            problem(source_z, {"0": x_measure, "1": x_measure}, {"merged": x_measure}),
            True,
            True,
            "genuine_grouping",
        ),
        (
            "no_merge_control",
            problem(
                source_z, controlled, {"left": ident, "right": flip}, {"0": "left", "1": "right"}
            ),
            True,
            True,
            "no_merge_control",
        ),
        (
            "naive_controlled_x",
            problem(source_z, controlled, {"merged": ident}),
            False,
            False,
            "failed_candidate_not_impossibility",
        ),
        (
            "reachable_reset_repair",
            problem(source_z, controlled, {"merged": reset}),
            False,
            True,
            "reachable_physical_replacement",
        ),
        (
            "erased_record_irrecoverable",
            problem(erasing, controlled, {"merged": ident}),
            False,
            False,
            "collision_impossibility_control",
        ),
        (
            "coin_averaged_future",
            problem(coin, {"0": ident, "1": unitary(S)}, {"merged": mixture}),
            False,
            True,
            "reachable_physical_replacement",
        ),
        (
            "two_qubit_local_forgetting",
            problem(
                embed(source_z, 0),
                {"0": embed(x_measure, 1), "1": embed(x_measure, 1)},
                {"merged": embed(x_measure, 1)},
                qubits=2,
            ),
            True,
            True,
            "genuine_grouping",
        ),
        (
            "multi_kraus_grouping",
            problem(dephase, {"0": y_measure, "1": y_measure}, {"merged": y_measure}),
            True,
            True,
            "genuine_grouping",
        ),
        (
            "zero_branch_control",
            problem(zero, controlled, {"merged": ident}),
            False,
            True,
            "unreachable_branch_control",
        ),
        (
            "phase_flip_nonphysical_inverse",
            problem(phase_error, {"0": ident, "1": unitary(Z)}, {"merged": ident}),
            False,
            False,
            "nonpositive_unique_inverse_control",
        ),
    ]


def checked_maps(wire):
    actual, independent = coarse.maps(wire), reference_qr02.reference_maps(wire)
    require(set(actual) == set(independent), "reference bundle inventory mismatch")
    for name, blocks in actual.items():
        converted = {
            record: tuple(tuple(ex.C(*v) for v in row) for row in block)
            for record, block in independent[name].items()
        }
        require(ex.difference(blocks, converted) is None, f"reference map mismatch: {name}")
    return actual


def bit_length(bundles):
    return max(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length())
        for blocks in bundles.values()
        for block in blocks.values()
        for row in block
        for scalar in row
        for value in (scalar.real, scalar.imag)
    )


def case_result(fixture):
    name, wire, expected_unrestricted, expected_reachable, kind = fixture
    bundles = checked_maps(wire)
    reachable_difference = ex.difference(
        bundles["fine_then_forget"], bundles["forget_then_candidate"]
    )
    unrestricted_difference = ex.difference(
        bundles["unrestricted_fine_future"], bundles["unrestricted_coarse_future"]
    )
    require(
        (reachable_difference is None) == expected_reachable, f"unexpected reachable result: {name}"
    )
    require(
        (unrestricted_difference is None) == expected_unrestricted,
        f"unexpected arbitrary-block result: {name}",
    )
    require(
        unrestricted_difference is not None or reachable_difference is None,
        "unrestricted equality failed to imply reachable equality",
    )
    d2 = (2 ** wire["qubits"]) ** 2
    return {
        "name": name,
        "classification": kind,
        "problem": wire,
        "expected_unrestricted_equal": expected_unrestricted,
        "expected_reachable_equal": expected_reachable,
        "unrestricted_equal": unrestricted_difference is None,
        "reachable_equal": reachable_difference is None,
        "unrestricted_difference": unrestricted_difference,
        "reachable_difference": reachable_difference,
        "initial_basis_evaluations": d2,
        "additional_future_basis_evaluations": d2
        * (len(wire["fine_future"]) + len(wire["coarse_future"])),
        "retained_map_blocks": sum(len(blocks) for blocks in bundles.values()),
        "max_retained_rational_bits": bit_length(bundles),
        "maps": {name: ex.maps_wire(blocks) for name, blocks in bundles.items()},
    }, bundles


def apply_map(superoperator, operator):
    d = len(operator)
    flat = tuple(value for row in operator for value in row)
    output = tuple(
        sum((a * b for a, b in zip(row, flat, strict=True)), ex.ZERO) for row in superoperator
    )
    return tuple(tuple(output[d * i + j] for j in range(d)) for i in range(d))


def states(wire, bundles, rho):
    result = coarse.propagate(coarse.parse(wire), rho)
    for name, blocks in result.items():
        expected = {record: apply_map(block, rho) for record, block in bundles[name].items()}
        require(ex.difference(blocks, expected) is None, f"state vs full map mismatch: {name}")
    return result


def state_wire(blocks):
    return [
        {
            "record": list(record),
            "unnormalized_state": ex.matrix_wire(state),
            "probability": ex.trace(state).wire(),
        }
        for record, state in blocks.items()
    ]


def controls(inventory, bundle_index):
    wires = {f[0]: f[1] for f in inventory}
    state_log = []

    def run(name, input_name, rho):
        outputs = states(wires[name], bundle_index[name], rho)
        state_log.append(
            {
                "fixture": name,
                "input": input_name,
                "input_matrix": ex.matrix_wire(rho),
                "outputs": {key: state_wire(value) for key, value in outputs.items()},
            }
        )
        return outputs

    merged = (("coarse", "merged"),)
    done = (("coarse", "merged"), ("future", "done"))
    plus = (("coarse", "merged"), ("future", "+"))
    forgotten = run("independent_x_after_z", "plus", PX[0])
    require(forgotten["source_coarse"][merged] == ex.scale(I, ex.q(H)), "forgotten Z is dephasing")
    require(ex.trace(forgotten["fine_then_forget"][plus]) == ex.q(H), "dephased X+ probability")
    coherent_sum = ex.add(P0, P1)
    wrong = ex.mul(ex.mul(coherent_sum, PX[0]), ex.dagger(coherent_sum))
    wrong_probability = ex.trace(ex.mul(PX[0], wrong))
    require(wrong == PX[0] and wrong_probability == ex.ONE, "coherent-sum negative control")

    erased0 = run("erased_record_irrecoverable", "zero", P0)
    erased1 = run("erased_record_irrecoverable", "one", P1)
    require(erased0["source_coarse"] == erased1["source_coarse"], "missing coarse-state collision")
    require(
        erased0["fine_then_forget"][done] == P0 and erased1["fine_then_forget"][done] == P1,
        "missing required future separation",
    )
    naive = run("naive_controlled_x", "one", P1)
    repaired = run("reachable_reset_repair", "one", P1)
    require(
        naive["fine_then_forget"][done] == P0 and naive["forget_then_candidate"][done] == P1,
        "naive candidate must fail on one",
    )
    require(
        repaired["fine_then_forget"][done] == repaired["forget_then_candidate"][done] == P0,
        "physical reset repair failed",
    )

    source0 = run("independent_x_after_z", "zero", P0)
    source1 = run("independent_x_after_z", "one", P1)
    require(
        ex.trace(source0["source_coarse"][merged])
        == ex.trace(source1["source_coarse"][merged])
        == ex.ONE,
        "coarse-probability identity control",
    )
    future_z_probs = [
        ex.trace(ex.mul(P0, output["source_coarse"][merged])) for output in (source0, source1)
    ]
    require(future_z_probs == [ex.ONE, ex.ZERO], "later Z must distinguish retained states")

    phase = bundle_index["phase_flip_nonphysical_inverse"]
    channel = phase["source_coarse"][merged]
    inverse = tuple(
        tuple(ex.q((1 if i in (0, 3) else Fraction(-25, 7)) if i == j else 0) for j in range(4))
        for i in range(4)
    )
    require(
        ex.mul(inverse, channel) == ex.mul(channel, inverse) == ex.identity(4),
        "phase channel inverse is not two-sided",
    )
    require(
        phase["fine_then_forget"][done] == ex.identity(4), "fine phase correction must be identity"
    )
    inverse_plus = apply_map(inverse, PX[0])
    expectation = ex.trace(ex.mul(PX[0], inverse_plus))
    require(
        inverse_plus == matrix([[H, Fraction(-25, 14)], [Fraction(-25, 14), H]])
        and expectation == ex.q(Fraction(-9, 7)),
        "nonpositive inverse witness failed",
    )
    bell = matrix([[H, 0, 0, H], [0, 0, 0, 0], [0, 0, 0, 0], [H, 0, 0, H]])
    entangled = run("two_qubit_local_forgetting", "bell", bell)
    require(
        entangled["fine_then_forget"] == entangled["forget_then_candidate"], "Bell grouping failed"
    )
    require(
        {ex.trace(block) for block in entangled["fine_then_forget"].values()} == {ex.q(H)},
        "Bell local future probabilities changed",
    )
    return {
        "state_executions": state_log,
        "classical_vs_coherent": {
            "classical_later_x_plus": ex.q(H).wire(),
            "coherent_later_x_plus": wrong_probability.wire(),
            "wrong_coherent_state": ex.matrix_wire(wrong),
        },
        "collision_proves_no_coarse_only_replacement": True,
        "failed_identity_candidate_has_physical_reset_repair": True,
        "same_coarse_probability_later_z_zero": [p.wire() for p in future_z_probs],
        "linear_inverse_is_not_physical": {
            "source_map": ex.matrix_wire(channel),
            "two_sided_inverse": ex.matrix_wire(inverse),
            "corrected_fine_map_is_identity": True,
            "inverse_of_plus": ex.matrix_wire(inverse_plus),
            "plus_expectation": expectation.wire(),
            "conclusion": "not_positive_therefore_not_CPTP",
        },
    }


def run_suite():
    inventory = fixtures()
    cases, bundles = [], {}
    for fixture in inventory:
        result, maps = case_result(fixture)
        cases.append(result)
        bundles[fixture[0]] = maps
    analytical = controls(inventory, bundles)
    return {
        "classification": "EXACT_FINITE_RESEARCH_NOT_EMPIRICAL",
        "cases": cases,
        "analytical_controls": analytical,
        "bounds": {
            "qubits": 2,
            "stages": 2,
            "supplied_outcomes_per_instrument": 2,
            "supplied_kraus_per_outcome": 2,
            "grouped_kraus_terms_per_outcome": 4,
            "input_rational_bits": 64,
            "internal_component_guard_bits": ex.MAX_BITS,
            "general_adaptive_graph": False,
            "general_channel_synthesis": False,
        },
        "ret_integration_tested": False,
        "new_physical_laws": False,
        "totals": {
            "fixtures": len(cases),
            "reference_bundle_comparisons": len(cases) * 6,
            "retained_map_blocks": sum(r["retained_map_blocks"] for r in cases),
            "initial_basis_evaluations": sum(r["initial_basis_evaluations"] for r in cases),
            "additional_future_basis_evaluations": sum(
                r["additional_future_basis_evaluations"] for r in cases
            ),
            "direct_state_executions": len(analytical["state_executions"]),
            "unrestricted_equal_fixtures": sum(r["unrestricted_equal"] for r in cases),
            "reachable_equal_fixtures": sum(r["reachable_equal"] for r in cases),
            "reachable_equal_but_unrestricted_unequal": sum(
                r["reachable_equal"] and not r["unrestricted_equal"] for r in cases
            ),
            "failed_candidate_fixtures": sum(not r["reachable_equal"] for r in cases),
            "analytic_impossibility_controls": 2,
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
        ledger[name] = {"sha256": digest(raw), "bytes": len(raw)}
    return ledger


def prior_identity():
    require(PRIOR.is_file() and not PRIOR.is_symlink(), "missing/plain QR-01 artifact violation")
    raw = PRIOR.read_bytes()
    require(digest(raw) == PRIOR_SHA, "QR-01 evidence differs from the retained baseline")
    return {"sha256": digest(raw), "bytes": len(raw)}


def canonical(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


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
        require(existing["schema_version"] == "det8-qr02-results-v1", "wrong results schema")
        require(
            existing["source_ledger"] == frozen and existing["prior_artifact"] == prior,
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
        "schema_version": "det8-qr02-results-v1",
        "source_ledger": frozen,
        "prior_artifact": prior,
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
            "accounting_scope": "exact suite; excludes artifact serialization and later comparison overhead",
            "dependencies": "Python standard library; pinned QR-01 research sources; no RET imports",
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
