"""BR fixed-record confidence boundary and source-bound evidence; no old math rerun."""

import argparse
import copy
import hashlib
import json
import math
import os
import platform
import stat
import sys
import time
import types
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_LIMIT = 262144
ARTIFACT_LIMIT = 16777216
PROTOCOL_SHA256 = "252d1a13c07129734fa30792ad18b2694d5e3b3cb659996c4017be0b4bf40ad2"
UTILITY_SHA256 = "157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55"
UTILITY_SOURCE = "../qr-05bm-relative-volume-verification-2026-09-09/study.py"
UTILITY_PATH = ROOT / UTILITY_SOURCE
SOURCE_PATHS = (
    "README.md",
    "protocol.json",
    "primary.py",
    "reference.py",
    "study.py",
    "test_qr05br.py",
    UTILITY_SOURCE,
    "../qr-05bq-finite-record-uncertainty-design-2026-09-09/README.md",
    "../qr-05bq-finite-record-uncertainty-design-2026-09-09/RESULTS.md",
    "../qr-05bp-population-intervals-2026-09-09/README.md",
    "../qr-05bp-population-intervals-2026-09-09/RESULTS.md",
)
EXPECTED_PROTOCOL = {
    "schema": "qr05br-protocol-v1",
    "quota": 4,
    "alpha": [1, 20],
    "tail_allocations": [[1, 80], [1, 80], [1, 80], [1, 80]],
    "grid_denominator": 256,
    "regions": {
        "Q": [[0, 1], [1, 1], [0, 1], [1, 1]],
        "I1": [[0, 1], [1, 2], [0, 1], [1, 2]],
        "I2": [[0, 1], [3, 4], [0, 1], [1, 2]],
    },
    "geometries": [
        {"id": "flat", "eta": 0, "scale": 1},
        {"id": "conformal", "eta": 1, "scale": 1},
        {"id": "flat_x4", "eta": 0, "scale": 4},
        {"id": "conformal_x4", "eta": 1, "scale": 4},
    ],
    "density_bounds": [
        {"id": "uniform", "interval": [[0, 1], [0, 1]]},
        {"id": "half", "interval": [[0, 1], [1, 2]]},
        {"id": "one", "interval": [[0, 1], [1, 1]]},
        {"id": "two", "interval": [[0, 1], [2, 1]]},
    ],
    "fixtures": [
        {"id": "flat_0", "eta": 0, "delta": [0, 1]},
        {"id": "flat_1", "eta": 0, "delta": [1, 1]},
        {"id": "flat_interior", "eta": 0, "delta": [16, 11]},
        {"id": "conformal_0", "eta": 1, "delta": [0, 1]},
        {"id": "conformal_1", "eta": 1, "delta": [1, 1]},
        {"id": "conformal_interior", "eta": 1, "delta": [45, 158]},
    ],
    "ties": [
        {"id": "lower_tie", "side": "lower", "k": 4, "epsilon": [1, 16]},
        {"id": "upper_tie", "side": "upper", "k": 0, "epsilon": [1, 16]},
    ],
    "observer": {
        "schema": "qr05br-record-query-v1",
        "protocol_id": "qr05br-n4-g256-a20-v1",
        "data_kind": "paired_causal_records",
        "bound_basis": "external_assumption",
        "result_schema": "qr05br-record-result-v1",
        "confidence_basis": "fixed_iid_paired_binomial_union",
        "coverage_kind": "unconditional_model_relative",
    },
    "coverage": {
        "tail_rows": 1285,
        "tail_values": 2570,
        "intervals": 5,
        "counts": 15,
        "cases": 60,
        "hypotheses": 240,
        "fixtures": 6,
        "count_probabilities": 90,
        "summaries": 24,
        "scale_pairs": 2,
        "comparisons": 2,
        "ties": 2,
        "obstruction_cases": 60,
        "obstruction_coverage": 4,
    },
    "limits": {
        "source_bytes": 262144,
        "artifact_bytes": 16777216,
        "analysis_seconds": 30,
        "suite_seconds": 120,
        "alternate_reference_runs": 1,
    },
}


def _load_utilities(path):
    """Authenticate the bounded regular source before executing any of its bytes."""
    path = Path(path)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        before = path.stat(follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode) or before.st_size > SOURCE_LIMIT:
            raise ValueError("utility must be a bounded regular source")
        with os.fdopen(os.open(path, flags), "rb") as handle:
            opened = os.fstat(handle.fileno())
            if not stat.S_ISREG(opened.st_mode) or opened.st_size > SOURCE_LIMIT:
                raise ValueError("utility source type/size changed")
            data = handle.read(SOURCE_LIMIT + 1)
            after = os.fstat(handle.fileno())
        visible = path.stat(follow_symlinks=False)
    except OSError as exc:
        raise ValueError("unreadable utility source") from exc
    signature = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)
    if (
        signature(before) != signature(opened)
        or signature(opened) != signature(after)
        or signature(after) != signature(visible)
        or len(data) > SOURCE_LIMIT
        or hashlib.sha256(data).hexdigest() != UTILITY_SHA256
    ):
        raise ValueError("utility source identity differs")
    module = types.ModuleType("_qr05br_checked_bm_utilities")
    module.__file__ = str(path.resolve())
    # The literal digest is checked before this fresh local-source execution.
    exec(compile(data, module.__file__, "exec"), module.__dict__)  # noqa: S102
    return data, module


UTILITY_BYTES, UTILITY = _load_utilities(UTILITY_PATH)
read_bounded = UTILITY.read_bounded
strict_loads = UTILITY.strict_loads
canonical = UTILITY.canonical
encode = UTILITY.encode
decode = UTILITY.decode
require_equal = UTILITY.require_equal
identities = UTILITY.identities
_analysis_deadline = UTILITY._analysis_deadline
_write_new = UTILITY._write_new


def source_snapshot():
    snapshot = {name: read_bounded(ROOT / name, SOURCE_LIMIT) for name in SOURCE_PATHS}
    if snapshot[UTILITY_SOURCE] != UTILITY_BYTES:
        raise ValueError("loaded utility bytes differ from current source snapshot")
    return snapshot


def _check_snapshot(snapshot):
    if snapshot != source_snapshot():
        raise ValueError("BR source bytes changed")


def _protocol(snapshot):
    if snapshot[UTILITY_SOURCE] != UTILITY_BYTES:
        raise ValueError("utility snapshot differs from loaded code")
    data = snapshot["protocol.json"]
    if hashlib.sha256(data).hexdigest() != PROTOCOL_SHA256:
        raise ValueError("protocol bytes differ from prospective specification")
    protocol = strict_loads(data)
    require_equal(protocol, EXPECTED_PROTOCOL)
    return protocol


def load_engine(blob, name):
    module = types.ModuleType(name)
    module.__file__ = str(ROOT / (name + ".py"))
    # Fresh code from the checked BR source snapshot, with no cached imports.
    exec(compile(blob, module.__file__, "exec"), module.__dict__)  # noqa: S102
    return module


def analyze():
    with _analysis_deadline():
        snapshot = source_snapshot()
        protocol = _protocol(snapshot)
        reports = []
        for filename in ("primary.py", "reference.py"):
            supplied = copy.deepcopy(protocol)
            engine = load_engine(snapshot[filename], filename[:-3])
            report = engine.analyze(supplied)
            require_equal(supplied, protocol)
            require_equal(report, report)
            reports.append(report)
        require_equal(reports[0], reports[1])
        _check_snapshot(snapshot)
        return reports[0]


def _confidence():
    return {
        "quota": 4,
        "alpha": Fraction(1, 20),
        "tail_allocations": [Fraction(1, 80) for _ in range(4)],
        "grid_denominator": 256,
        "confidence_basis": "fixed_iid_paired_binomial_union",
        "bound_basis": "external_assumption",
        "coverage_kind": "unconditional_model_relative",
    }


def _interval_for_count(k):
    """Fixed inclusive tails, selected directly with integer inequalities."""
    if type(k) is not int or not 0 <= k <= 4:
        raise ValueError("count outside fixed quota")
    denominator = 256**4
    lower, upper = 0, 256
    found_upper = False
    for j in range(257):
        if j == 0:
            masses = [denominator, 0, 0, 0, 0]
        elif j == 256:
            masses = [0, 0, 0, 0, denominator]
        else:
            masses = [math.comb(4, r) * j**r * (256 - j) ** (4 - r) for r in range(5)]
        plus, minus = sum(masses[k:]), sum(masses[: k + 1])
        if 80 * plus <= denominator:
            lower = j
        if not found_upper and 80 * minus <= denominator:
            upper, found_upper = j, True
    if lower > upper:
        raise ValueError("reversed count interval")
    return [Fraction(lower, 256), Fraction(upper, 256)]


def _inverse(intervals, bound_pair):
    upper = Fraction(*bound_pair)
    nested = intervals[0][0] <= intervals[1][1]
    worlds, targets, nuisance = [], set(), []
    areas = (Fraction(1), Fraction(1, 4), Fraction(3, 8))
    for identifier, eta in (("flat", 0), ("conformal", 1), ("flat_x4", 0), ("conformal_x4", 1)):
        # Common metric scale cancels. These are public continuous-family moments.
        coefficients = [(t + eta * t**2 / 4, t**2 / 4 + eta * t**3 / 9) for t in areas]
        aq, bq = coefficients[0]
        low, high = Fraction(0), upper
        feasible = True
        for (ai, bi), (lower_q, upper_q) in zip(coefficients[1:], intervals, strict=True):
            for constant, slope in (
                (ai - lower_q * aq, bi - lower_q * bq),
                (upper_q * aq - ai, upper_q * bq - bi),
            ):
                if slope == 0:
                    if constant < 0:
                        feasible = False
                        break
                elif slope > 0:
                    low = max(low, -constant / slope)
                else:
                    high = min(high, -constant / slope)
                if low > high:
                    feasible = False
                    break
            if not feasible:
                break
        if not feasible:
            continue
        if not nested:
            raise ValueError("coupled inverse contradicts nested channel")
        for delta in (low, high):
            denominator = aq + bq * delta
            if denominator <= 0 or any(
                not lower_q <= (ai + bi * delta) / denominator <= upper_q
                for (ai, bi), (lower_q, upper_q) in zip(coefficients[1:], intervals, strict=True)
            ):
                raise ValueError("coupled interval failed endpoint certification")
        worlds.append(identifier)
        targets.add(Fraction(16 + eta, 16 * (4 + eta)))
        nuisance.append({"id": identifier, "delta": [low, high]})
    target_list = sorted(targets)
    status = "infeasible" if not worlds else "identified" if len(target_list) == 1 else "ambiguous"
    return {
        "nested_nonempty": nested,
        "worlds": worlds,
        "targets": target_list,
        "status": status,
        "nuisance": nuisance,
    }


def infer_records(query):
    """Fixed four-attempt record interface, distinct from population-box input."""
    fields = {"schema", "protocol_id", "data_kind", "records", "density_bound", "bound_basis"}
    if (
        type(query) is not dict
        or any(type(key) is not str for key in query)
        or set(query) != fields
    ):
        raise ValueError("record-query fields")
    expected = {
        "schema": "qr05br-record-query-v1",
        "protocol_id": "qr05br-n4-g256-a20-v1",
        "data_kind": "paired_causal_records",
        "bound_basis": "external_assumption",
    }
    for key in (*expected, "density_bound"):
        if type(query[key]) is not str:
            raise ValueError("plain record-query metadata")
    if any(query[key] != wanted for key, wanted in expected.items()):
        raise ValueError("fixed record confidence protocol")
    bounds = {"uniform": (0, 1), "half": (1, 2), "one": (1, 1), "two": (2, 1)}
    if query["density_bound"] not in bounds:
        raise ValueError("unknown external density bound")
    records = query["records"]
    if type(records) is not list or len(records) != 4:
        raise ValueError("exactly four attempts required")
    # Validate every row before checking model support, counting, or arithmetic.
    for index, row in enumerate(records, 1):
        if (
            type(row) is not dict
            or any(type(key) is not str for key in row)
            or set(row) != {"attempt", "bits"}
        ):
            raise ValueError("attempt fields")
        if type(row["attempt"]) is not int or row["attempt"] != index:
            raise ValueError("ordered unique positional attempt IDs")
        bits = row["bits"]
        if (
            type(bits) is not list
            or len(bits) != 2
            or any(type(bit) is not int or bit not in (0, 1) for bit in bits)
        ):
            raise ValueError("two native bits per attempt")
    if any(row["bits"] == [1, 0] for row in records):
        return {
            "schema": "qr05br-record-result-v1",
            "status": "refused",
            "reason": "impossible_nested_symbol",
            "confidence": {},
            "counts": [],
            "intervals": [],
            "answer": {},
        }
    counts = [sum(row["bits"][i] for row in records) for i in range(2)]
    intervals = [_interval_for_count(k) for k in counts]
    return {
        "schema": "qr05br-record-result-v1",
        "status": "accepted",
        "reason": "",
        "confidence": _confidence(),
        "counts": counts,
        "intervals": intervals,
        "answer": _inverse(intervals, bounds[query["density_bound"]]),
    }


def freeze(path):
    snapshot = source_snapshot()
    _protocol(snapshot)
    artifact = {
        "schema": "qr05br-source-freeze-v1",
        "sources": identities(snapshot),
        "runtime": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "optimization": sys.flags.optimize,
        },
    }
    _check_snapshot(snapshot)
    data = canonical(artifact)
    _write_new(path, data)
    _check_snapshot(snapshot)
    if read_bounded(path) != data:
        raise ValueError("BR freeze changed after publication")
    return artifact


def _checked_freeze(path, snapshot):
    data = read_bounded(path)
    value = strict_loads(data)
    if type(value) is not dict or set(value) != {"schema", "sources", "runtime"}:
        raise ValueError("BR freeze schema")
    runtime = value["runtime"]
    if (
        type(runtime) is not dict
        or set(runtime) != {"implementation", "version", "optimization"}
        or type(runtime["implementation"]) is not str
        or not runtime["implementation"]
        or type(runtime["version"]) is not str
        or not runtime["version"]
        or type(runtime["optimization"]) is not int
        or runtime["optimization"] not in (0, 1, 2)
    ):
        raise ValueError("BR freeze runtime")
    require_equal(value["schema"], "qr05br-source-freeze-v1")
    require_equal(value["sources"], identities(snapshot))
    if canonical(value) != data:
        raise ValueError("BR freeze noncanonical bytes")
    return data


def _stable_inputs(snapshot, freeze_path, freeze_data):
    _check_snapshot(snapshot)
    if read_bounded(freeze_path) != freeze_data:
        raise ValueError("BR freeze changed")


def capture(path, freeze_path=ROOT / "source-freeze.json"):
    if Path(path).exists() or Path(path).is_symlink():
        raise FileExistsError(str(path))
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    report = analyze()
    _stable_inputs(snapshot, freeze_path, freeze_data)
    artifact = {
        "schema": "qr05br-capture-v1",
        "sources": identities(snapshot),
        "freeze_sha256": hashlib.sha256(freeze_data).hexdigest(),
        "report": encode(report),
    }
    data = canonical(artifact)
    _write_new(path, data)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("BR capture changed after publication")
    return report


def replay(path, freeze_path=ROOT / "source-freeze.json"):
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    data = read_bounded(path)
    artifact = strict_loads(data)
    if type(artifact) is not dict or set(artifact) != {
        "schema",
        "sources",
        "freeze_sha256",
        "report",
    }:
        raise ValueError("BR capture schema")
    require_equal(artifact["schema"], "qr05br-capture-v1")
    require_equal(artifact["sources"], identities(snapshot))
    require_equal(artifact["freeze_sha256"], hashlib.sha256(freeze_data).hexdigest())
    retained = decode(artifact["report"])
    if canonical(artifact) != data:
        raise ValueError("BR capture noncanonical bytes")
    recomputed = analyze()
    require_equal(retained, recomputed)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("BR capture changed during replay")
    return recomputed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--freeze", type=Path)
    actions.add_argument("--capture", type=Path)
    actions.add_argument("--replay", type=Path)
    options = parser.parse_args()
    started = time.monotonic()
    if options.freeze is not None:
        result = freeze(options.freeze)
        print(json.dumps({"action": "freeze", "sources": len(result["sources"])}))
        return
    result = capture(options.capture) if options.capture is not None else replay(options.replay)
    data = canonical(encode(result))
    print(
        json.dumps(
            {
                "action": "capture" if options.capture is not None else "replay",
                "cases": len(result["cases"]),
                "hypotheses": sum(len(c["hypotheses"]) for c in result["cases"]),
                "report_bytes": len(data),
                "report_sha256": hashlib.sha256(data).hexdigest(),
                "seconds": round(time.monotonic() - started, 6),
            }
        )
    )


if __name__ == "__main__":
    main()
