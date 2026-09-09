"""BO population-query boundary and source-bound evidence; no BM math rerun."""

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
PROTOCOL_SHA256 = "85123ce52fa1597330e6bc817ef0d6d3d3498948060d785abebb5ad3a19ea91c"
UTILITY_SHA256 = "157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55"
UTILITY_SOURCE = "../qr-05bm-relative-volume-verification-2026-09-09/study.py"
UTILITY_PATH = ROOT / UTILITY_SOURCE
SOURCE_PATHS = (
    "README.md",
    "protocol.json",
    "primary.py",
    "reference.py",
    "study.py",
    "test_qr05bo.py",
    UTILITY_SOURCE,
    "../qr-05bn-bounded-density-identification-2026-09-09/README.md",
    "../qr-05bn-bounded-density-identification-2026-09-09/RESULTS.md",
)
EXPECTED_PROTOCOL = {
    "schema": "qr05bo-protocol-v1",
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
    "fixtures": [
        {"id": "flat_0", "eta": 0, "scale": 1, "delta": [0, 1]},
        {"id": "flat_1", "eta": 0, "scale": 1, "delta": [1, 1]},
        {"id": "flat_2", "eta": 0, "scale": 1, "delta": [2, 1]},
        {"id": "flat_interior", "eta": 0, "scale": 1, "delta": [16, 11]},
        {"id": "conformal_0", "eta": 1, "scale": 1, "delta": [0, 1]},
        {"id": "conformal_1", "eta": 1, "scale": 1, "delta": [1, 1]},
        {"id": "conformal_2", "eta": 1, "scale": 1, "delta": [2, 1]},
        {"id": "conformal_interior", "eta": 1, "scale": 1, "delta": [45, 158]},
        {"id": "flat_0_x4", "eta": 0, "scale": 4, "delta": [0, 1]},
        {"id": "flat_1_x4", "eta": 0, "scale": 4, "delta": [1, 1]},
        {"id": "flat_2_x4", "eta": 0, "scale": 4, "delta": [2, 1]},
        {"id": "flat_interior_x4", "eta": 0, "scale": 4, "delta": [16, 11]},
        {"id": "conformal_0_x4", "eta": 1, "scale": 4, "delta": [0, 1]},
        {"id": "conformal_1_x4", "eta": 1, "scale": 4, "delta": [1, 1]},
        {"id": "conformal_2_x4", "eta": 1, "scale": 4, "delta": [2, 1]},
        {"id": "conformal_interior_x4", "eta": 1, "scale": 4, "delta": [45, 158]},
    ],
    "fixture_data": [
        "flat_0",
        "flat_1",
        "flat_2",
        "flat_interior",
        "conformal_0",
        "conformal_1",
        "conformal_2",
        "conformal_interior",
    ],
    "control_data": [
        {"id": "zero", "q": [[0, 1], [0, 1]]},
        {"id": "one", "q": [[1, 1], [1, 1]]},
        {"id": "equal", "q": [[1, 4], [1, 4]]},
        {"id": "zero_constant", "q": [[1, 16], [9, 64]]},
    ],
    "density_bounds": [
        {"id": "uniform", "interval": [[0, 1], [0, 1]]},
        {"id": "half", "interval": [[0, 1], [1, 2]]},
        {"id": "one", "interval": [[0, 1], [1, 1]]},
        {"id": "two", "interval": [[0, 1], [2, 1]]},
    ],
    "observer": {
        "schema": "qr05bo-query-v1",
        "data_kind": "population_pair",
        "bound_basis": "external_assumption",
        "integer_cap": 2147483647,
    },
    "coverage": {
        "worlds": 16,
        "records": 4096,
        "marginals": 256,
        "data": 12,
        "cases": 48,
        "hypotheses": 192,
        "monotonicity": 36,
        "support": 256,
        "collisions": 2,
        "scale_pairs": 8,
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
    module = types.ModuleType("_qr05bo_checked_bm_utilities")
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
        raise ValueError("BO source bytes changed")


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
    # Fresh code from the checked BO source snapshot, with no cached imports.
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


def identify(query):
    """Exact bounded-rational population-pair inverse, not a record estimator."""
    fields = {"schema", "data_kind", "q", "density_bound", "bound_basis"}
    if (
        type(query) is not dict
        or any(type(key) is not str for key in query)
        or set(query) != fields
    ):
        raise ValueError("population-query fields")
    for key in ("schema", "data_kind", "density_bound", "bound_basis"):
        if type(query[key]) is not str:
            raise ValueError("query metadata type")
    if (
        query["schema"] != "qr05bo-query-v1"
        or query["data_kind"] != "population_pair"
        or query["bound_basis"] != "external_assumption"
    ):
        raise ValueError("query observation/assumption mode")
    values = query["q"]
    if type(values) is not list or len(values) != 2:
        raise ValueError("two canonical rational pairs required")
    for pair in values:
        if type(pair) is not list or len(pair) != 2:
            raise ValueError("canonical rational pair required")
        if any(type(v) is not int or v.bit_length() > 31 for v in pair):
            raise ValueError("plain bounded integers required")
    # Bound the complete input before any supplied-integer gcd or rational work.
    for pair in values:
        if pair[1] <= 0 or math.gcd(pair[0], pair[1]) != 1:
            raise ValueError("reduced rational with positive denominator required")
    q1, q2 = (Fraction(*pair) for pair in values)
    if not 0 <= q1 <= q2 <= 1:
        raise ValueError("nested population probabilities required")
    bounds = {"uniform": (0, 1), "half": (1, 2), "one": (1, 1), "two": (2, 1)}
    if query["density_bound"] not in bounds:
        raise ValueError("unknown external density bound")
    upper = Fraction(*bounds[query["density_bound"]])
    worlds, targets, nuisance = [], set(), []
    t2 = Fraction(3, 8)
    # Public continuous-family equations, never a validation-fixture lookup.
    for identifier, eta in (("flat", 0), ("conformal", 1), ("flat_x4", 0), ("conformal_x4", 1)):
        a, b, c, d = 144 + 9 * eta, 9 + eta, 576 + 144 * eta, 144 + 64 * eta
        divisor = d * q1 - b
        if divisor == 0:
            continue
        delta = (a - c * q1) / divisor
        if not 0 <= delta <= upper:
            continue
        denominator = c + d * delta
        if denominator <= 0 or (a + b * delta) / denominator != q1:
            raise ValueError("first inverse failed forward certification")
        mass_q = 1 + (eta + delta) / 4 + eta * delta / 9
        mass_i2 = t2 + (eta + delta) * t2**2 / 4 + eta * delta * t2**3 / 9
        if mass_i2 != q2 * mass_q:
            continue
        worlds.append(identifier)
        targets.add(Fraction(16 + eta, 16 * (4 + eta)))
        nuisance.append({"id": identifier, "delta": delta})
    target_list = sorted(targets)
    status = "infeasible" if not worlds else "identified" if len(target_list) == 1 else "ambiguous"
    return {"worlds": worlds, "targets": target_list, "status": status, "nuisance": nuisance}


def freeze(path):
    snapshot = source_snapshot()
    _protocol(snapshot)
    artifact = {
        "schema": "qr05bo-source-freeze-v1",
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
        raise ValueError("BO freeze changed after publication")
    return artifact


def _checked_freeze(path, snapshot):
    data = read_bounded(path)
    value = strict_loads(data)
    if type(value) is not dict or set(value) != {"schema", "sources", "runtime"}:
        raise ValueError("BO freeze schema")
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
        raise ValueError("BO freeze runtime")
    require_equal(value["schema"], "qr05bo-source-freeze-v1")
    require_equal(value["sources"], identities(snapshot))
    if canonical(value) != data:
        raise ValueError("BO freeze noncanonical bytes")
    return data


def _stable_inputs(snapshot, freeze_path, freeze_data):
    _check_snapshot(snapshot)
    if read_bounded(freeze_path) != freeze_data:
        raise ValueError("BO freeze changed")


def capture(path, freeze_path=ROOT / "source-freeze.json"):
    if Path(path).exists() or Path(path).is_symlink():
        raise FileExistsError(str(path))
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    report = analyze()
    _stable_inputs(snapshot, freeze_path, freeze_data)
    artifact = {
        "schema": "qr05bo-capture-v1",
        "sources": identities(snapshot),
        "freeze_sha256": hashlib.sha256(freeze_data).hexdigest(),
        "report": encode(report),
    }
    data = canonical(artifact)
    _write_new(path, data)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("BO capture changed after publication")
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
        raise ValueError("BO capture schema")
    require_equal(artifact["schema"], "qr05bo-capture-v1")
    require_equal(artifact["sources"], identities(snapshot))
    require_equal(artifact["freeze_sha256"], hashlib.sha256(freeze_data).hexdigest())
    retained = decode(artifact["report"])
    if canonical(artifact) != data:
        raise ValueError("BO capture noncanonical bytes")
    recomputed = analyze()
    require_equal(retained, recomputed)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("BO capture changed during replay")
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
