"""Bounded exact certificate and create-only, source-bound evidence driver."""

import argparse
import hashlib
import itertools
import json
import os
import signal
import sys
import types
import unittest
from contextlib import contextmanager
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_PATHS = (
    "README.md",
    "primary.py",
    "reference.py",
    "study.py",
    "test_study.py",
    "../t8-q-renewal-port-candidate-2026-09-12/CANDIDATE.md",
)
BRANCHES = tuple(itertools.product(("a", "b", "ab"), (0, 1)))
SCHEMA = "t8-q-renewal-port-verification-v1"


@contextmanager
def deadline(seconds=60):
    def expired(_signum, _frame):
        raise TimeoutError("60-second bounded certificate deadline")

    old = signal.signal(signal.SIGALRM, expired)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    if type(value) is Fraction:
        return {"q": [value.numerator, value.denominator]}
    if type(value) in (tuple, list):
        return [encode(item) for item in value]
    if type(value) is dict:
        return {key: encode(item) for key, item in value.items()}
    if value is None or type(value) in (str, int, bool):
        return value
    raise ValueError("unsupported report type")


def canonical(value):
    return (json.dumps(encode(value), sort_keys=True, separators=(",", ":")) + "\n").encode()


def strict_loads(blob):
    require(type(blob) is bytes and len(blob) <= 20_000_000, "oversize evidence")

    def pairs(items):
        answer = {}
        for key, value in items:
            require(key not in answer, "duplicate JSON key")
            answer[key] = value
        return answer

    def reject(_value):
        raise ValueError("nonfinite JSON value")

    return json.loads(blob, object_pairs_hook=pairs, parse_constant=reject)


def snapshot(root=ROOT):
    result = {}
    for name in SOURCE_PATHS:
        blob = (root / name).read_bytes()
        require(len(blob) <= 200_000, "source exceeds fixed byte bound")
        result[name] = blob
    return result


def manifest(sources):
    require(set(sources) == set(SOURCE_PATHS), "source inventory mismatch")
    return {
        "schema": SCHEMA + "-freeze",
        "sources": {
            name: {"bytes": len(sources[name]), "sha256": hashlib.sha256(sources[name]).hexdigest()}
            for name in SOURCE_PATHS
        },
    }


def checked_freeze(root=ROOT):
    sources = snapshot(root)
    recorded = strict_loads((root / "source-freeze.json").read_bytes())
    require(recorded == manifest(sources), "frozen source mismatch")
    return sources, recorded


def load_source(sources, name):
    require(name in ("primary.py", "reference.py", "test_study.py"), "unsupported executable")
    module = types.ModuleType(name[:-3])
    module.__file__ = str(ROOT / name)
    # Fixed allow-listed local source bytes, authenticated on every frozen run.
    exec(compile(sources[name], module.__file__, "exec"), module.__dict__)  # noqa: S102
    return module


def routes(sources):
    return load_source(sources, "primary.py"), load_source(sources, "reference.py")


def histories():
    for length in range(4):
        for word in itertools.product(BRANCHES, repeat=length):
            yield (
                f"n{length}:" + ",".join(action + str(bit) for action, bit in word),
                [[i, action, bit] for i, (action, bit) in enumerate(word)],
            )
    yield "named:diamond", [[0, "ab", 0], [1, "a", 0], [2, "b", 0], [3, "ab", 0]]


def transport_labels(row, mapping):
    return {
        **row,
        "events": sorted(mapping[e] for e in row["events"]),
        "order": sorted([mapping[u], mapping[v]] for u, v in row["order"]),
        "records": sorted(
            [mapping[e], action, bit, setting] for e, action, bit, setting in row["records"]
        ),
        "pasts": sorted([mapping[e], sorted(mapping[v] for v in past)] for e, past in row["pasts"]),
        "next": [
            {**branch, "past": sorted(mapping[e] for e in branch["past"])} for branch in row["next"]
        ],
    }


def controls(primary, reference):
    fork = primary.evaluate([[0, "ab", 0], [1, "a", 0], [2, "b", 0]])
    join = reference.evaluate([[0, "a", 0], [1, "b", 0], [2, "ab", 0]])
    coordinates = []
    for action, setting in BRANCHES:
        forward = primary.permutation(action, setting)
        inverse = reference.inverse(action, setting)
        require([inverse[v] for v in forward] == list(range(9)), "inverse failure")
        coordinates.append(
            {"action": action, "setting": setting, "forward": forward, "inverse": inverse}
        )
    cycle = primary.permutation("a", 0)
    reflection = primary.permutation("a", 1)
    cycle_after = [cycle[reflection[v]] for v in range(9)]
    reflection_after = [reflection[cycle[v]] for v in range(9)]
    outside = []
    for changed_bit in (0, 1):
        row = primary.evaluate([[0, "a", 1], [1, "b", changed_bit]])
        outside.append(
            next(
                branch
                for branch in row["next"]
                if branch["action"] == "a" and branch["outcome"] == 0
            )
        )
    stage_orders = []
    for word in (("a", "b"), ("b", "a")):
        image = list(range(9))
        for stage, action in enumerate(word):
            perm = primary.permutation(action, stage % 2)
            image = [perm[v] for v in image]
        stage_orders.append(image)
    zero = (Fraction(0), Fraction(0))
    dstar = [zero for _ in range(81)]
    for atom in range(9):
        dstar[9 * atom + atom] = (Fraction(1, 10), Fraction(0))
    dstar[3] = (Fraction(1, 20), Fraction(1, 20))
    dstar[27] = (Fraction(1, 20), Fraction(-1, 20))
    conjugate = [(real, -imaginary) for real, imaginary in dstar]
    zero_mass = [zero for _ in range(81)]
    zero_mass[0] = zero_mass[10] = (Fraction(1), Fraction(0))
    zero_mass[1] = zero_mass[9] = (Fraction(-1), Fraction(0))

    def apply(kernel, cell_map, weight):
        result = [zero for _ in range(81)]
        for source, target in enumerate(cell_map):
            if target is not None:
                result[target] = tuple(weight * part for part in kernel[source])
        return result

    def mass(kernel):
        return tuple(sum((entry[part] for entry in kernel), Fraction(0)) for part in (0, 1))

    branches = primary.evaluate([])["next"]
    witnesses = []
    for name, kernel in (
        ("dstar", dstar),
        ("conjugate", conjugate),
        ("nonzero_zero_mass", zero_mass),
    ):
        outputs = [apply(kernel, branch["cell_map"], branch["weight"]) for branch in branches]
        witnesses.append(
            {
                "name": name,
                "kernel": kernel,
                "mass": mass(kernel),
                "branch_outputs": outputs,
                "branch_masses": [mass(output) for output in outputs],
            }
        )
    return {
        "coordinates": coordinates,
        "fork_join": {
            "fork": fork,
            "join": join,
            "same_payload": fork["cell_map"] == join["cell_map"]
            and fork["weight"] == join["weight"],
            "distinct_order": fork["order"] != join["order"],
        },
        "same_port": {
            "cycle_after_reflection": cycle_after,
            "reflection_after_cycle": reflection_after,
            "unequal": cycle_after != reflection_after,
        },
        "wrong_inverse": [
            {
                "action": action,
                "setting": setting,
                "detected": primary.permutation(action, setting)
                != reference.inverse(action, setting),
            }
            for action, setting in (("a", 0), ("ab", 1))
        ],
        "locality": {
            "outside_bit_zero": outside[0],
            "outside_bit_one": outside[1],
            "equal": outside[0] == outside[1],
        },
        "stage_negative": {
            "ab": stage_orders[0],
            "ba": stage_orders[1],
            "detected": stage_orders[0] != stage_orders[1],
        },
        "kernels": witnesses,
        "dstar_unscaled_block_determinant": Fraction(1) - Fraction(1, 2),
        "singleton_restriction_total": sum((dstar[9 * i + i][0] for i in range(9)), Fraction(0)),
        "interference": dstar[3][0] + dstar[27][0],
        "branch_effects": [[branch["weight"] for _ in range(81)] for branch in branches],
        "sum_effect": [
            sum((branch["weight"] for branch in branches), Fraction(0)) for _ in range(81)
        ],
    }


def analyze(sources=None):
    sources = snapshot() if sources is None else sources
    primary, reference = routes(sources)
    rows = []
    extension_count = 0
    for case, history in histories():
        expected = primary.evaluate(history)
        require(expected == reference.evaluate(history), f"route mismatch: {case}")
        extensions = []
        records = {event: (action, bit) for event, action, bit in history}
        for ordering in itertools.permutations(expected["events"]):
            positions = {event: i for i, event in enumerate(ordering)}
            if any(positions[u] >= positions[v] for u, v in expected["order"]):
                continue
            replay = [[event, *records[event]] for event in ordering]
            require(primary.evaluate(replay) == expected, f"primary covariance: {case}")
            require(reference.evaluate(replay) == expected, f"reference covariance: {case}")
            extensions.append(list(ordering))
        extension_count += len(extensions)
        mapping = {event: 10 + 7 * (len(history) - 1 - event) for event in expected["events"]}
        relabeled = [[mapping[e], action, bit] for e, action, bit in history]
        transported = transport_labels(expected, mapping)
        require(primary.evaluate(relabeled) == transported, f"primary label covariance: {case}")
        require(reference.evaluate(relabeled) == transported, f"reference label covariance: {case}")
        rows.append(
            {
                "case": case,
                "history": history,
                "result": expected,
                "linear_extensions": extensions,
                "label_map": sorted([e, target] for e, target in mapping.items()),
                "relabeled": transported,
            }
        )
    return {
        "schema": SCHEMA + "-report",
        "scope": {
            "base_rows": 260,
            "exhaustive_through_births": 3,
            "named_four_birth_rows": 1,
            "linear_extension_replays_per_route": extension_count,
            "label_replays_per_route": len(rows),
            "matrix_units_per_map": 81,
            "next_branches_per_row": 9,
        },
        "rows": rows,
        "controls": controls(primary, reference),
    }


def write_exclusive(path, value):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(canonical(value))


def capture(root=ROOT):
    require(
        not (root / "source-freeze.json").exists() and not (root / "results.json").exists(),
        "capture already exists or is partial",
    )
    sources = snapshot(root)
    report = analyze(sources)
    require(snapshot(root) == sources, "source changed during execution")
    frozen = manifest(sources)
    result = {"schema": SCHEMA + "-capture", "freeze": frozen, "report": report}
    write_exclusive(root / "source-freeze.json", frozen)
    write_exclusive(root / "results.json", result)
    return result


def verify(root=ROOT):
    sources, frozen = checked_freeze(root)
    captured = strict_loads((root / "results.json").read_bytes())
    require(
        captured
        == encode({"schema": SCHEMA + "-capture", "freeze": frozen, "report": analyze(sources)}),
        "captured report mismatch",
    )
    require(snapshot(root) == sources, "source changed during replay")
    return captured


def run_tests(sources):
    sys.modules["study"] = sys.modules[__name__]
    module = load_source(sources, "test_study.py")
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(module)
    )
    require(result.wasSuccessful(), "test suite failed")
    return {
        "tests": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--tests", action="store_true")
    selection.add_argument("--capture", action="store_true")
    selection.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    with deadline():
        if args.tests:
            sources = checked_freeze()[0] if (ROOT / "source-freeze.json").exists() else snapshot()
            print(json.dumps(run_tests(sources), sort_keys=True))
        else:
            result = capture() if args.capture else verify()
            print(
                json.dumps(
                    {
                        "operation": "capture" if args.capture else "verify",
                        "scope": result["report"]["scope"],
                        "results_sha256": hashlib.sha256(
                            (ROOT / "results.json").read_bytes()
                        ).hexdigest(),
                    },
                    sort_keys=True,
                )
            )


if __name__ == "__main__":
    main()
