"""BV exact acquisition-distortion evidence with authenticated stored BT classes."""

import argparse
import copy
import hashlib
import json
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
PROTOCOL_SHA256 = "1d8be64dba3efe598a007724c9fedc165bd78ea1417e1057eef188d51179ba36"
UTILITY_SHA256 = "157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55"
UTILITY_SOURCE = "../qr-05bm-relative-volume-verification-2026-09-09/study.py"
UTILITY_PATH = ROOT / UTILITY_SOURCE
BASELINE_SOURCE = "../qr-05bt-separation-budget-verification-2026-09-09/results.json"
BASELINE_SHA256 = "6beb088e27e0ec0c843b9be1c0794add02d8418a2fcbce9d4ade95ca685a9adb"
SOURCE_PATHS = (
    "README.md",
    "protocol.json",
    "primary.py",
    "reference.py",
    "study.py",
    "test_qr05bv.py",
    UTILITY_SOURCE,
    "../qr-05bu-acquisition-distortion-design-2026-09-09/README.md",
    "../qr-05bu-acquisition-distortion-design-2026-09-09/RESULTS.md",
    "../qr-05bt-separation-budget-verification-2026-09-09/README.md",
    "../qr-05bt-separation-budget-verification-2026-09-09/RESULTS.md",
    BASELINE_SOURCE,
)
EXPECTED_PROTOCOL = {
    "schema": "qr05bv-protocol-v1",
    "quota": 65536,
    "grid_denominator": 256,
    "alpha": [1, 20],
    "tail_allocations": [[1, 80], [1, 80], [1, 80], [1, 80]],
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
        {"id": "uniform", "upper": [0, 1]},
        {"id": "half", "upper": [1, 2]},
        {"id": "one", "upper": [1, 1]},
        {"id": "two", "upper": [2, 1]},
    ],
    "cases": [
        {"id": "uniform/zero", "bound": "uniform", "fraction": [0, 1]},
        {"id": "uniform/quarter", "bound": "uniform", "fraction": [1, 4]},
        {"id": "uniform/contact", "bound": "uniform", "fraction": [1, 2]},
        {"id": "half/zero", "bound": "half", "fraction": [0, 1]},
        {"id": "half/quarter", "bound": "half", "fraction": [1, 4]},
        {"id": "half/contact", "bound": "half", "fraction": [1, 2]},
        {"id": "one/zero", "bound": "one", "fraction": [0, 1]},
        {"id": "two/zero", "bound": "two", "fraction": [0, 1]},
    ],
    "boxes": [
        {"id": "uniform/flat", "bound": "uniform", "point": "flat", "fraction": [1, 4]},
        {"id": "uniform/conformal", "bound": "uniform", "point": "conformal", "fraction": [1, 4]},
        {
            "id": "uniform/midpoint_quarter",
            "bound": "uniform",
            "point": "midpoint",
            "fraction": [1, 4],
        },
        {
            "id": "uniform/midpoint_contact",
            "bound": "uniform",
            "point": "midpoint",
            "fraction": [1, 2],
        },
        {"id": "half/flat", "bound": "half", "point": "flat", "fraction": [1, 4]},
        {"id": "half/conformal", "bound": "half", "point": "conformal", "fraction": [1, 4]},
        {"id": "half/midpoint_quarter", "bound": "half", "point": "midpoint", "fraction": [1, 4]},
        {"id": "half/midpoint_contact", "bound": "half", "point": "midpoint", "fraction": [1, 2]},
        {"id": "one/collision", "bound": "one", "point": "midpoint", "fraction": [0, 1]},
        {"id": "two/collision", "bound": "two", "point": "midpoint", "fraction": [0, 1]},
    ],
    "negative": {"eta": 0, "delta": [0, 1], "lambda": [1, 16]},
    "baseline": {
        "schema": "qr05bv-bt-baseline-v1",
        "sha256": "6beb088e27e0ec0c843b9be1c0794add02d8418a2fcbce9d4ade95ca685a9adb",
    },
    "coverage": {
        "geometries": 4,
        "classes": 4,
        "cases": 8,
        "plans": 8,
        "boxes": 10,
        "hypotheses": 40,
        "unexpanded_hypotheses": 40,
        "negative_controls": 1,
        "scale_pairs": 2,
        "baseline_classes": 4,
        "baseline_plans": 4,
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
    module = types.ModuleType("_qr05bv_checked_bm_utilities")
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
        name: read_bounded(ROOT / name, ARTIFACT_LIMIT if name == BASELINE_SOURCE else SOURCE_LIMIT)
        for name in SOURCE_PATHS
    }
    if snapshot[UTILITY_SOURCE] != UTILITY_BYTES:
        raise ValueError("loaded utility bytes differ from current source snapshot")
    return snapshot


def _check_snapshot(snapshot):
    if snapshot != source_snapshot():
        raise ValueError("BV source bytes changed")


def _protocol(snapshot):
    if snapshot[UTILITY_SOURCE] != UTILITY_BYTES:
        raise ValueError("utility snapshot differs from loaded code")
    if hashlib.sha256(snapshot[BASELINE_SOURCE]).hexdigest() != BASELINE_SHA256:
        raise ValueError("stored BT capture identity differs")
    data = snapshot["protocol.json"]
    if hashlib.sha256(data).hexdigest() != PROTOCOL_SHA256:
        raise ValueError("protocol bytes differ from prospective specification")
    protocol = strict_loads(data)
    require_equal(protocol, EXPECTED_PROTOCOL)
    return protocol


def _baseline_shape(baseline):
    """Validate complete retained native shapes, not their mathematical truth."""
    rational = Fraction
    point = [rational, rational]
    segment = {"start": point, "end": point, "vector": point}
    lower = {
        "normal": point,
        "coefficients": [rational] * 3,
        "corner_values": [rational] * 4,
        "norm": rational,
        "value": rational,
    }
    class_shape = {
        "bound": str,
        "upper": rational,
        "segments": [segment, segment],
        "kind": str,
        "deltas": point,
        "parameters": point,
        "points": [point, point],
        "residual": point,
        "distance": rational,
        "closed_form": rational,
        "lower": lower,
    }
    plan_shape = {
        "id": str,
        "kind": str,
        "source": str,
        "distance": rational,
        "in_premise": bool,
        "slack": rational,
        "score": rational,
        "grid_positive": bool,
        "threshold_holds": bool,
        "sufficient": bool,
        "eligible": bool,
        "status": str,
        "guarantees": list,
    }

    def shape(value, wanted, active=None):
        active = set() if active is None else active
        if isinstance(wanted, type):
            if type(value) is not wanted:
                raise ValueError("BT baseline native type")
            return
        if type(value) is not type(wanted) or id(value) in active:
            raise ValueError("BT baseline container or cycle")
        active.add(id(value))
        try:
            if type(wanted) is dict:
                if set(value) != set(wanted):
                    raise ValueError("BT baseline keys")
                for key in wanted:
                    shape(value[key], wanted[key], active)
            elif type(wanted) is list:
                if len(value) != len(wanted):
                    raise ValueError("BT baseline length")
                for item, spec in zip(value, wanted):
                    shape(item, spec, active)
            else:
                raise ValueError("invalid native specification")
        finally:
            active.remove(id(value))

    shape(
        baseline,
        {
            "schema": str,
            "classes": [class_shape] * 4,
            "plans": [plan_shape] * 4,
        },
    )
    require_equal(baseline["schema"], "qr05bv-bt-baseline-v1")
    guarantee = {
        "correct_singleton_at_least": rational,
        "conditional_wrong_singleton_at_most": rational,
    }
    for bound, row, plan in zip(
        ("uniform", "half", "one", "two"), baseline["classes"], baseline["plans"]
    ):
        require_equal(row["bound"], bound)
        require_equal(row["kind"], "ordered" if bound in ("uniform", "half") else "collision")
        for key, value in (
            ("id", "class/" + bound),
            ("kind", "class"),
            ("source", bound),
            ("in_premise", True),
        ):
            require_equal(plan[key], value)
        if plan["status"] not in ("certified", "not_certified"):
            raise ValueError("BT baseline plan status")
        if len(plan["guarantees"]) > 1:
            raise ValueError("BT baseline guarantee length")
        for item in plan["guarantees"]:
            shape(item, guarantee)
    return baseline


def _baseline(snapshot):
    """Authenticate complete BT capture before extracting complete classes/plans."""
    data = snapshot[BASELINE_SOURCE]
    if hashlib.sha256(data).hexdigest() != BASELINE_SHA256:
        raise ValueError("stored BT capture identity differs before parse")
    artifact = strict_loads(data)
    if type(artifact) is not dict or set(artifact) != {
        "schema",
        "sources",
        "freeze_sha256",
        "report",
    }:
        raise ValueError("stored BT capture shape")
    require_equal(artifact["schema"], "qr05bt-capture-v1")
    if canonical(artifact) != data:
        raise ValueError("stored BT capture noncanonical")
    report = artifact["report"]
    if type(report) is not dict:
        raise ValueError("stored BT report type")
    require_equal(report.get("schema"), "qr05bt-report-v1")
    if type(report.get("classes")) is not list or type(report.get("plans")) is not list:
        raise ValueError("stored BT row collections")
    if any(type(row) is not dict for row in report["plans"]):
        raise ValueError("stored BT plan row type")
    baseline = {
        "schema": "qr05bv-bt-baseline-v1",
        "classes": decode(report["classes"]),
        "plans": decode([row for row in report["plans"] if row.get("kind") == "class"]),
    }
    return _baseline_shape(baseline)


def load_engine(blob, name):
    module = types.ModuleType(name)
    module.__file__ = str(ROOT / (name + ".py"))
    # Fresh code from the checked BV source snapshot, with no cached imports.
    exec(compile(blob, module.__file__, "exec"), module.__dict__)  # noqa: S102
    return module


def analyze():
    with _analysis_deadline():
        snapshot = source_snapshot()
        protocol = _protocol(snapshot)
        baseline = _baseline(snapshot)
        reports = []
        for filename in ("primary.py", "reference.py"):
            supplied = copy.deepcopy(protocol)
            supplied_baseline = copy.deepcopy(baseline)
            engine = load_engine(snapshot[filename], filename[:-3])
            report = engine.analyze(supplied, supplied_baseline)
            require_equal(supplied, protocol)
            require_equal(supplied_baseline, baseline)
            require_equal(report, report)
            reports.append(report)
        require_equal(reports[0], reports[1])
        _check_snapshot(snapshot)
        return reports[0]


def freeze(path):
    snapshot = source_snapshot()
    _protocol(snapshot)
    artifact = {
        "schema": "qr05bv-source-freeze-v1",
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
        raise ValueError("BV freeze changed after publication")
    return artifact


def _checked_freeze(path, snapshot):
    data = read_bounded(path)
    value = strict_loads(data)
    if type(value) is not dict or set(value) != {"schema", "sources", "runtime"}:
        raise ValueError("BV freeze schema")
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
        raise ValueError("BV freeze runtime")
    require_equal(value["schema"], "qr05bv-source-freeze-v1")
    require_equal(value["sources"], identities(snapshot))
    if canonical(value) != data:
        raise ValueError("BV freeze noncanonical bytes")
    return data


def _stable_inputs(snapshot, freeze_path, freeze_data):
    _check_snapshot(snapshot)
    if read_bounded(freeze_path) != freeze_data:
        raise ValueError("BV freeze changed")


def capture(path, freeze_path=ROOT / "source-freeze.json"):
    if Path(path).exists() or Path(path).is_symlink():
        raise FileExistsError(str(path))
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    report = analyze()
    _stable_inputs(snapshot, freeze_path, freeze_data)
    artifact = {
        "schema": "qr05bv-capture-v1",
        "sources": identities(snapshot),
        "freeze_sha256": hashlib.sha256(freeze_data).hexdigest(),
        "report": encode(report),
    }
    data = canonical(artifact)
    _write_new(path, data)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("BV capture changed after publication")
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
        raise ValueError("BV capture schema")
    require_equal(artifact["schema"], "qr05bv-capture-v1")
    require_equal(artifact["sources"], identities(snapshot))
    require_equal(artifact["freeze_sha256"], hashlib.sha256(freeze_data).hexdigest())
    retained = decode(artifact["report"])
    if canonical(artifact) != data:
        raise ValueError("BV capture noncanonical bytes")
    recomputed = analyze()
    require_equal(retained, recomputed)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("BV capture changed during replay")
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
                "plans": len(result["plans"]),
                "report_bytes": len(data),
                "report_sha256": hashlib.sha256(data).hexdigest(),
                "seconds": round(time.monotonic() - started, 6),
            }
        )
    )


if __name__ == "__main__":
    main()
