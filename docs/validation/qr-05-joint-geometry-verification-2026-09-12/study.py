"""Source-bound evidence for the fixed exact joint-geometry verification."""

import argparse
import hashlib
import json
import os
import platform
import stat
import sys
import types
from fractions import Fraction
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_LIMIT = 262144
ARTIFACT_LIMIT = 16777216
PROTOCOL_SHA256 = "0e6cc49495d8ad9772b573d102fac5f0d774bc173a371d6e93b632426f26cfa7"
UTILITY_SHA256 = "157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55"
UTILITY_SOURCE = "../qr-05bm-relative-volume-verification-2026-09-09/study.py"
UTILITY_PATH = ROOT / UTILITY_SOURCE
QUOTIENT_SOURCE = "../qr-05-bridge-reconciliation-2026-09-12/calculus.py"
DESIGN_README = "../qr-05-joint-geometry-design-2026-09-12/README.md"
DESIGN_RESULTS = "../qr-05-joint-geometry-design-2026-09-12/RESULTS.md"
DEPENDENCY_PINS = {
    UTILITY_SOURCE: UTILITY_SHA256,
    QUOTIENT_SOURCE: "0fdfad80ffca8902c1af472b75afbbff2397f10b86cb7e1e7cb99697d4ca9d10",
    DESIGN_README: "abd6df782f40f091163eab72b0891249a81e5525c7e6ea55d6cf7e9d61f10921",
    DESIGN_RESULTS: "c69fd56da11116ebbbd615bca8665fc54b7b00e48d320860433bbc8c1735cf07",
}
SOURCE_PATHS = (
    "README.md",
    "protocol.json",
    "primary.py",
    "reference.py",
    "study.py",
    "test_joint_geometry.py",
    DESIGN_README,
    DESIGN_RESULTS,
    UTILITY_SOURCE,
    QUOTIENT_SOURCE,
)
EXPECTED_PROTOCOL = {
    "schema": "qr05-joint-geometry-protocol-v1",
    "model": {
        "kappa": [1, 2],
        "orientation": [-1, 1],
        "a": [0, 1],
        "b": [0, 1],
        "L": [[1, 1], [3, 2]],
        "r": [[1, 1], [2, 3]],
        "probes": [[[1, 8], [1, 8]], [[7, 8], [1, 8]], [[7, 8], [5, 8]]],
        "strip": [1, 2],
    },
    "channels": ["O", "P", "T", "D", "R"],
    "coverage": {
        "worlds": 64,
        "menus": 32,
        "targets": 16,
        "different_target_pairs": 1920,
        "omission_witnesses": 5,
        "collision_groups": 4,
        "identifying_menus": 1,
    },
    "controls": {
        "scale_multiplier": [3, 2],
        "repetitions": [1, 3],
        "null_probes": [[[1, 4], [1, 4]], [[3, 4], [3, 4]]],
    },
    "limits": {
        "source_bytes": 262144,
        "artifact_bytes": 16777216,
        "analysis_seconds": 30,
        "suite_seconds": 60,
        "input_rational_bits": 128,
        "alternate_replays": 1,
    },
    "dependencies": {
        "design_readme_sha256": "abd6df782f40f091163eab72b0891249a81e5525c7e6ea55d6cf7e9d61f10921",
        "design_results_sha256": "c69fd56da11116ebbbd615bca8665fc54b7b00e48d320860433bbc8c1735cf07",
        "quotient_sha256": "0fdfad80ffca8902c1af472b75afbbff2397f10b86cb7e1e7cb99697d4ca9d10",
        "utility_sha256": "157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55",
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
    module = types.ModuleType("_qr05_joint_geometry_checked_bm_utilities")
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
        raise ValueError("joint geometry sources changed")


def _protocol(snapshot):
    if snapshot[UTILITY_SOURCE] != UTILITY_BYTES:
        raise ValueError("utility snapshot mismatch")
    for name, digest in DEPENDENCY_PINS.items():
        if hashlib.sha256(snapshot[name]).hexdigest() != digest:
            raise ValueError("pinned dependency changed before protocol parse")
    blob = snapshot["protocol.json"]
    if hashlib.sha256(blob).hexdigest() != PROTOCOL_SHA256:
        raise ValueError("prospective protocol mismatch before parse")
    protocol = strict_loads(blob)
    require_equal(protocol, EXPECTED_PROTOCOL)
    return protocol


def load_engine(blob, name):
    module = types.ModuleType(name)
    filename = name if name.endswith(".py") else name + ".py"
    module.__file__ = str(ROOT / filename)
    exec(compile(blob, module.__file__, "exec"), module.__dict__)  # noqa: S102
    return module


def _expected_worlds(protocol):
    fields = ("kappa", "orientation", "a", "b", "L", "r")
    model = protocol["model"]
    values = [
        [Fraction(*v) for v in model[name]] if name in ("L", "r") else model[name]
        for name in fields
    ]
    return [dict(zip(fields, parts, strict=True)) for parts in product(*values)]


def analyze(snapshot=None):
    with _analysis_deadline():
        snapshot = source_snapshot() if snapshot is None else snapshot
        protocol = _protocol(snapshot)
        reports = []
        for filename in ("primary.py", "reference.py"):
            engine = load_engine(snapshot[filename], filename)
            report = engine.analyze()
            require_equal(report, report)
            reports.append(report)
        require_equal(reports[0], reports[1])
        report = reports[0]
        require_equal(report["schema"], "qr05-joint-geometry-report-v1")
        require_equal(report["channels"], protocol["channels"])
        expected = _expected_worlds(protocol)
        require_equal([row["world"] for row in report["worlds"]], expected)
        require_equal(
            [row["id"] for row in report["worlds"]],
            [f"w{index:03d}" for index in range(len(expected))],
        )
        coverage = protocol["coverage"]
        target_keys = {canonical(encode(row["target"])) for row in report["worlds"]}
        for actual, key in (
            (len(report["worlds"]), "worlds"),
            (len(report["partitions"]), "menus"),
            (len(target_keys), "targets"),
            (len(report["obstructions"]), "different_target_pairs"),
            (len(report["omission_witnesses"]), "omission_witnesses"),
            (len(report["collision_groups"]), "collision_groups"),
            (sum(row["identifying"] for row in report["partitions"]), "identifying_menus"),
        ):
            require_equal(actual, coverage[key])
        _check_snapshot(snapshot)
        return report


def freeze(path):
    snapshot = source_snapshot()
    _protocol(snapshot)
    artifact = {
        "schema": "qr05-joint-geometry-source-freeze-v1",
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
        raise ValueError("joint geometry freeze changed after publication")
    return artifact


def _checked_freeze(path, snapshot):
    data = read_bounded(path)
    value = strict_loads(data)
    if type(value) is not dict or set(value) != {"schema", "sources", "runtime"}:
        raise ValueError("joint geometry freeze schema")
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
        raise ValueError("joint geometry freeze runtime")
    require_equal(value["schema"], "qr05-joint-geometry-source-freeze-v1")
    require_equal(value["sources"], identities(snapshot))
    if canonical(value) != data:
        raise ValueError("joint geometry freeze noncanonical bytes")
    return data


def _stable_inputs(snapshot, freeze_path, freeze_data):
    _check_snapshot(snapshot)
    if read_bounded(freeze_path) != freeze_data:
        raise ValueError("joint geometry freeze changed")


def capture(path, freeze_path=ROOT / "source-freeze.json"):
    if Path(path).exists() or Path(path).is_symlink():
        raise FileExistsError(str(path))
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    report = analyze(snapshot)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    artifact = {
        "schema": "qr05-joint-geometry-capture-v1",
        "sources": identities(snapshot),
        "freeze_sha256": hashlib.sha256(freeze_data).hexdigest(),
        "report": encode(report),
    }
    data = canonical(artifact)
    _write_new(path, data)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("joint geometry capture changed after publication")
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
        raise ValueError("joint geometry capture schema")
    require_equal(artifact["schema"], "qr05-joint-geometry-capture-v1")
    require_equal(artifact["sources"], identities(snapshot))
    require_equal(artifact["freeze_sha256"], hashlib.sha256(freeze_data).hexdigest())
    retained = decode(artifact["report"])
    if canonical(artifact) != data:
        raise ValueError("joint geometry capture noncanonical bytes")
    recomputed = analyze(snapshot)
    require_equal(retained, recomputed)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("joint geometry capture changed during replay")
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
                "worlds": len(result["worlds"]),
                "menus": len(result["partitions"]),
                "report_bytes": len(blob),
                "report_sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
    )


if __name__ == "__main__":
    main()
