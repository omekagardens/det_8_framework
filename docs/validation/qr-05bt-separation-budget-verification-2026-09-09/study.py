"""BT exact separation/budget evidence with authenticated stored BR intervals."""

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
PROTOCOL_SHA256 = "14e591817da2b8f45a2a0dc34ed7425ac72586bb717fa8780e8815a8ac82b7c5"
UTILITY_SHA256 = "157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55"
UTILITY_SOURCE = "../qr-05bm-relative-volume-verification-2026-09-09/study.py"
UTILITY_PATH = ROOT / UTILITY_SOURCE
BASELINE_SOURCE = "../qr-05br-finite-record-confidence-2026-09-09/results.json"
BASELINE_SHA256 = "9bf4751ee7a044a7ec5a0d413d71bf0c83713f94cbcce07ef3503962dee24e6c"
SOURCE_PATHS = (
    "README.md",
    "protocol.json",
    "primary.py",
    "reference.py",
    "study.py",
    "test_qr05bt.py",
    UTILITY_SOURCE,
    "../qr-05bs-separation-budget-design-2026-09-09/README.md",
    "../qr-05bs-separation-budget-design-2026-09-09/RESULTS.md",
    "../qr-05br-finite-record-confidence-2026-09-09/README.md",
    "../qr-05br-finite-record-confidence-2026-09-09/RESULTS.md",
    BASELINE_SOURCE,
)
EXPECTED_PROTOCOL = {
    "schema": "qr05bt-protocol-v1",
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
    "fixtures": [
        {"id": "flat_0", "eta": 0, "delta": [0, 1]},
        {"id": "flat_1", "eta": 0, "delta": [1, 1]},
        {"id": "flat_interior", "eta": 0, "delta": [16, 11]},
        {"id": "conformal_0", "eta": 1, "delta": [0, 1]},
        {"id": "conformal_1", "eta": 1, "delta": [1, 1]},
        {"id": "conformal_interior", "eta": 1, "delta": [45, 158]},
    ],
    "boxes": {
        "fixtures": ["flat_interior", "conformal_interior"],
        "bound": "two",
        "kinds": ["half_square", "touch_square", "contact_rectangle"],
    },
    "rational_control": {"quota": 40, "grid_denominator": 8, "radius": [1, 4], "distance": [3, 4]},
    "baseline": {
        "schema": "qr05bt-br-baseline-v1",
        "quota": 4,
        "grid_denominator": 256,
        "alpha": [1, 20],
        "sha256": "9bf4751ee7a044a7ec5a0d413d71bf0c83713f94cbcce07ef3503962dee24e6c",
    },
    "coverage": {
        "geometries": 4,
        "fixtures": 6,
        "distances": 24,
        "classes": 4,
        "plans": 28,
        "scale_pairs": 2,
        "baseline_intervals": 5,
        "baseline_comparisons": 28,
        "boxes": 6,
        "rational_controls": 1,
        "obstructions": 1,
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
    module = types.ModuleType("_qr05bt_checked_bm_utilities")
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
        raise ValueError("BT source bytes changed")


def _protocol(snapshot):
    if snapshot[UTILITY_SOURCE] != UTILITY_BYTES:
        raise ValueError("utility snapshot differs from loaded code")
    if hashlib.sha256(snapshot[BASELINE_SOURCE]).hexdigest() != BASELINE_SHA256:
        raise ValueError("stored BR capture identity differs")
    data = snapshot["protocol.json"]
    if hashlib.sha256(data).hexdigest() != PROTOCOL_SHA256:
        raise ValueError("protocol bytes differ from prospective specification")
    protocol = strict_loads(data)
    require_equal(protocol, EXPECTED_PROTOCOL)
    return protocol


def _baseline(snapshot):
    """Authenticate the complete BR capture before parsing only its retained intervals."""
    data = snapshot[BASELINE_SOURCE]
    if hashlib.sha256(data).hexdigest() != BASELINE_SHA256:
        raise ValueError("stored BR capture identity differs before parse")
    artifact = strict_loads(data)
    if type(artifact) is not dict or set(artifact) != {
        "schema",
        "sources",
        "freeze_sha256",
        "report",
    }:
        raise ValueError("stored BR capture shape")
    require_equal(artifact["schema"], "qr05br-capture-v1")
    if canonical(artifact) != data:
        raise ValueError("stored BR capture noncanonical")
    report = artifact["report"]
    require_equal(report["schema"], "qr05br-report-v1")
    confidence = report["confidence"]
    rows = [{"k": row["k"], "interval": decode(row["interval"])} for row in report["intervals"]]
    baseline = {
        "schema": "qr05bt-br-baseline-v1",
        "quota": confidence["quota"],
        "grid_denominator": confidence["grid_denominator"],
        "alpha": decode(confidence["alpha"]),
        "intervals": rows,
    }
    expected = {
        "schema": "qr05bt-br-baseline-v1",
        "quota": 4,
        "grid_denominator": 256,
        "alpha": Fraction(1, 20),
        "intervals": [
            {"k": 0, "interval": [Fraction(0), Fraction(171, 256)]},
            {"k": 1, "interval": [Fraction(0), Fraction(109, 128)]},
            {"k": 2, "interval": [Fraction(3, 64), Fraction(61, 64)]},
            {"k": 3, "interval": [Fraction(19, 128), Fraction(1)]},
            {"k": 4, "interval": [Fraction(85, 256), Fraction(1)]},
        ],
    }
    require_equal(baseline, expected)
    return baseline


def load_engine(blob, name):
    module = types.ModuleType(name)
    module.__file__ = str(ROOT / (name + ".py"))
    # Fresh code from the checked BT source snapshot, with no cached imports.
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
        "schema": "qr05bt-source-freeze-v1",
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
        raise ValueError("BT freeze changed after publication")
    return artifact


def _checked_freeze(path, snapshot):
    data = read_bounded(path)
    value = strict_loads(data)
    if type(value) is not dict or set(value) != {"schema", "sources", "runtime"}:
        raise ValueError("BT freeze schema")
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
        raise ValueError("BT freeze runtime")
    require_equal(value["schema"], "qr05bt-source-freeze-v1")
    require_equal(value["sources"], identities(snapshot))
    if canonical(value) != data:
        raise ValueError("BT freeze noncanonical bytes")
    return data


def _stable_inputs(snapshot, freeze_path, freeze_data):
    _check_snapshot(snapshot)
    if read_bounded(freeze_path) != freeze_data:
        raise ValueError("BT freeze changed")


def capture(path, freeze_path=ROOT / "source-freeze.json"):
    if Path(path).exists() or Path(path).is_symlink():
        raise FileExistsError(str(path))
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    report = analyze()
    _stable_inputs(snapshot, freeze_path, freeze_data)
    artifact = {
        "schema": "qr05bt-capture-v1",
        "sources": identities(snapshot),
        "freeze_sha256": hashlib.sha256(freeze_data).hexdigest(),
        "report": encode(report),
    }
    data = canonical(artifact)
    _write_new(path, data)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("BT capture changed after publication")
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
        raise ValueError("BT capture schema")
    require_equal(artifact["schema"], "qr05bt-capture-v1")
    require_equal(artifact["sources"], identities(snapshot))
    require_equal(artifact["freeze_sha256"], hashlib.sha256(freeze_data).hexdigest())
    retained = decode(artifact["report"])
    if canonical(artifact) != data:
        raise ValueError("BT capture noncanonical bytes")
    recomputed = analyze()
    require_equal(retained, recomputed)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("BT capture changed during replay")
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
                "distances": len(result["distances"]),
                "plans": len(result["plans"]),
                "report_bytes": len(data),
                "report_sha256": hashlib.sha256(data).hexdigest(),
                "seconds": round(time.monotonic() - started, 6),
            }
        )
    )


if __name__ == "__main__":
    main()
