"""Source-bound evidence for the fixed exact measure-divergence verification."""

import argparse
import hashlib
import json
import os
import platform
import stat
import sys
import types
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_LIMIT = 262144
ARTIFACT_LIMIT = 16777216
PROTOCOL_SHA256 = "b8a9484c63ebb3748f14a13960df6b9f7b2728331a474adb4da37fd81b0f9b21"
UTILITY_SHA256 = "157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55"
UTILITY_SOURCE = "../qr-05bm-relative-volume-verification-2026-09-09/study.py"
UTILITY_PATH = ROOT / UTILITY_SOURCE
DESIGN_README = "../qr-05-measure-divergence-design-2026-09-12/README.md"
DESIGN_RESULTS = "../qr-05-measure-divergence-design-2026-09-12/RESULTS.md"
DEPENDENCY_PINS = {
    UTILITY_SOURCE: UTILITY_SHA256,
    DESIGN_README: "dcd542f088495953659865a8137eb195b0aba48e77b6cb46b9728f7303399d76",
    DESIGN_RESULTS: "d8296e32e57111371281327da6ced2e99952d05b5c69209eba955bf4d2b7271e",
}
SOURCE_PATHS = (
    "README.md",
    "protocol.json",
    "primary.py",
    "reference.py",
    "study.py",
    "test_measure_divergence.py",
    DESIGN_README,
    DESIGN_RESULTS,
    UTILITY_SOURCE,
)
EXPECTED_PROTOCOL = {
    "schema": "qr05-measure-divergence-protocol-v1",
    "cases": [
        {
            "id": "singleton_closed",
            "world": {
                "mu": [[1, 1]],
                "edges": [],
                "k": [],
                "x": [[0, 1]],
                "mode": "closed",
                "I": [0],
                "D": [],
                "f": [[2, 1]],
                "g": [],
                "q": [[0, 1]],
            },
        },
        {
            "id": "unequal_closed",
            "world": {
                "mu": [[1, 1], [2, 1]],
                "edges": [[0, 1]],
                "k": [[1, 1]],
                "x": [[0, 1], [1, 1]],
                "mode": "closed",
                "I": [0, 1],
                "D": [],
                "f": [[0, 1], [1, 1]],
                "g": [],
                "q": [[0, 1], [0, 1]],
            },
        },
        {
            "id": "zero_edge_closed",
            "world": {
                "mu": [[1, 1], [2, 1], [1, 1]],
                "edges": [[0, 1], [1, 2]],
                "k": [[1, 1], [0, 1]],
                "x": [[0, 1], [1, 1], [2, 1]],
                "mode": "closed",
                "I": [0, 1, 2],
                "D": [],
                "f": [[0, 1], [1, 1], [2, 1]],
                "g": [],
                "q": [[0, 1], [0, 1], [0, 1]],
            },
        },
        {
            "id": "arithmetic_face_closed",
            "world": {
                "mu": [[1, 1], [1, 1], [1, 1]],
                "edges": [[0, 1], [1, 2]],
                "k": [[3, 2], [1, 1]],
                "x": [[-1, 1], [0, 1], [1, 1]],
                "mode": "closed",
                "I": [0, 1, 2],
                "D": [],
                "f": [[0, 1], [1, 1], [0, 1]],
                "g": [],
                "q": [[0, 1], [0, 1], [0, 1]],
            },
        },
        {
            "id": "pointwise_reweighted",
            "world": {
                "mu": [[1, 2], [1, 1], [1, 1]],
                "edges": [[0, 1], [1, 2]],
                "k": [[1, 1], [1, 1]],
                "x": [[-1, 1], [0, 1], [1, 1]],
                "mode": "closed",
                "I": [0, 1, 2],
                "D": [],
                "f": [[0, 1], [1, 1], [0, 1]],
                "g": [],
                "q": [[0, 1], [0, 1], [0, 1]],
            },
        },
        {
            "id": "prescribed_flux",
            "world": {
                "mu": [[1, 1], [2, 1]],
                "edges": [[0, 1]],
                "k": [[1, 1]],
                "x": [[0, 1], [1, 1]],
                "mode": "flux",
                "I": [0, 1],
                "D": [],
                "f": [[1, 1], [2, 1]],
                "g": [],
                "q": [[2, 1], [-2, 1]],
            },
        },
        {
            "id": "dirichlet_grounded",
            "world": {
                "mu": [[1, 1], [1, 1], [1, 1]],
                "edges": [[0, 1], [1, 2]],
                "k": [[3, 2], [1, 1]],
                "x": [[-1, 1], [0, 1], [1, 1]],
                "mode": "dirichlet",
                "I": [1],
                "D": [0, 2],
                "f": [[1, 1]],
                "g": [[0, 1], [0, 1]],
                "q": [[0, 1], [0, 1], [0, 1]],
            },
        },
        {
            "id": "dirichlet_driven",
            "world": {
                "mu": [[1, 1], [1, 1], [1, 1]],
                "edges": [[0, 1], [1, 2]],
                "k": [[3, 2], [1, 1]],
                "x": [[-1, 1], [0, 1], [1, 1]],
                "mode": "dirichlet",
                "I": [1],
                "D": [0, 2],
                "f": [[1, 2]],
                "g": [[1, 1], [1, 1]],
                "q": [[0, 1], [0, 1], [0, 1]],
            },
        },
        {
            "id": "dirichlet_unanchored",
            "world": {
                "mu": [[1, 1], [2, 1], [1, 1]],
                "edges": [[0, 1], [1, 2]],
                "k": [[1, 1], [0, 1]],
                "x": [[0, 1], [1, 1], [2, 1]],
                "mode": "dirichlet",
                "I": [1, 2],
                "D": [0],
                "f": [[1, 1], [2, 1]],
                "g": [[0, 1]],
                "q": [[0, 1], [0, 1], [0, 1]],
            },
        },
    ],
    "variants": ["identity", "cyclic", "reversal", "rescale"],
    "scale_multiplier": [3, 2],
    "coverage": {
        "rows": 36,
        "event_occurrences": 92,
        "edges": 56,
        "matrix_cells": 252,
        "dynamic_occurrences": 72,
        "effective_matrix_cells": 168,
        "witnesses": 9,
    },
    "limits": {
        "nodes": 3,
        "rational_bits": 128,
        "source_bytes": 262144,
        "artifact_bytes": 16777216,
        "analysis_seconds": 30,
        "suite_seconds": 60,
        "alternate_replays": 1,
    },
    "dependencies": {
        "design_readme_sha256": "dcd542f088495953659865a8137eb195b0aba48e77b6cb46b9728f7303399d76",
        "design_results_sha256": "d8296e32e57111371281327da6ced2e99952d05b5c69209eba955bf4d2b7271e",
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
    module = types.ModuleType("_qr05_measure_divergence_checked_bm_utilities")
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
        raise ValueError("measure divergence sources changed")


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


def _expected_rows(protocol):
    """Decode and transport only protocol inputs, without either engine."""
    rows = []
    rational_keys = ("mu", "k", "x", "f", "g", "q")
    for case in protocol["cases"]:
        raw = case["world"]
        n = len(raw["mu"])
        for variant in protocol["variants"]:
            world = {key: [Fraction(*value) for value in raw[key]] for key in rational_keys}
            world.update(
                mode=raw["mode"],
                I=raw["I"][:],
                D=raw["D"][:],
                edges=[edge[:] for edge in raw["edges"]],
            )
            if variant == "cyclic":
                for key in ("mu", "x", "q"):
                    old = world[key]
                    world[key] = [old[(i - 1) % n] for i in range(n)]
                world["edges"] = [[(i + 1) % n, (j + 1) % n] for i, j in world["edges"]]
                if world["mode"] == "dirichlet":
                    world["I"] = [(i + 1) % n for i in world["I"]]
                    world["D"] = [(i + 1) % n for i in world["D"]]
                else:
                    old = world["f"]
                    world["f"] = [old[(i - 1) % n] for i in range(n)]
            elif variant == "reversal":
                world["edges"] = [[j, i] for i, j in world["edges"]]
            elif variant == "rescale":
                scale = Fraction(*protocol["scale_multiplier"])
                for key in ("mu", "k", "q"):
                    world[key] = [scale * value for value in world[key]]
            elif variant != "identity":
                raise ValueError("unknown prospective variant")
            rows.append(
                {
                    "id": case["id"] + ":" + variant,
                    "base": case["id"],
                    "variant": variant,
                    "world": world,
                }
            )
    return rows


def _coverage(report):
    rows = report["rows"]
    return {
        "rows": len(rows),
        "event_occurrences": sum(len(row["world"]["mu"]) for row in rows),
        "edges": sum(len(row["world"]["edges"]) for row in rows),
        "matrix_cells": sum(len(row["world"]["mu"]) ** 2 for row in rows),
        "dynamic_occurrences": sum(len(row["world"]["I"]) for row in rows),
        "effective_matrix_cells": sum(len(row["world"]["I"]) ** 2 for row in rows),
        "witnesses": len(report["witnesses"]),
    }


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
        if set(report) != {"schema", "rows", "witnesses"}:
            raise ValueError("measure divergence report fields")
        require_equal(report["schema"], "qr05-measure-divergence-report-v1")
        expected = _expected_rows(protocol)
        require_equal(
            [
                {key: row[key] for key in ("id", "base", "variant", "world")}
                for row in report["rows"]
            ],
            expected,
        )
        require_equal(_coverage(report), protocol["coverage"])
        _check_snapshot(snapshot)
        return report


def freeze(path):
    snapshot = source_snapshot()
    _protocol(snapshot)
    artifact = {
        "schema": "qr05-measure-divergence-source-freeze-v1",
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
        raise ValueError("measure divergence freeze changed after publication")
    return artifact


def _checked_freeze(path, snapshot):
    data = read_bounded(path)
    value = strict_loads(data)
    if type(value) is not dict or set(value) != {"schema", "sources", "runtime"}:
        raise ValueError("measure divergence freeze schema")
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
        raise ValueError("measure divergence freeze runtime")
    require_equal(value["schema"], "qr05-measure-divergence-source-freeze-v1")
    require_equal(value["sources"], identities(snapshot))
    if canonical(value) != data:
        raise ValueError("measure divergence freeze noncanonical bytes")
    return data


def _stable_inputs(snapshot, freeze_path, freeze_data):
    _check_snapshot(snapshot)
    if read_bounded(freeze_path) != freeze_data:
        raise ValueError("measure divergence freeze changed")


def capture(path, freeze_path=ROOT / "source-freeze.json"):
    if Path(path).exists() or Path(path).is_symlink():
        raise FileExistsError(str(path))
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    report = analyze(snapshot)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    artifact = {
        "schema": "qr05-measure-divergence-capture-v1",
        "sources": identities(snapshot),
        "freeze_sha256": hashlib.sha256(freeze_data).hexdigest(),
        "report": encode(report),
    }
    data = canonical(artifact)
    _write_new(path, data)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("measure divergence capture changed after publication")
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
        raise ValueError("measure divergence capture schema")
    require_equal(artifact["schema"], "qr05-measure-divergence-capture-v1")
    require_equal(artifact["sources"], identities(snapshot))
    require_equal(artifact["freeze_sha256"], hashlib.sha256(freeze_data).hexdigest())
    retained = decode(artifact["report"])
    if canonical(artifact) != data:
        raise ValueError("measure divergence capture noncanonical bytes")
    recomputed = analyze(snapshot)
    require_equal(retained, recomputed)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("measure divergence capture changed during replay")
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
                "rows": len(result["rows"]),
                "edges": sum(len(row["world"]["edges"]) for row in result["rows"]),
                "report_bytes": len(blob),
                "report_sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
    )


if __name__ == "__main__":
    main()
