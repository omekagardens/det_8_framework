"""Source-bound evidence for the fixed exact causal-operator verification."""

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
PROTOCOL_SHA256 = "76b530ba0c7761b48a5538ae7ca4aa0b556bf73da6616c6eacaf7edb67861090"
UTILITY_SHA256 = "157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55"
UTILITY_SOURCE = "../qr-05bm-relative-volume-verification-2026-09-09/study.py"
UTILITY_PATH = ROOT / UTILITY_SOURCE
DESIGN_README = "../qr-05-causal-operator-design-2026-09-12/README.md"
DESIGN_RESULTS = "../qr-05-causal-operator-design-2026-09-12/RESULTS.md"
DEPENDENCY_PINS = {
    UTILITY_SOURCE: UTILITY_SHA256,
    DESIGN_README: "5c6ffb21efea81dcecf81213d57536ff4a84111c49ed11d1219bae8212388817",
    DESIGN_RESULTS: "86aa262486380140c4bf2a63efebba51d1fe0557a08d0f6bb88d0ee5f81d48d4",
}
SOURCE_PATHS = (
    "README.md",
    "protocol.json",
    "primary.py",
    "reference.py",
    "study.py",
    "test_causal_operator.py",
    DESIGN_README,
    DESIGN_RESULTS,
    UTILITY_SOURCE,
)
EXPECTED_PROTOCOL = {
    "schema": "qr05-causal-operator-protocol-v1",
    "cases": [
        {"id": "singleton", "n": 1, "relation": [], "weights": [], "d": [1, 1]},
        {"id": "antichain", "n": 3, "relation": [], "weights": [], "d": [1, 1]},
        {
            "id": "chain",
            "n": 3,
            "relation": [[1, 0], [2, 0], [2, 1]],
            "weights": [[1, 0, 1, 1], [2, 1, 1, 1]],
            "d": [1, 1],
        },
        {
            "id": "fork",
            "n": 3,
            "relation": [[1, 0], [2, 0]],
            "weights": [[1, 0, 1, 1], [2, 0, 1, 1]],
            "d": [1, 1],
        },
        {
            "id": "diamond",
            "n": 4,
            "relation": [[1, 0], [2, 0], [3, 0], [3, 1], [3, 2]],
            "weights": [[1, 0, 1, 1], [2, 0, 1, 1], [3, 1, 1, 1], [3, 2, 1, 1]],
            "d": [1, 1],
        },
        {
            "id": "missing_cover",
            "n": 3,
            "relation": [[1, 0], [2, 0], [2, 1]],
            "weights": [[1, 0, 1, 1]],
            "d": [1, 1],
        },
        {"id": "single_edge", "n": 3, "relation": [[1, 0]], "weights": [[1, 0, 1, 1]], "d": [1, 1]},
        {
            "id": "signed_diamond",
            "n": 4,
            "relation": [[1, 0], [2, 0], [3, 0], [3, 1], [3, 2]],
            "weights": [[1, 0, 1, 1], [2, 0, 1, 1], [3, 1, 1, 1], [3, 2, -1, 1]],
            "d": [1, 1],
        },
        {
            "id": "toy_cancel",
            "n": 3,
            "relation": [[1, 0], [2, 0], [2, 1]],
            "weights": [[1, 0, 3, 1], [2, 0, -3, 1], [2, 1, 3, 1]],
            "d": [3, 1],
        },
        {
            "id": "toy_sign",
            "n": 3,
            "relation": [[1, 0], [2, 0], [2, 1]],
            "weights": [[1, 0, 3, 1], [2, 0, -3, 1], [2, 1, 3, 1]],
            "d": [5, 1],
        },
        {
            "id": "forward_pair",
            "n": 2,
            "relation": [[1, 0]],
            "weights": [[1, 0, 1, 1]],
            "d": [1, 1],
        },
        {
            "id": "reversed_signed_pair",
            "n": 2,
            "relation": [[0, 1]],
            "weights": [[0, 1, -1, 1]],
            "d": [1, 1],
        },
        {
            "id": "signed_relabelled_chain",
            "n": 3,
            "relation": [[0, 1], [2, 0], [2, 1]],
            "weights": [[0, 1, -1, 1], [2, 0, 1, 1], [2, 1, 1, 1]],
            "d": [1, 1],
        },
    ],
    "variants": ["identity", "cyclic", "reversal", "rescale"],
    "scale_multiplier": [3, 2],
    "witnesses": [
        {"kind": "zero_cover_order", "channel": "G", "cases": ["missing_cover", "single_edge"]},
        {
            "kind": "signed_orientation",
            "channel": "Delta",
            "cases": ["forward_pair", "reversed_signed_pair"],
        },
        {
            "kind": "signed_nonisomorphic",
            "channel": "Delta",
            "cases": ["fork", "signed_relabelled_chain"],
        },
    ],
    "coverage": {
        "rows": 52,
        "event_occurrences": 148,
        "matrix_cells": 452,
        "strict_pairs": 120,
        "covers": 92,
        "nonzero_A": 100,
        "nonzero_G_off": 100,
        "paths": 304,
        "trivial_paths": 148,
        "one_edge_paths": 120,
        "two_edge_paths": 36,
        "zero_paths": 24,
        "direct_equal": 36,
        "reachability_equal": 48,
        "witnesses": 12,
    },
    "limits": {
        "nodes": 4,
        "rational_bits": 128,
        "source_bytes": 262144,
        "artifact_bytes": 16777216,
        "analysis_seconds": 30,
        "suite_seconds": 60,
        "alternate_replays": 1,
    },
    "dependencies": {
        "design_readme_sha256": "5c6ffb21efea81dcecf81213d57536ff4a84111c49ed11d1219bae8212388817",
        "design_results_sha256": "86aa262486380140c4bf2a63efebba51d1fe0557a08d0f6bb88d0ee5f81d48d4",
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
    module = types.ModuleType("_qr05_causal_operator_checked_bm_utilities")
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
        raise ValueError("causal operator sources changed")


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
    """Decode only the declared world inputs, independently of both engines."""
    rows = []
    for case in protocol["cases"]:
        n = case["n"]
        relation = [[0 for _ in range(n)] for _ in range(n)]
        weights = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i, j in case["relation"]:
            relation[i][j] = 1
        for i, j, numerator, denominator in case["weights"]:
            weights[i][j] = Fraction(numerator, denominator)
        diagonal = Fraction(*case["d"])
        for variant in protocol["variants"]:
            C = [line[:] for line in relation]
            A = [line[:] for line in weights]
            d = diagonal
            if variant == "cyclic":
                C = [[relation[(i - 1) % n][(j - 1) % n] for j in range(n)] for i in range(n)]
                A = [[weights[(i - 1) % n][(j - 1) % n] for j in range(n)] for i in range(n)]
            elif variant == "reversal":
                C = [[relation[j][i] for j in range(n)] for i in range(n)]
                A = [[weights[j][i] for j in range(n)] for i in range(n)]
            elif variant == "rescale":
                scale = Fraction(*protocol["scale_multiplier"])
                A = [[scale * item for item in line] for line in A]
                d *= scale
            elif variant != "identity":
                raise ValueError("unknown prospective variant")
            rows.append(
                {
                    "id": case["id"] + ":" + variant,
                    "base": case["id"],
                    "variant": variant,
                    "world": {"C": C, "A": A, "d": d},
                }
            )
    return rows


def _coverage(report):
    rows = report["rows"]
    paths = [path for row in rows for path in row["paths"]]
    return {
        "rows": len(rows),
        "event_occurrences": sum(len(row["world"]["C"]) for row in rows),
        "matrix_cells": sum(len(row["world"]["C"]) ** 2 for row in rows),
        "strict_pairs": sum(sum(line) for row in rows for line in row["world"]["C"]),
        "covers": sum(len(row["covers"]) for row in rows),
        "nonzero_A": sum(sum(line) for row in rows for line in row["support_A"]),
        "nonzero_G_off": sum(sum(line) for row in rows for line in row["support_G"]),
        "paths": len(paths),
        "trivial_paths": sum(len(path["nodes"]) == 1 for path in paths),
        "one_edge_paths": sum(len(path["nodes"]) == 2 for path in paths),
        "two_edge_paths": sum(len(path["nodes"]) == 3 for path in paths),
        "zero_paths": sum(path["contribution"] == 0 for path in paths),
        "direct_equal": sum(row["flags"]["direct_equal"] for row in rows),
        "reachability_equal": sum(row["flags"]["reachability_equal"] for row in rows),
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
            raise ValueError("causal operator report fields")
        require_equal(report["schema"], "qr05-causal-operator-report-v1")
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
        "schema": "qr05-causal-operator-source-freeze-v1",
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
        raise ValueError("causal operator freeze changed after publication")
    return artifact


def _checked_freeze(path, snapshot):
    data = read_bounded(path)
    value = strict_loads(data)
    if type(value) is not dict or set(value) != {"schema", "sources", "runtime"}:
        raise ValueError("causal operator freeze schema")
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
        raise ValueError("causal operator freeze runtime")
    require_equal(value["schema"], "qr05-causal-operator-source-freeze-v1")
    require_equal(value["sources"], identities(snapshot))
    if canonical(value) != data:
        raise ValueError("causal operator freeze noncanonical bytes")
    return data


def _stable_inputs(snapshot, freeze_path, freeze_data):
    _check_snapshot(snapshot)
    if read_bounded(freeze_path) != freeze_data:
        raise ValueError("causal operator freeze changed")


def capture(path, freeze_path=ROOT / "source-freeze.json"):
    if Path(path).exists() or Path(path).is_symlink():
        raise FileExistsError(str(path))
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    report = analyze(snapshot)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    artifact = {
        "schema": "qr05-causal-operator-capture-v1",
        "sources": identities(snapshot),
        "freeze_sha256": hashlib.sha256(freeze_data).hexdigest(),
        "report": encode(report),
    }
    data = canonical(artifact)
    _write_new(path, data)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("causal operator capture changed after publication")
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
        raise ValueError("causal operator capture schema")
    require_equal(artifact["schema"], "qr05-causal-operator-capture-v1")
    require_equal(artifact["sources"], identities(snapshot))
    require_equal(artifact["freeze_sha256"], hashlib.sha256(freeze_data).hexdigest())
    retained = decode(artifact["report"])
    if canonical(artifact) != data:
        raise ValueError("causal operator capture noncanonical bytes")
    recomputed = analyze(snapshot)
    require_equal(retained, recomputed)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("causal operator capture changed during replay")
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
                "paths": sum(len(row["paths"]) for row in result["rows"]),
                "report_bytes": len(blob),
                "report_sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
    )


if __name__ == "__main__":
    main()
