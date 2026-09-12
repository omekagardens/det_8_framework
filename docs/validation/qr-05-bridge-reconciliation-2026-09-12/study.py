"""Hash-bound evidence for the reconciled finite channel calculus."""

import argparse
import copy
import hashlib
import json
import os
import platform
import stat
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_LIMIT = 262144
ARTIFACT_LIMIT = 16777216
PROTOCOL_SHA256 = "7dbc57504a7dbe366e47ac4b38a4c042f40ca19e2c244b0e3d806e421e71546f"
UTILITY_SHA256 = "157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55"
UTILITY_SOURCE = "../qr-05bm-relative-volume-verification-2026-09-09/study.py"
UTILITY_PATH = ROOT / UTILITY_SOURCE
SOURCE_PATHS = (
    "CALCULUS.md",
    "protocol.json",
    "calculus.py",
    "study.py",
    "test_calculus.py",
    UTILITY_SOURCE,
)
EXPECTED_PROTOCOL = {
    "schema": "qr05-reconciliation-v1",
    "source_branch_commit": "ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8",
    "cases": [
        {
            "id": "xor_joint",
            "packet": {
                "channels": ["a", "b", "xor"],
                "rows": [
                    {"id": "00", "observations": [0, 0, 0], "target": [0, 0]},
                    {"id": "01", "observations": [0, 1, 1], "target": [0, 1]},
                    {"id": "10", "observations": [1, 0, 1], "target": [1, 0]},
                    {"id": "11", "observations": [1, 1, 0], "target": [1, 1]},
                ],
            },
        },
        {
            "id": "scale_anchor",
            "packet": {
                "channels": ["colour", "colour_copy", "external_scale"],
                "rows": [
                    {"id": "blue1", "observations": [0, 0, 1], "target": [0, 1]},
                    {"id": "blue2", "observations": [0, 0, 2], "target": [0, 2]},
                    {"id": "red1", "observations": [1, 1, 1], "target": [1, 1]},
                    {"id": "red2", "observations": [1, 1, 2], "target": [1, 2]},
                ],
            },
        },
        {
            "id": "constant",
            "packet": {
                "channels": [],
                "rows": [
                    {"id": "x", "observations": [], "target": [0]},
                    {"id": "y", "observations": [], "target": [0]},
                ],
            },
        },
        {
            "id": "blind",
            "packet": {
                "channels": ["same"],
                "rows": [
                    {"id": "x", "observations": [1], "target": [0]},
                    {"id": "y", "observations": [1], "target": [1]},
                ],
            },
        },
        {
            "id": "minimal_not_minimum",
            "packet": {
                "channels": ["a", "b", "xor"],
                "rows": [
                    {"id": "00", "observations": [0, 0, 0], "target": [0]},
                    {"id": "01", "observations": [0, 1, 1], "target": [0]},
                    {"id": "10", "observations": [1, 0, 1], "target": [1]},
                    {"id": "11", "observations": [1, 1, 0], "target": [1]},
                ],
            },
        },
    ],
    "limits": {
        "channels": 8,
        "worlds": 64,
        "target_coordinates": 8,
        "analysis_seconds": 30,
        "suite_seconds": 60,
        "source_bytes": 262144,
        "artifact_bytes": 16777216,
    },
    "coverage": {"packets": 5, "subsets": 27},
    "regressions": [
        "same-data union bound",
        "all-pair versus link max-plus",
        "visibility is not CHSH",
        "signed-path cancellation",
    ],
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
    module = types.ModuleType("_qr05_reconciliation_checked_bm_utilities")
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
        raise ValueError("utility source changed")
    return snapshot


def _check_snapshot(snapshot):
    if snapshot != source_snapshot():
        raise ValueError("reconciliation sources changed")


def _protocol(snapshot):
    if snapshot[UTILITY_SOURCE] != UTILITY_BYTES:
        raise ValueError("utility snapshot mismatch")
    blob = snapshot["protocol.json"]
    if hashlib.sha256(blob).hexdigest() != PROTOCOL_SHA256:
        raise ValueError("prospective protocol mismatch before parse")
    protocol = strict_loads(blob)
    require_equal(protocol, EXPECTED_PROTOCOL)
    return protocol


def load_engine(blob, name="reconciled_calculus"):
    module = types.ModuleType(name)
    module.__file__ = str(ROOT / "calculus.py")
    exec(compile(blob, module.__file__, "exec"), module.__dict__)  # noqa: S102
    return module


def analyze(snapshot=None):
    with _analysis_deadline():
        snapshot = source_snapshot() if snapshot is None else snapshot
        protocol = _protocol(snapshot)
        engine = load_engine(snapshot["calculus.py"])
        cases = []
        for case in protocol["cases"]:
            supplied = copy.deepcopy(case["packet"])
            result = engine.analyze(supplied)
            require_equal(supplied, case["packet"])
            require_equal(result, result)
            cases.append({"id": case["id"], "result": result})
        require_equal(len(cases), protocol["coverage"]["packets"])
        require_equal(
            sum(len(case["result"]["partitions"]) for case in cases),
            protocol["coverage"]["subsets"],
        )
        _check_snapshot(snapshot)
        return {
            "schema": "qr05-reconciliation-report-v1",
            "source_branch_commit": protocol["source_branch_commit"],
            "cases": cases,
        }


def freeze(path):
    snapshot = source_snapshot()
    _protocol(snapshot)
    artifact = {
        "schema": "qr05-reconciliation-source-freeze-v1",
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
        raise ValueError("reconciliation freeze changed after publication")
    return artifact


def _checked_freeze(path, snapshot):
    data = read_bounded(path)
    value = strict_loads(data)
    if type(value) is not dict or set(value) != {"schema", "sources", "runtime"}:
        raise ValueError("reconciliation freeze schema")
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
        raise ValueError("reconciliation freeze runtime")
    require_equal(value["schema"], "qr05-reconciliation-source-freeze-v1")
    require_equal(value["sources"], identities(snapshot))
    if canonical(value) != data:
        raise ValueError("reconciliation freeze noncanonical bytes")
    return data


def _stable_inputs(snapshot, freeze_path, freeze_data):
    _check_snapshot(snapshot)
    if read_bounded(freeze_path) != freeze_data:
        raise ValueError("reconciliation freeze changed")


def capture(path, freeze_path=ROOT / "source-freeze.json"):
    if Path(path).exists() or Path(path).is_symlink():
        raise FileExistsError(str(path))
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    report = analyze(snapshot)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    artifact = {
        "schema": "qr05-reconciliation-capture-v1",
        "sources": identities(snapshot),
        "freeze_sha256": hashlib.sha256(freeze_data).hexdigest(),
        "report": encode(report),
    }
    data = canonical(artifact)
    _write_new(path, data)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("reconciliation capture changed after publication")
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
        raise ValueError("reconciliation capture schema")
    require_equal(artifact["schema"], "qr05-reconciliation-capture-v1")
    require_equal(artifact["sources"], identities(snapshot))
    require_equal(artifact["freeze_sha256"], hashlib.sha256(freeze_data).hexdigest())
    retained = decode(artifact["report"])
    if canonical(artifact) != data:
        raise ValueError("reconciliation capture noncanonical bytes")
    recomputed = analyze(snapshot)
    require_equal(retained, recomputed)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("reconciliation capture changed during replay")
    return recomputed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--freeze", type=Path)
    actions.add_argument("--capture", type=Path)
    actions.add_argument("--replay", type=Path)
    options = parser.parse_args()
    if options.freeze is not None:
        result = freeze(options.freeze)
        print(json.dumps({"action": "freeze", "sources": len(result["sources"])}))
        return
    result = capture(options.capture) if options.capture is not None else replay(options.replay)
    blob = canonical(encode(result))
    print(
        json.dumps(
            {
                "action": "capture" if options.capture is not None else "replay",
                "cases": len(result["cases"]),
                "report_bytes": len(blob),
                "report_sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
    )


if __name__ == "__main__":
    main()
