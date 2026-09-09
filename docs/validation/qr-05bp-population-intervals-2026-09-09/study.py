"""BP population-query boundary and source-bound evidence; no BM math rerun."""

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
PROTOCOL_SHA256 = "721dc6f2831e69540d618c5ca1d35cb235736915ff187b679eca62ac17dd15c8"
UTILITY_SHA256 = "157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55"
UTILITY_SOURCE = "../qr-05bm-relative-volume-verification-2026-09-09/study.py"
UTILITY_PATH = ROOT / UTILITY_SOURCE
PRIOR_SOURCE = "../qr-05bo-richer-causal-queries-2026-09-09/results.json"
PRIOR_SHA256 = "df967357d18bf384a9e1fb05a560e9b791a17382463eb2f25ba0a547e1bca105"
SOURCE_PATHS = (
    "README.md",
    "protocol.json",
    "primary.py",
    "reference.py",
    "study.py",
    "test_qr05bp.py",
    UTILITY_SOURCE,
    "../qr-05bo-richer-causal-queries-2026-09-09/README.md",
    "../qr-05bo-richer-causal-queries-2026-09-09/RESULTS.md",
    PRIOR_SOURCE,
)
EXPECTED_PROTOCOL = {
    "schema": "qr05bp-protocol-v1",
    "quota": 4,
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
    "points": [
        {"id": "flat_0", "q": [[1, 4], [3, 8]]},
        {"id": "flat_1", "q": [[17, 80], [21, 64]]},
        {"id": "flat_2", "q": [[3, 16], [19, 64]]},
        {"id": "flat_interior", "q": [[1, 5], [5, 16]]},
        {"id": "conformal_0", "q": [[17, 80], [21, 64]]},
        {"id": "conformal_1", "q": [[163, 928], [2079, 7424]]},
        {"id": "conformal_2", "q": [[173, 1136], [567, 2272]]},
        {"id": "conformal_interior", "q": [[1, 5], [2275, 7296]]},
        {"id": "zero", "q": [[0, 1], [0, 1]]},
        {"id": "one", "q": [[1, 1], [1, 1]]},
        {"id": "equal", "q": [[1, 4], [1, 4]]},
        {"id": "zero_constant", "q": [[1, 16], [9, 64]]},
    ],
    "boxes": [
        {"id": "flat_small", "center": "flat_interior", "radius": [1, 65536]},
        {"id": "flat_wide", "center": "flat_interior", "radius": [1, 1024]},
        {"id": "conformal_small", "center": "conformal_interior", "radius": [1, 65536]},
        {"id": "conformal_wide", "center": "conformal_interior", "radius": [1, 1024]},
        {"id": "collision_small", "center": "flat_1", "radius": [1, 65536]},
        {"id": "full", "intervals": [[[0, 1], [1, 1]], [[0, 1], [1, 1]]]},
        {"id": "inconsistent", "intervals": [[[1, 4], [1, 4]], [[19, 64], [21, 64]]]},
        {"id": "touch", "intervals": [[[3, 16], [17, 80]], [[21, 64], [3, 8]]]},
        {"id": "crossing", "intervals": [[[1, 5], [2, 5]], [[3, 10], [1, 2]]]},
        {"id": "non_nested", "intervals": [[[3, 4], [1, 1]], [[0, 1], [1, 4]]]},
        {"id": "pole_band", "intervals": [[[1, 16], [1, 16]], [[0, 1], [1, 1]]]},
    ],
    "box_inclusions": [
        ["flat_interior", "flat_small"],
        ["flat_small", "flat_wide"],
        ["flat_wide", "full"],
        ["conformal_interior", "conformal_small"],
        ["conformal_small", "conformal_wide"],
        ["conformal_wide", "full"],
        ["flat_1", "collision_small"],
        ["collision_small", "full"],
        ["flat_1", "touch"],
        ["touch", "full"],
        ["inconsistent", "full"],
        ["crossing", "full"],
    ],
    "observer": {
        "schema": "qr05bp-query-v1",
        "data_kind": "population_intervals",
        "bound_basis": "external_assumption",
        "uncertainty_basis": "external_population_bounds",
        "integer_cap": 2147483647,
    },
    "coverage": {
        "geometries": 4,
        "data": 23,
        "cases": 92,
        "hypotheses": 368,
        "density_monotonicity": 69,
        "box_monotonicity": 48,
        "scale_pairs": 2,
        "obstruction_cases": 92,
        "point_recovery": 48,
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
    module = types.ModuleType("_qr05bp_checked_bm_utilities")
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
    snapshot = {
        name: read_bounded(ROOT / name, ARTIFACT_LIMIT if name == PRIOR_SOURCE else SOURCE_LIMIT)
        for name in SOURCE_PATHS
    }
    if snapshot[UTILITY_SOURCE] != UTILITY_BYTES:
        raise ValueError("loaded utility bytes differ from current source snapshot")
    return snapshot


def _check_snapshot(snapshot):
    if snapshot != source_snapshot():
        raise ValueError("BP source bytes changed")


def _protocol(snapshot):
    if snapshot[UTILITY_SOURCE] != UTILITY_BYTES:
        raise ValueError("utility snapshot differs from loaded code")
    if hashlib.sha256(snapshot[PRIOR_SOURCE]).hexdigest() != PRIOR_SHA256:
        raise ValueError("prior BO point-comparison capture identity differs")
    data = snapshot["protocol.json"]
    if hashlib.sha256(data).hexdigest() != PROTOCOL_SHA256:
        raise ValueError("protocol bytes differ from prospective specification")
    protocol = strict_loads(data)
    require_equal(protocol, EXPECTED_PROTOCOL)
    return protocol


def load_engine(blob, name):
    module = types.ModuleType(name)
    module.__file__ = str(ROOT / (name + ".py"))
    # Fresh code from the checked BP source snapshot, with no cached imports.
    exec(compile(blob, module.__file__, "exec"), module.__dict__)  # noqa: S102
    return module


def _previous_report(snapshot):
    """Authenticate the retained BO comparison input, without an old executor."""
    data = snapshot[PRIOR_SOURCE]
    if hashlib.sha256(data).hexdigest() != PRIOR_SHA256:
        raise ValueError("prior BO capture differs before parsing")
    artifact = strict_loads(data)
    if type(artifact) is not dict or set(artifact) != {
        "schema",
        "sources",
        "freeze_sha256",
        "report",
    }:
        raise ValueError("prior BO capture schema")
    require_equal(artifact["schema"], "qr05bo-capture-v1")
    if canonical(artifact) != data:
        raise ValueError("prior BO capture is not canonical")
    report = decode(artifact["report"])
    require_equal(report["schema"], "qr05bo-report-v1")
    return report


def _verify_point_recovery(report, previous):
    """Compare all 48 shared BO projections; no old interval answers exist."""
    point_ids = [point["id"] for point in EXPECTED_PROTOCOL["points"]]
    require_equal([row["id"] for row in previous["data"]], point_ids)
    require_equal([row["id"] for row in report["data"][: len(point_ids)]], point_ids)
    for new, old in zip(report["data"], previous["data"]):
        require_equal(new["id"], old["id"])
        require_equal(new["intervals"], [[q, q] for q in old["q"]])
        require_equal(new["nested_nonempty"], True)
    require_equal(len(previous["cases"]), EXPECTED_PROTOCOL["coverage"]["point_recovery"])
    cases = {case["id"]: case for case in report["cases"]}
    require_equal(len(cases), len(report["cases"]))
    for old in previous["cases"]:
        current = cases[old["id"]]
        for field in ("bound", "data", "worlds", "targets", "status"):
            require_equal(current[field], old[field])
        require_equal(current["intervals"], [[q, q] for q in old["q"]])
        require_equal(current["nested_nonempty"], True)
        require_equal(len(current["hypotheses"]), len(old["hypotheses"]))
        for new_hyp, old_hyp in zip(current["hypotheses"], old["hypotheses"], strict=True):
            require_equal(new_hyp["id"], old_hyp["id"])
            expected = [] if not old_hyp["delta_set"] else [old_hyp["delta_set"][0]] * 2
            require_equal(new_hyp["delta_set"], expected)
            require_equal(new_hyp["status"], old_hyp["status"])
    return len(previous["cases"])


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
        _verify_point_recovery(reports[0], _previous_report(snapshot))
        _check_snapshot(snapshot)
        return reports[0]


def identify(query):
    """Closed population-box inverse with one shared continuous nuisance."""
    fields = {
        "schema",
        "data_kind",
        "intervals",
        "density_bound",
        "bound_basis",
        "uncertainty_basis",
    }
    if (
        type(query) is not dict
        or any(type(key) is not str for key in query)
        or set(query) != fields
    ):
        raise ValueError("population interval-query fields")
    expected = {
        "schema": "qr05bp-query-v1",
        "data_kind": "population_intervals",
        "bound_basis": "external_assumption",
        "uncertainty_basis": "external_population_bounds",
    }
    for key in (*expected, "density_bound"):
        if type(query[key]) is not str:
            raise ValueError("plain query metadata required")
    if any(query[key] != value for key, value in expected.items()):
        raise ValueError("population/uncertainty premise mode")
    values = query["intervals"]
    if type(values) is not list or len(values) != 2:
        raise ValueError("two probability intervals required")
    pairs = []
    for band in values:
        if type(band) is not list or len(band) != 2:
            raise ValueError("lower and upper endpoints required")
        for pair in band:
            if type(pair) is not list or len(pair) != 2:
                raise ValueError("canonical rational endpoint required")
            if any(type(v) is not int or v.bit_length() > 31 for v in pair):
                raise ValueError("plain bounded integers required")
            pairs.append(pair)
    for pair in pairs:
        if pair[1] <= 0 or math.gcd(pair[0], pair[1]) != 1:
            raise ValueError("reduced endpoint with positive denominator required")
    intervals = [[Fraction(*pair) for pair in band] for band in values]
    if any(not 0 <= low <= high <= 1 for low, high in intervals):
        raise ValueError("ordered unit probability intervals required")
    bounds = {"uniform": (0, 1), "half": (1, 2), "one": (1, 1), "two": (2, 1)}
    if query["density_bound"] not in bounds:
        raise ValueError("unknown external density bound")
    upper = Fraction(*bounds[query["density_bound"]])
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


def freeze(path):
    snapshot = source_snapshot()
    _protocol(snapshot)
    artifact = {
        "schema": "qr05bp-source-freeze-v1",
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
        raise ValueError("BP freeze changed after publication")
    return artifact


def _checked_freeze(path, snapshot):
    data = read_bounded(path)
    value = strict_loads(data)
    if type(value) is not dict or set(value) != {"schema", "sources", "runtime"}:
        raise ValueError("BP freeze schema")
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
        raise ValueError("BP freeze runtime")
    require_equal(value["schema"], "qr05bp-source-freeze-v1")
    require_equal(value["sources"], identities(snapshot))
    if canonical(value) != data:
        raise ValueError("BP freeze noncanonical bytes")
    return data


def _stable_inputs(snapshot, freeze_path, freeze_data):
    _check_snapshot(snapshot)
    if read_bounded(freeze_path) != freeze_data:
        raise ValueError("BP freeze changed")


def capture(path, freeze_path=ROOT / "source-freeze.json"):
    if Path(path).exists() or Path(path).is_symlink():
        raise FileExistsError(str(path))
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    report = analyze()
    _stable_inputs(snapshot, freeze_path, freeze_data)
    artifact = {
        "schema": "qr05bp-capture-v1",
        "sources": identities(snapshot),
        "freeze_sha256": hashlib.sha256(freeze_data).hexdigest(),
        "report": encode(report),
    }
    data = canonical(artifact)
    _write_new(path, data)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("BP capture changed after publication")
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
        raise ValueError("BP capture schema")
    require_equal(artifact["schema"], "qr05bp-capture-v1")
    require_equal(artifact["sources"], identities(snapshot))
    require_equal(artifact["freeze_sha256"], hashlib.sha256(freeze_data).hexdigest())
    retained = decode(artifact["report"])
    if canonical(artifact) != data:
        raise ValueError("BP capture noncanonical bytes")
    recomputed = analyze()
    require_equal(retained, recomputed)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("BP capture changed during replay")
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
